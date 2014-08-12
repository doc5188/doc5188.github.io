---
layout: post
title: "Linux下查看某个进程的线程数量"
date:   2014-08-12 13:56:11
categories: Linux
---


1.根据进程号进行查询：

{% highlight python %}
# pstree -p 进程号

# top -Hp 进程号
{% endhighlight %}

2.根据进程名字进行查询：

{% highlight python %}
# pstree -p `ps -e | grep server | awk '{print $1}'`

# pstree -p `ps -e | grep server | awk '{print $1}'` | wc -l
{% endhighlight %}
