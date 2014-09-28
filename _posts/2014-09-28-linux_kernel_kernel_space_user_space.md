---
layout: post
categories: Linux内核
tags: [linux内核]
date: 2014-09-28 15:03:41
title: "Linux内核态与用户态通信的常用方法"
---

前言

最近做的事情很多地方用到Linux驱动层与应用层的通信，在此总结下常见的并且在我工作中用到的通信方法。
总结

由于每种方法都可以找到大量的示例代码，同时还有详细的函数手册，我就不贴代码了。只列下相关的方法和一个链接。

<pre>
    procfs
    netlink
    syscall
</pre>

syscall的范围就广了，通过注册字符设备可以使用mmap和ioctl等来进行操作，要注意的是在内核态ioctl已经被废弃，现在应该使用unlocked_ioctl，需要自己来加锁。

用户态通过系统暴露出来的系统调用来进行操作，如mmap，ioctl，open，close，read，write，内核态通过建立共享内存remap_pfn_range或者copy_to_user, copy_from_user来进行操作。

选择哪种方式需要考虑是用户态单进程与内核态通信还是多进程的通信，还要考虑通信的数据量。根据不同的需求来使用不同的方法。

