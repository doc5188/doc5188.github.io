---
layout: post
title: "python 时间格式化/数值格式化"
categories: python
tags: [python]
date: 2014-10-01 17:22:37
---

 time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(1228828570))


time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


'%.2fG'%(float(3222566706)/(1024 * 1024 * 1024))
