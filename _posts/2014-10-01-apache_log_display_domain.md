---
layout: post
title: "Apache 按域名拆分日志"
categories: linux
tags: [apache]
date: 2014-10-01 11:52:19
---

使用rotatelogs也可以，但是会开启多个rotatelogs进程，且影响性能<br><br>一、设置Apache日志记录访问主机名<br><br><wbr><br>httpd.conf<br># 单虚拟主机多子域日志<br>LogFormat "<font color="#ff0000">%V</font> %h %l %u %t \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"" subdomain_combined<br><br>二、多个虚拟主机，只有一个访问日志<br>自动按不同域名拆分日志<br># awk '{print $0&gt;$1}' access_log_20110930<br><br>三、单个虚拟主机，多个子域名<br>拆分bbs域名日志<br># awk '$1=="bbs.china.com" {print $0&gt;$1}' ./access_log_20110930<br># awk '$1=="info.china.com" {print $0&gt;$1}' ./access_log_20110930<br># awk '$1!="bbs.china.com" &amp;&amp;&nbsp; $1!="info.china.com" {print $0&gt;"china.com.log"}' ./access_log_20110930
