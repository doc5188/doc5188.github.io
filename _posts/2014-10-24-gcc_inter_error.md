---
layout: post
title: "gcc 编译出现 internal compiler error: Killed"
categories: c/c++
tags: [gcc编译出错]
date: 2014-10-24 00:22:53
---

<pre>
internal compiler error: Killed (program cc1plus)
</pre>

在 640M 内存的 vps 做编译的时候出现了上述错误.

几经搜索, 才发可能是系统没有交换分区, 编译过程中内存耗尽, 导致了编译中断 …

解决方式也很简单, 就是增加一个交换分区:

* 1. 创建分区文件, 大小 2G
{% highlight bash %}
dd if=/dev/zero of=/swapfile bs=1k count=2048000
{% endhighlight %}

* 2. 生成 swap 文件系统

{% highlight bash %}
mkswap /swapfile
{% endhighlight %}

* 3. 激活 swap 文件

{% highlight bash %}
swapon /swapfile
{% endhighlight %}

这样就木有问题了, 但是这样并不能在系统重启的时候自动挂载交换分区, 这样我们就需要修改 fstab.

修改 /etc/fstab 文件, 新增如下内容:
<pre>
/swapfile  swap  swap    defaults 0 0
</pre>

这样每次重启系统的时候就会自动加载 swap 文件了.

<pre>
referer:http://xwsoul.com/posts/684
</pre>
