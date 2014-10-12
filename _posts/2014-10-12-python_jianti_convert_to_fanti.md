---
layout: post
title: "python实现中文字符繁体和简体中文转换"
categories: python
tags: [python]
date: 2014-10-12 08:53:46
---

需求：把中文字符串进行繁体和简体中文的转换；

思路：引入简繁体处理库，有兴趣的同学可以研究一下内部实现，都是python写的


1、下载zh_wiki.py及langconv


zh_wiki.py:https://github.com/skydark/nstools/blob/master/zhtools/zh_wiki.py


langconv.py:https://github.com/skydark/nstools/blob/master/zhtools/langconv.py


下载langconv.py和zh_wiki.py，放在python代码所在目录即可


2、代码实例

{% highlight bash %}
# -*- coding：utf-8 -*-
  
from langconv import *
  
# 转换繁体到简体
line = Converter('zh-hans').convert(line.decode('utf-8'))
line = line.encode('utf-8')
  
# 转换简体到繁体
line = Converter('zh-hant').convert(line.decode('utf-8'))
line = line.encode('utf-8')

{% endhighlight %}
