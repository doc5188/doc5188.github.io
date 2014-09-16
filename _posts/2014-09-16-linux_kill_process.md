---
layout: post
title: "杀死Linux系统僵死进程"
categories: linux
tags: [linux]
date: 2014-09-16 10:35:45
---

杀死系统僵死进程

先用TOP看一下

<pre>
top - 16:00:43 up 3 days, 17:10,  1 user,  load average: 1.35, 1.60, 1.54
Tasks: 384 total,   1 running, 381 sleeping,   0 stopped,   2 zombie
Cpu(s):  0.2%us, 16.0%sy,  0.0%ni, 83.9%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
Mem:  16429044k total, 11552248k used,  4876796k free,   188340k buffers
Swap:  4096564k total,        0k used,  4096564k free,  9485144k cached
</pre>
发现

 2 zombie
用一下命令查找 

{% highlight bash %}
# ps -A -o stat,ppid,pid,cmd | grep -e '^[Zz]'
{% endhighlight %}

 

命令注解：
<pre>
　　-A 参数列出所有进程
　　-o 自定义输出字段 我们设定显示字段为 stat（状态）, ppid（进程父id）, pid(进程id)，cmd（命令）这四个参数
　　状态为 z或者Z 的进程为僵尸进程
</pre>

结果
<pre>
Z     5114  5227 [xinitrc] <defunct>
Z     5889  5910 [xinitrc] <defunct>
</pre>

 

先杀进程

{% highlight bash %}
# kill -9 5227
# kill -9 5910
{% endhighlight %}
再查看

{% highlight bash %}
# ps -A -o stat,ppid,pid,cmd | grep -e '^[Zz]'
{% endhighlight %}

结果发现还在
<pre>
Z     5114  5227 [xinitrc] <defunct>
Z     5889  5910 [xinitrc] <defunct>
</pre>

直接干掉父进程

{% highlight bash %}
# kill -9 5114
# kill -9 5889
{% endhighlight %}
再来看一下
{% highlight bash %}
# ps -A -o stat,ppid,pid,cmd | grep -e '^[Zz]'
{% endhighlight %}

结果没有2

2点说明一下：

先杀子进程，如果杀不死直接干掉父进程，这样保险一点，当然你无所谓的话可以直接干掉父进程。
