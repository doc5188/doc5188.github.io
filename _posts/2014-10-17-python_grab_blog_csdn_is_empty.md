---
layout: post
title: "python抓取csdn博客内容怎么实现？"
categories: python
tags: [python采集csdn]
date: 2014-10-17 16:50:21
---

我是想先把 http://blog.csdn.net/u013055678页面内对应的链接提取出来，然后再循环打开每一个链接，到里面提取内容写到一个txt中

可是我用BeautifulSoup提取整个页面的链接都提取不出来，为什么呢？？？？

{% highlight bash %}
from bs4 import BeautifulSoup

import requests
import re
  
r = requests.get('http://blog.csdn.net/u013055678').content
content = BeautifulSoup(r).findAll('a')
print content
 
outfile=open('test2.txt','w')
for line in str(content):
    outfile.write(line)
{% endhighlight %}

BeautifulSoup(r).findAll('a')为什么是空？？？



<pre>
r = requests.get('http://blog.csdn.net/u013055678')
</pre>

这句，csdn防爬虫做了保护，你必须加个头
<pre>
r = requests.get('http://blog.csdn.net/u013055678'，headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'})
</pre>
