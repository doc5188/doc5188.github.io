---
layout: post
title: "CentOS使用virt-what知道虚拟机的虚拟化技术"
tags: [linux, centos, virt-what]
categories: linux
date: 2014-08-22 13:16:00
---

通常拿到一台vps，提供商可能不会告诉我们具体的虚拟化技术，对于CentOS的系统的vm，可以使用virt-what来知道。

如果提示virt-what命令找不到，则需要安装一下

{% highlight bash %}
# yum install virt-what
{% endhighlight %}

我找了一台vm执行virt-what，输出如下

{% highlight bash %}
[root@xxx  ~]$ virt-what
xen
xen-hvm
{% endhighlight %}

从这个结果看，这个vm使用了xen作为虚拟化，并且使用xen的hvm虚拟化方式

再看一台vm，可以看到用的是Windows的hyperv虚拟化机器

{% highlight bash %}
[root@xxx ~]$ virt-what
hyperv
{% endhighlight %}

执行man virt-what 查看更多信息
