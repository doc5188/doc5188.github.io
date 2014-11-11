---
layout: post
title: "编译错误\"/usr/bin/ld: cannot find -lz\""
categories: linux
tags: [linux]
date: 2014-11-11 11:57:25
---

编译的时候出现"/usr/bin/ld: cannot find -lz"错误，需要安装zlib-dev这个包，在线安装命令为：

apt-get install zlib1g-dev

