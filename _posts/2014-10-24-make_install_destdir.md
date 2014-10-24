---
layout: post
title: "make install的时候指定安装路径"
categories: c/c++
tags: [make]
date: 2014-10-24 09:53:17
---

指定安装路径。

<pre>
make DESTDIR=/path install 
</pre>


注意: DESTDIR必须为绝对路径
