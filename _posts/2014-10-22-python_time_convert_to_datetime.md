---
layout: post
title: "python time 和datetime类型转换，字符串型变量转成日期型变量"
categories: python 
tags: [python, time和datetime互转]
date: 2014-10-22 11:18:30
---

<pre>
s1='20120125';
s2='20120216';
a=time.strptime(s1,'%Y%m%d');
b=time.strptime(s2,'%Y%m%d');
a_datetime=datetime.datetime(*a[:3]);
b_datetime=datetime.datetime(*b[:3]);
print b_datetime-a_datetime;
</pre>

 


为了从字符串中提取时间，并进行比较，因此有了这个问题，如何将字符串转换成datetime类型

 

* 1.字符串与time类型的转换

<pre>
>>> import time
>>> timestr = "time2009-12-14"
>>> t = time.strptime(timestr, "time%Y-%m-%d")
>>> print t
(2009, 12, 14, 0, 0, 0, 0, 348, -1)

>>> type(t)
<type 'time.struct_time'>
>>>
</pre>

 

如代码所示使用strptime进行转换，第一个参数是要转换的字符串，第二个参数是字符串中时间的格式

 

与之对应的有函数strftime，是将time类型转换相应的字符串

 

下面是格式化符号汇总

<pre>
　　%a 星期几的简写 Weekday name, abbr.
　　%A 星期几的全称 Weekday name, full
　　%b 月分的简写 Month name, abbr.
　　%B 月份的全称 Month name, full
　　%c 标准的日期的时间串 Complete date and time representation
　　%d 十进制表示的每月的第几天 Day of the month
　　%H 24小时制的小时 Hour (24-hour clock)
　　%I 12小时制的小时 Hour (12-hour clock)
　　%j 十进制表示的每年的第几天 Day of the year
　　%m 十进制表示的月份 Month number
　　%M 十时制表示的分钟数 Minute number
　　%S 十进制的秒数 Second number
　　%U 第年的第几周，把星期日做为第一天（值从0到53）Week number (Sunday first weekday)
　　%w 十进制表示的星期几（值从0到6，星期天为0）weekday number
　　%W 每年的第几周，把星期一做为第一天（值从0到53） Week number (Monday first weekday)
　　%x 标准的日期串 Complete date representation (e.g. 13/01/08)
　　%X 标准的时间串 Complete time representation (e.g. 17:02:10)
　　%y 不带世纪的十进制年份（值从0到99）Year number within century
　　%Y 带世纪部分的十制年份 Year number
　　%z，%Z 时区名称，如果不能得到时区名称则返回空字符。Name of time zone
　　%% 百分号
</pre>

 

 

* 2.time类型与datetime类型的转换

 

这一步比较简单，使用datetime函数，代码如下

<pre>
>>> import datetime
>>> d = datetime.datetime(* t[:6])
>>> print d
2009-12-14 00:00:00

>>> type(d)
<type 'datetime.datetime'>
>>> 

</pre>
