---
layout: post
title: "nginx+php-fpm页面显示空白的解决方法"
categories: linux
tags: [nginx, php-fpm]
date: 2014-11-21 13:06:13
---

在nginx与php的环境中，配置了一个wordpress，访问时发现php的页面一直显示空白，起初以为是权限问题，将权限改成755后还是不行。

然后，开启nginx和php的日志，但在日志里也没有发现有价值的错误。

继续尝试更改php的日志，依然无果。

最后发现是nginx的配置文件里面少写了一条配置信息：

fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;

未配置以上信息时，会导致nginx没有发送要解析的php文件地址给phpfpm，所以页面一直是空白的，也没有解析的错误信息。
