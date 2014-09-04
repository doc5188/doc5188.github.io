---
layout: post
title: "Shell script: 获取适配器/IP/子网掩码/网关地址的脚本"
categories: linux
tags: [shell, linux]
date: 2014-09-04 17:52:21
---

{% highlight bash%}
#/bin/bash
 
adapter=$(ifconfig | grep -m1 'encap:Ethernet' | cut -d' ' -f1)
echo "Adapter: $adapter"
 
ip=$(ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}')
echo "IP: $ip"
 
mask=$(ifconfig | grep 'Mask:'| grep -v '127.0.0.1' | cut -d: -f4 | awk '{ print $1}')
echo "Mask: $mask"
 
gateway=$(netstat -r | grep 'default' | awk '{ print $2}')
echo "Gateway: $gateway"
{% endhighlight %}
