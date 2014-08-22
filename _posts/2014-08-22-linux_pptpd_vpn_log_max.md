---
layout: post
title: "pptpd VPN服务器日志log错误提示"
categories: linux
tags: [linux, pptpd, vpn]
date: 2014-08-22 16:37:23  
---

<pre>
Dec 18 02:19:55 test1 pptpd[23539]: MGR: connections limit (100) reached, extra IP addresses ignored
Dec 18 02:19:55 test1 pptpd[23540]: MGR: Manager process started
Dec 18 02:19:55 test1 pptpd[23540]: MGR: Maximum of 100 connections available
</pre> 

解决办法：注释掉/etc/pptpd.conf中logwtmp项即可。

PPTPD作VPN服务器架设简单几步：

在el5上的kernel已经支持PPTPD所需环境了。

1、只需先安装PPTP、PPTPD、即可(采用RPM方式安装，或者yum直接Install)

2、编辑pptpd.conf修改

<pre>
localip  #服务器本机的虚地址（和客户端在一个网段，不是实际服务器网卡IP）
remoteip  ＃分发给服务器的IP地址段
netmask
</pre>

修改/etc/ppp/option.pptpd中

<pre>
name pptpd
ms-dns
</pre>

修改／etc/ppp/chap-secrets

<pre>
# Secrets for authentication using CHAP
# client        server  secret                  IP addresses
test pptpd test *
</pre>
