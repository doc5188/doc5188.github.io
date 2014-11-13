---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--出错处理模块（bterror.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:27
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &quot;bterror.h&quot;

void btexit(int errno,char *file,int line)
{
	printf(&quot;exit at %s : %d with error number : %d\n&quot;,file, line, errno);
	exit(errno);
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971473
</pre>
