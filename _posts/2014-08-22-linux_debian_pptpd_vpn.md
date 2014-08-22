---
layout: post
title: "Debian下pptpd VPN服务器端和客户端的设置"
categories: linux
tags: [linux, pptpd, vpn]
date: 2014-08-22 16:40:22
---

这里选择的VPN方案，是和Windows VPN 相容的解决方案，因为有一些用户是用的Windows系统，他们也可以用这里的VPN服务器，而不需要装另外的软件。

服务器端：

1. 安装包：pptpd

2. 加入mppe内核模块：modprobe -a ppp_mppe

3. 配置文件：

1) /etc/pptpd.conf文件

<pre>
option /etc/ppp/pptpd-options
stimeout 10
logwtmp
# localip和remoteip可以自己设定
localip 192.168.3.253
remoteip 192.168.3.2-240
</pre>

2) /etc/ppp/pptpd-options文件

<pre>
name pptpd
refuse-pap
refuse-chap
refuse-mschap
require-mschap-v2
require-mppe-128
ms-dns 202.117.0.20
ms-dns 202.117.0.21
proxyarp
nodefaultroute
lock
nobsdcomp
</pre>

3) /etc/ppp/chap-secrets文件
<pre>
test * test 192.168.3.2
</pre>

4 防火墙设置：

1) 加入端口转发：
{% highlight bash%}
# iptables -t nat -A POSTROUTING -p all -o eth0 -s 172.16.0.0/24 -j SNAT --to $ETH0IP
{% endhighlight %}

2) 开放端口TCP 1723
{% highlight bash%}
# iptables -A INPUT -p tcp --dport 1723 -j ACCEPT
# iptables -A INPUT -p gre -j ACCEPT
{% endhighlight %}

3) 如果是redhat/centos系列系统，防火墙中再加入
{% highlight bash%}
# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
{% endhighlight %}


常见问题：

1. Q: GRE: Bad checksum from pppd

A: 防火墙gre协议没有打开

客户端：


1. 安装pptp-linux包

2. 创建一个连接配置

pptpsetup --create fwvpn --server ip --username USERNAME --password PASSWORD --encrypt

3. 拨入fwvpn

pon fwvpn

4. 离线

poff fwvpn

5. 拨入以后，要让所有的流量走fwvpn，还得添加一条路由：route add default dev ppp0

poff以后，这条路由会自动删除。

