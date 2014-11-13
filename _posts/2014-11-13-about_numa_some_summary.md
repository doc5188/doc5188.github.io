---
layout: post
title: "关于numa的一些总结"
categories: 技术文章 
tags: [NUMA]
date: 2014-11-13 14:25:00
---

<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">1.不同的操作系统对numa的支持不一样.</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">1.1 solaris提供了locality group api. 可以使用它方便地进行 locality操作.api可以参考<a href="http://docs.oracle.com/cd/E19082-01/820-1691/lgroups-1/index.html" style="color: rgb(34, 0, 0); text-decoration: none; line-height: 26px;">http://docs.oracle.com/cd/E19082-01/820-1691/lgroups-1/index.html</a>.
 另外还有一点需要注意, solaris提供的系统调用mmap分配内存的时候会在多个node上都分配内存.所以在调度的时候,可以使用numa的locality特性来访问数据,以提高性能.</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">1.2 linux对numa也提供了一些函数,但是它提供的操作并不好用.如mbind,set_mempolicy.sched_setaffinity等.</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">不过linux上提供了一个api libnuma.可以用它来进行相关调用.不过个人感觉也不是很好用.</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">具体的比较可以参考论文"Exploring Thread and Memory Placement on&nbsp;NUMA Architectures: Solaris and Linux,<br>
UltraSPARC/FirePlane and&nbsp;Opteron/HyperTransport".</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;"><br>
</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">2.libnuma提供的api:<a href="http://linux.die.net/man/3/numa">http://linux.die.net/man/3/numa</a>.</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">3.从指定的内存地址得到其对应的node结点:<a href="http://stackoverflow.com/questions/7986903/can-i-get-the-numa-node-from-a-pointer-address-in-c-on-linux">http://stackoverflow.com/questions/7986903/can-i-get-the-numa-node-from-a-pointer-address-in-c-on-linux</a>.</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;"><a href="http://stackoverflow.com/questions/8154162/numa-aware-cache-aligned-memory-allocation">http://stackoverflow.com/questions/8154162/numa-aware-cache-aligned-memory-allocation</a>.<br>
</span></p>
<p><span style="font-family: KaiTi_GB2312; font-size: 18px;">4.给定一个进程,绑定到指定的node上.</span></p>


<pre>
referer: http://blog.csdn.net/chrysanthemumcao/article/details/9237891
</pre>
