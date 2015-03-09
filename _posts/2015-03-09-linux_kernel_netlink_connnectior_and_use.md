---
layout: post
title: "连接器（Netlink Connector）及其应用"
categories: linux
tags: [linux, kernel, 连接器, NetLink]
date: 2015-03-09 09:21:46
---

连接器（Netlink Connector）及其应用

本文详细介绍了 Linux 2.6 内核引入的内核空间与用户空间通信的新机制连接器，并通过典型示例讲解了它的使用。


* 一、引言

连接器是一种新的用户态与内核态的通信方式，它使用起来非常方便。本质上，连接器是一种netlink，它的 netlink 协议号为 NETLINK_CONNECTOR，与一般的 netlink 相比，它提供了更容易的使用接口，使用起来更方便。目前，最新稳定内核有两个连接器应用实例，一个是进程事件连接器，另一个是 CIFS 文件系统。连接器核心实现代码在内核源码树的driver/connector/connector.c 和 drivers/connector/cn_queue.c 文件中，文件 drivers/connector/cn_proc.c 是进程事件连接器的实现代码，而 CIFS 连接器的实现则在该文件系统的实现代码中。连接器是一个可选模块，用户可以在配置内核时在设备驱动（Device drivers）菜单中选择或不选它。

任何内核模块要想使用连接器，必须先注册一个标识 ID 和回调函数，当连接器收到 netlink 消息后，会根据消息对应的标识 ID 调用相应该 ID 的回调函数。

对用户态而言，连接器的使用跟普通的 netlink 没有差别，只要指定 netlink 协议类型为NETLINK_CONNECTOR 就可以了。


* 二、连接器相关数据结构和 API

下面是连接器的 API 以及相关的数据结构

<pre>
struct cb_id
{
	__u32			idx;
	__u32			val;
};
struct cn_msg
{
	struct cb_id 		id;
	__u32			seq;
	__u32			ack;
	__u32			len;		/* Length of the following data */
	__u8			data[0];
};
int cn_add_callback(struct cb_id *id, char *name, void (*callback) (void *));
void cn_del_callback(struct cb_id *id);
void cn_netlink_send(struct cn_msg *msg, u32 __group, int gfp_mask);
</pre>


结构 cb_id 是连接器实例的标识 ID，它用于确定 netlink 消息与回调函数的对应关系。当连接器接收到标识 ID 为 {idx，val} 的 netlink 消息时，注册的回调函数 void (*callback) (void *) 将被调用。该回调函数的参数为结构 struct cn_msg 的指针。

接口函数 cn_add_callback 用于向连接器注册新的连接器实例以及相应的回调函数，参数 id 指定注册的标识 ID，参数 name 指定连接器回调函数的符号名，参数 callback 为回调函数。

接口函数 cn_del_callback 用于卸载回调函数，参数 id 为注册函数 cn_add_callback 注册的连接器标识 ID。

接口函数 cn_netlink_send 用于向给定的组发送消息，它可以在任何上下文安全地调用。但是，如果内存不足，可能会发送失败。在具体的连接器实例中，该函数用于向用户态发送 netlink 消息。

参数 msg 为发送的 netlink 消息的消息头。参数 __group 为接收消息的组，如果它为 0，那么连接器将搜索所有注册的连接器用户，最终将发送给用户 ID 与在 msg 中的 ID 相同的组，但如果 __group 不为 0，消息将发送给 __group 指定的组。参数 gfp_mask 指定页分配标志。

注意：当注册新的回调函数时，连接器将指定它的组为 id.idx。

cn_msg 是连接器定义的消息头，字段 seq 和 ack 用于确保消息的可靠传输，刚才已经提到，netlink 在内存紧张的情况下可能丢失消息，因此该头使用顺序号和响应号来满足要求可靠传输用户的需求。当发送消息时，用户需要设置独一无二的顺序号和随机的响应号，顺序号也应当设置到 nlmsghdr->nlmsg_seq。注意 nlmsghdr 是类型为结构 struct nlmsghdr 的变量，它用于设置或保存 netlink 的消息头。每发送一个消息，顺序号应当加 1，如果需要发送响应消息，那么响应消息的顺序号应当与被响应的消息的顺序号相同，同时响应消息的响应号应当为被响应消息的顺序号加1。如果接收到的消息的顺序号不是期望的顺序号，那表明该消息是一个新的消息，如果接收到的消息的顺序号是期望的顺序号，但它的响应号不等于上次发送消息的顺序号加1，那么它也是新消息。


* 三、用户态如何使用连接器

内核 2.6.14 对 netlink 套接字有新的实现，它缺省情况下不允许用户态应用发送给组号非 1 的netlink 组，因此用户态应用要想使用非1的组，必须先加入到该组，这可以通过如下代码实现：

<pre>
#ifndef  SOL_NETLINK
#define  SOL_NETLINK 270
#endif
#ifndef  NETLINK_DROP_MEMBERSHIP
#define  NETLINK_DROP_MEMBERSHIP 0
#endif
#ifndef  NETLINK_ADD_MEMBERSHIP
#define  NETLINK_ADD_MEMBERSHIP 1
#endif
int group = 5;
s = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_CONNECTOR);
l_local.nl_family = AF_NETLINK;
l_local.nl_groups = group;
l_local.nl_pid = getpid();
if (bind(s, (struct sockaddr *)&l_local, sizeof(struct sockaddr_nl)) == -1) {
	perror("bind");
	close(s);
	return -1;
}
setsockopt(s, SOL_NETLINK, NETLINK_ADD_MEMBERSHIP, &group, sizeof(group));
</pre>

在不需要使用该连接器时使用语句

<pre>
setsockopt(s, SOL_NETLINK, NETLINK_DROP_MEMBERSHIP, &group, sizeof(group));
</pre>

退出NETLINK_CONNECTOR的group组。

宏 SOL_NETLINK、NETLINK_ADD_MEMBERSHIP 和 NETLINK_DROP_MEMBERSHIP 在旧的系统中并没有定义，因此需要用户显式定义。

内核 2.6.14 的 netlink 代码只允许选择一个小于或等于最大组号的组，对于连接器，最大的组号为CN_NETLINK_USERS + 0xf， 即16，因此如果想使用更大的组号，必须修改CN_NETLINK_USERS 到该大值。增加的 0xf 个号码供非内核态用户使用。因此，组 0xffffffff目前不能使用。


* 四、进程事件连接器的使用

进程事件连接器是连接器的第一个使用实例，它通过连接器来报告进程相关的事件，包括进程 fork、exec、exit 以及进程用户 ID 与组 ID 的变化。如果用户想监视系统的进程事件，就可以编一个应用程序通过 netlink 套接字来获取进程事件信息。下面将详细描述如何编写一个进程事件监视程序。

<pre>
#include <sys/types.h>
#include <sys/socket.h>
#include <signal.h>
#include <linux/netlink.h>
#include <linux/connector.h>
#define _LINUX_TIME_H
#include <linux/cn_proc.h>

</pre>

上面这些 include 语句包含了进程监视程序需要的必要头文件，其中头文件 sys/types.h 和sys/socket.h 是编写套接字程序所必须的，头文件 signal.h 包含了信号处理相关的函数，本程序需要信号处理，因此需要包含该头文件。其余的三个头文件是内核相关的头文件，头文件linux/netlink.h 是编写netlink套接字程序所必须的，头文件 linux/connector.h 包含了内核实现的连接器的一些结构和宏，使用连接器监视系统事件的程序必须包含它，头文件 linux/cn_proc.h 则定义了进程事件连接器的一些结构和宏，应用程序需要包含该头文件以便正确分析进程事件。注意，在包含头文件 linux/cn_proc.h 之前定义了宏_LINUX_TIME_H，因为在用户态应用中包含linux/time.h会导致结构struct timespec 定义冲突，所以该宏避免了头文件linux/cn_proc.h包含linux/time.h。

<pre>
#define  MAX_MSGSIZE 256
#ifndef  SOL_NETLINK
#define  SOL_NETLINK 270
#endif
</pre>

旧的系统并没有定义 SOL_NETLINK，因此程序必须处理这种情况。宏 MAX_MSGSIZE 定义了最大的进程事件消息大小，它用于指定接收进程事件消息的缓存的大小，这里只是很粗略的大小，实际的消息比这小。

<pre>
int sd;
struct sockaddr_nl l_local, daddr;
int on;
int len;
struct nlmsghdr *nlhdr = NULL;
struct msghdr msg;
struct iovec iov;
int * connector_mode;
struct cn_msg * cnmsg;
struct proc_event * procevent;
int counter = 0;
int ret;
struct sigaction sigint_action;
</pre>

这些变量用于处理 netlink 消息，其中 sd 为套接字描述符，l_local 和 daddr 分别表示 netlink消息的源地址和目的地址，后面部分将详细解释这种地址的设置。

<pre>
void change_cn_proc_mode(int mode)
</pre>

函数 change_cn_proc_mode 用于打开和关闭进程事件的报告，进程事件连接器初始化时是关闭进程事件报告的，一个进程要想监视进程事件，必须首先打开进程事件连接器的报告开关，在它退出是必须关闭进程事件连接器的报告开关，否则进程事件连接器将继续报告进程事件，尽管没有一个监视进程对这些事件感兴趣，这将造成不必要的系统开销，同时因为缓存这些事件浪费了宝贵的系统内存。下面代码是该函数的实现：

<pre>
{
	memset(nlhdr, 0, sizeof(NLMSG_SPACE(MAX_MSGSIZE)));
	memset(&iov, 0, sizeof(struct iovec));
	memset(&msg, 0, sizeof(struct msghdr));
        cnmsg = (struct cn_msg *)NLMSG_DATA(nlhdr);
        connector_mode = (int *)cnmsg->data;
        * connector_mode = mode;
        nlhdr->nlmsg_len = NLMSG_LENGTH(sizeof(struct cn_msg) + sizeof(enum
		proc_cn_mcast_op));
        nlhdr->nlmsg_pid = getpid();
        nlhdr->nlmsg_flags = 0;
        nlhdr->nlmsg_type = NLMSG_DONE;
        nlhdr->nlmsg_seq = 0;
</pre>

对于进程事件连接器，netlink 消息包括 netlink 消息头、连接器消息头、进程事件或控制操作指令，其中进程事件或控制操作指令部分是变长的，如果是控制指令，仅包含4个字节，如果是进程事件，它应当为类型 struct proc_event 的结构，对于不同的事件，尺寸不同，可能的事件包括控制指令的应答、进程 fork、进程 exec、进程 exit、进程用户 ID 改变以及进程组 ID 的改变。变量 connector_mode 用于设置控制指令，对于进程事件连接器，只有两种控制指令，分别是PROC_CN_MCAST_LISTEN 和 PROC_CN_MCAST_IGNORE，对应于打开和关闭进程事件报告。这两个宏定义在头文件 linux/cn_proc.h。变量 nlhdr 用于设置 netlink 的消息头，nlmsg_len用于指明消息的数据部分长度，该消息的数据部分包含了固定长度的连接器的消息头以及进程连接器的消息，nlmsg_pid用于指定消息的来源，一般为进程或线程ID，nlmsg_flags用于指定一些特殊标志，一般设置为0就足够了。应用程序设置 nlmsg_type 为 NLMSG_DONE，表示该消息是完整的，没有后续的消息碎片。一般地，nlmsg_seq 应当与连接器消息头的顺序号一致。

<pre>
        cnmsg->id.idx = CN_IDX_PROC;
        cnmsg->id.val = CN_VAL_PROC;
        cnmsg->seq = 0;
        cnmsg->ack = 0;
        cnmsg->len = sizeof(enum proc_cn_mcast_op);
</pre>

这部分代码用于设置连接器消息头，对于进程事件连接器，cnmsg->id.idx 和 cnmsg->id.val 必须分别设置为CN_IDX_PROC和CN_VAL_PROC，否则该消息无法派送给进程事件连接器。Seq 和ack 用于指定消息的顺序号和响应号，对于非响应消息，ack 应当设置为 0，而顺序号应当为上一个发送的消息的顺序号加1，对于第一个消息可以随意指定顺序号。

<pre>
        iov.iov_base = (void *)nlhdr;
        iov.iov_len = nlhdr->nlmsg_len;
        msg.msg_name = (void *)&daddr;
        msg.msg_namelen = sizeof(daddr);
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;
        ret = sendmsg(sd, &msg, 0);
        if (ret == -1) {
        	perror("sendmsg error:");
		exit(-1);
        }
}
</pre>

这部分代码用于发送 netlink 消息，为了通过函数 sendmsg 发送该消息，程序必须填写类型为结构 struct msghdr 的变量 msg，因为该函数可以一次发送多个消息，因此通过结构 struct iovec 来组织所有要发送的消息。iov.iov_base 指向消息的开始位置，iov.iov_len 指定消息的大小，msg.msg_name 指定消息的目的地址，msg.msg_namelen 则指定消息的目的地址长度，msg.msg_iov 指向结构为 struct iovec 的数组开始位置，对于这里的情况，它只包含了一个元素，因此 msg.msg_iovlen 设置为 1，如果有多个消息，该字段应该设置为实际的消息数，当然那时 iov 应当是一个多元素的数组，每一个元素都应当象前面的 iov 结构去设置。

<pre>
void sigint_handler(int signo)
{
	change_cn_proc_mode(PROC_CN_MCAST_IGNORE);
	printf("process event: turn off process event listening.\n");
	close(sd);
	exit(0);
}
</pre>

这是一个信号处理函数，它用于在该程序退出时关闭进程事件的报告。

下面是程序的主体部分。

<pre>
int main(void)
{
	memset(&sigint_action, 0, sizeof(struct sigaction));
	sigint_action.sa_flags = SA_ONESHOT;
	sigint_action.sa_handler = &sigint_handler;
	sigaction(SIGINT, &sigint_action, NULL);
</pre>

这段代码用于设置信号 SIGINT 的处理函数，该程序是一个无限循环，用户通过 CTRL + C 来退出，当用户按下 CTRL + C 时，系统将发送信号 SIGINT 该该程序，相应的处理函数将被执行，前面已经讲过，该信号处理函数用于关闭进程事件报告。

<pre>
	nlhdr = (struct nlmsghdr *)malloc(NLMSG_SPACE(MAX_MSGSIZE));
	if (nlhdr == NULL) {
		perror("malloc:");
		exit(-1);
	}
	
daddr.nl_family = AF_NETLINK;
daddr.nl_pid = 0;
daddr.nl_groups = CN_IDX_PROC;
</pre>

netlink 消息的地址结构包括三个主要的字段，nl_family 必须设置为 AF_NETLINK，nl_pid 则用于指定 netlink 消息的接收者或发送者的地址，一般为进程 ID 或线程 ID，如果该消息的发送者为内核或接收者有多个，它设置为 0，此时 nl_groups 指定接收者的组号。

<pre>
		sd = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_CONNECTOR);
</pre>

该语句创建了一个 netlink 套接字，注意对于使用连接器的应用，第三个参数必须指定为 NETLINK_CONNECTOR。所有使用 netlink 的应用程序，函数 socket 的前两个参数都是一样的，应当分别为 PF_NETLINK 和 SOCK_DGRAM。

<pre>
	l_local.nl_family = AF_NETLINK;
	l_local.nl_groups = CN_IDX_PROC;
	l_local.nl_pid = getpid();
</pre>

这段代码用于设置 netlink 消息的源地址。

<pre>
	if (bind(sd, (struct sockaddr *)&l_local, sizeof(struct sockaddr_nl)) == -1)
	{
        	perror("bind");
	        close(sd);
        	return -1;
	}
</pre>

使用 bind 函数主要为了把源地址与套接字 sd 绑定起来，以便后面消息的发送不必指定源地址。

<pre>
		change_cn_proc_mode(PROC_CN_MCAST_LISTEN);
</pre>

该调用打开了进程事件的报告。

<pre>
	printf("process event: turn on process event listening.\n");
	while (1) {
		memset(nlhdr, 0, NLMSG_SPACE(MAX_MSGSIZE));
		memset(&iov, 0, sizeof(struct iovec));
		memset(&msg, 0, sizeof(struct msghdr));
                iov.iov_base = (void *)nlhdr;
                iov.iov_len = NLMSG_SPACE(MAX_MSGSIZE);
                msg.msg_name = (void *)&daddr;
                msg.msg_namelen = sizeof(daddr);
                msg.msg_iov = &iov;
                msg.msg_iovlen = 1;
                ret = recvmsg(sd, &msg, 0);
                if (ret == 0) {
                        printf("Exit.\n");
                        exit(0);
                }
                else if (ret == -1) {
                        perror("recvmsg:");
                        exit(1);
                }
		else {
</pre>

这部分代码用于接收进程事件消息，使用函数 recvmsg 时，用户也必须设置 msg，这时各字段的意义与发送时不一样，iov 用于指定消息的存放位置以及最大可利用的缓存大小，msg.msgname 则表示该调用希望接收的消息的目的地址，msg.msg_iovlen 则指定该调用应当返回的消息数。

<pre>
cnmsg = (struct cn_msg *)NLMSG_DATA(nlhdr);
procevent = (struct proc_event *)cnmsg->data;
switch (procevent->what) {
  case PROC_EVENT_NONE:
    printf("process event: acknowledge for turning on process
    event listening\n\n\n");
    break;
  case PROC_EVENT_FORK:
    printf("process event: fork\n");
    printf("parent tid:%d, pid:%d\nchild tid:%d, pid:%d\n\n\n",
     procevent->event_data.fork.parent_pid,
     procevent->event_data.fork.parent_tgid,
     procevent->event_data.fork.child_pid,
     procevent->event_data.fork.child_tgid);
    break;
  case PROC_EVENT_EXEC:
    printf("process event: exec\n");
    printf("tid:%d, pid:%d\n\n\n",
     procevent->event_data.exec.process_pid,
     procevent->event_data.exec.process_tgid);
    break;
  case PROC_EVENT_UID:
    printf("process event: uid\n");
    printf("process tid:%d, pid:%d, uid:%d->%d\n\n\n",
     procevent->event_data.id.process_pid,
     procevent->event_data.id.process_tgid,
     procevent->event_data.id.r.ruid,
     procevent->event_data.id.e.euid);
    break;
  case PROC_EVENT_GID:
    printf("process event: gid\n");
    printf("process tid:%d, pid:%d, uid:%d->%d\n\n\n",
     procevent->event_data.id.process_pid,
     procevent->event_data.id.process_tgid,
     procevent->event_data.id.r.rgid,
     procevent->event_data.id.e.egid);
    break;
  case PROC_EVENT_EXIT:
    printf("process event: exit\n");
    printf("tid:%d, pid:%d, exit code:%d\n\n\n",
     procevent->event_data.exit.process_pid,
     procevent->event_data.exit.process_tgid,
     procevent->event_data.exit.exit_code);
    break;
  default:
    printf("Unkown process action\n\n\n");
    break;
}
    }
  }
}
</pre>

这部分代码用于处理各种不同的进程事件，并输出具体的事件信息，对于 fork 事件，输出父进程和线程的 ID 以及子进程和线程的 ID，对于 exec 事件则输出执行 exec 调用的进程和线程的 ID，对于用户 ID 变更事件，则输出制造该事件的进程和线程的 ID，旧的用户 ID 以及新的用户 ID，对于组 ID 变更事件，则输出制造该事件的进程和线程的 ID，旧的组 ID 以及新的组 ID，对于 exit 事件，则输出结束运行的进程和线程的 ID 以及退出码。

下面是该程序在作者的红旗 Linux 桌面版 4.1 上的运行结果示例：

<pre>
[root@localhost yangyi]# gcc -I linux-2.6.15.4/include cn_proc_user.c -o
cn_proc_user
[root@localhost yangyi]# ./cn_proc_user
process event: turn on process event listening.
process event: acknowledge for turning on process event listening
process event: fork
parent tid:2720, pid:2720
child tid:2775, pid:2775
process event: exec
tid:2775, pid:2775
process event: exit
tid:2775, pid:2775, exit code:0
.
.
.
process event: uid
process tid:2877, pid:2877, uid:500->0
process event: gid
process tid:2877, pid:2877, gid:500->500
process event: uid
process tid:2877, pid:2877, uid:500->0
process event: uid
process tid:2877, pid:2877, uid:500->0
process event: uid
process tid:2877, pid:2877, uid:500->0
process event: uid
process tid:2877, pid:2877, uid:500->0
process event: fork
parent tid:2877, pid:2877
child tid:2878, pid:2878
process event: gid
process tid:2878, pid:2878, gid:500->500
process event: uid
process tid:2878, pid:2878, uid:500->500
process event: exec
tid:2878, pid:2878
process event: exit
tid:2878, pid:2878, exit code:0
process event: turn off process event listening.
[root@localhost yangyi]#
</pre>


* 五、如何实现一个新的连接器实例

要想实现一个新的连接器，必须首先定义个新的连接器标识，目前最新的内核包括两个连接器实例，一个是进程事件连接器，另一个为 CIFS 连接器，因此新的连接器标识必须不同于现有的任何一个连接器标识。例如，用户可以使用如下语句来定义一个新的连接器标识：

<pre>
#define CN_IDX_NEW 3
#define CN_VAL_NEW 1
</pre>

当然连接器必须在内核实现，因此需要通过内核模块来定义相应的回调函数并在初始化代码中注册该回调函数，回调函数实际上用于处理发送给该连接器的消息。该模块也必须实现消息发送函数供其它内核子系统方便使用该连接器。下面是作者编写的一个文件系统事件连接器的实现代码，该代码根据进程事件连接器（drivers/connector/cn_proc.c）编写而成。

头文件 include/linux/cn_fs.h 定义了文件系统事件处理的数据结构、open 消息发送函数声明以及一些相关的宏定义，结构 struct fs_event 定义了文件系统事件连接器消息结构。

<pre>
#ifndef CN_FS_H
#define CN_FS_H
#include <linux/types.h>
#include <linux/time.h>
#include <linux/connector.h>
#define TASK_NAME_LEN 16
#define FILE_NAME_LEN 256
#define CN_IDX_FS 3
#define CN_VAL_FS 1
/*
 * Userspace sends this enum to register with the kernel that it is listening
 * for events on the connector.
 */
enum fs_cn_mcast_op {
	FS_CN_MCAST_LISTEN = 1,
	FS_CN_MCAST_IGNORE = 2
};
struct fs_event {
	enum type {
		/* Use successive bits so the enums can be used to record
		 * sets of events as well
		 */
		FS_EVENT_NONE = 0x00000000,
		FS_EVENT_OPEN = 0x00000001
	} type;
	__u32 cpu;
	struct timespec timestamp;
	union {
		struct {
			__u32 err;
		} ack;
		struct fs_read_event {
			char proc_name[TASK_NAME_LEN];
			char file_name[FILE_NAME_LEN];
		} read;
	} event_data;
};
#ifdef __KERNEL__
#ifdef CONFIG_FS_EVENTS
void fs_open_connector(struct dentry * dentryp);
#else
static void fs_open_connector(struct dentry * dentryp)
{}
#endif	/* CONFIG_FS_EVENTS */
#endif	/* __KERNEL__ */
#endif	/* CN_FS_H */
</pre>

下面文件 drivers/connector/cn_fs.c 是文件系统连接器的实现代码。

<pre>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cn_fs.h>
#include <asm/atomic.h>
</pre>

这些是必要的内核头文件。

<pre>
#define CN_FS_MSG_SIZE (sizeof(struct cn_msg) + sizeof(struct fs_event))
</pre>

该宏定义了文件系统消息的大小。

<pre>
static atomic_t fs_event_listeners = ATOMIC_INIT(0);
</pre>

该变量用于控制文件系统 open 事件的报告，初始化时设置为 0，即不报告 open 事件。用户态应用可以通过向文件系统连接器发送控制消息来打开和关闭 open 事件的报告。

<pre>
static struct cb_id cn_fs_event_id = { CN_IDX_FS, CN_VAL_FS }; 这是连接器的唯一标识，连接器需要它来找到对应的连接器实例。

/* fs_event_counts is used as the sequence number of the netlink message */
static DEFINE_PER_CPU(__u32, fs_event_counts) = { 0 };
</pre>

该 PER_CPU 变量用于统计总共的文件系统事件，并通过它来获得连接器消息的顺序号。

<pre>
static inline void get_seq(__u32 *ts, int *cpu)
{
	*ts = get_cpu_var(fs_event_counts)++;
	*cpu = smp_processor_id();
	put_cpu_var(fs_event_counts);
}
</pre>

该函数用于得到下一个消息的顺序号。

<pre>
void fs_open_connector(struct dentry * dentryp)
{
	struct cn_msg *msg;
	struct fs_event *event;
	__u8 buffer[CN_FS_MSG_SIZE];
	if (atomic_read(&fs_event_listeners) < 1)
		return;
	printk("cn_fs: fs_open_connector\n");
	msg = (struct cn_msg*)buffer;
	event = (struct fs_event*)msg->data;
	get_seq(&msg->seq, &event->cpu);
	getnstimestamp(&event->timestamp);
	event->type = FS_EVENT_OPEN;
	memcpy(event->event_data.read.proc_name, current->comm,
	TASK_NAME_LEN);
	memcpy(event->event_data.read.file_name, dentryp->d_name.name,
	dentryp->d_name.len);
	event->event_data.read.file_name[dentryp->d_name.len] = '\0';
	memcpy(&msg->id, &cn_fs_event_id, sizeof(msg->id));
	msg->ack = 0; /* not used */
	msg->len = sizeof(struct fs_event);
	/*  If cn_netlink_send() failed, the data is not sent */
	cn_netlink_send(msg, CN_IDX_FS, GFP_KERNEL);
}
</pre>

该函数为 open 事件消息的发送函数，它被文件系统的 open 操作调用来向文件系统事件连接器发送 open 事件。它首先设置文件系统事件结构 struct fs_event 的各个字段，字段event->timestamp为发生事件的时间，event->type为事件的类型，该模块只实现了两个事件，一个为对控制操作的响应，另一个为 open 事件。字段event->event_data.read.proc_name为打开文件的进程名称，event->event_data.read.file_name 则为被打开的文件名。消息设置完毕后可通过连接器接口函数 cn_netlink_send 直接发送，该发送函数不能保证消息发送成功，因此对于要求可靠传输消息的应用，必须通过响应来最终确认是否发送成功。

<pre>
static void cn_fs_ack(int err, int rcvd_seq, int rcvd_ack)
{
	struct cn_msg *msg;
	struct fs_event *event;
	__u8 buffer[CN_FS_MSG_SIZE];
	if (atomic_read(&fs_event_listeners) < 1)
		return;
	msg = (struct cn_msg*)buffer;
	event = (struct fs_event*)msg->data;
	msg->seq = rcvd_seq;
	getnstimestamp(&event->timestamp);
	event->cpu = -1;
	event->type = FS_EVENT_NONE;
	event->event_data.ack.err = err;
	memcpy(&msg->id, &cn_fs_event_id, sizeof(msg->id));
	msg->ack = rcvd_ack + 1;
	msg->len = sizeof(struct fs_event);
	cn_netlink_send(msg, CN_IDX_FS, GFP_KERNEL);
}
</pre>

该函数用于给用户态发送响应消息。注意，响应消息的顺序号必须为被响应的消息的顺序号，响应号则为顺序号加1。

<pre>
static void cn_fs_mcast_ctl(void *data)
{
	struct cn_msg *msg = data;
	enum fs_cn_mcast_op *mc_op = NULL;
	int err = 0;
	if (msg->len != sizeof(*mc_op))
		return;
	mc_op = (enum fs_cn_mcast_op*)msg->data;
	switch (*mc_op) {
	case FS_CN_MCAST_LISTEN:
		atomic_inc(&fs_event_listeners);
		break;
	case FS_CN_MCAST_IGNORE:
		atomic_dec(&fs_event_listeners);
		break;
	default:
		err = EINVAL;
		break;
	}
	cn_fs_ack(err, msg->seq, msg->ack);
}
</pre>

该函数为注册给连接器的回调函数，它用于处理用户态应用发送给该连接器的消息。因此，实际上它是消息接收函数。对于该模块，它实际上用于处理控制命令，用户态发送的控制命令消息最后将由它来处理，它实际上用于打开和关闭文件系统事件报告开关，同时它也负责发送响应消息给用户态应用。

<pre>
static int __init cn_fs_init(void)
{
	int err;
	if ((err = cn_add_callback(&cn_fs_event_id, "cn_fs",
	 			   &cn_fs_mcast_ctl))) {
		printk(KERN_WARNING "cn_fs failed to register\n");
		return err;
	}
	return 0;
}
</pre>

该函数在内核初始化时调用，它使用连接器接口函数 cn_add_callback 注册了一个新的连接器实例。

<pre>
module_init(cn_fs_init);
</pre>

该语句用于告诉内核函数 cn_fs_init 需要在内核初始化时调用。

程序源码包中的 cn_fs_user.c 是使用该文件系统连接器来监视文件系统 open 事件的一个示例程序，它的大部分代码与前面的进程事件监视程序示例一样，只是把进程事件相关的处理部分替换为文件系统事件对应处理。另外一点需要特别注意，对于组号大于 1 的连接器，用户态应用必须通过第三节介绍的方式来加入到组中，否则，应用无法收到连接器的消息。

下面是作者在红旗 Linux 桌面版 4.1 上运行 cn_fs_user 的输出结果示例：

<pre>
[root@localhost yangyi]# gcc -I linux-2.6.14.5/include cn_fs_user.c -o
cn_fs_user
[root@localhost yangyi]# ./cn_fs_user
filesystem event: turn on filesystem event listening.
filesystem event: acknowledge for turning on filesystem event listening
filesystem event: open
process 'rfdock' open file 'en.xpm'
filesystem event: open
process 'bash' open file 'passwd'
filesystem event: open
process 'cat' open file 'ld.so.cache'
filesystem event: open
process 'cat' open file 'libc-2.3.2.so'
filesystem event: open
process 'cat' open file 'locale-archive'
filesystem event: open
process 'cat' open file 'test_cn_proc.c'
filesystem event: open
process 'rfdock' open file 'en.xpm'
filesystem event: turn off filesystem event listening.
[root@localhost yangyi]#
</pre>

小结

连接器是非常便利的用户态与内核态的通信方式，内核开发者在编写内核子系统或模块时可以采用这种方式方便地进行用户态与内核态的数据交换。
