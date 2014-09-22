---
layout: post
title: "Linux中命令cat /proc/meminfo读出的内核信息进行解释"
categories: linux
tags: [linux, meminfo, proc]
date: 2014-09-22 15:45:54
---

今天重新尝试了一些命令，其中让我最敢兴趣的就是“cat /proc/meminfo”这个命令，或许这个命令大家很少用，这个命令其实跟

“free -m”这个命令差不多的，只是得出来的信息更详细

{% highlight bash %}
root@vpsroll:~# cat /proc/meminfo
MemTotal: 262144 kB
MemFree: 237904 kB
Cached: 10540 kB
Active: 10220 kB
Inactive: 7004 kB
Active(anon): 6608 kB
Inactive(anon): 76 kB
Active(file): 3612 kB
Inactive(file): 6928 kB
Unevictable: 0 kB
Mlocked: 0 kB
SwapTotal: 524288 kB
SwapFree: 524288 kB
Dirty: 0 kB
Writeback: 0 kB
AnonPages: 6684 kB
Shmem: 2632 kB
Slab: 6972 kB
SReclaimable: 4288 kB
SUnreclaim: 2684 kB
{% endhighlight %}

MemTotal: 所有可用RAM大小（即物理内存减去一些预留位和内核的二进制代码大小）

MemFree: LowFree与HighFree的总和，被系统留着未使用的内存

Buffers: 用来给文件做缓冲大小

Cached: 被高速缓冲存储器（cache memory）用的内存的大小（等于 diskcache minus SwapCache ）.

SwapCached:被高速缓冲存储器（cache memory）用的交换空间的大小

已经被交换出来的内存，但仍然被存放在swapfile中。用来在需要的时候很快的被替换而不需要再次打开I/O端口。

Active: 在活跃使用中的缓冲或高速缓冲存储器页面文件的大小，除非非常必要否则不会被移作他用.

Inactive: 在不经常使用中的缓冲或高速缓冲存储器页面文件的大小，可能被用于其他途径.

HighTotal:

HighFree: 该区域不是直接映射到内核空间。内核必须使用不同的手法使用该段内存。

LowTotal:

LowFree: 低位可以达到高位内存一样的作用，而且它还能够被内核用来记录一些自己的数据结构。Among many

other things, it is where everything from the Slab is allocated. Bad things happen when you’re out of lowmem.

SwapTotal: 交换空间的总大小

SwapFree: 未被使用交换空间的大小

Dirty: 等待被写回到磁盘的内存大小。

Writeback: 正在被写回到磁盘的内存大小。

AnonPages：未映射页的内存大小

Mapped: 设备和文件等映射的大小。

Slab: 内核数据结构缓存的大小，可以减少申请和释放内存带来的消耗。

SReclaimable:可收回Slab的大小

SUnreclaim：不可收回Slab的大小（SUnreclaim+SReclaimable＝Slab）

PageTables：管理内存分页页面的索引表的大小。

NFS_Unstable:不稳定页表的大小

VmallocTotal: 可以vmalloc虚拟内存大小

VmallocUsed: 已经被使用的虚拟内存大小。

VmallocChunk: largest contigious block of vmalloc area which is free
