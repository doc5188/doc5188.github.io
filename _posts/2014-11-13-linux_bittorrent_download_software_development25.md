---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--Makefile"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:43
---

<pre name="code" class="cpp">CC=gcc
CFLAGS= -Iinclude -Wall  -g -DDEBUG
LDFLAGS=-L./lib -Wl,-rpath=./lib -Wl,-rpath=/usr/local/lib

ttorrent: main.o parse_metafile.o tracker.o bitfield.o sha1.o message.o peer.o data.o policy.o torrent.o bterror.o log.o signal_hander.o
	$(CC) -o $@ $(LDFLAGS) $^ -ldl

clean:
	rm -rf *.o ttorrent
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8973117
</pre>
