---
layout: post
title: "Shell 三目运算符"
categories: linux
tags: [shell, linux, shell三目运算符]
date: 2014-10-09 11:14:27
---

shell的三目运算符应该怎么写?

虽然需求用if可以实现，网上说和c一样，但是不知怎么写

a=(2>1)?2:1;

shell中该怎么写？

<pre>
cmd1 && cmd2 || cmd3
等价
if cmd1; then cmd2; else cmd3
</pre>
