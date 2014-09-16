---
layout: post
title: "Linux中查看某个库是否存在的命令"
categories: linux
tags: [linux, ldconfig]
date: 2014-09-16 09:36:21
---

在我们做Linux开发的时候，往往会出现 某些库 can not found 的情况，在我们添加了这些库之后，如何查看这些库的路径是否被识别了呢？下面介绍一个命令：

{% highlight bash %}
# ldconfig -p | grep lts
{% endhighlight %}

说明：使用 ldconfig -p 命令用来打印出当前缓存所保存的所有库的名字，然后用管道符传递给 grep lts 命令用于解析出 liblts.so 共享库的路径是否已加入缓存中。


