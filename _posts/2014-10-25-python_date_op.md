---
layout: post
title: "Python日期操作"
categories: python
tags: [python]
date: 2014-10-25 17:46:03
---


* 1. 日期输出格式化

所有日期、时间的api都在datetime模块内。

1. datetime => string
<pre>
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
</pre>
输出2012-03-05 16:26:23.870105

strftime是datetime类的实例方法。

2. string => datetime

<pre>
t_str = '2012-03-05 16:26:23'
d = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
</pre>
strptime是datetime类的静态方法。

* 2. 日期比较操作

在datetime模块中有timedelta类，这个类的对象用于表示一个时间间隔，比如两个日期或者时间的差别。

构造方法：
<pre>
datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
</pre>
所有的参数都有默认值0，这些参数可以是int或float，正的或负的。

可以通过timedelta.days、tiemdelta.seconds等获取相应的时间值。

timedelta类的实例，支持加、减、乘、除等操作，所得的结果也是timedelta类的实例。比如：

<pre>
year = timedelta(days=365)
ten_years = year *10
nine_years = ten_years - year
</pre>

同时，date、time和datetime类也支持与timedelta的加、减运算。

<pre>
datetime1 = datetime2 +/- timedelta
timedelta = datetime1 - datetime2
</pre>
这样，可以很方便的实现一些功能。

1. 两个日期相差多少天。

<pre>
d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print delta.days
</pre>

输出：3

2. 今天的n天后的日期。

<pre>
now = datetime.datetime.now()
delta = datetime.timedelta(days=3)
n_days = now + delta
print n_days.strftime('%Y-%m-%d %H:%M:%S')
</pre>
输出：2012-03-08 17:44:50

<pre>
#coding=utf-8
import datetime
now=datetime.datetime.now()
print now
#将日期转化为字符串 datetime => string

print now.strftime('%Y-%m-%d %H:%M:%S')

t_str = '2012-03-05 16:26:23'

#将字符串转换为日期 string => datetime
d=datetime.datetime.strptime(t_str,'%Y-%m-%d %H:%M:%S')
print d
#在datetime模块中有timedelta类，这个类的对象用于表示一个时间间隔，比如两个日#期或者时间的差别。

#计算两个日期的间隔

d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print delta.days
print delta

#今天的n天后的日期。
now=datetime.datetime.now()
delta=datetime.timedelta(days=3)
n_days=now+delta
print n_days.strftime('%Y-%m-%d %H:%M:%S')
</pre>

<img src="/upload/images/201204102330094314.png" />

datetime的好处是可以实现方便的时间运算,比如 endTime - starTime,这在时间duration计算时非常方便.


============================================================================== 
我喜欢程序员，他们单纯、固执、容易体会到成就感；面对压力，能够挑灯夜战不眠不休；面对困难，能够迎难而上挑战自我。他
们也会感到困惑与傍徨，但每个程序员的心中都有一个比尔盖茨或是乔布斯的梦想“用智慧开创属于自己的事业”。我想说的是，其
实我是一个程序员
==============================================================================
