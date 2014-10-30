---
layout: post
title: "mongodb释放内存-切换日志"
categories: 数据库
tags: [mongodb, mongodb释放内存]
date: 2014-10-30 23:30:46
---

1、由于碰到过mongodb吃掉所有闲置内存的情况，导致服务器操作越来越慢。虽然对mongodb的读操作没有太多影响，

但是此时写入的性能却极剧下降（怀疑内存不够引起的）。由于要收集大量的历史文件数据，

每次多线程收集到一定的程度时，写入文件速度越来越慢，经过多次测试发现，均与服务内存的使用峰值有关。

当服务器内存使用率较低时，多线程写入较快，当服务器内存被mongodb 映射耗尽时，多线程写入速度慢到惨不忍赌了，

即使是单线程情况这种情况表现也很明显。虽然mongodb提供了runCommnad({closeAllDatabase:1})或关闭数据库释放缓存。

{% highlight bash %}
mongo>use admin

switched to db admin

mongo>db.runCommand({closeAllDatabases:1})
{% endhighlight %}

但是这却影响到了正常读写操作。因此给服务器预留一定的内存空间成了保障快速写入的一个方案，

当然在正常情况下不会出现如此频率的文件写入操作，只是现在面对的情况特殊，是要收集大量历史的文件。

=====================================================================================================



平时可以通过mongo命令行来监控MongoDB的内存使用情况，如下所示：

{% highlight bash %}
mongo> db.serverStatus().mem:
{
    "resident" : 22346,
    "virtual" : 1938524,
    "mapped" : 962283
}还可以通过mongostat命令来监控MongoDB的内存使用情况，如下所示：

shell> mongostat
mapped  vsize    res faults
  940g  1893g  21.9g      0其中内存相关字段的含义是：

mapped：映射到内存的数据大小 
visze：占用的虚拟内存大小 
res：占用的物理内存大小 
{% endhighlight %}

注：如果操作不能在内存中完成，结果faults列的数值不会是0，视大小可能有性能问题。

在上面的结果中，vsize是mapped的两倍，而mapped等于数据文件的大小，所以说vsize是数据文件的两倍，

之所以会这样，是因为本例中，MongoDB开启了journal，需要在内存里多映射一次数据文件，如果关闭journal，

则vsize和mapped大致相当。



==================================================================================

查看内存情况最常用的是free命令：

{% highlight bash %}
shell> free -m
             total       used       free     shared    buffers     cached
Mem:         32101      29377       2723          0        239      25880
-/+ buffers/cache:       3258      28842
Swap:         2047          0       2047
{% endhighlight %}

新手看到used一栏数值偏大，free一栏数值偏小，

往往会认为内存要用光了。其实并非如此，之所以这样是因为每当我们操作文件的时候，

Linux都会尽可能的把文件缓存到内存里，这样下次访问的时候，就可以直接从内存中取结果，

所以cached一栏的数值非常的大，不过不用担心，这部分内存是可回收的，

操作系统的虚拟内存管理器会按照LRU算法淘汰冷数据。还有一个buffers，也是可回收的，不过它是保留给块设备使用的。

知道了原理，我们就可以推算出系统可用的内存是free + buffers + cached：

{% highlight bash %}
shell> echo $((2723 + 239 + 25880))
28842至于系统实际使用的内存是used – buffers – cached：

shell> echo $((29377 - 239 - 25880))
3258
{% endhighlight %}



####切换日志
{% highlight bash %}
use admin
db.runCommand("logRotate")
{% endhighlight %}
