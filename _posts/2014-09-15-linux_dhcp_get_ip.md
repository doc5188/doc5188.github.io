---
layout: post
date: 2014-09-15 21:44:21
title: "Linux 重新获取DHCP IP的几个命令"
categories: linux
tags: [linux, dhcp]
---

1. 重启网络服务

{% highlight bash %}
# /etc/init.d/network restart

# service network restart
{% endhighlight %}

2. 网卡禁用启用

{% highlight bash %}
# ifconfig eth0 down

# ifconfig eth0 up
{% endhighlight %}

3. 重新获取

{% highlight bash %}
# dhclient -r

# dhclient
{% endhighlight %}
