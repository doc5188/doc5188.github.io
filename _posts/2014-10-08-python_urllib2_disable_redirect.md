---
layout: post
title: "Python:防止urllib2 302自动跳转"
categories: python
tags: [python, urllib2]
date: 2014-10-08 23:29:03
---

说明：python的urllib2获取网页(urlopen)会自动重定向（301,302）。但是，有时候我们需要获取302,301页面的状态信息。就必须获取到转向前的调试信息。

下面代码将可以做到避免302重定向到新的网页
{% highlight python %}
#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
#Filename:states_code.py
 
import urllib2
 
class RedirctHandler(urllib2.HTTPRedirectHandler):
    """docstring for RedirctHandler"""
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass
 
def getUnRedirectUrl(url,timeout=10):
    req = urllib2.Request(url)
    debug_handler = urllib2.HTTPHandler(debuglevel = 1)
    opener = urllib2.build_opener(debug_handler, RedirctHandler)
 
    html = None
    response = None
    try:
        response = opener.open(url,timeout=timeout)
        html = response.read()
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            error_info = e.code
        elif hasattr(e, 'reason'):
            error_info = e.reason
    finally:
        if response:
            response.close()
    if html:
        return html
    else:
        return error_info
 
html = getUnRedirectUrl('http://phpno.com')
print html
{% endhighlight %}

<pre>
 来源: http://www.phpno.com/getunredirecturl.html
</pre>
