---
layout: post
title: "FUSE(Filesystem in userspace)(用户空间文件系统),user-space框架简单介绍"
categories: 文件系统
tags: [linux, filesystem, fuse]
date: 2014-08-15 16:31:30
---

<pre>
具体为：
user-space框架之前我们需要面向内核去开发文件系统，user-space框架之后我们则直接面向文件系统进行开发，不需要了解内核的相关细节。
详细如下：

在用户空间的文件系统出现之前，文件系统的开发曾是内核开发人员的工作。创建文件系统需要了解内核编程和内核技术（例如 vfs）方面的知识。调试则需要 C 和 C++ 方面的专业技能。但是其他开发人员需要熟练地操作文件系统以添加个性化特性（例如添加历史记录或转发缓存）及对其改进。
使用FUSE，您无需理解文件系统的内幕，也不用学习内核模块编程的知识，就可以开发用户空间的文件系统框架。 
FUSE简介
                   FUSE structure
       使用 FUSE 您可以开发功能完备的文件系统：其具有简单的 API 库，可以被非特权用户访问，并可以安全的实施。更重要的是，FUSE 以往的表现充分证明了其稳定性。
      使用 FUSE，您可以像可执行二进制文件一样来开发文件系统，它们需要链接到 FUSE 库上 —— 换言之，这个文件系统框架并不需要您了解文件系统的内幕和内核模块编程的知识。
FUSE源码包
      要开发一个文件系统，首先请下载 FUSE 的源代码（我们使用最新的稳定版本2.7.4）并展开这个包：tar -zxvf fuse-2.7.4.tar.gz。这会创建一个 FUSE 目录，其中保存的是源代码。fuse-2.4 目录的内容如下：

    * ./doc 包含了与 FUSE 有关的文档。
    * ./kernel 包含了 FUSE 内核模块的源代码（对于使用 FUSE 开发文件系统来说，您当然不用懂得这些代码的机制）。
    * ./include 包含了 FUSE API 头，您需要这些文件来创建文件系统。您现在唯一需要的就是 fuse.h。
    * ./lib 中存放的是创建 FUSE 库的源代码，您需要将它们与您的二进制文件链接在一起来创建文件系统。
    * ./util 中存放的是 FUSE 工具库的源代码。
    * ./example 当然包含的是一些供您参考的例子，例如 fusexmp.null 和 hello 文件系统。
FUSE安装
       我们是在FC6的环境下进行安装的，在这些版本中大都已经自动安装了fuse，我们也可以下载最新的源码进行安装。
       1. 在 fuse-2.7.4 目录中运行 configure 脚本： ./configure --enable-kernel-module。这会创建所需要的 makefile 等内容。因为FC6中已有比较老的版本，增加命令--enable-kernel-module可以强制编译kernel module。
       2. 运行 ./make 来编译库、二进制文件和内核模块。查看 kernel 目录中的文件 ./kernel/fuse.ko —— 这是内核模块文件。还要查看 lib 目录中的 fuse.o、mount.o 和 helper.o。
       3. 运行 ./make install 完成 FUSE 的安装。
要使用 FUSE 来创建一个文件系统，您需要声明一个 fuse_operations 类型的结构变量，并将其传递给 fuse_main 函数。fuse_operations 结构中有一个指针，指向在执行适当操作时需要调用的函数。清单 1 给出了 fuse_operations 结构。
定义需要的函数
fuse_operation 结构中需要的函数：
</pre>

{% highlight c %}
struct fuse_operations {
    int (*getattr) (const char *, struct stat *);
    int (*readlink) (const char *, char *, size_t);
    int (*getdir) (const char *, fuse_dirh_t, fuse_dirfil_t);
    int (*mknod) (const char *, mode_t, dev_t);
    int (*mkdir) (const char *, mode_t);
    int (*unlink) (const char *);
    int (*rmdir) (const char *);
    int (*symlink) (const char *, const char *);
    int (*rename) (const char *, const char *);
    int (*link) (const char *, const char *);
    int (*chmod) (const char *, mode_t);
    int (*chown) (const char *, uid_t, gid_t);
    int (*truncate) (const char *, off_t);
    int (*utime) (const char *, struct utimbuf *);
    int (*open) (const char *, struct fuse_file_info *);
    int (*read) (const char *, char *, size_t, off_t, struct fuse_file_info *);
    int (*write) (const char *, const char *, size_t, off_t,struct fuse_file_info *);
    int (*statfs) (const char *, struct statfs *);
    int (*flush) (const char *, struct fuse_file_info *);
    int (*release) (const char *, struct fuse_file_info *);
    int (*fsync) (const char *, int, struct fuse_file_info *);
    int (*setxattr) (const char *, const char *, const char *, size_t, int);
    int (*getxattr) (const char *, const char *, char *, size_t);
    int (*listxattr) (const char *, char *, size_t);
    int (*removexattr) (const char *, const char *);
};
{% endhighlight %}

<pre>
       这些操作并非都是必需的，但是一个文件系统要想正常工作，就需要其中的很多函数。您可以实现一个具有特殊目的的 .flush、.release 或 .fsync 方法的功能完备的文件系统。
    * getattr: int (*getattr) (const char *, struct stat *);
      这个函数与 stat() 类似。st_dev 和 st_blksize 域都可以忽略。st_ino 域也会被忽略，除非在执行 mount 时指定了 use_ino 选项。
    * readlink: int (*readlink) (const char *, char *, size_t);
      这个函数会读取一个符号链接的目标。缓冲区应该是一个以 null 结束的字符串。缓冲区的大小参数包括这个 null 结束字符的空间。如果链接名太长，不能保存到缓冲区中，就应该被截断。成功时的返回值应该是 “0”。
    * getdir: int (*getdir) (const char *, fuse_dirh_t, fuse_dirfil_t);
      这个函数会读取一个目录中的内容。这个操作实际上是在一次调用中执行 opendir()、readdir()、...、closedir() 序列。对于每个目录项来说，都应该调用 filldir() 函数。
    * mknod: int (*mknod) (const char *, mode_t, dev_t);
      这个函数会创建一个文件节点。此处没有 create() 操作；mknod() 会在创建非目录、非符号链接的节点时调用。
    * mkdir: int (*mkdir) (const char *, mode_t);
      rmdir: int (*rmdir) (const char *);
      这两个函数分别用来创建和删除一个目录。
    * unlink: int (*unlink) (const char *);
      rename: int (*rename) (const char *, const char *);
      这两个函数分别用来删除和重命名一个文件。
    * symlink: int (*symlink) (const char *, const char *);
      这个函数用来创建一个符号链接。
    * link: int (*link) (const char *, const char *);
      这个函数创建一个到文件的硬链接。
    * chmod: int (*chmod) (const char *, mode_t);
      chown: int (*chown) (const char *, uid_t, gid_t);
      truncate: int (*truncate) (const char *, off_t);
      utime: int (*utime) (const char *, struct utimbuf *);
      这 4 个函数分别用来修改文件的权限位、属主和用户、大小以及文件的访问/修改时间。
    * open: int (*open) (const char *, struct fuse_file_info *);
      这是文件的打开操作。对 open() 函数不能传递创建或截断标记（O_CREAT、O_EXCL、O_TRUNC）。这个函数应该检查是否允许执行给定的标记的操作。另外，open() 也可能在 fuse_file_info 结构中返回任意的文件句柄，这会传递给所有的文件操作。
    * read: int (*read) (const char *, char *, size_t, off_t, struct fuse_file_info *);
      这个函数从一个打开文件中读取数据。除非碰到 EOF 或出现错误，否则 read() 应该返回所请求的字节数的数据；否则，其余数据都会被替换成 0。一个例外是在执行 mount 命令时指定了 direct_io 选项，在这种情况中 read() 系统调用的返回值会影响这个操作的返回值。
    * write: int (*write) (const char *, const char *, size_t, off_t, struct fuse_file_info *);
      这个函数将数据写入一个打开的文件中。除非碰到 EOF 或出现错误，否则 write() 应该返回所请求的字节数的数据。一个例外是在执行 mount 命令时指定了 direct_io 选项（这于 read() 操作的情况类似）。
    * statfs: int (*statfs) (const char *, struct statfs *);
      这个函数获取文件系统的统计信息。f_type 和 f_fsid 域都会被忽略。
    * flush: int (*flush) (const char *, struct fuse_file_info *);
      这表示要刷新缓存数据。它并不等于 fsync() 函数 —— 也不是请求同步脏数据。每次对一个文件描述符执行 close() 函数时，都会调用 flush()；因此如果文件系统希望在 close() 中返回写错误，并且这个文件已经缓存了脏数据，那么此处就是回写数据并返回错误的好地方。由于很多应用程序都会忽略 close() 错误，因此这通常用处不大。

注意：我们也可以对一个 open() 多次调用 flush() 方法。如果由于调用了 dup()、dup2() 或 fork() 而产生多个文件描述符指向一个打开文件的情况，就可能会需要这种用法。我们无法确定哪个 flush 操作是最后一次操作，因此每个 flush 都应该同等地对待。多个写刷新序列相当罕见，因此这并不是什么问题。

    * release: int (*release) (const char *, struct fuse_file_info *);
      这个函数释放一个打开文件。release() 是在对一个打开文件没有其他引用时调用的 —— 此时所有的文件描述符都会被关闭，所有的内存映射都会被取消。对于每个 open() 调用来说，都必须有一个使用完全相同标记和文件描述符的 release() 调用。对一个文件打开多次是可能的，在这种情况中只会考虑最后一次 release，然后就不能再对这个文件执行更多的读/写操作了。release 的返回值会被忽略。
    * fsync: int (*fsync) (const char *, int, struct fuse_file_info *);
      这个函数用来同步文件内容。如果 datasync 参数为非 0，那么就只会刷新用户数据，而不会刷新元数据。
    * setxattr: int (*setxattr) (const char *, const char *, const char *, size_t, int);
      getxattr: int (*getxattr) (const char *, const char *, char *, size_t);
      listxattr: int (*listxattr) (const char *, char *, size_t);
      removexattr: int (*removexattr) (const char *, const char *);
      这些函数分别用来设置、获取、列出和删除扩展属性。

example/fusexmp
        FUSE提供了几个例子，这里主要用fusexmp举个例子。fusexmp可以将根目录（默认）或者某一目录以镜像形式挂载到指定目录中。对镜像目录进行操作的同时也在对根目录或指定目录进行操作。 
       切换到example目录； 
       使用gcc对文件进行编译 gcc -Wall `pkg-config fuse --cflags --libs` fusexmp.c -o fusexmp；
       创建一个空的目录 mkdir /home/chen/tmp；
       执行./fuxexmp /home/user/tmp 则将/root目录以镜像形式挂载到用户的tmp目录下，使用ls命令可以看到目录中的文件和跟目录下的文件一样。
       执行fusermount －u /home/user/tmp则可卸载文件系统，此时在tmp目录下执行ls，得到结果为空。
       
       若想挂载指定目录，则使用命令 ./fuxexmp -o modules=subdir,subdir=/home/otheruser/，不能指定tmp目录及其父目录，会引起崩溃。
      卸载命令同上，fusermount －u /home/user/tmp 

      若在执行挂载的过程当中报错failed to open /dev/fuse: Permission denied 时，将用户添加fuse组即可正常使用。执行ls －l /dev/fuse 即可发现 /dev/fuse的所属用户与用户组为 root:fuse (。。。本人在root权限下make install)
</pre>

下面以hello.c为例分析FUSE的编写规范： 

{% highlight c %}
#define FUSE_USE_VERSION 26
#include <fuse.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>

static const char *hello_str = "Hello World!\n";
static const char *hello_path = "/hello";

/*该函数与stat()类似，用于得到文件的属性，将其存入到结构体struct stat中*/
static int hello_getattr(const char *path, struct stat *stbuf)
{
	int res = 0;
	memset(stbuf, 0, sizeof(struct stat)); //用于初始化结构体stat
	if (strcmp(path, "/") == 0) {
		stbuf->st_mode = S_IFDIR | 0755; //S_IFDIR 用于说明/为目录，详见S_IFDIR定义
		stbuf->st_nlink = 2; //文件链接数
	} else if (strcmp(path, hello_path) == 0) {
		stbuf->st_mode = S_IFREG | 0444; //S_IFREG用于说明/hello为常规文件
		stbuf->st_nlink = 1;
		stbuf->st_size = strlen(hello_str); //设置文件长度为hello_str的长度
	} else
		res = -ENOENT; //返回错误信息，没有该文件或目录
	return res; //执行成功返回0
}

/*该函数用于读取/目录中的内容，并在/目录下增加了. .. hello三个目录项*/
static int hello_readdir(const char *path, void *buf, fuse_fill_dir_t filler,
		off_t offset, struct fuse_file_info *fi)
{
	(void) offset;
	(void) fi;

	if (strcmp(path, "/") != 0)
		return -ENOENT;

	/*
	   fill的定义：
	   typedef int (*fuse_fill_dir_t) (void *buf, const char *name,
	   const struct stat *stbuf, off_t off);

	   其作用是在readdir函数中增加一个目录项
	 */
	filler(buf, ".", NULL, 0);
	//在/目录下增加. 这个目录项
	filler(buf, "..", NULL, 0);
	// 增加.. 目录项
	filler(buf, hello_path + 1, NULL, 0);
	//增加hello目录项
	return 0;
}

/*用于打开hello文件*/
static int hello_open(const char *path, struct fuse_file_info *fi)
{
	if (strcmp(path, hello_path) != 0)
		return -ENOENT;

	if ((fi->flags & 3) != O_RDONLY)
		return -EACCES;
	return 0;
}

/*读取hello文件时的操作，它实际上读取的是字符串hello_str的内容*/
static int hello_read(const char *path, char *buf, size_t size, off_t offset,
		struct fuse_file_info *fi)
{
	size_t len;
	(void) fi;

	if(strcmp(path, hello_path) != 0)
		return -ENOENT;

	len = strlen(hello_str);
	if (offset < len) {
		if (offset + size > len)
			size = len - offset;
		memcpy(buf, hello_str + offset, size);
	} else
		size = 0;
	return size;
}

/*注册上面定义的函数*/
static struct fuse_operations hello_oper = {
	.getattr = hello_getattr,
	.readdir = hello_readdir,
	.open = hello_open,
	.read = hello_read,
};

/*用户只需要调用fuse_main()，剩下的事就交给FUSE了*/
int main(int argc, char *argv[])
{
	return fuse_main(argc, argv, &hello_oper, NULL);
}
{% endhighlight %}

终端运行：

~/fuse/example$ mkdir /tmp/fuse //在/tmp下建立fuse目录，用于挂载hello文件系统

~/fuse/example$ ./hello /tmp/fuse //挂载hello文件系统

~/fuse/example$ ls -l /tmp/fuse //执行ls时，会调用到readdir函数，该函数会添加一个hello 文件

总用量 0

-r--r--r-- 1 root root 13 1970-01-01 07:00 hello

~/fuse/example$ cat /tmp/fuse/hello //执行cat hello时，会调用open以及read函数，将

Hello World! 字符串hello_str中的内容读出

~/fuse/example$ fusermount -u /tmp/fuse //卸载hello文件系统

通过上述的分析可以知道，使用FUSE必须要自己实现对文件或目录的操作，系统调用也会最终调用到用户自己实现的函数。用户实现的函数需要在结构体fuse_operations中注册。而在main()函数中，用户只需要调用fuse_main()函数就可以了，剩下的复杂工作可以交给FUSE。
