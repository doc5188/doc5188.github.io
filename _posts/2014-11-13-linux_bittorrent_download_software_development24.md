---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--Main函数模块（main.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:42
---

<pre name="code" class="html">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;malloc.h&gt;
#include &quot;data.h&quot;
#include &quot;tracker.h&quot;
#include &quot;bitfield.h&quot;
#include &quot;torrent.h&quot;
#include &quot;parse_metafile.h&quot;
#include &quot;signal_hander.h&quot;
#include &quot;policy.h&quot;
#include &quot;log.h&quot;

// #define  DEBUG

int main(int argc, char *argv[])
{
	int ret;

	if(argc != 2) {
		printf(&quot;usage:%s metafile\n&quot;,argv[0]);
		exit(-1);
	}

	// 设置信号处理函数
	ret = set_signal_hander();
	if(ret != 0)  { printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); return -1; }

	// 解析种子文件
	ret = parse_metafile(argv[1]);
	if(ret != 0)  { printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); return -1; }

	// 初始化非阻塞peer
	init_unchoke_peers();

	// 创建用于保存下载数据的文件
	ret = create_files();
	if(ret != 0)  { printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); return -1; }

	// 创建位图
	ret = create_bitfield();
	if(ret != 0)  { printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); return -1; }

	// 创建缓冲区
	ret = create_btcache();
	if(ret != 0)  { printf(&quot;%s:%d error\n&quot;,__FILE__,__LINE__); return -1; }

	// 负责与所有Peer收发数据、交换消息
	download_upload_with_peers();

	// 做一些清理工作,主要是释放动态分配的内存
	do_clear_work();

	return 0;
}</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8973110
</pre>
