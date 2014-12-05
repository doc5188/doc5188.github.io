---
layout: post
title: "coreseek增量索引，建立索引后查不出结果"
categories: linux
tags: [coreseek, 搜索引擎, sphinx]
date: 2014-12-05 17:16:40
---



问题在于你的主索引和增量索引的生成地址是一样的., 修改生成地址，即可以解决问题。
