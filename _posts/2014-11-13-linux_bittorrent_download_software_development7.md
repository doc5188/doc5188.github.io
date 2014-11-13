---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--日志管理模块（log.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:30
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;sys/stat.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;fcntl.h&gt;
#include &quot;log.h&quot;

int logfile_fd = -1;

void logcmd(char *fmt,...)
{
        va_list ap;//这是一个结构体变量，用于可变参数问题

	va_start(ap,fmt);//获取可变参数列表，第一个参数的地址。
	vprintf(fmt,ap);//和printf相似，fmt为format(格式)，ap为可变参数列表，通过vprintf将其打印出来。
	va_end(ap);//清空va_list可变列表。
}

int init_logfile(char *filename)
{
	logfile_fd = open(filename,O_RDWR|O_CREAT|O_APPEND,0666);
	if(logfile_fd &lt; 0) {
		printf(&quot;open logfile failed\n&quot;);
		return -1;
	}

	return 0;
}

int logfile(char *file,int line,char *msg)
{
	char buff[256];

	if(logfile_fd &lt; 0)  return -1;

	snprintf(buff,256,&quot;%s:%d %s\n&quot;,file,line,msg);
	write(logfile_fd,buff,strlen(buff));
	
	return 0;
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971492
</pre>
