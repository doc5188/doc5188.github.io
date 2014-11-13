---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--peer模块（peer.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:34
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;malloc.h&gt;
#include &quot;peer.h&quot;
#include &quot;message.h&quot;
#include &quot;bitfield.h&quot;

extern Bitmap *bitmap;

// 指向当前与之进行通信的peer列表
Peer *peer_head = NULL;

int  initialize_peer(Peer *peer)
{
	if(peer == NULL)   return -1;

	peer-&gt;socket = -1;
	memset(peer-&gt;ip,0,16);
	peer-&gt;port = 0;
	memset(peer-&gt;id,0,21);
	peer-&gt;state = INITIAL;

	peer-&gt;in_buff      = NULL;
	peer-&gt;out_msg      = NULL;
	peer-&gt;out_msg_copy = NULL;

	peer-&gt;in_buff = (char *)malloc(MSG_SIZE);
	if(peer-&gt;in_buff == NULL)  goto OUT;
	memset(peer-&gt;in_buff,0,MSG_SIZE);
	peer-&gt;buff_len = 0;

	peer-&gt;out_msg = (char *)malloc(MSG_SIZE);
	if(peer-&gt;out_msg == NULL)  goto OUT;
	memset(peer-&gt;out_msg,0,MSG_SIZE);
	peer-&gt;msg_len  = 0;
	
	peer-&gt;out_msg_copy = (char *)malloc(MSG_SIZE);//这里为out_ms_copy分配了16KB的缓存空间
	if(peer-&gt;out_msg_copy == NULL)  goto OUT;
	memset(peer-&gt;out_msg_copy,0,MSG_SIZE);
	peer-&gt;msg_copy_len   = 0;
	peer-&gt;msg_copy_index = 0;

	peer-&gt;am_choking      = 1;
	peer-&gt;am_interested   = 0;
	peer-&gt;peer_choking    = 1;
	peer-&gt;peer_interested = 0;
	
	peer-&gt;bitmap.bitfield        = NULL;
	peer-&gt;bitmap.bitfield_length = 0;
	peer-&gt;bitmap.valid_length    = 0;
	
	peer-&gt;Request_piece_head     = NULL;
	peer-&gt;Requested_piece_head   = NULL;
	
	peer-&gt;down_total = 0;
	peer-&gt;up_total   = 0;
	
	peer-&gt;start_timestamp     = 0;
	peer-&gt;recet_timestamp     = 0;
	
	peer-&gt;last_down_timestamp = 0;
	peer-&gt;last_up_timestamp   = 0;
	peer-&gt;down_count          = 0;
	peer-&gt;up_count            = 0;
	peer-&gt;down_rate           = 0.0;
	peer-&gt;up_rate             = 0.0;
	
	peer-&gt;next = (Peer *)0;
	return 0;

OUT:
	if(peer-&gt;in_buff != NULL)      free(peer-&gt;in_buff);
	if(peer-&gt;out_msg != NULL)      free(peer-&gt;out_msg);
	if(peer-&gt;out_msg_copy != NULL) free(peer-&gt;out_msg_copy);
	return -1;
}

Peer* add_peer_node()
{
	int  ret;
	Peer *node, *p;

	// 分配内存空间
	node = (Peer *)malloc(sizeof(Peer));
	if(node == NULL)  { 
		printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); 
		return NULL;
	}

	// 进行初始化
	ret = initialize_peer(node);
	if(ret &lt; 0) { 
		printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__);
		free(node);
		return NULL;
	}

	// 将node加入到peer链表中
	if(peer_head == NULL)  { peer_head = node; }
	else {
		p = peer_head;
		while(p-&gt;next != NULL)  p = p-&gt;next;
		p-&gt;next = node;
	}

	return node;
}

int del_peer_node(Peer *peer)
{
	Peer *p = peer_head, *q;

	if(peer == NULL)  return -1;

	while(p != NULL) {
		if( p == peer ) {
			if(p == peer_head)  peer_head = p-&gt;next;
			else  q-&gt;next = p-&gt;next;
			free_peer_node(p);  // 可能存在问题
			return 0;
		} else {
			q = p;
			p = p-&gt;next;
		}
	}

	return -1;
}

// 撤消当前请求队列
int cancel_request_list(Peer *node)
{
	Request_piece  *p;

	p = node-&gt;Request_piece_head;  //这里的关键是需要一个变量，用于对节点的释放
	while(p != NULL) {
		node-&gt;Request_piece_head = node-&gt;Request_piece_head-&gt;next;
		free(p);
		p = node-&gt;Request_piece_head;
	}

	return 0;
}

// 撤消当前被请求队列
int cancel_requested_list(Peer *node)
{
	Request_piece  *p;
	
	p = node-&gt;Requested_piece_head;//同样也是需要一个变量，用于释放内存
	while(p != NULL) {
		node-&gt;Requested_piece_head = node-&gt;Requested_piece_head-&gt;next;
		free(p);
		p = node-&gt;Requested_piece_head;
	}
	
	return 0;
}

void  free_peer_node(Peer *node) //将peer结构体本身的内存，以及为peer结构体所分配的内存，都统统释放掉
{
	if(node == NULL)  return;
	if(node-&gt;bitmap.bitfield != NULL) {
		free(node-&gt;bitmap.bitfield);
		node-&gt;bitmap.bitfield = NULL;
	}
	if(node-&gt;in_buff != NULL) {
		free(node-&gt;in_buff); 
		node-&gt;in_buff = NULL;
	}
	if(node-&gt;out_msg != NULL) {
		free(node-&gt;out_msg);
		node-&gt;out_msg = NULL;
	}
	if(node-&gt;out_msg_copy != NULL) {
		free(node-&gt;out_msg_copy);
		node-&gt;out_msg_copy = NULL;
	}

	cancel_request_list(node);
	cancel_requested_list(node);

	// 释放完peer成员的内存后,再释放peer所占的内存
	free(node);
}

void  release_memory_in_peer()//由peer_head起始，然后删除所链接的节点
{
	Peer *p;

	if(peer_head == NULL)  return;

	p = peer_head;
	while(p != NULL) {
		peer_head = peer_head-&gt;next;
		free_peer_node(p);
		p = peer_head;
	}
}

void print_peers_data()
{
	Peer *p    = peer_head;
	int  index = 0;

	while(p != NULL) {
		printf(&quot;peer: %d  down_rate: %.2f \n&quot;, index, p-&gt;down_rate);

		index++;
		p = p-&gt;next;
	}
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971519
</pre>
