---
layout: post
title: "请问apache运行正常，能运行*.php文件，但是不能执行php代码，为什么？"
categories: linux
tags: [apache, http]
date: 2014-10-03 01:53:54
---

请问apache运行正常，能运行*.php文件，但是不能执行php代码，为什么？


解答:


http.conf里要加上:
<pre>
    AddType application/x-httpd-php .php
    AddType application/x-httpd-php3 .php3
</pre>
