---
layout: post
title: "python url格式解析(转)"
categories: python
tags: [python, url解析]
date: 2014-11-26 20:42:24
---

<pre>

from urlparse import urlparse

url_str = "http://www.163.com/mail/index.htm"
url = urlparse(url_str)
print 'protocol:',url.scheme
print 'hostname:',url.hostname
print 'port:',url.port
print 'path:',url.path

i = len(url.path) - 1
while i > 0:
    if url.path[i] == '/':
        break
    i = i - 1
print 'filename:',url.path[i+1:len(url.path)]

</pre>
