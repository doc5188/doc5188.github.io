---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--策略管理模块（policy.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:36
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
#include &quot;parse_metafile.h&quot;
#include &quot;peer.h&quot;
#include &quot;data.h&quot;
#include &quot;message.h&quot;
#include &quot;policy.h&quot;

Unchoke_peers  unchoke_peers; //存放非阻塞peer以及优化非阻塞peer的指针
long long      total_down = 0L, total_up = 0L; //总的上传量以及下载量
float          total_down_rate = 0.0F, total_up_rate = 0.0F;//上传速度以及下载速度
int            total_peers = 0;//已连接的总的peer数

extern int	   end_mode;
extern Bitmap  *bitmap;
extern Peer    *peer_head;
extern int     pieces_length;//每个piece_hash值的长度
extern int     piece_length;//每一个piece的长度

extern Btcache *btcache_head;
extern int     last_piece_index;
extern int     last_piece_count;
extern int     last_slice_len;
extern int     download_piece_num;

// 初始化全局变量unchoke_peers
void init_unchoke_peers()
{
	int i;

	for(i = 0; i &lt; UNCHOKE_COUNT; i++) {
		*(unchoke_peers.unchkpeer + i) = NULL;		
	}

	unchoke_peers.count = 0;
	unchoke_peers.optunchkpeer = NULL;//对非阻塞指针以及优化非阻塞指针全部赋值为空
}

// 判断一个peer是否已经存在于unchoke_peers
int is_in_unchoke_peers(Peer *node)
{
	int i;

	for(i = 0; i &lt; unchoke_peers.count; i++) {
		if( node == (unchoke_peers.unchkpeer)[i] )  return 1;
	}

	return 0;// node为peer指针，所以通过比较可以完全判断
}

// 从unchoke_peers中获取下载速度最慢的peer的索引
int get_last_index(Peer **array,int len)
{
	int i, j = -1;

	if(len &lt;= 0) return j;//这里len为非阻塞peer指针的维度
	else j = 0;

	for(i = 0; i &lt; len; i++)
		if( array[i]-&gt;down_rate &lt; array[j]-&gt;down_rate )  j = i;

	return j;
}

// 找出当前下载速度最快的4个peer,将其unchoke  //实现了阻塞算法
int select_unchoke_peer()
{
	Peer*  p;
	Peer*  now_fast[UNCHOKE_COUNT];//现在最快
	Peer*  force_choke[UNCHOKE_COUNT];//强制阻塞
	int    unchoke_socket[UNCHOKE_COUNT], choke_socket[UNCHOKE_COUNT];//阻塞套接字还有非阻塞套接字
	int    i, j, index = 0, len = UNCHOKE_COUNT;

	for(i = 0; i &lt; len; i++) {
		now_fast[i]       = NULL;
		force_choke[i]    = NULL;
		unchoke_socket[i] = -1;
		choke_socket[i]   = -1;//重新赋值
	}

	// 将那些在过去10秒已断开连接而又处于unchoke队列中的peer清除出unchoke队列
	for(i = 0, j = 0; i &lt; unchoke_peers.count; i++) { //unchoke_peers.count记录当前一共有多少个非阻塞的peer,其值并不一定为4
		p = peer_head;
		while(p != NULL) {
			if(p == unchoke_peers.unchkpeer[i])  break;
			p = p-&gt;next;
		}
		if(p == NULL)  { unchoke_peers.unchkpeer[i] = NULL; j++; }//如果p等于NULL，说明peer队列中根本就没有非阻塞peer的指针，这说明非阻塞peer指针过时了
	}
	if(j != 0) {//这个时候说明，存在过时的非阻塞peer指针
	        unchoke_peers.count = unchoke_peers.count - j;//跟新当前非阻塞peer的数目
		for(i = 0, j = 0; i &lt; len; i++) {
			if(unchoke_peers.unchkpeer[i] != NULL) {
			        force_choke[j] = unchoke_peers.unchkpeer[i];//将非阻塞的peer指针放入到另一数组中
				j++;
			}
		}
		for(i = 0; i &lt; len; i++) {
		  unchoke_peers.unchkpeer[i] = force_choke[i];//这样的目的就是使得非阻塞的peer指针在内存中保持连续性，以便后面的处理
		  force_choke[i] = NULL;//并且将强制阻塞数组清空
		}
	}

	// 将那些在过去10秒上传速度超过20KB/S而下载速度过小的peer强行阻塞
	// 注意：up_rate和down_rate的单位是B/S而不是KB/S
	for(i = 0, j = -1; i &lt; unchoke_peers.count; i++) {
		if( (unchoke_peers.unchkpeer)[i]-&gt;up_rate &gt; 50*1024 &amp;&amp;
			(unchoke_peers.unchkpeer)[i]-&gt;down_rate &lt; 0.1*1024 ) {
			j++;
			force_choke[j] = unchoke_peers.unchkpeer[i];
		}
	}

	// 从当前所有Peer中选出下载速度最快的四个peer
	p = peer_head;
	while(p != NULL) {
	          if(p-&gt;state==DATA &amp;&amp; is_interested(bitmap,&amp;(p-&gt;bitmap)) &amp;&amp; is_seed(p)!=1) {//要进行下一步，则p需要满足三种状态
			// p不应该在force_choke数组中
			for(i = 0; i &lt; len; i++) {
			  if(p == force_choke[i]) break;//如果peer本身就在强制阻塞数组中，就直接跳过
			}
			if(i == len) {
			        if( index &lt; UNCHOKE_COUNT ) {//指明非阻塞peer的数目，在这里UNCHOKE_COUNT的值为4
					now_fast[index] = p; 
					index++; 
				} else {
				        j = get_last_index(now_fast,UNCHOKE_COUNT);//如果说index的值超过或等于4，说明需要判断是否将那一个peer置换出去
					if(p-&gt;down_rate &gt;= now_fast[j]-&gt;down_rate) now_fast[j] = p;//上面的函数就是选择下载速度最小的那个
				}
			}
		}
		  p = p-&gt;next;//不满足上述的三种状态的时候就应该判断下一个peer是否满足
	}

	// 假设now_fast中所有的peer都是要unchoke的
	for(i = 0; i &lt; index; i++) {
		Peer*  q = now_fast[i];
		unchoke_socket[i] = q-&gt;socket;//通过socket与peer通信，这里是给非阻塞套接字赋值
	}

	// 假设unchoke_peers.unchkpeer中所有peer都是choke的
	for(i = 0; i &lt; unchoke_peers.count; i++) {
		Peer*  q = (unchoke_peers.unchkpeer)[i];
		choke_socket[i] = q-&gt;socket;//这里是给阻塞套接字赋值
	}

	// 如果now_fast某个元素已经存在于unchoke_peers.unchkpeer
	// 则没有必要进行choke或unckoke
	for(i = 0; i &lt; index; i++) {
		if( is_in_unchoke_peers(now_fast[i]) == 1) {
			for(j = 0; j &lt; len; j++) {
			  Peer*  q = now_fast[i];//最快的peer是4个，所以index为4，其实这几个数组的大小完全相同，都等于UNCHOKE_COUNT
				if(q-&gt;socket == unchoke_socket[i])  unchoke_socket[i] = -1;
				if(q-&gt;socket == choke_socket[i])    choke_socket[i]   = -1;
			}
		}
	}

	// 更新当前unchoke的peer，也就是重新选择unchoke peer
	for(i = 0; i &lt; index; i++) {
	  (unchoke_peers.unchkpeer)[i] = now_fast[i];//将下载最快的4个peer放入到非阻塞peer数组中
	}
	unchoke_peers.count = index;

	// 状态变化后,要对peer的状态值重新赋值,并且创建choke、unchoke消息
	p = peer_head;
	while(p != NULL) {
		for(i = 0; i &lt; len; i++) {
		        if(unchoke_socket[i]==p-&gt;socket &amp;&amp; unchoke_socket[i]!=-1) {//如果某一个套接字为非阻塞套接子，并且其值不为-1
			  p-&gt;am_choking = 0;//解除自我阻塞
				create_chock_interested_msg(1,p);//创建unchoke消息
			}
			if(choke_socket[i]==p-&gt;socket &amp;&amp; choke_socket[i]!=-1) { //这个地方好像写错了
			  p-&gt;am_choking = 1;//自我阻塞
				cancel_requested_list(p);
				create_chock_interested_msg(0,p);//创建chock消息
			}
		}
		p = p-&gt;next;
	}

	//for(i = 0; i &lt; unchoke_peers.count; i++)
	//	printf(&quot;unchoke peer:%s \n&quot;,(unchoke_peers.unchkpeer)[i]-&gt;ip);

	return 0;
}

// 假设要下载的文件共有100个piece
// 以下函数的功能是将0到99这100个数的顺序以随机的方式打乱
// 从而得到一个随机的数组,该数组以随机的方式存储0～99,供片断选择算法使用

int *rand_num = NULL;//也是定义的全局变量
int get_rand_numbers(int length)
{
	int i, index, piece_count, *temp_num;
	
	if(length == 0)  return -1;
	piece_count = length;//说明有多少个piece
	
	rand_num = (int *)malloc(piece_count * sizeof(int));
	if(rand_num == NULL)    return -1;
	
	temp_num = (int *)malloc(piece_count * sizeof(int));//用于临时存放
	if(temp_num == NULL)    return -1;
	for(i = 0; i &lt; piece_count; i++)  temp_num[i] = i;
	
	srand(time(NULL));//随机函数发生器的初始化函数，如果种子相同，那么后面rand（）的值也是相同的
	for(i = 0; i &lt; piece_count; i++) {
	  index = (int)( (float)(piece_count-i) * rand() / (RAND_MAX+1.0) );//index的值不同，这样就做到了打乱了赋值
	  rand_num[i] = temp_num[index];          //RAND_MAX在哪里定义的？
        temp_num[index] = temp_num[piece_count-1-i];
    }
	
	if(temp_num != NULL)  free(temp_num);
	return 0;
}

// 从peer队列中选择一个优化非阻塞peer
int select_optunchoke_peer()
{
	int   count = 0, index, i = 0, j, ret;
	Peer  *p = peer_head; 

	// 获取peer队列中peer的总数
	while(p != NULL) {
		count++;
		p =  p-&gt;next;
	}

	// 如果peer总数太少(小于等于4),则没有必要选择优化非阻塞peer
	if(count &lt;= UNCHOKE_COUNT)  return 0;

	ret = get_rand_numbers(count);
	if(ret &lt; 0) {
		printf(&quot;%s:%d get rand numbers error\n&quot;,__FILE__,__LINE__);
		return -1;
	}
	while(i &lt; count) {
		// 随机选择一个数,该数在0～count-1之间
	        index = rand_num[i];//在之前就有定义，get_rand_numbers函数之前

		p = peer_head;
		j = 0;
		while(j &lt; index &amp;&amp; p != NULL) {
			p = p-&gt;next;
			j++;
		}//找到对应的peer
                

                /*如果该peer要想成为优化非阻塞peer，则必须满足5个条件：
                  1、首先他不是当前4个非阻塞peer中的一个
                  2、p不是种子
                  3、p的状态处于数据交换状态
                  4、p并不是当前的优化非阻塞peer，从上面可以看出，优化非阻塞peer都是随机选择的
                  5、这个peer含有客户端没有的piece*/

		if( is_in_unchoke_peers(p) != 1 &amp;&amp; is_seed(p) != 1 &amp;&amp; p-&gt;state == DATA &amp;&amp;
		    p != unchoke_peers.optunchkpeer &amp;&amp; is_interested(bitmap,&amp;(p-&gt;bitmap)) ) {
		
		        if( (unchoke_peers.optunchkpeer) != NULL ) {//说明之前存在优化非阻塞peer，这次不过是另外选择一个罢了
				Peer  *temp = peer_head;
				while( temp != NULL ) {
					if(temp == unchoke_peers.optunchkpeer) break;
					temp = temp-&gt;next;//在peer队列中找到当前的优化非阻塞peer
				}
				if(temp != NULL) {
				  (unchoke_peers.optunchkpeer)-&gt;am_choking = 1;//找到后将其阻塞，并同时发送阻塞消息
					create_chock_interested_msg(0,unchoke_peers.optunchkpeer);
				}
			}

			p-&gt;am_choking = 0;//找到优化的非阻塞peer，并解除阻塞
			create_chock_interested_msg(1,p);//发布非阻塞消息
			unchoke_peers.optunchkpeer = p;//更新优化非阻塞peer
			//printf(&quot;*** optunchoke:%s ***\n&quot;,p-&gt;ip);
			break;
		}

		i++;
	}

	if(rand_num != NULL) { free(rand_num); rand_num = NULL; }//这个时候释放rand_num内存
	return 0;
}

// 计算最近一段时间(如10秒)每个peer的上传下载速度
int compute_rate()
{
	Peer    *p       = peer_head;
	time_t  time_now = time(NULL);//记录当前的日历时间
	long    t        = 0;

	while(p != NULL) {
		if(p-&gt;last_down_timestamp == 0) {
			p-&gt;down_rate  = 0.0f;
			p-&gt;down_count = 0;
		} else {
		        t = time_now - p-&gt;last_down_timestamp;//最近一次下载的时间
			if(t == 0)  printf(&quot;%s:%d time is 0\n&quot;,__FILE__,__LINE__);
			else  p-&gt;down_rate = p-&gt;down_count / t;//计算下载的速率
			p-&gt;down_count          = 0;
			p-&gt;last_down_timestamp = 0;
		}

		if(p-&gt;last_up_timestamp == 0) {
			p-&gt;up_rate  = 0.0f;
			p-&gt;up_count = 0;
		} else {
		        t = time_now - p-&gt;last_up_timestamp;//计算最近一次上传的时间
			if(t == 0)  printf(&quot;%s:%d time is 0\n&quot;,__FILE__,__LINE__);
			else  p-&gt;up_rate = p-&gt;up_count / t;//计算上传的速率
			p-&gt;up_count          = 0;
			p-&gt;last_up_timestamp = 0;//重新设置
		}

		p = p-&gt;next;
	}

	return 0;
}

// 计算总的下载和上传速度
int compute_total_rate()//总的上传和下载速度等于各个peer的和
{
        Peer *p = peer_head;//指向与之通信的peer列表

	total_peers     = 0;
	total_down      = 0;
	total_up        = 0;  
	total_down_rate = 0.0f;
	total_up_rate   = 0.0f;

	while(p != NULL) {
		total_down      += p-&gt;down_total;
		total_up        += p-&gt;up_total;
		total_down_rate += p-&gt;down_rate;
		total_up_rate   += p-&gt;up_rate;

		total_peers++;
		p = p-&gt;next;
	}

	return 0;
}

/*何为种子？
  种子就是不缺少任何一个piece,其位图信息必须全部为1*/

int is_seed(Peer *node)
{
	int            i;
	//其实下面的这两条语句，就是为了描述完整位图的信息，因为根据piece的数目很自然的可以构造出完整的位图
	unsigned char  c = (unsigned char)0xFF, last_byte;
	unsigned char  cnst[8] = { 255, 254, 252, 248, 240, 224, 192, 128 };//分别为128，128+64，128+64+32，128+64+32+1……
	
	if(node-&gt;bitmap.bitfield == NULL)  return 0;
	
	for(i = 0; i &lt; node-&gt;bitmap.bitfield_length-1; i++) {//位图的长度，根据piece的数目肯定可以得到完整位图的信息
	  if( (node-&gt;bitmap.bitfield)[i] != c ) return 0;//这样的目的就是为了找到最后一个字节
	}
		
	// 获取位图的最后一个字节
	last_byte = node-&gt;bitmap.bitfield[i];
	// 获取最后一个字节的无效位数
	i = 8 * node-&gt;bitmap.bitfield_length - node-&gt;bitmap.valid_length; //valid_length表示的是piece的数目
	// 判断最后一个是否位种子的最后一个字节
	if(last_byte &gt;= cnst[i]) return 1;
	else return 0;
}

// 生成request请求消息,实现了片断选择算法,17为一个request消息的固定长度，peer* node本身发送请求消息，而不是主机发送，里面牵扯到主机的内容是怎么回事呢？
int create_req_slice_msg(Peer *node)
{
	int index, begin, length = 16*1024;
	int i, count = 0;

	if(node == NULL)  return -1;
	// 如果被peer阻塞或对peer不感兴趣,就没有必要生成request消息
	if(node-&gt;peer_choking==1 || node-&gt;am_interested==0 )  return -1; //相当于peer向主机请求某一个slice

	// 如果之前向该peer发送过请求,则根据之前的请求构造新请求
	// 遵守一条原则：同一个piece的所有slice应该从同一个peer处下载 //是不是片断选择的策略1？
	Request_piece *p = node-&gt;Request_piece_head, *q = NULL;
	if(p != NULL) {
		while(p-&gt;next != NULL)  { p = p-&gt;next; } // 定位到最后一个结点处，这最后一个节点也是为某一个piece的请求消息

		/*确定last slice的位置，为后面生成slice消息做准备。 一个piece的最后一个slice的起始下标*/
		int last_begin = piece_length - 16*1024;
		// 如果是最后一个piece
		if(p-&gt;index == last_piece_index) { //如果说这个piece为最后一个piece，那么其最后一个slice的坐标也会发生变化
			last_begin = (last_piece_count - 1) * 16 * 1024;
		}
		

                /*
                  从下面的函数可以看出，在Request_piece_head所代表的列表中，如果最后一个piece中的slice请求还有未发送，那么就就构建
                  slice请求将最后一个piece中的一个slice发送出去*/
		// 当前piece还有未请求的slice,则构造请求消息
		if(p-&gt;begin &lt; last_begin) {
			index = p-&gt;index;
			begin = p-&gt;begin + 16*1024;
			count = 0; //这句话的意思是，每次调用这个函数也就只能发送一个slice,如果想多次发送，则需要多次调用

			while(begin!=piece_length &amp;&amp; count&lt;1) {//这里是请求slice的信息，所以begin的值不能等于piece_length
				// 如果是最后一个piece的最后一个slice
				if(p-&gt;index == last_piece_index) {
					if( begin == (last_piece_count - 1) * 16 * 1024 )
					      length = last_slice_len;//如果为最后一个piece的最后一个slice，那么length的长度可能达不到一个slice也就是16k
				}                                     //因为在本函数的开始处，就默认的定义length为16k，所以这种情况是一个特例

				create_request_msg(index,begin,length,node);//创建request消息，注意了这是node创建的消息
				
				q = (Request_piece *)malloc(sizeof(Request_piece));//将当前的请求记录到请求队列
				if(q == NULL) { 
					printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__);
					return -1;
				}
				q-&gt;index  = index;
				q-&gt;begin  = begin;
				q-&gt;length = length;
				q-&gt;next   = NULL;
				p-&gt;next   = q;
				p         = q;

				begin += 16*1024;//用于while循环，但是这句话好像没有任何作用，因为是count控制着循环
				count++;
			}//while循环结束
			
			return 0;  // 构造完毕,就返回
		}//while之前的if语句结束
	}//再之前的if语句结束



	//片断选择策略的2和3
       /*然后去btcache_head中寻找这样的piece:它没有下载完,但它不在任何peer的
	 request消息队列中,应该优先下载这样的piece,出现这样的piece的原因是:
	 从一个peer处下载一个piece,还没下载完,那个peer就将我们choke了或下线了

	 但是测试结果表明, 以这种方式这种方式创建rquest请求执行效率并不高
	 如果直接丢弃未下载完成的piece,则没有必要进行这种生成请求的方式
	 int ret = create_req_slice_msg_from_btcache(node);
	 if(ret == 0) return 0;*/

	// 生成随机数  
	if(get_rand_numbers(pieces_length/20) == -1) { //说明slice请求消息并没有构造完毕
		printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__);
		return -1;
	}
	// 随机选择一个piece的下标,该下标所代表的piece应该没有向任何peer请求过
	for(i = 0; i &lt; pieces_length/20; i++) {
		index = rand_num[i];

		// 判断对于以index为下标的piece,peer是否拥有
		if( get_bit_value(&amp;(node-&gt;bitmap),index) == 1)  continue;//要想执行下去，那么其值应该为1，也就是拥有,但是如果其拥有了又何必发request请求？我觉得有错误！！
		// 判断对于以index为下标的piece,是否已经下载
		if( get_bit_value(bitmap,index) == 1) continue;//但是主机没有

		// 判断对于以index为下标的piece,是否已经请求过了
		Peer          *peer_ptr = peer_head;
		Request_piece *reqt_ptr;
		int           find = 0;
		while(peer_ptr != NULL) {
		        reqt_ptr = peer_ptr-&gt;Request_piece_head;//前面提到过，它不再任何peer的请求队列中
			while(reqt_ptr != NULL) {
				if(reqt_ptr-&gt;index == index)  { find = 1; break; }
				reqt_ptr = reqt_ptr-&gt;next;
			}
			if(find == 1) break;

			peer_ptr = peer_ptr-&gt;next;
		}
		if(find == 1) continue;//说明能够在peer的请求队列中找到这样的piece,这样就不是我们想要下载的piece 

		break; // 程序若执行到此处,说明已经找到一个复合要求的index
	}
	if(i == pieces_length/20) {//这个时候说明没有找到符合条件的index
		if(end_mode == 0)  end_mode = 1;
		for(i = 0; i &lt; pieces_length/20; i++) {
		     if( get_bit_value(bitmap,i) == 0 )  { index = i; break; }//在没有找到理想的index的情况下，查找现在还有那一个piece还没有下载
		}
		
		if(i == pieces_length/20) { //如果是这种情况，说明所有的piece已经下载，没有需要下载的piece,也就没有必要发送slice消息
			printf(&quot;Can not find an index to IP:%s\n&quot;,node-&gt;ip);
			return -1;
		}
	}

	// 构造piece请求消息，走到这一步说明本机中还是有piece没有被下载
	begin = 0;
	count = 0;
	p = node-&gt;Request_piece_head;
	if(p != NULL)
		while(p-&gt;next != NULL)  p = p-&gt;next;
	while(count &lt; 4) {
		// 如果是构造最后一个piece的请求消息
		if(index == last_piece_index) {
			if(count+1 &gt; last_piece_count) 
				break;
			if(begin == (last_piece_count - 1) * 16 * 1024)
				length = last_slice_len;
		}

		create_request_msg(index,begin,length,node); //到最后还是node构造request请求

		q = (Request_piece *)malloc(sizeof(Request_piece));
		if(q == NULL) { printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); return -1; }
		q-&gt;index  = index;
		q-&gt;begin  = begin;
		q-&gt;length = length;
		q-&gt;next   = NULL;
		if(node-&gt;Request_piece_head == NULL)  { node-&gt;Request_piece_head = q; p = q; }
		else  { p-&gt;next = q; p = q; }
		//printf(&quot;*** create request index:%-6d begin:%-6x to IP:%s ***\n&quot;,
		//	index,q-&gt;begin,node-&gt;ip);
		begin += 16*1024;
		count++;
	}

	if(rand_num != NULL)  { free(rand_num); rand_num = NULL; }
	return 0;
}

// 以下这个函数实际并未调用,若要使用需先在头文件中声明
int create_req_slice_msg_from_btcache(Peer *node)
{
	// 指针b用于遍历btcache缓冲区
	// 指针b_piece_first指向每个piece第一个slice处
	// slice_count指明一个piece含有多少个slice
	// valid_count指明一个piece中已下载的slice数
	Btcache        *b = btcache_head, *b_piece_first;
	Peer           *p;
	Request_piece  *r;
	int            slice_count = piece_length / (16*1024);
	int            count = 0, num, valid_count;
	int            index = -1, length = 16*1024;
	
	while(b != NULL) {
		if(count%slice_count == 0) {
			num           = slice_count;
			b_piece_first = b;
			valid_count   = 0;
			index         = -1;
			
			// 遍历btcache中一个piece的所有slice
			while(num&gt;0 &amp;&amp; b!=NULL) {
				if(b-&gt;in_use==1 &amp;&amp; b-&gt;read_write==1 &amp;&amp; b-&gt;is_writed==0)
					valid_count++;
				if(index==-1 &amp;&amp; b-&gt;index!=-1) index = b-&gt;index;
				num--;
				count++;
				b = b-&gt;next;
			}
			
			// 找到一个未下载完piece
			if(valid_count&gt;0 &amp;&amp; valid_count&lt;slice_count) {
				// 检查该piece是否存在于某个peer的请求队列中
				p = peer_head;
				while(p != NULL) {
					r = p-&gt;Request_piece_head;
					while(r != NULL) {
						if(r-&gt;index==index &amp;&amp; index!=-1) break;
						r = r-&gt;next;
					}
					if(r != NULL) break;
					p = p-&gt;next;
				}
				// 如果该piece没有存在于任何peer的请求队列中,那么就找到了需要的piece
				if(p==NULL &amp;&amp; get_bit_value(&amp;(node-&gt;bitmap),index)==1) {
					int request_count = 5;
					num = 0;
					// 将r定位到peer最后一个请求消息处
					r = node-&gt;Request_piece_head;
					if(r != NULL) {
						while(r-&gt;next != NULL) r = r-&gt;next;
					}
					while(num&lt;slice_count &amp;&amp; request_count&gt;0) {
						if(b_piece_first-&gt;in_use == 0) {
							create_request_msg(index,num*length,length,node);
							
							Request_piece *q;
							q = (Request_piece *)malloc(sizeof(Request_piece));
							if(q == NULL) { 
								printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__);
								return -1;
							}
							q-&gt;index  = index;
							q-&gt;begin  = num*length;
							q-&gt;length = length;
							q-&gt;next   = NULL;
							printf(&quot;create request from btcache index:%-6d begin:%-6x\n&quot;,
								index,q-&gt;begin);
							if(r == NULL) {
								node-&gt;Request_piece_head = q;
								r = q;
							} else{
								r-&gt;next = q;
								r = q;
							}
							request_count--;
						}
						num++;
						b_piece_first = b_piece_first-&gt;next;
					}
					return 0;
				}
			}
		}
	}
	
	return -1;
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971527
</pre>
