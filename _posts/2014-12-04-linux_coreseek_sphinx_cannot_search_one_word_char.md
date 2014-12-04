---
layout: post
title: "coreseek 不能搜索单字母英文的解决方法"
categories: linux
tags: [coreseek, sphinx, 搜索引擎]
date: 2014-12-04 17:02:09
---

本文讲解了为什么在coreseek下不能搜索单字符英文的原因和解决方法.

问题描述：

被搜索名字为：php

这时搜索php正常，但是搜索p就搜不到。

解决办法，在索引配置文件中的index中添加

<pre>
min_infix_len = 1
</pre>

最后还要重新索引一下/usr/local/coreseek/bin/indexer -c mysql.conf mysql --rotate

上面的命令不要直接复制确定好自己coreseek的安装目录找到bin下面的命令才行
