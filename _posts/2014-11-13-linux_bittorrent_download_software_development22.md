---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--tracker服务器交互模块（tracker.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:41
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;malloc.h&gt;
#include &lt;errno.h&gt;
#include &lt;ctype.h&gt;
#include &lt;unistd.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
#include &lt;sys/time.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/socket.h&gt;
#include &lt;netinet/in.h&gt;
#include &lt;netdb.h&gt;
#include &lt;arpa/inet.h&gt;
#include &quot;parse_metafile.h&quot;
#include &quot;peer.h&quot;
#include &quot;tracker.h&quot;

extern unsigned char  info_hash[20];//这两个数据都是在种子解析文件中定义的
extern unsigned char  peer_id[20];
extern Announce_list  *announce_list_head;//为存放各个Tracker的URL

extern int                 *sock;//连接Tracker的套接字
extern struct sockaddr_in  *tracker;
extern int                 *valid;//traker服务器的状态
extern int                  tracker_count;//tracker服务器的状态

extern int                 *peer_sock;//链接peer的套接字
extern struct sockaddr_in  *peer_addr;
extern int                 *peer_valid;//指示连接peer的状态
extern int                  peer_count;//尝试与多少个peer建立连接

Peer_addr  *peer_addr_head = NULL;//根据多少个Tracker服务器，建立多少个peer_addr

int http_encode(unsigned char *in,int len1,char *out,int len2)//http协议说明，非数字和字母都要进行装换
{                                                            //函数参数为一个是转换输入，另一个为转换输出
	int  i, j;
	char hex_table[16] = &quot;0123456789abcdef&quot;; 
	
	if( (len1 != 20) || (len2 &lt;= 90) )  return -1;
	for(i = 0, j = 0; i &lt; 20; i++, j++) { //如果len1不等于20或者len2小于等于90，则出错
		if( isalpha(in[i]) || isdigit(in[i]) )
			out[j] = in[i];
		else { 
		        out[j] = '%';//这是编码部分，至于为何是20与90，不太清楚
			j++;
			out[j] = hex_table[in[i] &gt;&gt; 4];
			j++;
			out[j] = hex_table[in[i] &amp; 0xf];
		}
	}
	out[j] = '\0';
	
#ifdef DEBUG
	//printf(&quot;http encoded:%s\n&quot;,out);
#endif
	
	return 0;
}

int get_tracker_name(Announce_list *node,char *name,int len)
{
	int i = 0, j = 0;

	if( (len &lt; 64) || (node == NULL) )  return -1;
	if( memcmp(node-&gt;announce,&quot;http://&quot;,7) == 0 ) 
		i = i + 7;
	while( (node-&gt;announce[i] != '/') &amp;&amp; (node-&gt;announce[i] != ':') ) {//因为本书就是要得到主机的名字
	        name[j] = node-&gt;announce[i];//将主机名写入name中
		i++;
		j++;
		if( i == strlen(node-&gt;announce) )  break;//这种情况下说明其URL中没有‘/’以及‘：’所以才要靠这个来判断
	}
	name[j] = '\0';

#ifdef DEBUG
	printf(&quot;%s\n&quot;,node-&gt;announce);
	printf(&quot;tracker name:%s\n&quot;,name);
#endif

	return 0;
}

int get_tracker_port(Announce_list *node,unsigned short *port)
{
	int i = 0;

	if( (node == NULL) || (port == NULL) )  return -1;
	if( memcmp(node-&gt;announce,&quot;http://&quot;,7) == 0 )  i = i + 7;
	*port = 0;
	while( i &lt; strlen(node-&gt;announce) ) {
		if( node-&gt;announce[i] != ':')   { i++; continue; }

		i++;  // skip ':'
		while( isdigit(node-&gt;announce[i]) ) { 
		  *port =  *port * 10 + (node-&gt;announce[i] - '0');//如果判断为数字，则求出其端口号
			i++;
		}
		break;
	}
	if(*port == 0)  *port = 80;

#ifdef DEBUG
	printf(&quot;tracker port:%d\n&quot;,*port);
#endif

	return 0;
}

int create_request(char *request,int len,Announce_list *node,
				   unsigned short port,long long down,long long up,
				   long long left,int numwant)
{
	char           encoded_info_hash[100];
	char           encoded_peer_id[100];
	int            key;
	char           tracker_name[128];
	unsigned short tracker_port;

	http_encode(info_hash,20,encoded_info_hash,100);//这就可以解释为何输入字节数为20了，因为它为info_hash或者为peer_id的长度
	http_encode(peer_id,20,encoded_peer_id,100);

	srand(time(NULL));
	key = rand() / 10000;//得到随机的key值

	get_tracker_name(node,tracker_name,128);
	get_tracker_port(node,&amp;tracker_port);

	sprintf(request,
	&quot;GET /announce?info_hash=%s&amp;peer_id=%s&amp;port=%u&quot;
	&quot;&amp;uploaded=%lld&amp;downloaded=%lld&amp;left=%lld&quot;
	&quot;&amp;event=started&amp;key=%d&amp;compact=1&amp;numwant=%d HTTP/1.0\r\n&quot;
	&quot;Host: %s\r\nUser-Agent: Bittorrent\r\nAccept: */*\r\n&quot;
	&quot;Accept-Encoding: gzip\r\nConnection: closed\r\n\r\n&quot;, //包含上传数据量，以及下载数据量，left为还有多少剩余，numwant，表示希望返回的peer数
	encoded_info_hash,encoded_peer_id,port,up,down,left,
		key,numwant,tracker_name);//key关键字一般用来标识客户端，但是已经有了peer_id,所以这个参数可选

#ifdef DEBUG
	printf(&quot;request:%s\n&quot;,request);
#endif

	return 0;
}

int get_response_type(char *buffer,int len,int *total_length)//这里的total_length用于在之后的调用函数中分配内存
{
	int i, content_length = 0;

	for(i = 0; i &lt; len-7; i++) {
		if(memcmp(&amp;buffer[i],&quot;5:peers&quot;,7) == 0) { 
			i = i+7;
			break; //相当于在buffer所指向的字符串数组中查找‘5：peers’，如果下标=len-7，则buffer中没有机会存储“5:peers”字符串
		}
	}
	if(i == len-7)        return -1;  // 返回的消息不含&quot;5:peers&quot;关键字
	if(buffer[i] != 'l')  return 0;   //这说明消息并不是B编码的列表，所以返回的消息的类型为第一种

	*total_length = 0;
	for(i = 0; i &lt; len-16; i++) {
		if(memcmp(&amp;buffer[i],&quot;Content-Length: &quot;,16) == 0) {
			i = i+16;
			break; 
		}
	}
	if(i != len-16) {//用于判断是否找到content_length,不相等，说明找到
		while(isdigit(buffer[i])) {
		  content_length = content_length * 10 + (buffer[i] - '0');//用于计算content_length
			i++;
		}
		for(i = 0; i &lt; len-4; i++) {//用于判断是否找到“\r\n\r\n”
		  if(memcmp(&amp;buffer[i],&quot;\r\n\r\n&quot;,4) == 0)  { i = i+4; break; }//用于计算total_length
		}
		if(i != len-4)  *total_length = content_length + i;
	}

	if(*total_length == 0)  return -1;
	else return 1;
}

int prepare_connect_tracker(int *max_sockfd)
{
	int             i, flags, ret, count = 0;
	struct hostent  *ht;//通过gethostbyname 返回的类型
	/* hostent的定义如下：
           struct hostent {
                  char *h_name;
                  char **h_aliases;
                  int h_addrtype;
                  int h_length;
                  char **h_addr_list;
                  #define h_addr h_addr_list[0]
                };

        h_name – 地址的正式名称。
        h_aliases – 空字节-地址的预备名称的指针。
        h_addrtype –地址类型; 通常是AF_INET。  
        h_length – 地址的比特长度。
        h_addr_list – 零字节-主机网络地址指针。网络字节顺序。
        h_addr - h_addr_list中的第一地址*/
 
	Announce_list   *p = announce_list_head;

	while(p != NULL)  { count++; p = p-&gt;next; }
	tracker_count = count; //得到Tracker服务器的个数
	sock = (int *)malloc(count * sizeof(int));//有多少个Tracker服务器就有多少个套接字
	if(sock == NULL)  goto OUT;
	tracker = (struct sockaddr_in *)malloc(count * sizeof(struct sockaddr_in));//用来保存地址信息
	if(tracker == NULL)  goto OUT;
	valid = (int *)malloc(count * sizeof(int));//用来查看是否有效
	if(valid == NULL)  goto OUT;
	
	p = announce_list_head;
	for(i = 0; i &lt; count; i++) {
		char            tracker_name[128];
		unsigned short  tracker_port = 0;
		
		sock[i] = socket(AF_INET,SOCK_STREAM,0);//创建TCP套接字，针对Tracker地址
		if(sock &lt; 0) {
			printf(&quot;%s:%d socket create failed\n&quot;,__FILE__,__LINE__);
			valid[i] = 0;
			p = p-&gt;next;
			continue;
		}

		get_tracker_name(p,tracker_name,128);
		get_tracker_port(p,&amp;tracker_port);
		
		// 从主机名获取IP地址
		ht = gethostbyname(tracker_name);
		if(ht == NULL) {
		        printf(&quot;gethostbyname failed:%s\n&quot;,hstrerror(h_errno)); //如果出错的话，错误信息是写入h_errno当中的
			valid[i] = 0;
		} else {
			memset(&amp;tracker[i], 0, sizeof(struct sockaddr_in));
			memcpy(&amp;tracker[i].sin_addr.s_addr, ht-&gt;h_addr_list[0], 4);//将得到的地址信息存储到多对应的tracker结构中
			tracker[i].sin_port = htons(tracker_port);//设置端口号以及相关参数
			tracker[i].sin_family = AF_INET;
			valid[i] = -1;//此时的这个状态还没有建立链接
		}
		
		p = p-&gt;next;//对每一个Tracker服务器，都构建一个套接字
	}

	for(i = 0; i &lt; tracker_count; i++) {
		if(valid[i] != 0) {
			if(sock[i] &gt; *max_sockfd) *max_sockfd = sock[i];
			// 设置套接字为非阻塞
			flags = fcntl(sock[i],F_GETFL,0);//关于fcntl的相关设置为P163值，关键在获得文件打开的方式，成功返回标志值
			fcntl(sock[i],F_SETFL,flags|O_NONBLOCK);//设置文件的打开方式为第三个参数指定的方式，等于原打开方式加上非阻塞方式
			// 连接tracker
			ret = connect(sock[i],(struct sockaddr *)&amp;tracker[i], //有套接字，并且有相关的Tracker地址信息，那么就可以建立连接
				          sizeof(struct sockaddr));
			if(ret &lt; 0 &amp;&amp; errno != EINPROGRESS)  valid[i] = 0;	//等于0，说明链接建立失败
			// 如果返回0，说明连接已经建立
			if(ret == 0)  valid[i] = 1;  //只有在全部建立完成之后，才会叫valid设置为1
		}
	}

	return 0;

OUT:
	if(sock != NULL)    free(sock);
	if(tracker != NULL) free(tracker);
	if(valid != NULL)   free(valid);
	return -1;
}

//以非阻塞的方式来链接peer。下面的这个函数与prepare_connect_tracker基本上一样
int prepare_connect_peer(int *max_sockfd)//max_sockfd为最大套接字的值
{
	int       i, flags, ret, count = 0;
	Peer_addr *p;
	
	p = peer_addr_head;//这个时候peer_addr_head的值为NULL
	while(p != 0)  { count++; p = p-&gt;next; }

	peer_count = count;
	peer_sock = (int *)malloc(count*sizeof(int));//这边所有的sock都加上了前缀peer
	if(peer_sock == NULL)  goto OUT;
	peer_addr = (struct sockaddr_in *)malloc(count*sizeof(struct sockaddr_in));
	if(peer_addr == NULL)  goto OUT;
	peer_valid = (int *)malloc(count*sizeof(int));
	if(peer_valid == NULL) goto OUT;
	
	p = peer_addr_head;  // 此处p重新赋值
	for(i = 0; i &lt; count &amp;&amp; p != NULL; i++) {
		peer_sock[i] = socket(AF_INET,SOCK_STREAM,0);
		if(peer_sock[i] &lt; 0) { 
			printf(&quot;%s:%d socket create failed\n&quot;,__FILE__,__LINE__);
			valid[i] = 0;
			p = p-&gt;next;
			continue; 
		}

		memset(&amp;peer_addr[i], 0, sizeof(struct sockaddr_in));
		peer_addr[i].sin_addr.s_addr = inet_addr(p-&gt;ip);//因为p的类型为Peer_addr,所以其包含ip地址信息
		peer_addr[i].sin_port = htons(p-&gt;port);
		peer_addr[i].sin_family = AF_INET;
		peer_valid[i] = -1;
		
		p = p-&gt;next;
	}
	count = i;
	
	for(i = 0; i &lt; count; i++) {
		if(peer_sock[i] &gt; *max_sockfd) *max_sockfd = peer_sock[i];
		// 设置套接字为非阻塞
		flags = fcntl(peer_sock[i],F_GETFL,0);//获得文件的打开方式
		fcntl(peer_sock[i],F_SETFL,flags|O_NONBLOCK);//重新设置文件的打开方式，加上非阻塞
		// 连接peer
		ret = connect(peer_sock[i],(struct sockaddr *)&amp;peer_addr[i],
			          sizeof(struct sockaddr));
		if(ret &lt; 0 &amp;&amp; errno != EINPROGRESS)  peer_valid[i] = 0;
		// 如果返回0，说明连接已经建立
		if(ret == 0)  peer_valid[i] = 1;
	}
	
	free_peer_addr_head();
	return 0;

OUT:
	if(peer_sock  != NULL)  free(peer_sock);
	if(peer_addr  != NULL)  free(peer_addr);
	if(peer_valid != NULL)  free(peer_valid);
	return -1;
}

int parse_tracker_response1(char *buffer,int ret,char *redirection,int len)//对Tracker服务器返回的第一种类型的消息解析
{
	int           i, j, count = 0;
	unsigned char c[4];
	Peer_addr     *node, *p;

	for(i = 0; i &lt; ret - 10; i++) {
		if(memcmp(&amp;buffer[i],&quot;Location: &quot;,10) == 0) { 
			i = i + 10;
			j = 0;
			while(buffer[i]!='?' &amp;&amp; i&lt;ret &amp;&amp; j&lt;len) {//在遇到？之前，将“Location:”与“？”之间的内容从buffer拷贝到redirection
			  redirection[j] = buffer[i];      //为何这样拷贝，我也不太清楚
				i++;
				j++;
			}
			redirection[j] = '\0';
			return 1;//如果真的出现这种情况的话，就直接返回了，后面都不用继续求了
		}
	}

	// 获取返回的peer数,关键词&quot;5:peers&quot;之后为各个Peer的IP和端口
	for(i = 0; i &lt; ret - 7; i++) {
	  if(memcmp(&amp;buffer[i],&quot;5:peers&quot;,7) == 0) { i = i + 7; break; }//说明存在peer的IP地址以及端口
	}
	if(i == ret - 7	) { 
		printf(&quot;%s:%d can not find keyword 5:peers \n&quot;,__FILE__,__LINE__);
		return -1; 
	}
	while( isdigit(buffer[i]) ) {//计算总共的字节数
		count = count * 10 + (buffer[i] - '0');
		i++;
	}
	i++;  // 跳过&quot;:&quot;

	count = (ret - i) / 6;//一个IP地址占四个字节，端口占两个字节，所以确定每一peer需要6个字节，count为peer的数目
		
	// 将每个peer的IP和端口保存到peer_addr_head指向的链表中
	for(; count != 0; count--) {
		node = (Peer_addr*)malloc(sizeof(Peer_addr));
		c[0] = buffer[i];   c[1] = buffer[i+1]; 
		c[2] = buffer[i+2]; c[3] = buffer[i+3];
		sprintf(node-&gt;ip,&quot;%u.%u.%u.%u&quot;,c[0],c[1],c[2],c[3]);//将得到的IP地址存储在Peer_addr结构体中
		i += 4;
		node-&gt;port = ntohs(*(unsigned short*)&amp;buffer[i]);//unsigned short为两个字节，所以确定了根据起始地址如何取值
		i += 2;
		node-&gt;next = NULL;
	
		// 判断当前peer是否已经存在于链表中
		p = peer_addr_head;
		while(p != NULL) {
			if( memcmp(node-&gt;ip,p-&gt;ip,strlen(node-&gt;ip)) == 0 ) { 
				free(node); 
				break;
			}
			p = p-&gt;next;
		}
			
		// 将当前结点添加到链表中
		if(p == NULL) {//此时说明这个peer_addr节点没有在peer_addr_head的链表中，可以添加进去
			if(peer_addr_head == NULL)
				peer_addr_head = node;
			else {
				p = peer_addr_head;
				while(p-&gt;next != NULL) p = p-&gt;next;
				p-&gt;next = node;
			}
		}
	}
		
#ifdef DEBUG
		count = 0;
		p = peer_addr_head;
		while(p != NULL) {
		  printf(&quot;+++ connecting peer %-16s:%-5d +++ \n&quot;,p-&gt;ip,p-&gt;port);//调试信息，将链接的peer的地址以及端口信息打印出来
			p = p-&gt;next;
			count++;
		}
		printf(&quot;peer count is :%d \n&quot;,count);
#endif

		return 0;
}


//解析Tracker服务器返回的第二种消息
int parse_tracker_response2(char *buffer,int ret)
{
	int        i, ip_len, port;
	Peer_addr  *node = NULL, *p = peer_addr_head;

	if(peer_addr_head != NULL) {
		printf(&quot;Must free peer_addr_head\n&quot;);
		return -1;
	}
	
	for(i = 0; i &lt; ret; i++) {
	         if(memcmp(&amp;buffer[i],&quot;2:ip&quot;,4) == 0) {//第二种消息的查找更简单，查找ip，查找port，构造peer_addr，然后加入peer_addr_head中就可以了
			i += 4;
			ip_len = 0;
			while(isdigit(buffer[i])) {
				ip_len = ip_len * 10 + (buffer[i] - '0');
				i++;
			}//确定ip地址所占有的字节数
			i++;  // skip &quot;:&quot;
			node = (Peer_addr*)malloc(sizeof(Peer_addr));
			if(node == NULL) { 
				printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); 
				continue;
			}
			memcpy(node-&gt;ip,&amp;buffer[i],ip_len);//因为在第二种方式中，已经包含了格式，所以直接拷贝就可以了，因为为字符串，所以最后家少‘\0’
			(node-&gt;ip)[ip_len] = '\0';
			node-&gt;next = NULL;
		}
		if(memcmp(&amp;buffer[i],&quot;4:port&quot;,6) == 0) {
			i += 6;
			i++;  // skip &quot;i&quot;//这个很关键
			port = 0;
			while(isdigit(buffer[i])) {
				port = port * 10 + (buffer[i] - '0');
				i++;
			}
			if(node != NULL)  node-&gt;port = port;//因为i之后就是port，所以直接赋值就可以了
			else continue;
			
			printf(&quot;+++ add a peer %-16s:%-5d +++ \n&quot;,node-&gt;ip,node-&gt;port);
			
			if(p == peer_addr_head) { peer_addr_head = node; p = node; }//加入到pee_addr_head中
			else p-&gt;next = node;
			node = NULL;
		}
	}
	
	return 0;
}

int add_peer_node_to_peerlist(int *sock,struct sockaddr_in saptr)//这个函数相当与将peer_addr与peer建立了联系
{
	Peer *node;
	
	node = add_peer_node();//在这个地方构建peer_head队列
	if(node == NULL)  return -1;
	
	node-&gt;socket = *sock; //相当于对peer的前几个元素进行赋值进行赋值
	node-&gt;port   = ntohs(saptr.sin_port);
	node-&gt;state  = INITIAL;
	strcpy(node-&gt;ip,inet_ntoa(saptr.sin_addr));
	node-&gt;start_timestamp = time(NULL);

	return 0;
}

void free_peer_addr_head()
{
	Peer_addr *p = peer_addr_head;
    while(p != NULL) {
		p = p-&gt;next;
		free(peer_addr_head);
		peer_addr_head = p;
    }
	peer_addr_head = NULL;
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8973101
</pre>
