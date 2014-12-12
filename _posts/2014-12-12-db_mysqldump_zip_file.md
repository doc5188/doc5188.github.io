---
layout: post
title: "用mysqldump导出压缩文件"
categories: 数据库 
tags: [mysql, mysqldump]
date: 2014-12-12 16:27:34
---

直接用mysqldump导出的文件是文本的，所以会很大。导成文本文件再压缩，过程中仍然要占用额外的空间，如果使用管道，则可以直接导成压缩文件。既迅速，又少占空间。比如：

mysqldump sms | gzip > sms.sql.gz

如果不压缩，我直接导成的文件有3G，压缩了则只有100M，还是非常显著的。
