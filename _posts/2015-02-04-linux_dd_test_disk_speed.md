---
layout: post
title: "linux dd读取写入磁盘速度"
categories: linux
tags: [dd测试]
date: 2015-02-04 18:09:39
---

　time有计时作用，dd用于复制，从if读出，写到of。if=/dev/zero不产生IO，因此可以用来测试纯写速度。同理of=/dev/null不产生IO，可以用来测试纯读速度。bs是每次读或写 

<p>　　的大小，即一个块的大小，count是读写块的数量。</p>

<p>　　指定出读取，写入文件到硬盘的速度</p>

<p>　　1.测/目录所在磁盘的纯写速度：</p>

<p>　　[root@base-dmz1 /]# time dd if=/dev/zero bs=1024 count=1000000 of=/1Gb.file</p>

<p>　　1000000+0 records in</p>

<p>　　1000000+0 records out</p>

<p>　　1024000000 bytes (1.0 GB) copied, 2.57314 seconds, 398 MB/s</p>

<p>　　real&nbsp;&nbsp;&nbsp; 0m2.787s</p>

<p>　　user&nbsp;&nbsp;&nbsp; 0m0.920s</p>

<p>　　sys&nbsp;&nbsp;&nbsp;&nbsp; 0m1.867s</p>

<p>　　以上是因为使用了time才显示的，linux5中不需要使用，在linux4中是不会有（1024000000 bytes (1.0 GB) copied, 2.57314 seconds, 398 MB/s）部分，因此需要time命令来计</p>

<p>　　算复制的时间。</p>

<p>　　2.测/目录所在磁盘的纯读速度：</p>

<p>　　dd if=/kvm/ftp/other/1Gb.file bs=64k |dd of=/dev/null</p>

<p>　　382860+0 records in</p>

<p>　　382860+0 records out</p>

<p>　　3136389120 bytes (3.1 GB) copied, 68.38 seconds, 45.9 MB/s</p>

<p>　　real&nbsp;&nbsp;&nbsp; 1m8.406s</p>

<p>　　user&nbsp;&nbsp;&nbsp; 0m0.039s</p>

<p>　　sys&nbsp;&nbsp;&nbsp;&nbsp; 0m4.573s</p>

<p>　　3.测读写速度（这是什么）：</p>

<p>　　dd if=/vat/test of=/oradata/test1 bs=64k</p>

<p>　　dd: writing `/oradata/test1': No space left on device</p>

<p>　　5025+0 records in</p>

<p>　　5024+0 records out</p>

<p>　　329261056 bytes (329 MB) copied, 23.8813 seconds, 13.8 MB/s</p>

<p>　　注：理论上复制量越大测试越准确。</p>
