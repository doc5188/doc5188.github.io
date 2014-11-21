---
layout: post
title: "Cannot open or remove a file containing a running program"
categories: aix
tags: [aix]
date: 2014-11-21 11:22:08
---

<p>AIX上用tar更换java版本的时候发生此问题，但ps -ef检查后并未发现相关进程。<br />
用&#8221;slibclean”命令清一下系统的动态库 搞定！</p>
