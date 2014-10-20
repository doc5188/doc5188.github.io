---
layout: post
title: "KVM网络配置"
categories: 虚拟化
tags: [kvm, KVM网络配置]
date: 2014-10-20 13:06:24
---

=============================================================================================

近几天在搞kvm。kvm真的是很不错，运行操作系统速度非常快，至少比我以前用的vbox要快。但是 kvm的网络配置让我头疼了一阵，上网找了很多资料，无奈那些资料要不省略了一些内容（都把我当高手看了），要不就是写了一堆东西，不说原理，看了半天都搞不懂为什么要那么做，反正都不适合我这种“从0开始”的人。故今天花了几个小时做实验，终于弄出了一个解决方法，现在从头到尾讲出来跟大家分享一下。

对于那些跟我一样想要找到一个只要照着它的提示打命令就多半能成功的方法的人，此帖应该有用。高手请无视此帖～

首先说一下实现原理。我是想先在host上造一块假网卡，然后guest的系统跟这假网卡连接构成一个局域网。guest想连外网的话，就把host当路由器。至于域名服务器，在guest系统里直接指定。

本人实验的host是ubuntu 8.04 server，guest是freebsd 7.0 release。（都是64位）

接下来我会假设你已经装了kvm，而且能用它启动虚拟机。

（以下一到四参照了vbox的网络设定，都在host下操作）

* 一，首先把必要的工具装了：
{% highlight bash %}
sudo apt-get install uml-utilities
{% endhighlight %}


* 二，再造假网卡tap0（名字随便取）并作一些基本配置

{% highlight bash %}
sudo tunctl -t tap0 -u xxx
{% endhighlight %}

此处xxx换成你自己的用户名

{% highlight bash %}
sudo chmod 0666 /dev/net/tun
{% endhighlight %}

这样大家都有权力去读写那个假网卡。即使在上面那行代码中你指定了自己的用户名，你还是没有办法读写tap0（很奇怪），所以这条命令是有用的。


* 三，配置网卡的网络参数。

{% highlight bash %}
sudo ifconfig tap0 192.168.0.10 netmask 255.255.255.0 up
{% endhighlight %}


随便设，但是你要确保你待会设置的guest的网卡ip跟tap0的属于同一个网段。

* 四，接下来是系统的配置（连外网所必须）

{% highlight bash %}
sudo echo 1 > /proc/sys/net/ipv4/ip_forward
{% endhighlight %}

这样开启了linux的ip转发功能，host可以当路由器用了。如果你想让guest连上外网的话这条一定要。

{% highlight bash %}
sudo iptables -t nat -A POSTROUTING -j MASQUERADE
{% endhighlight %}

