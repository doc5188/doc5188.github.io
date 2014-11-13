---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--日志管理模块（log.h）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:31
---

<pre name="code" class="cpp">#ifndef  LOG_H
#define  LOG_H
#include &lt;stdarg.h&gt;

// 用于记录程序的行为
void logcmd(char *fmt,...);

// 打开日志文件
int init_logfile(char *filename);

// 将程序运行日志记录到文件
int logfile(char *file,int line,char *msg);

#endif</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971497
</pre>
