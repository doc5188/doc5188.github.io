---
layout: post
title: "Python日期和字符串的互转"
categories: python
tags: [python]
date: 2014-11-13 11:25:42
---

用的分别是time和datetime函数

 

<pre>
import time,datetime

# date to str
print time.strftime("%Y-%m-%d %X", time.localtime())

#str to date
t = time.strptime("2009 - 08 - 08", "%Y - %m - %d")
y,m,d = t[0:3]
print datetime.datetime(y,m,d)
</pre>

输出当前时间：
<pre>
2009-09-02 23:51:01
2009-08-08 00:00:00
</pre>

 

符：

<pre>
%a 英文星期简写
%A 英文星期的完全
%b 英文月份的简写
%B 英文月份的完全
%c 显示本地日期时间
%d 日期，取1-31
%H 小时， 0-23
%I 小时， 0-12 
%m 月， 01 -12
%M 分钟，1-59
%j 年中当天的天数
%w 显示今天是星期几
%W 第几周
%x 当天日期
%X 本地的当天时间
%y 年份 00-99间
%Y 年份的完整拼写
</pre>
