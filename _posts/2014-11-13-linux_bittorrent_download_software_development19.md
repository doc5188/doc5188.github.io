---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--消息处理模块（signal_handler.h）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:38
---

<pre name="code" class="cpp">#ifndef SIGNAL_HANDER_H
#define SIGNAL_HANDER_H

// 做一些清理工作,如释放动态分配的内存
void do_clear_work();

// 处理一些信号
void process_signal(int signo);

// 设置信号处理函数
int set_signal_hander();

#endif</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971548
</pre>
