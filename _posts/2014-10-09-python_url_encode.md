---
layout: post
title: "实现URL编码解码的python程序"
categories: python
tags: [pyhon, URL编码解码]
date: 2014-10-09 13:55:10
---

实现URL编码解码的python程序

{% highlight python %}
#!/usr/bin/python
import urllib
import sys
string = sys.argv[1]
string = unicode(string,"gbk")
utf8_string = string.encode("utf-8")
gbk_string=string.encode("gbk")
gbk=urllib.quote(gbk_string)
utf8=urllib.quote(utf8_string)
print gbk
print utf8
{% endhighlight %}

解码使用unqute和decode函数

