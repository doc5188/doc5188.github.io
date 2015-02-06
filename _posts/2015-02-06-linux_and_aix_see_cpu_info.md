---
layout: post
title: "AIX和Linux下如何查看CPU和内存信息"
categories: linux
tags: [aix, linux]
date: 2015-02-06 14:04:48
---

AIX操作系统

AIX的硬件信息可以通过prtconf命令看到。

1. 查看逻辑CPU个数

<pre>
#pmcycles -m

CPU 0 runs at 4204 MHz
CPU 1 runs at 4204 MHz
CPU 2 runs at 4204 MHz
CPU 3 runs at 4204 MHz
CPU 4 runs at 4204 MHz
CPU 5 runs at 4204 MHz
CPU 6 runs at 4204 MHz
CPU 7 runs at 4204 MHz
</pre>

上面描述有8个CPU，CPU的主频为4.2G赫兹

 

2. 查看物理CPU个数

<pre>
#prtconf|grep Processors

Number Of Processors: 4
</pre>

 

3. 确定CPU是几核

用逻辑CPU除以物理CPU就是核数。

 

4. 查看单个CPU的详细信息

<pre>
#lsattr -E -l proc0

frequency   4204000000     Processor Speed       False
smt_enabled true           Processor SMT enabled False
smt_threads 2              Processor SMT threads False
state       enable         Processor state       False
type        PowerPC_POWER6 Processor type        False
</pre>

 

Linux操作系统

Linux下的CPU信息全部都在/proc/cpuinfo这个文件中，可以直接打开看。

 

1. 查看物理CPU的个数

<pre>
#cat /proc/cpuinfo |grep "physical id"|sort |uniq|wc -l
</pre>

 

2. 查看逻辑CPU的个数

<pre>
#cat /proc/cpuinfo |grep "processor"|wc -l
</pre>

 

3. 查看CPU是几核

<pre>
#cat /proc/cpuinfo |grep "cores"|uniq
</pre>

 

4. 查看CPU的主频

<pre>
#cat /proc/cpuinfo |grep MHz|uniq
</pre>
