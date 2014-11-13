---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--peer交互模块（torrent.h）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:39
---

<pre name="code" class="cpp">#ifndef TORRENT_H
#define TORRENT_H

#include &quot;tracker.h&quot;

// 负责与所有Peer收发数据、交换消息
int download_upload_with_peers();

int  print_peer_list();
void print_process_info();

void clear_connect_tracker();
void clear_connect_peer();
void clear_tracker_response();
void release_memory_in_torrent();

#endif</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8973098
</pre>
