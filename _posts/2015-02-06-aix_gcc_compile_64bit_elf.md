---
layout: post
title: "在gcc中如何设定编译模式为64位"
categories: aix 
tags: [gcc]
date: 2015-02-06 15:57:05
---

我的环境是AIX 4.3，gcc2.95.3

原来是使用AIX自带的cc编译器，但现在由于要编译、连接C++的文件，所以使用gcc。我需要在编译、连接的时候指定编译模式为64位的，原来使用AIX自带的cc编译器时是用-q64指定的，但gcc中不支持-q64这个选项。


g++ -maix64
