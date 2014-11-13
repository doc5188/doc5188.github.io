---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--消息处理模块（message.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:32
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;malloc.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
#include &lt;string.h&gt;
#include &lt;sys/socket.h&gt;
#include &quot;parse_metafile.h&quot;
#include &quot;bitfield.h&quot;
#include &quot;peer.h&quot;
#include &quot;data.h&quot;
#include &quot;policy.h&quot;
#include &quot;message.h&quot;

#define HANDSHAKE   -2
#define KEEP_ALIVE  -1
#define CHOKE        0
#define UNCHOKE      1
#define INTERESTED   2
#define UNINTERESTED 3
#define HAVE         4
#define BITFIELD     5
#define REQUEST      6
#define PIECE        7
#define CANCEL       8
#define PORT         9

#define KEEP_ALIVE_TIME 45

extern Bitmap *bitmap;
extern char    info_hash[20];
extern char    peer_id[20];
extern int     have_piece_index[64];
extern Peer   *peer_head;

int int_to_char(int i, unsigned char c[4])//我们认为一个整形i如果转换为字符的话，其最低位应该放在c[0],但是从现在的角度看，放在c[3],所以说采用的是大端顺序
{
	c[3] = i%256;
	c[2] = (i-c[3])/256%256;
	c[1] = (i-c[3]-c[2]*256)/256/256%256;
	c[0] = (i-c[3]-c[2]*256-c[1]*256*256)/256/256/256%256;

	return 0;
}

int char_to_int(unsigned char c[4])
{
	int i;

	i = c[0]*256*256*256 + c[1]*256*256 + c[2]*256 + c[3];//c[0]放的是最高位
	
	return i;
}

int create_handshake_msg(char *info_hash,char *peer_id,Peer *peer)
{
	int            i;
	unsigned char  keyword[20] = &quot;BitTorrent protocol&quot;, c = 0x00;
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;  //创建握手信号，并将其放入out_msg缓冲区中，但是在此之前，缓冲区中可能已经存有数据，这样只有放在其后。
	int            len = MSG_SIZE - peer-&gt;msg_len;

	if(len &lt; 68)  return -1;  // 68为握手消息的固定长度

	buffer[0] = 19;
	for(i = 0; i &lt; 19; i++)  buffer[i+1]  = keyword[i]; 
	for(i = 0; i &lt; 8;  i++)  buffer[i+20] = c;
	for(i = 0; i &lt; 20; i++)  buffer[i+28] = info_hash[i];//为种子文件的关键字info所对应的hash值，其算法描述在hash.c中
	for(i = 0; i &lt; 20; i++)  buffer[i+48] = peer_id[i];

	peer-&gt;msg_len += 68;
	return 0;
}

int create_keep_alive_msg(Peer *peer)//保活消息
{
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;

	if(len &lt; 4)  return -1;  // 4为keep_alive消息的固定长度

	memset(buffer,0,4);
	peer-&gt;msg_len += 4;
	return 0;
}

int create_chock_interested_msg(int type,Peer *peer)
{
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;

	// 5为choke、unchoke、interested、uninterested消息的固定长度
	if(len &lt; 5)  return -1;

	memset(buffer,0,5);
	buffer[3] = 1;
	buffer[4] = type; //type取不同的四个值，便对应上面所述的四种消息，这里的数据存储的格式为大端顺序

	peer-&gt;msg_len += 5;
	return 0;
}

int create_have_msg(int index,Peer *peer)
{
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;
	unsigned char  c[4];

	if(len &lt; 9)  return -1;  // 9为have消息的固定长度
	
	memset(buffer,0,9);//这里是严格按照消息定义的格式来做的	
	buffer[3] = 5;
	buffer[4] = 4;
	
	int_to_char(index,c);
	buffer[5] = c[0];
	buffer[6] = c[1];
	buffer[7] = c[2];
	buffer[8] = c[3];
	
	peer-&gt;msg_len += 9;
	return 0;
}

int create_bitfield_msg(char *bitfield,int bitfield_len,Peer *peer)//即使这样，我们可以看出，bitfield的消息长度是不固定的，前四个字节表示长度
{
	int            i;
	unsigned char  c[4];
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;

	if( len &lt; bitfield_len+5 )  {  // bitfield消息的长度为bitfield_len+5
		printf(&quot;%s:%d buffer too small\n&quot;,__FILE__,__LINE__); 
		return -1;
	}

	int_to_char(bitfield_len+1,c);//将长度之和转换为前四个字节的前缀
	for(i = 0; i &lt; 4; i++)  buffer[i] = c[i];//前四个字节为前缀，指明了id以及负载的长度之和。
	buffer[4] = 5;               //这里解释了为何为bitfield+5
	for(i = 0; i &lt; bitfield_len; i++) buffer[i+5] = bitfield[i];

	peer-&gt;msg_len += bitfield_len+5;  
	return 0;
}

int create_request_msg(int index,int begin,int length,Peer *peer)
{
	int            i;
	unsigned char  c[4];
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;

	if(len &lt; 17)  return -1;  // 17为request消息的固定长度

	memset(buffer,0,17);//固定长度为17字节，但是去除前缀的4个字节，所以id以及负载的长度之和为13个字节。
	buffer[3] = 13;
	buffer[4] = 6;
	int_to_char(index,c); //分别为索引，偏移，以及长度
	for(i = 0; i &lt; 4; i++)  buffer[i+5]  = c[i];
	int_to_char(begin,c);
	for(i = 0; i &lt; 4; i++)  buffer[i+9]  = c[i];
	int_to_char(length,c);
	for(i = 0; i &lt; 4; i++)  buffer[i+13] = c[i];

	peer-&gt;msg_len += 17;
	return 0;
}

int create_piece_msg(int index,int begin,char *block,int b_len,Peer *peer)//block为消息的内容，b_len为消息的长度。在缓冲区传值的过程中，分别传node-&gt;buff,node-&gt;length
{
	int            i;
	unsigned char  c[4];
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;//用来查看peer是否有足够的空间来存储一个piece消息

	if( len &lt; b_len+13 ) {  // piece消息的长度为b_len+13
		printf(&quot;IP:%s len:%d\n&quot;,peer-&gt;ip,len);
		printf(&quot;%s:%d buffer too small\n&quot;,__FILE__,__LINE__); 
		return -1;
	}
	
	int_to_char(b_len+9,c); //这里的是block的长度+id+index+begin，后面三个的值为9
	for(i = 0; i &lt; 4; i++)      buffer[i]    = c[i];
	buffer[4] = 7;
	int_to_char(index,c);
	for(i = 0; i &lt; 4; i++)      buffer[i+5]  = c[i];
	int_to_char(begin,c);
	for(i = 0; i &lt; 4; i++)      buffer[i+9]  = c[i];
	for(i = 0; i &lt; b_len; i++)  buffer[i+13] = block[i];

	peer-&gt;msg_len += b_len+13;  
	return 0;
}

int create_cancel_msg(int index,int begin,int length,Peer *peer)
{
	int            i;
	unsigned char  c[4];
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;
	
	if(len &lt; 17)  return -1;  // 17为cancel消息的固定长度
	
	memset(buffer,0,17);
	buffer[3] = 13;//这就是cancel消息的消息结构，前四个字节为前缀，在这里设为13.后面的8为id
	buffer[4] = 8;
	int_to_char(index,c);
	for(i = 0; i &lt; 4; i++)  buffer[i+5]  = c[i];
	int_to_char(begin,c);
	for(i = 0; i &lt; 4; i++)  buffer[i+9]  = c[i];
	int_to_char(length,c);
	for(i = 0; i &lt; 4; i++)  buffer[i+13] = c[i];

	peer-&gt;msg_len += 17;	
	return 0;
}

int create_port_msg(int port,Peer *peer)
{
	unsigned char  c[4];
	unsigned char  *buffer = peer-&gt;out_msg + peer-&gt;msg_len;
	int            len = MSG_SIZE - peer-&gt;msg_len;

	if( len &lt; 7)  return 0;  // 7为port消息的固定长度

	memset(buffer,0,7);
	buffer[3] = 3;
	buffer[4] = 9;
	int_to_char(port,c);//port占有两个字节c[2]为高位
	buffer[5] = c[2];
	buffer[6] = c[3];

	peer-&gt;msg_len += 7;
	return 0;
}

// 以十六进制的形式打印消息的内容,用于调试
int print_msg_buffer(unsigned char *buffer, int len)
{
	int i;

	for(i = 0; i &lt; len; i++) {
		printf(&quot;%.2x &quot;,buffer[i]);
		if( (i+1) % 16 == 0 )  printf(&quot;\n&quot;); //buffer此时放置有各种各样的消息，各种消息存放在一起，要如何区分呢?
	}
	printf(&quot;\n&quot;);

	return 0;
}

// 判断缓冲区中是否存放了一条完整的消息
int is_complete_message(unsigned char *buff,unsigned int len,int *ok_len)
{
	unsigned int   i;
	char           btkeyword[20];                //位图消息以及piece消息的长度是不顾定的

	unsigned char  keep_alive[4]   = { 0x0, 0x0, 0x0, 0x0 };
	unsigned char  chocke[5]       = { 0x0, 0x0, 0x0, 0x1, 0x0};
	unsigned char  unchocke[5]     = { 0x0, 0x0, 0x0, 0x1, 0x1};
	unsigned char  interested[5]   = { 0x0, 0x0, 0x0, 0x1, 0x2};
	unsigned char  uninterested[5] = { 0x0, 0x0, 0x0, 0x1, 0x3};
	unsigned char  have[5]         = { 0x0, 0x0, 0x0, 0x5, 0x4};
	unsigned char  request[5]      = { 0x0, 0x0, 0x0, 0xd, 0x6};
	unsigned char  cancel[5]       = { 0x0, 0x0, 0x0, 0xd, 0x8};
	unsigned char  port[5]         = { 0x0, 0x0, 0x0, 0x3, 0x9};
	
	if(buff==NULL || len&lt;=0 || ok_len==NULL)  return -1;
	*ok_len = 0;
	
	btkeyword[0] = 19;
	memcpy(&amp;btkeyword[1],&quot;BitTorrent protocol&quot;,19);  // BitTorrent协议关键字

	unsigned char  c[4];
	unsigned int   length;
	
	for(i = 0; i &lt; len; ) {                    //这个函数用于比较各种各样的消息类型，i的值也随着发生变化
		// 握手、chocke、have等消息的长度是固定的
		if( i+68&lt;=len &amp;&amp; memcmp(&amp;buff[i],btkeyword,20)==0 )         i += 68;
		else if( i+4 &lt;=len &amp;&amp; memcmp(&amp;buff[i],keep_alive,4)==0 )    i += 4;
		else if( i+5 &lt;=len &amp;&amp; memcmp(&amp;buff[i],chocke,5)==0 )        i += 5;
		else if( i+5 &lt;=len &amp;&amp; memcmp(&amp;buff[i],unchocke,5)==0 )      i += 5;
		else if( i+5 &lt;=len &amp;&amp; memcmp(&amp;buff[i],interested,5)==0 )    i += 5;
		else if( i+5 &lt;=len &amp;&amp; memcmp(&amp;buff[i],uninterested,5)==0 )  i += 5;
		else if( i+9 &lt;=len &amp;&amp; memcmp(&amp;buff[i],have,5)==0 )          i += 9;
		else if( i+17&lt;=len &amp;&amp; memcmp(&amp;buff[i],request,5)==0 )       i += 17;
		else if( i+17&lt;=len &amp;&amp; memcmp(&amp;buff[i],cancel,5)==0 )        i += 17;
		else if( i+7 &lt;=len &amp;&amp; memcmp(&amp;buff[i],port,5)==0 )          i += 7;//这个函数的另一个目的就是移动i，来做终极判断
		// bitfield消息的长度是变化的
		else if( i+5 &lt;=len &amp;&amp; buff[i+4]==5 )  {
			c[0] = buff[i];   c[1] = buff[i+1];
			c[2] = buff[i+2]; c[3] = buff[i+3];
			length = char_to_int(c);	
			// 消息长度占4字节,消息本身占length个字节
			if( i+4+length &lt;= len )  i += 4+length; //这样也就算出了i需要移动的位数
			else { *ok_len = i; return -1; }
		}
		// piece消息的长度也是变化的
		else if( i+5 &lt;=len &amp;&amp; buff[i+4]==7 )  {
			c[0] = buff[i];   c[1] = buff[i+1];
			c[2] = buff[i+2]; c[3] = buff[i+3];
			length = char_to_int(c);
			// 消息长度占4字节,消息本身占length个字节
			if( i+4+length &lt;= len )  i += 4+length;
			else { *ok_len = i; return -1; }
		}
		else {
			// 处理未知类型的消息
			if(i+4 &lt;= len) {
				c[0] = buff[i];   c[1] = buff[i+1];
				c[2] = buff[i+2]; c[3] = buff[i+3];
				length = char_to_int(c);
				// 消息长度占4字节,消息本身占length个字节
				if(i+4+length &lt;= len)  { i += 4+length; continue; }
				else { *ok_len = i; return -1; }
			}
			// 如果也不是未知消息类型,则认为目前接收的数据还不是一个完整的消息
			*ok_len = i;
			return -1;
		      }
	}//此处for循环结束
	
	*ok_len = i;//用于返回完整消息的长度，当然这个消息的长度可能是包含了多条消息，
	return 1; // 可以用返回值来判断是否为完整的消息呢？现在的理解是当i==len时，则为完整的消息，返回为1.
}

int process_handshake_msg(Peer *peer,unsigned char *buff,int len)
{
	if(peer==NULL || buff==NULL)  return -1;

	if(memcmp(info_hash,buff+28,20) != 0) { //这里的情况是peer本身的info与buff中的info不同的时候的情况
		peer-&gt;state = CLOSING;
		// 丢弃发送缓冲区中的数据
		discard_send_buffer(peer);
		clear_btcache_before_peer_close(peer);
		close(peer-&gt;socket);
		return -1;
	}
	
	memcpy(peer-&gt;id,buff+48,20);//两者info相同的时候，将握手消息的peer_id进行拷贝
	(peer-&gt;id)[20] = '\0';
	
	if(peer-&gt;state == INITIAL) {//根据peer的不同的状态，来采取不同的操作，如果为初始状态，发送消息之后，则变为握手状态。
		peer-&gt;state = HANDSHAKED;
		create_handshake_msg(info_hash,peer_id,peer);//创建消息，并将消息放入out_msg所代表的缓存中
         }
 	if(peer-&gt;state == HALFSHAKED)  peer-&gt;state = HANDSHAKED;//如果本身就是半握手状态，则将状态直接变为peer的状态变为握手状态

	peer-&gt;start_timestamp = time(NULL);
	return 0;
}

int process_keep_alive_msg(Peer *peer,unsigned char *buff,int len) //其实这里的len便是消息的长度
{
	if(peer==NULL || buff==NULL)  return -1;

	peer-&gt;start_timestamp = time(NULL); //为了得到当前的日历时间
	return 0;
}

/*函数原型: time_t time(time_t *timer) 　　
函数功能: 得到机器的日历时间或者设置日历时间 　　
函数返回: 机器日历时间 　　
参数说明: timer=NULL时得到机器日历时间，timer=时间数值时，用于设置日历时间，time_t是一个long类型 */

int process_choke_msg(Peer *peer,unsigned char *buff,int len)
{
	if(peer==NULL || buff==NULL)  return -1;

	if( peer-&gt;state!=CLOSING &amp;&amp; peer-&gt;peer_choking==0 ) {//此时peer的状态处于关闭状态
         	  peer-&gt;peer_choking = 1; //这里并没有用到buff的内容，只是调用这个函数的时候将peer的相关参数进行设置。
		peer-&gt;last_down_timestamp = 0;
		peer-&gt;down_count          = 0;
		peer-&gt;down_rate           = 0;
	}

	peer-&gt;start_timestamp = time(NULL);//得到当前的日历时间
	return 0;
}

int process_unchoke_msg(Peer *peer,unsigned char *buff,int len)
{
	if(peer==NULL || buff==NULL)  return -1;

	if( peer-&gt;state!=CLOSING &amp;&amp; peer-&gt;peer_choking==1 ) {//在处理unchoke消息的时候，如果peer的状态为closed，并且peer_choking阻塞，才进行处理
		peer-&gt;peer_choking = 0;
		if(peer-&gt;am_interested == 1)  create_req_slice_msg(peer);//构造request消息，请求peer发送数据！！！
               // 构造数据请求,为了提高效率一次请求5个slice
               //int create_req_slice_msg(Peer *node);  这个函数定义于policy（策略）部分，创建请求slice消息

		else {
		        peer-&gt;am_interested = is_interested(&amp;(peer-&gt;bitmap), bitmap);//这个函数定义与bitfield位图模块
			if(peer-&gt;am_interested == 1) create_req_slice_msg(peer);
			else printf(&quot;Received unchoke but Not interested to IP:%s \n&quot;,peer-&gt;ip);
		}

		peer-&gt;last_down_timestamp = 0;
		peer-&gt;down_count          = 0;
		peer-&gt;down_rate           = 0;
	}

	peer-&gt;start_timestamp = time(NULL);//得到当前日历时间
	return 0;
}

int process_interested_msg(Peer *peer,unsigned char *buff,int len)
{
	if(peer==NULL || buff==NULL)  return -1;

	if( peer-&gt;state!=CLOSING &amp;&amp; peer-&gt;state==DATA ) { //也就是说这个时候的peer状态，为DATA状态
        	  peer-&gt;peer_interested = is_interested(bitmap, &amp;(peer-&gt;bitmap));//说的是别人对我感兴趣，也就是将peer_interested置1
		if(peer-&gt;peer_interested == 0)  return -1; 
		if(peer-&gt;am_choking == 0) create_chock_interested_msg(1,peer);//此时如果本身并没有阻塞，那么创建消息进行发送，这个函数也没有遇到过，之前
	}

	peer-&gt;start_timestamp = time(NULL);
	return 0;
}

int process_uninterested_msg(Peer *peer,unsigned char *buff,int len)
{
	if(peer==NULL || buff==NULL)  return -1;

	if( peer-&gt;state!=CLOSING &amp;&amp; peer-&gt;state==DATA ) {
		peer-&gt;peer_interested = 0;
		cancel_requested_list(peer);//别人都不感兴趣，那么取消别人的请求队列
	}

	peer-&gt;start_timestamp = time(NULL);//得到当前的日历时间
	return 0;
}

int process_have_msg(Peer *peer,unsigned char *buff,int len)
{
	int           rand_num;
	unsigned char c[4];

	if(peer==NULL || buff==NULL)  return -1;

	srand(time(NULL));
	rand_num = rand() % 3;

	if( peer-&gt;state!=CLOSING &amp;&amp; peer-&gt;state==DATA ) {
		c[0] = buff[5]; c[1] = buff[6];
		c[2] = buff[7]; c[3] = buff[8];	//因为这是处理have消息，所以这四个值代表的是piece的index	
		if(peer-&gt;bitmap.bitfield != NULL)
            		  set_bit_value(&amp;(peer-&gt;bitmap),char_to_int(c),1);//这个时候对下标所代表的piece进行重新设值

		if(peer-&gt;am_interested == 0) {
         		  peer-&gt;am_interested = is_interested(&amp;(peer-&gt;bitmap), bitmap);//这里的bitmap为在bitfield中定义的变量
			// 由原来的对peer不感兴趣变为感兴趣时,发interested消息
			if(peer-&gt;am_interested == 1) create_chock_interested_msg(2,peer);	
		} else {  // 收到三个have则发一个interested消息
			if(rand_num == 0) create_chock_interested_msg(2,peer);
		}
	}

	peer-&gt;start_timestamp = time(NULL);
	return 0;
}

int process_cancel_msg(Peer *peer,unsigned char *buff,int len)//取消对某个slice的数据请求
{
	unsigned char c[4];
	int           index, begin, length;

	if(peer==NULL || buff==NULL)  return -1;
	
	c[0] = buff[5];  c[1] = buff[6];
	c[2] = buff[7];  c[3] = buff[8];
	index = char_to_int(c); //cancel的信号格式，分别是下标，偏移，长度
	c[0] = buff[9];  c[1] = buff[10];
	c[2] = buff[11]; c[3] = buff[12];
	begin = char_to_int(c);
	c[0] = buff[13]; c[1] = buff[14];
	c[2] = buff[15]; c[3] = buff[16];
	length = char_to_int(c);
	
	Request_piece *p, *q;//为结构体，在message.h中定义，为下标，起始或者偏移，长度
	p = q = peer-&gt;Requested_piece_head;//这里是被请求的队列，如果是request_piece_head为向peer请求的队列
	while(p != NULL) { 
		if( p-&gt;index==index &amp;&amp; p-&gt;begin==begin &amp;&amp; p-&gt;length==length ) {
			if(p == peer-&gt;Requested_piece_head) 
				peer-&gt;Requested_piece_head = p-&gt;next;
			else
				q-&gt;next = p-&gt;next;
			free(p);
			break;
		}
		q = p;
		p = p-&gt;next;//只要有一个条件不满足，则将p向后移动。
	}	

	peer-&gt;start_timestamp = time(NULL);
	return 0;
}

int process_bitfield_msg(Peer *peer,unsigned char *buff,int len)
{
	unsigned char c[4];

	if(peer==NULL || buff==NULL)  return -1;
	if(peer-&gt;state==HANDSHAKED || peer-&gt;state==SENDBITFIELD) {
		c[0] = buff[0];   c[1] = buff[1];
		c[2] = buff[2];   c[3] = buff[3];			

		if( peer-&gt;bitmap.bitfield != NULL ) {//若原先收到一个位图消息，则清空原来的位图
			free(peer-&gt;bitmap.bitfield);
			peer-&gt;bitmap.bitfield = NULL;
		}
		peer-&gt;bitmap.valid_length = bitmap-&gt;valid_length;//一个为peer的位图的有效长度，另一个bitmap则为bitfield中定义的全局变量
		if(bitmap-&gt;bitfield_length != char_to_int(c)-1) {//这里减一，是因为其长度值包含了一个字节的id信息
			peer-&gt;state = CLOSING;
			// 丢弃发送缓冲区中的数据
			discard_send_buffer(peer);//如果收到一个错误的位图，则做相应的处理工作
			clear_btcache_before_peer_close(peer);
			close(peer-&gt;socket);
			return -1;
		}
		peer-&gt;bitmap.bitfield_length = char_to_int(c) - 1;
		peer-&gt;bitmap.bitfield = 
			(unsigned char *)malloc(peer-&gt;bitmap.bitfield_length);
		memcpy(peer-&gt;bitmap.bitfield,&amp;buff[5],peer-&gt;bitmap.bitfield_length);//将buffer中的位图信息拷贝到peer的位图当中
	
		// 如果原状态为已握手,收到位图后应该向peer发位图
		if(peer-&gt;state == HANDSHAKED) {
			create_bitfield_msg(bitmap-&gt;bitfield,bitmap-&gt;bitfield_length,peer);
			peer-&gt;state = DATA;
		}
		// 如果原状态为已发送位图，收到位图后可以准备交换数据
		if(peer-&gt;state == SENDBITFIELD) {
			peer-&gt;state = DATA;
		}

		// 判断peer是否对我们感兴趣
		peer-&gt;peer_interested = is_interested(bitmap,&amp;(peer-&gt;bitmap));//这里的bitmap代表我们，说的是我们是否对peer的bitmap感兴趣
		// 判断对peer是否感兴趣,若是则发送interested消息
		peer-&gt;am_interested = is_interested(&amp;(peer-&gt;bitmap), bitmap);//说的是peer是否对我们的bitmap感兴趣。
		if(peer-&gt;am_interested == 1) create_chock_interested_msg(2,peer);//如果对我们的bitmap感兴趣，则发送感兴趣的消息
	}
	
	peer-&gt;start_timestamp = time(NULL);//记录最近的日历时间
	return 0;
}

int process_request_msg(Peer *peer,unsigned char *buff,int len)
{
	unsigned char  c[4];
	int            index, begin, length;
	Request_piece  *request_piece, *p;
	
	if(peer==NULL || buff==NULL)  return -1;

	if(peer-&gt;am_choking==0 &amp;&amp; peer-&gt;peer_interested==1) {//这些都是对peer来说的，am_choking表明客户端可以从中下载数据，并且客户端对其感兴趣
		c[0] = buff[5];  c[1] = buff[6];
		c[2] = buff[7];  c[3] = buff[8];
		index = char_to_int(c);
		c[0] = buff[9];  c[1] = buff[10];
		c[2] = buff[11]; c[3] = buff[12];
		begin = char_to_int(c);
		c[0] = buff[13]; c[1] = buff[14];
		c[2] = buff[15]; c[3] = buff[16];
		length = char_to_int(c);

		// 错误的slice请求
		if( begin%(16*1024) != 0 ) {//因为每个slice的大小为16k，所以说begin的值一定为16k的倍数
			return 0;
		}
		
		// 查看该请求是否已存在,若已存在,则不进行处理
		p = peer-&gt;Requested_piece_head;
		while(p != NULL) {
			if(p-&gt;index==index &amp;&amp; p-&gt;begin==begin &amp;&amp; p-&gt;length==length) {
				break;
			}
			p = p-&gt;next;
		}
		if(p != NULL)  return 0;

		// 将请求加入到请求队列中
		request_piece = (Request_piece *)malloc(sizeof(Request_piece));
		if(request_piece == NULL)  { 
		  printf(&quot;%s:%d error&quot;,__FILE__,__LINE__); //对于分配的内存一定要判断是否分配成功
			return 0; 
		}
		request_piece-&gt;index  = index;
		request_piece-&gt;begin  = begin;
		request_piece-&gt;length = length;
		request_piece-&gt;next   = NULL;
		if( peer-&gt;Requested_piece_head == NULL ) //将生成的Request_piece*指针，加入到链表当中。
			peer-&gt;Requested_piece_head = request_piece;
		else {
			p = peer-&gt;Requested_piece_head;
			while(p-&gt;next != NULL)  p = p-&gt;next;
			p-&gt;next = request_piece;
		}
		//printf(&quot;*** add a request FROM IP:%s index:%-6d begin:%-6x ***\n&quot;,
		//       peer-&gt;ip,index,begin);
	}

	peer-&gt;start_timestamp = time(NULL);
	return 0;
}

int process_piece_msg(Peer *peer,unsigned char *buff,int len)//如果客户端收到peer的Request消息，并且没有将该peer阻塞，则将其请求的数据通过piece消息发送过去
{
	unsigned char  c[4];
	int            index, begin, length;
	Request_piece  *p;

	if(peer==NULL || buff==NULL)  return -1;
	
	if(peer-&gt;peer_choking==0) {
		c[0] = buff[0];    c[1] = buff[1];
		c[2] = buff[2];    c[3] = buff[3];
		length = char_to_int(c) - 9; //求出请求的block的长度，一般情况下，为16k
		c[0] = buff[5];    c[1] = buff[6];
		c[2] = buff[7];    c[3] = buff[8];
		index = char_to_int(c);//确定出为某个piece
		c[0] = buff[9];    c[1] = buff[10];
		c[2] = buff[11];   c[3] = buff[12];
		begin = char_to_int(c);//确定其偏移量

		p = peer-&gt;Request_piece_head;
		while(p != NULL) {
			if(p-&gt;index==index &amp;&amp; p-&gt;begin==begin &amp;&amp; p-&gt;length==length)
				break;
			p = p-&gt;next;
		}
		if(p == NULL) {printf(&quot;did not found matched request\n&quot;); return -1;}//根据收到的Request消息，来发送piece消息，如果请求队列中根本就没有
                                                                                     //则没有办法处理
		if(peer-&gt;last_down_timestamp == 0)
		     peer-&gt;last_down_timestamp = time(NULL);//最近一次下载的时间
		peer-&gt;down_count += length;
		peer-&gt;down_total += length;

		write_slice_to_btcache(index,begin,length,buff+13,length,peer);//这些process函数，全部为收到某个消息的反映，发送消息便是将消息写入缓存区

		create_req_slice_msg(peer);
	}

	peer-&gt;start_timestamp = time(NULL);
	return 0;
}

int parse_response(Peer *peer)//消息解析协议，对收到的消息进行确认和处理
{
	unsigned char  btkeyword[20];
	unsigned char  keep_alive[4] = { 0x0, 0x0, 0x0, 0x0 };
	int            index;
	unsigned char  *buff = peer-&gt;in_buff;//in_buff存放的都是从peer处获得的消息
	int            len = peer-&gt;buff_len;

	if(buff==NULL || peer==NULL)  return -1;

	btkeyword[0] = 19;
	memcpy(&amp;btkeyword[1],&quot;BitTorrent protocol&quot;,19);  // BitTorrent协议关键字

	// 分别处理12种消息
	for(index = 0; index &lt; len; ) {	

	  if( (len-index &gt;= 68) &amp;&amp; (memcmp(&amp;buff[index],btkeyword,20) == 0) ) {//用于判断多种消息类型，以便处理
			process_handshake_msg(peer,buff+index,68);
			index += 68;
		} 
		else if( (len-index &gt;= 4) &amp;&amp; (memcmp(&amp;buff[index],keep_alive,4) == 0)){
        		process_keep_alive_msg(peer,buff+index,4); //判断是否为保活消息
			index += 4; 
		}
		else if( (len-index &gt;= 5) &amp;&amp; (buff[index+4] == CHOKE) ) {
		  process_choke_msg(peer,buff+index,5);    //判断是否为阻塞消息
			index += 5;
		}
		else if( (len-index &gt;= 5) &amp;&amp; (buff[index+4] == UNCHOKE) ) {
		  process_unchoke_msg(peer,buff+index,5);  //判断是否为接触阻塞消息
			index += 5;
		}
		else if( (len-index &gt;= 5) &amp;&amp; (buff[index+4] == INTERESTED) ) {
		  process_interested_msg(peer,buff+index,5);//判断是否为感兴趣消息
			index += 5;
		}
		else if( (len-index &gt;= 5) &amp;&amp; (buff[index+4] == UNINTERESTED) ) {
		  process_uninterested_msg(peer,buff+index,5);//判断是否为不感兴趣消息
			index += 5;
		}
		else if( (len-index &gt;= 9) &amp;&amp; (buff[index+4] == HAVE) ) {
		  process_have_msg(peer,buff+index,9);      //判断是否为have消息
			index += 9;
		}
		else if( (len-index &gt;= 5) &amp;&amp; (buff[index+4] == BITFIELD) ) {
		  process_bitfield_msg(peer,buff+index,peer-&gt;bitmap.bitfield_length+5);//判断是否为位图消息
		  index += peer-&gt;bitmap.bitfield_length + 5;//这里之所以不用采用piece消息的处理方式，则bitmap的长度可以从bitfield_length获得
		}
		else if( (len-index &gt;= 17) &amp;&amp; (buff[index+4] == REQUEST) ) {
		  process_request_msg(peer,buff+index,17); //判断是否为请求消息
			index += 17;
		}
		else if( (len-index &gt;= 13) &amp;&amp; (buff[index+4] == PIECE) ) {
         		  unsigned char  c[4];             //判断是否为piece消息
			int            length;
			
			c[0] = buff[index];    c[1] = buff[index+1];
			c[2] = buff[index+2];  c[3] = buff[index+3];
			length = char_to_int(c) - 9;
			
			process_piece_msg(peer,buff+index,length+13);
			index += length + 13; // length+13为piece消息的长度，这也全部算在buff的缓冲区内
		}
		else if( (len-index &gt;= 17) &amp;&amp; (buff[index+4] == CANCEL) ) {
			process_cancel_msg(peer,buff+index,17);
			index += 17;
		}
		else if( (len-index &gt;= 7) &amp;&amp; (buff[index+4] == PORT) ) {
		  index += 7;         //处理的是PORT消息
		}
		else {
			// 如果是未知的消息类型,则跳过不予处理
			unsigned char c[4];
			int           length;
			if(index+4 &lt;= len) {
				c[0] = buff[index];   c[1] = buff[index+1];
				c[2] = buff[index+2]; c[3] = buff[index+3];
				length = char_to_int(c);
				if(index+4+length &lt;= len)  { index += 4+length; continue; }//未知消息类型
			}
			// 如果是一条错误的消息,清空接收缓冲区，如果连未知的类型都算不上，那么就是一条错误的消息
			peer-&gt;buff_len = 0;
			return -1;
		}
	} // end for

	// 接收缓冲区中的消息处理完毕后,清空接收缓冲区
	peer-&gt;buff_len = 0;

	return 0;
}

int parse_response_uncomplete_msg(Peer *p,int ok_len)
{
	char *tmp_buff;
	int   tmp_buff_len;

	// 分配存储空间,并保存接收缓冲区中不完整的消息
	tmp_buff_len = p-&gt;buff_len - ok_len;
	if(tmp_buff_len &lt;= 0)  return -1;
	tmp_buff = (char *)malloc(tmp_buff_len);
	if(tmp_buff == NULL) {
	  printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__);//还是用来检查内存是否分配成功。
		return -1;
	}
	memcpy(tmp_buff,p-&gt;in_buff+ok_len,tmp_buff_len);
	
	// 处理接收缓冲区中前面完整的消息
	p-&gt;buff_len = ok_len;
	parse_response(p); //这个时候已经将完整的消息处理完毕了

	// 将不完整的消息拷贝到接收缓冲区的开始处
	memcpy(p-&gt;in_buff,tmp_buff,tmp_buff_len);
	p-&gt;buff_len = tmp_buff_len;
	if(tmp_buff != NULL)  free(tmp_buff);

	return 0;
}

// 当下载完一个piece时,应该向所有的peer发送have消息
int prepare_send_have_msg()
{
	Peer *p = peer_head;
	int  i;

	if(peer_head == NULL)  return -1;
	if(have_piece_index[0] == -1)  return -1;//关于have_piece_index的数组，之前没有遇到过，并且这里为何要去64呢？！

	while(p != NULL) {
		for(i = 0; i &lt; 64; i++) {
			if(have_piece_index[i] != -1) {
				create_have_msg(have_piece_index[i],p);
			}
			else {
				break;
			}
		}//for循环结束
		p = p-&gt;next;
	}//while循环结束

	for(i = 0; i &lt; 64; i++) {
	  if(have_piece_index[i] == -1) {//将have_piece_index的元素全部置为-1
			break;
		}
		else {
			have_piece_index[i] = -1;
		}
	}
	
	return 0;
}

// 主动创建发送给peer的消息,而不是等收到某个消息再作出响应
int create_response_message(Peer *peer)
{
	if(peer==NULL)  return -1;

	if(peer-&gt;state == INITIAL) {
	  create_handshake_msg(info_hash,peer_id,peer);//如果peer处于INITAL状态则发送握手消息
		peer-&gt;state = HALFSHAKED;
		return 0;
	}

	if(peer-&gt;state == HANDSHAKED) {
		if(bitmap == NULL)  return -1;
		create_bitfield_msg(bitmap-&gt;bitfield,bitmap-&gt;bitfield_length,peer);
		peer-&gt;state = SENDBITFIELD;  //如果处于握手状态，则发送位图消息
		return 0;
	}

	// 发送piece消息,即发送下载文件的内容
	if( peer-&gt;am_choking==0 &amp;&amp; peer-&gt;Requested_piece_head!=NULL ) {
        	Request_piece *req_p = peer-&gt;Requested_piece_head; //如果被请求的队列不为空，也就是有peer想从这里下载数据

                /*如果请求队列中的数据，在btcache中找不到，那么就从硬盘上下载，如果在最开始的时候的bitfield都没有，说明根本没有这个数据*/
		int ret = read_slice_for_send(req_p-&gt;index,req_p-&gt;begin,req_p-&gt;length,peer);//在data.c文件中，但是肯定是将请求的数据以piece消息发送出去
		if(ret &lt; 0 ) { printf(&quot;read_slice_for_send ERROR\n&quot;);}
		else {
			if(peer-&gt;last_up_timestamp == 0) 
				peer-&gt;last_up_timestamp = time(NULL);
			peer-&gt;up_count += req_p-&gt;length;
			peer-&gt;up_total += req_p-&gt;length;
			peer-&gt;Requested_piece_head = req_p-&gt;next;

			//printf(&quot;********* sending a slice TO:%s index:%-5d begin:%-5x *********\n&quot;,
			//peer-&gt;ip,req_p-&gt;index,req_p-&gt;begin);

			free(req_p);
			return 0;
		}
	}

	// 如果3分钟没有收到任何消息关闭连接
	time_t now = time(NULL);  // 获取当前时间
	long interval1 = now - peer-&gt;start_timestamp; //为最近一次接受到peer消息的时间，如果很长的时间没有收到peer的任何消息，那么认为链接中断
	if( interval1 &gt; 180 ) {
		peer-&gt;state = CLOSING;
		discard_send_buffer(peer);  // 丢弃发送缓冲区中的数据
		clear_btcache_before_peer_close(peer);
		close(peer-&gt;socket);
	}
	// 如果45秒没有发送和接收消息,则发送一个keep_alive消息
	long interval2 = now - peer-&gt;recet_timestamp; //最近一次给peer发送消息的时间。
	if( interval1&gt;45 &amp;&amp; interval2&gt;45 &amp;&amp; peer-&gt;msg_len==0)
		create_keep_alive_msg(peer);

	return 0;
}

void discard_send_buffer(Peer *peer)//从字面意思理解为将发送缓存丢弃
{
	struct linger  lin;
	int            lin_len;
	
	lin.l_onoff  = 1;
	lin.l_linger = 0;
	lin_len      = sizeof(lin);
	
	if(peer-&gt;socket &gt; 0) {
		setsockopt(peer-&gt;socket,SOL_SOCKET,SO_LINGER,(char *)&amp;lin,lin_len);
	}
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971503
</pre>
