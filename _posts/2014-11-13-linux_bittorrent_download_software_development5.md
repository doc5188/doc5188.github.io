---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--缓冲管理模块（data.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:29
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;malloc.h&gt;
#include &quot;data.h&quot;
#include &quot;sha1.h&quot;
#include &quot;parse_metafile.h&quot;
#include &quot;bitfield.h&quot;
#include &quot;message.h&quot;
#include &quot;policy.h&quot;
#include &quot;torrent.h&quot;

// 对定义的缓冲区的说明：
// 设置缓冲区可以避免频繁读写硬盘,从而有利于保护硬盘
// 每个缓冲区结点的大小为16KB,默认生成1024个结点,总大小为16MB
// 缓冲区以256KB为单位使用,也就是临近的16个结点为一组存放一个piece
// 下标为0～15的结点存放一个piece,16～31存放一个piece,依次类推
// 也可以处理一个piece的大小不为256KB的情况,如一个piece大小为512KB
// 为了处理的方便,所有缓冲区在程序启动时统一申请,在程序结束时释放

// 缓冲区中共有多少个Btcache结点
#define btcache_len 1024

// 以下变量定义在parse_metafile.c文件
extern  char   *file_name;
extern  Files  *files_head;
extern  int     file_length;
extern  int     piece_length;
extern  int     pieces_length;
extern  char   *pieces;

extern  Bitmap *bitmap;
extern  int     download_piece_num;
extern  Peer   *peer_head;

// 指向一个16MB大小的缓冲区
Btcache *btcache_head = NULL;
// 存放待下载文件的最后一个piece
Btcache *last_piece = NULL;
int      last_piece_index = 0;
int      last_piece_count = 0;
int      last_slice_len   = 0;

// 存放文件描述符
int *fds    = NULL;
int fds_len = 0;

// 存放刚刚下载到的piece的索引
// 下载到一个新的piece要向所有的peer通报
int have_piece_index[64]; //这个在之前的massage.c中用到，抓要的用途就是辅助发送have消息

// 是否进入了终端模式
int end_mode = 0;

// 为Btcache节点分配内存空间
Btcache* initialize_btcache_node()
{
	Btcache *node;

	node = (Btcache *)malloc(sizeof(Btcache));
	if(node == NULL) {
		printf(&quot;%s:%d malloc error\n&quot;,__FILE__,__LINE__);
		return NULL;
	}

	node-&gt;buff = (unsigned char *)malloc(16*1024);//从这里开始，为node的成员赋值
	if(node-&gt;buff == NULL) {
		if(node != NULL)  free(node);
		printf(&quot;%s:%d malloc error\n&quot;,__FILE__,__LINE__);
		return NULL;
	}

	node-&gt;index  = -1;
	node-&gt;begin  = -1;
	node-&gt;length = -1;

	node-&gt;in_use       =  0;
	node-&gt;read_write   = -1;
	node-&gt;is_full      =  0;
	node-&gt;is_writed    =  0;
	node-&gt;access_count =  0;
	node-&gt;next         =  NULL;

	return node;
}

// 创建总大小为16K*1024即16MB的缓冲区
int create_btcache()
{
	int     i;
	Btcache *node, *last;

	for(i = 0; i &lt; btcache_len; i++) {
		node = initialize_btcache_node();
		if( node == NULL )  { 
			printf(&quot;%s:%d create_btcache error\n&quot;,__FILE__,__LINE__);
			release_memory_in_btcache();
			return -1;
		}

		if( btcache_head == NULL )  { btcache_head = node; last = node; }
		else  { last-&gt;next = node; last = node; }
	}
        //为最后一个piece申请空间

	int count = file_length % piece_length / (16*1024);//为计算最后一个piece的slice的数目
	if(file_length % piece_length % (16*1024) != 0)  count++;//如果最后一个slice外还有剩余，那么将count加1
	last_piece_count = count;//最后一个piece所包含的slice数目

	last_slice_len = file_length % piece_length % (16*1024);//最后一个slice的长度，单位为字节
	if(last_slice_len == 0)  last_slice_len = 16*1024;
	
	last_piece_index = pieces_length / 20 -1;//最后一个piece的index值

	while(count &gt; 0) {
		node = initialize_btcache_node();
		if(node == NULL) {
			printf(&quot;%s:%d create_btcache error\n&quot;,__FILE__,__LINE__);
			release_memory_in_btcache();
			return -1;
		}

		if(last_piece == NULL)  { last_piece = node; last = node; }//last_piece在文件的开始有定义
		else  { last-&gt;next = node; last = node; }

		count--;//将最后的一个piece中的slice用链表链接起来，链表的头节点为last_piece
	}

	for(i = 0; i &lt; 64; i++) {
	      have_piece_index[i] = -1;//存放刚下载的piece的索引，但是为何要设置为64呢?
	}

	return 0;
}

// 释放缓冲区动态分配的内存
void release_memory_in_btcache()
{
	Btcache *p;

	p = btcache_head;
	while(p != NULL) {      //将分配的16K*1024的内存释放掉
		btcache_head = p-&gt;next;
		if(p-&gt;buff != NULL) free(p-&gt;buff);
		free(p);
		p = btcache_head;
	}

	release_last_piece();
	if(fds != NULL)  free(fds);
}

void release_last_piece()
{
      Btcache *p = last_piece; //将最后一个piece中的分配的slice内存释放掉

	while(p != NULL) {
		last_piece = p-&gt;next;
		if(p-&gt;buff != NULL) free(p-&gt;buff);
		free(p);
		p = last_piece;
	}
}

// 判断种子文件中待下载的文件个数
int get_files_count()
{
	int count = 0;
	
	if(is_multi_files() == 0)  return 1;

	Files *p = files_head;//将文件名存放在以files_head为首的链表中，files_head存放的是一个文件的路径以及长度
	while(p != NULL) {
		count++;
		p = p-&gt;next;
	}
	
	return count;
}

// 根据种子文件中的信息创建保存下载数据的文件
// 通过lseek和write两个函数来实现物理存储空间的分配
int create_files()
{
	int  ret, i;
	char buff[1] = { 0x0 };
	
	fds_len = get_files_count();
	if(fds_len &lt; 0)  return -1;
	
	fds = (int *)malloc(fds_len * sizeof(int));//文件描述符指针，定义的时候就是定义int *fds
	if(fds == NULL)  return -1;
	
	
	if( is_multi_files() == 0 ) {  // 待下载的为单文件

		*fds = open(file_name,O_RDWR|O_CREAT,0777);
		if(*fds &lt; 0)  { printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1; }
				
		ret = lseek(*fds,file_length-1,SEEK_SET);//将文件的指针移动到文件的末尾
		if(ret &lt; 0)   { printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1; }
		
		ret = write(*fds,buff,1); //将buff中的1个字节写入文件描述符所对应的文件中，这样的话文件的开始的第一个字节为0x0.
		if(ret != 1)  { printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1; }
				
	} else {  // 待下载的是多个文件				
		// 查看目录是否已创建,若没有则创建
        	ret = chdir(file_name);//其工作目录由当前目录切换到file_name所指定的目录，并且只能影响当前的进程，这和cd有很大的区别
		if(ret &lt; 0) {
			ret = mkdir(file_name,0777);
			if(ret &lt; 0)  { printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1; }
			ret = chdir(file_name);
			if(ret &lt; 0)  { printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1; }
		}
					
		Files *p = files_head;
		i = 0;
		while(p != NULL) {
   		        fds[i] = open(p-&gt;path,O_RDWR|O_CREAT,0777); //在当前目录下，打开当前的文件，这就是切换目录的原因
			if(fds[i] &lt; 0) {printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1;}
					
			ret = lseek(fds[i],p-&gt;length-1,SEEK_SET);
			if(ret &lt; 0)    {printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1;}
					
			ret = write(fds[i],buff,1);
			if(ret != 1)   {printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); return -1;}
				
			p = p-&gt;next;
			i++;
		} //end while
	} //end else

	return 0;
}

// 判断一个Btcache结点(即一个slice)中的数据要写到哪个文件的哪个位置,并写入
int write_btcache_node_to_harddisk(Btcache *node) //可以理解为write_slice_to_harddisk,因为一个btcache结点就是一个slice
{
	long long     line_position;
	Files         *p;
	int           i;

	if((node == NULL) || (fds == NULL))  return -1;

	// 无论是否下载多文件，将要下载的所有数据看成一个线性字节流
	// line_position指示要写入硬盘的线性位置
	// piece_length为每个piece长度，它被定义在parse_metafile.c中
	line_position = node-&gt;index * piece_length + node-&gt;begin;//定义要写入硬盘的线性位置，其实也就是相对于文件起始处的相对未知

	if( is_multi_files() == 0 ) {  // 如果下载的是单个文件
		lseek(*fds,line_position,SEEK_SET);
		write(*fds,node-&gt;buff,node-&gt;length);//将buffer里面的内容写入文件描述符所代表的文件中
		return 0;
	}

	// 下载的是多个文件
	if(files_head == NULL) { 
		printf(&quot;%s:%d file_head is NULL&quot;,__FILE__,__LINE__);
		return -1;
	}
	p = files_head;
	i = 0;
	while(p != NULL) {
	  if((line_position &lt; p-&gt;length) &amp;&amp; (line_position+node-&gt;length &lt; p-&gt;length)) {//这两个的比较有作用吗？
			// 待写入的数据属于同一个文件
			lseek(fds[i],line_position,SEEK_SET);
			write(fds[i],node-&gt;buff,node-&gt;length);
			break;
		} 
	  else if((line_position &lt; p-&gt;length) &amp;&amp; (line_position+node-&gt;length &gt;= p-&gt;length)) {//需要确定的一点是，p-&gt;length放置的是文件的长度，但是对于一个文件来说，也是
			// 待写入的数据跨越了两个文件或两个以上的文件                                //终点的值            
			int offset = 0;             // buff内的偏移,也是已写的字节数
			int left   = node-&gt;length;  // 剩余要写的字节数
			
			lseek(fds[i],line_position,SEEK_SET);
			write(fds[i],node-&gt;buff,p-&gt;length - line_position);
			offset = p-&gt;length - line_position;        // offset存放已写的字节数
			left = left - (p-&gt;length - line_position); // 还需写在字节数
			p = p-&gt;next;                               // 用于获取下一个文件的长度
			i++;                                       // 获取下一个文件描述符
			
			while(left &gt; 0)
				if(p-&gt;length &gt;= left) {  // 当前文件的长度大于等于要写的字节数 
					lseek(fds[i],0,SEEK_SET);
					write(fds[i],node-&gt;buff+offset,left); // 写入剩余要写的字节数
					left = 0;
				} else {  // 当前文件的长度小于要写的字节数
					lseek(fds[i],0,SEEK_SET);
					write(fds[i],node-&gt;buff+offset,p-&gt;length); // 写满当前文件
					offset = offset + p-&gt;length;
					left = left - p-&gt;length;
					i++;
					p = p-&gt;next;
				}
				
				break;
		} else {
			// 待写入的数据不应写入当前文件，
                	    line_position = line_position - p-&gt;length;//这种是什么情况？
			i++;
			p = p-&gt;next;
		}
	}
	return 0;
}

// 从硬盘读出数据，存放到缓冲区中，在peer需要时发送给peer
// 该函数非常类似于write_btcache_node_to_harddisk
// 要读的piece的索引index，在piece中的起始位置begin和长度已存到node指向的节点中
int read_slice_from_harddisk(Btcache *node)//这两个函数基本上没有什么变化，只不过将write改为read
{
	unsigned int  line_position;
	Files         *p;
	int           i;
	
	if( (node == NULL) || (fds == NULL) )  return -1;
	
	if( (node-&gt;index &gt;= pieces_length/20) || (node-&gt;begin &gt;= piece_length) ||//pieces存放的是所有piece的hash值，每一个piece所对应的hash值为20个字节
	    (node-&gt;length &gt; 16*1024) )                      //每一个piece的长度一般为256k，node-&gt;length一般为16k
		return -1;

	// 计算线性偏移量
	line_position = node-&gt;index * piece_length + node-&gt;begin;
	
	if( is_multi_files() == 0 ) {  // 如果下载的是单个文件
		lseek(*fds,line_position,SEEK_SET);
		read(*fds,node-&gt;buff,node-&gt;length);
		return 0;
	}
	
	// 如果下载的是多个文件
	if(files_head == NULL)  get_files_length_path();
	p = files_head;
	i = 0;
	while(p != NULL) {
		if((line_position &lt; p-&gt;length) &amp;&amp; (line_position+node-&gt;length &lt; p-&gt;length)) {
			// 待读出的数据属于同一个文件
			lseek(fds[i],line_position,SEEK_SET);
			read(fds[i],node-&gt;buff,node-&gt;length);
			break;
		} else if((line_position &lt; p-&gt;length) &amp;&amp; (line_position+node-&gt;length &gt;= p-&gt;length)) {
			// 待读出的数据跨越了两个文件或两个以上的文件
			int offset = 0;             // buff内的偏移,也是已读的字节数
			int left   = node-&gt;length;  // 剩余要读的字节数

			lseek(fds[i],line_position,SEEK_SET);
			read(fds[i],node-&gt;buff,p-&gt;length - line_position);
			offset = p-&gt;length - line_position;        // offset存放已读的字节数
			left = left - (p-&gt;length - line_position); // 还需读在字节数
			p = p-&gt;next;                               // 用于获取下一个文件的长度
			i++;                                       // 获取下一个文件描述符

			while(left &gt; 0)
				if(p-&gt;length &gt;= left) {  // 当前文件的长度大于等于要读的字节数 
					lseek(fds[i],0,SEEK_SET);
					read(fds[i],node-&gt;buff+offset,left); // 读取剩余要读的字节数
					left = 0;
				} else {  // 当前文件的长度小于要读的字节数
				        lseek(fds[i],0,SEEK_SET);//这种情况下，说明left除了存储新的文件外，还有剩余
					read(fds[i],node-&gt;buff+offset,p-&gt;length); // 读取当前文件的所有内容
					offset = offset + p-&gt;length;
					left = left - p-&gt;length;
					i++;
					p = p-&gt;next;
				}

			break;
		} else {
			// 待读出的数据不应写入当前文件，这一个btcach节点确实不应该写入硬盘中
			line_position = line_position - p-&gt;length;
			i++;
			p = p-&gt;next;
		}
	}
	return 0;
}

// 在peer队列中删除对某个piece的请求
int delete_request_end_mode(int index)//这个模式的意义现在还没有搞清楚
{
	Peer          *p = peer_head;
	Request_piece *req_p, *req_q;

	if(index &lt; 0 || index &gt;= pieces_length/20)  return -1;

	while(p != NULL) {
		req_p = p-&gt;Request_piece_head;
		while(req_p != NULL) {
			if(req_p-&gt;index == index) {
			  if(req_p == p-&gt;Request_piece_head) p-&gt;Request_piece_head = req_p-&gt;next;//如果这个index恰好为请求piece队列的头节点，那么需要删除头节点
			        else req_q-&gt;next = req_p-&gt;next;//否则的话只需要跳过req_p，链接到后面的节点就可以了
				free(req_p);

				req_p = p-&gt;Request_piece_head;
				continue;
			}
			req_q = req_p;
			req_p = req_p-&gt;next;//req_p总是比req_q多前进一个未知
		}
		
		p = p-&gt;next;//对peer队列中的各个peer全部进行处理
	}

	return 0;
}

// 检查一个piece的数据是否正确,若正确存入硬盘
int write_piece_to_harddisk(int sequnce,Peer *peer)//sequnce为存放piece的第一个slice的btcashe的结点编号。将缓冲区的数据写入硬盘
{
	Btcache        *node_ptr = btcache_head, *p;
	unsigned char  piece_hash1[20], piece_hash2[20];
	int            slice_count = piece_length / (16*1024);
	int            index, index_copy;

	if(peer==NULL) return -1;

	int i = 0;
	while(i &lt; sequnce)  { node_ptr = node_ptr-&gt;next; i++; }//node_ptr指向第i个btcache节点
	p = node_ptr;  // p指向piece的第一个slice所在的btcache结点

	// 校验piece的HASH值
	SHA1_CTX ctx;
	SHA1Init(&amp;ctx);
	while(slice_count&gt;0 &amp;&amp; node_ptr!=NULL) {//计算该piece的hash值
	  SHA1Update(&amp;ctx,node_ptr-&gt;buff,16*1024);//计算的时候是一个slice,一个slice计算的
		slice_count--;
		node_ptr = node_ptr-&gt;next;
	}
	SHA1Final(piece_hash1,&amp;ctx);
	
        //从种子文件中获取该piece的正确的hash值
	index = p-&gt;index * 20;//求得index所在的字节数
	index_copy = p-&gt;index;  // 存放piece的index
	for(i = 0; i &lt; 20; i++)  piece_hash2[i] = pieces[index+i];
        
        //比较两个hash值是否一致
	int ret = memcmp(piece_hash1,piece_hash2,20);
	if(ret != 0)  { printf(&quot;piece hash is wrong\n&quot;); return -1; }
	
	node_ptr = p;
	slice_count = piece_length / (16*1024); 
	while(slice_count &gt; 0) {
	        write_btcache_node_to_harddisk(node_ptr);//如果两个piece的hash值是相同的，那么将对应的btcache(slice)写入到文件之中。

		// 在peer中的请求队列中删除piece请求
		Request_piece *req_p = peer-&gt;Request_piece_head;
		Request_piece *req_q = peer-&gt;Request_piece_head;//因为该piece已经写入硬盘，所以对该消息的请求终止
		while(req_p != NULL) {
			if(req_p-&gt;begin==node_ptr-&gt;begin &amp;&amp; req_p-&gt;index==node_ptr-&gt;index)
			{
				if(req_p == peer-&gt;Request_piece_head) 
				  peer-&gt;Request_piece_head = req_p-&gt;next;//为头节点的清空
				else
				  req_q-&gt;next = req_p-&gt;next;//非头节点的情况
				free(req_p);//不管怎么样，这两条语句都是要执行的
				req_p = req_q = NULL;
				break;
			}
			req_q = req_p;
			req_p = req_p-&gt;next;
		}

		node_ptr-&gt;index  = -1;//将node_ptr的值进行重新设定，相当与btcache节点空闲
		node_ptr-&gt;begin  = -1;
		node_ptr-&gt;length = -1;
		
		node_ptr-&gt;in_use       = 0;
		node_ptr-&gt;read_write   = -1;
		node_ptr-&gt;is_full      = 0;
		node_ptr-&gt;is_writed    = 0;
		node_ptr-&gt;access_count = 0;

		node_ptr = node_ptr-&gt;next;//指向下一个node_ptr的节点
		slice_count--;//count--，其实count的值为256，为一个piece的大小
	}
	
	if(end_mode == 1)  delete_request_end_mode(index_copy);//删除peer队列中对该piece的请求。之前的是删除本客户端对该消息的请求，在这个模式下，是删除
                                                               //peer对该消息的请求
	// 更新位图
	set_bit_value(bitmap,index_copy,1);

	// 准备发送have消息
	for(i = 0; i &lt; 64; i++) {
		if(have_piece_index[i] == -1) { 
			have_piece_index[i] = index_copy; 
			break; 
		}
	}

	download_piece_num++;
	if(download_piece_num % 10 == 0)  restore_bitmap();

	printf(&quot;%%%%%% Total piece download:%d %%%%%%\n&quot;,download_piece_num);
	printf(&quot;writed piece index:%d  total pieces:%d\n&quot;,index_copy,pieces_length/20);
	compute_total_rate();   // 计算总的下载、上传速度
	print_process_info();   // 打印下载进度信息

	return 0;
}

// 从硬盘上读取一个piece到p所指向的缓冲区中
int read_piece_from_harddisk(Btcache *p, int index)
{
	Btcache  *node_ptr   = p;
	int      begin       = 0;
	int      length      = 16*1024;
	int      slice_count = piece_length / (16*1024);
	int      ret;

	if(p==NULL || index&gt;=pieces_length/20)  return -1;

	while(slice_count &gt; 0) {
	        node_ptr-&gt;index  = index;//index的值一直不发生变化
		node_ptr-&gt;begin  = begin;
		node_ptr-&gt;length = length;

		ret = read_slice_from_harddisk(node_ptr);
		if(ret &lt; 0) return -1;

		node_ptr-&gt;in_use       = 1;//成功后对node_ptr的标志位进行赋值
		node_ptr-&gt;read_write   = 0;
		node_ptr-&gt;is_full      = 1;
		node_ptr-&gt;is_writed    = 0;
		node_ptr-&gt;access_count = 0;

		begin += 16*1024;//起始位置的值发生变化
		slice_count--;
		node_ptr = node_ptr-&gt;next;//btcashe结点指向下一个，index表示的是一个piece，所以其不发生变化
	}

	return 0;
}

// 将16MB缓冲区中已下载的piece写入硬盘,这样可以释放缓冲区
int write_btcache_to_harddisk(Peer *peer)
{
	Btcache          *p = btcache_head;
	int     slice_count = piece_length / (16*1024);//每一个piece_length的值都是256k，所以说slice_count的值为16
	int     index_count = 0;
	int      full_count = 0;
	int     first_index;

	while(p != NULL) {
		if(index_count % slice_count == 0) {
			full_count = 0;
			first_index = index_count;//first_index指向的是piece的第一个slice的位置
		}

		if( (p-&gt;in_use  == 1) &amp;&amp; (p-&gt;read_write == 1) &amp;&amp; //说的是数据要写入硬盘，所以read_write为1，is_writed,说明是否将数据写入硬盘
			(p-&gt;is_full == 1) &amp;&amp; (p-&gt;is_writed  == 0) ) {
			full_count++;
		}
		if(full_count == slice_count) {
		  write_piece_to_harddisk(first_index,peer);//凑齐一个piece，将piece写入到硬盘中，
		}

		index_count++;//不管if语句的结果如何，这条语句都会执行下去，每当到达一个slice_count的值，full_count,便重新计算
		p = p-&gt;next;
	}

	return 0;
}

// 当缓冲区不够用时,释放那些从硬盘上读取的piece
int release_read_btcache_node(int base_count)//这里的base_count为访问计数的意思，当访问计数达到某一个值的时候，则将该piece释放掉
{
	Btcache           *p = btcache_head;
	Btcache           *q = NULL;
	int            count = 0;
	int       used_count = 0;
	int      slice_count = piece_length / (16*1024);

	if(base_count &lt; 0)  return -1;

	while(p != NULL) {
	        if(count % slice_count == 0)  { used_count = 0; q = p; }//这里的意思是每经过一个piece，used_count就会重新赋值，而q每次都是指向一个新的piece的开始
		if(p-&gt;in_use==1 &amp;&amp; p-&gt;read_write==0)  used_count += p-&gt;access_count;//当对缓冲区的访问计数达到某一个值的时候，则终止
		if(used_count == base_count)  break;  // 找到一个空闲的piece
		
		count++;
		p = p-&gt;next;
	}

	if(p != NULL) {
	  p = q;// 释放piece,p此时指向该piece的第一个slice。
		while(slice_count &gt; 0) {
			p-&gt;index  = -1;
			p-&gt;begin  = -1;
			p-&gt;length = -1;
			
			p-&gt;in_use       =  0;
			p-&gt;read_write   = -1;
			p-&gt;is_full      =  0;
			p-&gt;is_writed    =  0;
			p-&gt;access_count =  0;

			slice_count--;
			p = p-&gt;next;
		}
	}

	return 0;
}

// 下载完一个slice后,检查是否该slice为一个piece最后一块  //下载完之后也是将其写入缓冲区
// 若是则写入硬盘,只对刚刚开始下载时起作用,这样可以立即使peer得知
int is_a_complete_piece(int index, int *sequnce)//这里的sequnce为btcache节点的编号，现在函数给出的两个参数，可能为该slice的索引，以及btcachenode的编号
{
	Btcache          *p = btcache_head;
	int     slice_count = piece_length / (16*1024);
	int           count = 0;
	int             num = 0;
	int        complete = 0;

	while(p != NULL) {//这个while循环的目的就是找到对应的piece以及btcache节点的位置
	        if( count%slice_count==0 &amp;&amp; p-&gt;index!=index ) {//现在判断的是下载的一个slice是否为一个piece的最后一个slice。p-&gt;index判断是否为该piece.
		        num = slice_count;//首先完成一份的赋值工作，让num=16
			while(num&gt;0 &amp;&amp; p!=NULL)  { p = p-&gt;next; num--; count++; }//每一个piece的第一个slice所对应的编号除以slice_count都是等于0的
			continue;
		}
		if( count%slice_count!=0 || p-&gt;read_write!=1 || p-&gt;is_full!=1) //走到这一步说明上面的if语句不成立了
			break;

		*sequnce = count;//走到这一步的条件是，count%slice_count==0,并且p-&gt;index==index.我们要找的就是这样的一种状态。
		num = slice_count;//此时的sequnce为piece的第一个slice结点的编号
	
		while(num&gt;0 &amp;&amp; p!=NULL) {
			if(p-&gt;index==index &amp;&amp; p-&gt;read_write==1 &amp;&amp; p-&gt;is_full==1)
			  complete++;//这样就可以知道该piece是否完整了
			else break;
	
			num--;
			p = p-&gt;next;
		}

		break;
	}

	if(complete == slice_count) return 1;//这样的话说明该slice是piece最后一个slice.
	else return 0;
}

// 将16MB的缓冲区中所存的所有数据清空
void clear_btcache()
{
	Btcache *node = btcache_head;
	while(node != NULL) {
		node-&gt;index  = -1;
		node-&gt;begin  = -1;
		node-&gt;length = -1;
		
		node-&gt;in_use       =  0;
		node-&gt;read_write   = -1;
		node-&gt;is_full      =  0;
		node-&gt;is_writed    =  0;
		node-&gt;access_count =  0;
		
		node = node-&gt;next;
	}
}

// 将从peer处获取的一个slice存储到缓冲区中
int write_slice_to_btcache(int index,int begin,int length,
						   unsigned char *buff,int len,Peer *peer)
{
	int     count = 0, slice_count, unuse_count;
	Btcache *p = btcache_head, *q = NULL;  // q指向每个piece第一个slice
	
	if(p == NULL)  return -1;
	if(index&gt;=pieces_length/20 || begin&gt;piece_length-16*1024)  return -1;//如果begin大于某一个值的话，那么它连请求一个slice的机会都没有了，所以说错误
	if(buff==NULL || peer==NULL)  return -1;

	if(index == last_piece_index) {//如果说该slice的索引为最后一个piece，那么调用函数将其写入
		write_slice_to_last_piece(index,begin,length,buff,len,peer);
		return 0;
	}

	if(end_mode == 1) {//在终端模式下，判断该piece是否被下载
		if( get_bit_value(bitmap,index) == 1 )  return 0;
	}
	
	// 遍历缓冲区,检查当前slice所在的piece的其他数据是否已存在
	// 若存在说明不是一个新的piece,若不存在说明是一个新的piece
	slice_count = piece_length / (16*1024);
	while(p != NULL) {
		if(count%slice_count == 0)  q = p;
		if(p-&gt;index==index &amp;&amp; p-&gt;in_use==1)  break;//用于判断该slice所在的piece是否存在

		count++;
		p = p-&gt;next;
	}
	
	// p非空说明当前slice所在的piece的有些数据已经下载
	if(p != NULL) {
		count = begin / (16*1024);  // count存放当前要存的slice在piece中的索引，在这里全部以slice为单位
		p = q;
		while(count &gt; 0)  { p = p-&gt;next; count--; }
		
		if(p-&gt;begin==begin &amp;&amp; p-&gt;in_use==1 &amp;&amp; p-&gt;read_write==1 &amp;&amp; p-&gt;is_full==1)//p指向的位置就是该slice应该存储的位置
			return 0; // 该slice已存在
		
		p-&gt;index  = index;
		p-&gt;begin  = begin;
		p-&gt;length = length; //这里的length是否为1？？
		
		p-&gt;in_use       = 1;
		p-&gt;read_write   = 1;
		p-&gt;is_full      = 1;
		p-&gt;is_writed    = 0;
		p-&gt;access_count = 0;
		
		memcpy(p-&gt;buff,buff,len);//将从peer得到的slice拷贝到btcache的结点中。
		printf(&quot;+++++ write a slice to btcache index:%-6d begin:%-6x +++++\n&quot;,
			   index,begin);
		
		// 如果是刚刚开始下载(下载到的piece不足10个),则立即写入硬盘,并告知peer
		if(download_piece_num &lt; 1000) {//但是这里表述的意思可不是10个，而是1000个
			int sequece;
			int ret;
			ret = is_a_complete_piece(index,&amp;sequece);//判断一个piece是否为一个完整的piece
			if(ret == 1) {
				printf(&quot;###### begin write a piece to harddisk ######\n&quot;);
				write_piece_to_harddisk(sequece,peer); //将该完整的piece写入硬盘
				printf(&quot;###### end   write a piece to harddisk ######\n&quot;);
			}
		}
		return 0;
	}
	
	// p为空说明当前slice是其所在的piece的第一块下载到的数据
	// 首先判断是否存在空的缓冲区,若不存在,则将已下载的写入硬盘
	int i = 4;
	while(i &gt; 0) {
		slice_count = piece_length / (16*1024);
		count       = 0;  // 计数当前指向第几个slice
		unuse_count = 0;  // 计数当前piece中有多少个空的slice
		Btcache *q;       
		p = btcache_head;
		
		while(p != NULL) {
			if(count%slice_count == 0)  { unuse_count = 0; q = p; }
			if(p-&gt;in_use == 0) unuse_count++;//因为要找到足够的缓冲空间来存放一个piece，所以来判断是否存在这样的条件
			if(unuse_count == slice_count)  break;  // 找到一个空闲的piece
			
			count++;
			p = p-&gt;next;
		}
		
		if(p != NULL) {//这个时候说明找到了足够的缓冲去来存放一个piece
		        p = q;//q存放的是每一个piece，第一个slice开始的位置
			count = begin / (16*1024);//begin的偏移为piece的内偏移
			while(count &gt; 0)  { p = p-&gt;next; count--; }

			p-&gt;index  = index;//将该slice的相关信息写入到p所代表的bitcache节点中
			p-&gt;begin  = begin;
			p-&gt;length = length;
			
			p-&gt;in_use       = 1;
			p-&gt;read_write   = 1;
			p-&gt;is_full      = 1;
			p-&gt;is_writed    = 0;
			p-&gt;access_count = 0;
			
			memcpy(p-&gt;buff,buff,len);//将buff里面的内容写入到p所在的bitcache结点中
			printf(&quot;+++++ write a slice to btcache index:%-6d begin:%-6x +++++\n&quot;,
				   index,begin);
			return 0;
		}
		
		if(i == 4) write_btcache_to_harddisk(peer);//走到这一步的时候，说明缓冲区没有足够的空间，这个时候需要将缓冲区的内容写入硬盘，并释放缓冲区数据
		if(i == 3) release_read_btcache_node(16);//当对某一个piece的访问技术达到16是，就将该peice释放掉
		if(i == 2) release_read_btcache_node(8);
		if(i == 1) release_read_btcache_node(0);//说明，没有访问过的也都释放掉，用以腾出足够的空间
		i--;
	}
	
	// 如果还没有空闲的缓冲区,丢弃下载到这个slice
	printf(&quot;+++++ write a slice to btcache FAILED :NO BUFFER +++++\n&quot;);
	clear_btcache();

	return 0;
}

// 从缓冲区获取一个slice,读取的slice存放到buff指向的数组中
// 若缓冲区中不存在该slice,则从硬盘读slice所在的piece到缓冲区中
int read_slice_for_send(int index,int begin,int length,Peer *peer)
{
	Btcache  *p = btcache_head, *q;  // q指向每个piece第一个slice
	int       ret;
	
	// 检查参数是否有误
	if(index&gt;=pieces_length/20 || begin&gt;piece_length-16*1024)  return -1;

	ret = get_bit_value(bitmap,index);//查看index所对应的piece是否在本机中
	if(ret &lt; 0)  { printf(&quot;peer requested slice did not download\n&quot;); return -1; }

	if(index == last_piece_index) {//当为最后一个piece时，调用不同的函数
		read_slice_for_send_last_piece(index,begin,length,peer);
		return 0;
	}

	// 待获取得slice缓冲区中已存在
	while(p != NULL) {
		if(p-&gt;index==index &amp;&amp; p-&gt;begin==begin &amp;&amp; p-&gt;length==length &amp;&amp;
		   p-&gt;in_use==1 &amp;&amp; p-&gt;is_full==1) {
			// 构造piece消息
		        ret = create_piece_msg(index,begin,p-&gt;buff,p-&gt;length,peer);//如果该slice存在，那么构造piece消息发送出去
			if(ret &lt; 0) { printf(&quot;Function create piece msg error\n&quot;); return -1; }
			p-&gt;access_count = 1;//该piece的访问计数设置为1
			return 0;
		}
		p = p-&gt;next;
	}

	int i = 4, count, slice_count, unuse_count;//走到这一步的时候说明，在cache中，这个消息不存在，要从硬盘中读取数据
	while(i &gt; 0) {
		slice_count = piece_length / (16*1024);
		count = 0;  // 计数当前指向第几个slice
		p = btcache_head;

		while(p != NULL) {
			if(count%slice_count == 0)  { unuse_count = 0; q = p; }
			if(p-&gt;in_use == 0) unuse_count++;
			if(unuse_count == slice_count)  break;  // 找到一个空闲的piece
			
			count++;
			p = p-&gt;next;
		}//结束的话说明缓冲区中，可以找到足够的空间用来存储一个piece
		
		if(p != NULL) {
		        read_piece_from_harddisk(q,index);//将index所对应的piece读入到q所代表的btcache结点缓存当中

			p = q;
			while(p != NULL) {
				if(p-&gt;index==index &amp;&amp; p-&gt;begin==begin &amp;&amp; p-&gt;length==length &amp;&amp;
					p-&gt;in_use==1 &amp;&amp; p-&gt;is_full==1) {
					// 构造piece消息
				        ret = create_piece_msg(index,begin,p-&gt;buff,p-&gt;length,peer);//然后构造piece发送出去
					if(ret &lt; 0) { printf(&quot;Function create piece msg error\n&quot;); return -1; }
					p-&gt;access_count = 1;
					return 0;
				}
				p = p-&gt;next;
			}
		}
		
		if(i == 4) write_btcache_to_harddisk(peer);//如果节点空间不足，则选择性的释放缓冲区的内存空间
		if(i == 3) release_read_btcache_node(16);
		if(i == 2) release_read_btcache_node(8);
		if(i == 1) release_read_btcache_node(0);
		i--;
	}

	// 如果实在没有缓冲区了,就不读slice所在的piece到缓冲区中
	p = initialize_btcache_node();//这个时候重新申请一块内存空间用来存放从硬盘中读到的slice消息
	if(p == NULL)  { printf(&quot;%s:%d allocate memory error&quot;,__FILE__,__LINE__); return -1; }
	p-&gt;index  = index;
	p-&gt;begin  = begin;
	p-&gt;length = length;
	read_slice_from_harddisk(p);
	// 构造piece消息
	ret = create_piece_msg(index,begin,p-&gt;buff,p-&gt;length,peer);
	if(ret &lt; 0) { printf(&quot;Function create piece msg error\n&quot;); return -1; }
	// 释放刚刚申请的内存
	if(p-&gt;buff != NULL)  free(p-&gt;buff);//消息发送出去之后，释放之前分配的空间
	if(p != NULL) free(p);

	return 0;
}

void clear_btcache_before_peer_close(Peer *peer)
{
        Request_piece  *req = peer-&gt;Request_piece_head;//为请求消息队列的头部
	int			   i = 0, index[2] = {-1, -1};//但是这个地方为什么要设置为2呢？

	if(req == NULL)  return;
	while(req != NULL &amp;&amp; i &lt; 2) {
		if(req-&gt;index != index[i]) { index[i] = req-&gt;index; i++; }
		req = req-&gt;next;//这样index[0]存有第一个piece请求的index，而index[1]存有第二个piece请求的index
	}

	Btcache *p = btcache_head;
	while( p != NULL ) {
		if( p-&gt;index != -1 &amp;&amp; (p-&gt;index==index[0] || p-&gt;index==index[1]) ) {
			p-&gt;index  = -1;
			p-&gt;begin  = -1;//在btcache链表中，只要遇到index[0]和index[1]所标注的index，就将其销毁掉，其实标注其无效就可以了
			p-&gt;length = -1;
			
			p-&gt;in_use       =  0;
			p-&gt;read_write   = -1;
			p-&gt;is_full      =  0;
			p-&gt;is_writed    =  0;
			p-&gt;access_count =  0;
		}
		p = p-&gt;next;
	}
}


// 针对下载最后一个piece的问题,修改以下几处：
// 在data.c头部增加了几个全局变量
// 在data.c中修改了初始分配动态内存函数和最终释放动态内存的函数
// 在rate.c中修改了create_req_slice_msg函数
// 在data.c中增加了以下4个函数

/*
 其实这四个函数很好理解：
 1、将last_piece写入硬盘
 2、将硬盘中的last_piece读入缓存区
 3、将slice写入缓存
 4、将slice从缓存中读出*/

int write_last_piece_to_btcache(Peer *peer)//这个的名字好像不争确，应该叫做write_last_piece_to_harddisk
{
        int            index = last_piece_index, i;//最后一个piece的index值
	unsigned char  piece_hash1[20], piece_hash2[20];
	Btcache        *p = last_piece;//最后一个piece的头链表指针，last_piece指向最后一个piece的第一个slice位置

	// 校验piece的HASH值
	SHA1_CTX ctx;
	SHA1Init(&amp;ctx);
	while(p != NULL) {
		SHA1Update(&amp;ctx,p-&gt;buff,p-&gt;length);
		p = p-&gt;next;
	}
	SHA1Final(piece_hash1,&amp;ctx);
	
	for(i = 0; i &lt; 20; i++)  piece_hash2[i] = pieces[index*20+i];//metepher_parse文件中，得到到hash值

	if(memcmp(piece_hash1,piece_hash2,20) == 0) {
		printf(&quot;@@@@@@  last piece downlaod OK @@@@@@\n&quot;);
	} else {
		printf(&quot;@@@@@@  last piece downlaod NOT OK @@@@@@\n&quot;);
		return -1;
	}

	p = last_piece;
	while( p != NULL) {
         	write_btcache_node_to_harddisk(p);//将最后一个piece的各个slice写入到硬盘中
		p = p-&gt;next;
	}
	printf(&quot;@@@@@@  last piece write to harddisk OK @@@@@@\n&quot;);

	// 在peer中的请求队列中删除piece请求

	// 更新位图
	set_bit_value(bitmap,index,1);
	
	// 准备发送have消息
	for(i = 0; i &lt; 64; i++) {
		if(have_piece_index[i] == -1) { 
		        have_piece_index[i] = index; //已经存在的piece的index，用于发送have消息
			break; 
		}
	}

	download_piece_num++;
	if(download_piece_num % 10 == 0)  restore_bitmap();

	return 0;
}

int write_slice_to_last_piece(int index,int begin,int length,
							  unsigned char *buff,int len,Peer *peer)
{
	if(index != last_piece_index || begin &gt; (last_piece_count-1)*16*1024)
		return -1;
	if(buff==NULL || peer==NULL)  return -1;

	// 定位到要写入哪个slice
	int count = begin / (16*1024);
	Btcache *p = last_piece;//count为slice相对与piece起点的偏移
	while(p != NULL &amp;&amp; count &gt; 0) {
		count--;
		p = p-&gt;next;
	}
        //定位到由，index,begin,length所确定的slice
	if(p-&gt;begin==begin &amp;&amp; p-&gt;in_use==1 &amp;&amp; p-&gt;is_full==1)
		return 0; // 该slice已存在
	
	p-&gt;index  = index;//走到这里说明，该slice不存在，不存在的话就要重新定义
	p-&gt;begin  = begin;
	p-&gt;length = length;

	p-&gt;in_use       = 1;
	p-&gt;read_write   = 1;
	p-&gt;is_full      = 1;
	p-&gt;is_writed    = 0;
	p-&gt;access_count = 0;
	
	memcpy(p-&gt;buff,buff,len);//这里的buff指的是存放slice的空间，因为不存在这个slice，所以将buff中的slice写入即可

	p = last_piece;
	while(p != NULL) {
		if(p-&gt;is_full != 1)  break;
		p = p-&gt;next;
	}
	if(p == NULL) {//感觉这个好像没有什么用处，再说这个也不是写入btcache而是写入harddisk
		write_last_piece_to_btcache(peer);
	}

	return 0;
}

int read_last_piece_from_harddisk(Btcache *p, int index)
{
	Btcache  *node_ptr   = p;
	int      begin       = 0;
	int      length      = 16*1024;
	int      slice_count = last_piece_count; 
	int      ret;
	
	if(p==NULL || index != last_piece_index)  return -1;
	
	while(slice_count &gt; 0) {
		node_ptr-&gt;index  = index;
		node_ptr-&gt;begin  = begin;
		node_ptr-&gt;length = length;
		if(begin == (last_piece_count-1)*16*1024) 
		  node_ptr-&gt;length = last_slice_len;//单位确实为字节
		
		ret = read_slice_from_harddisk(node_ptr);//将硬盘中的slice读入到node_ptr,所代表的缓存中
		if(ret &lt; 0) return -1;
		
		node_ptr-&gt;in_use       = 1;//对缓存中的节点进行重新设置
		node_ptr-&gt;read_write   = 0;
		node_ptr-&gt;is_full      = 1;
		node_ptr-&gt;is_writed    = 0;
		node_ptr-&gt;access_count = 0;
		
		begin += 16*1024;//从这里也可以看出来begin的单位为字节
		slice_count--;
		node_ptr = node_ptr-&gt;next;
	}
	
	return 0;
}

int read_slice_for_send_last_piece(int index,int begin,int length,Peer *peer)
{
	Btcache  *p;
	int       ret, count = begin / (16*1024);
	
	// 检查参数是否有误
	if(index != last_piece_index || begin &gt; (last_piece_count-1)*16*1024)
		return -1;
	
	ret = get_bit_value(bitmap,index);//查看我们的位图中是否有这个piece
	if(ret &lt; 0)  {printf(&quot;peer requested slice did not download\n&quot;); return -1;}

	p = last_piece;
	while(count &gt; 0) {
		p = p-&gt;next;
		count --;
	}
	if(p-&gt;is_full != 1) {//说明此时的piece还在硬盘中，没有读出
		ret = read_last_piece_from_harddisk(last_piece,index);
		if(ret &lt; 0)  return -1;
	}
	
	if(p-&gt;in_use == 1 &amp;&amp; p-&gt;is_full == 1) {
		ret = create_piece_msg(index,begin,p-&gt;buff,p-&gt;length,peer);
	}

	if(ret == 0)  return 0;
	else return -1;
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971483
</pre>
