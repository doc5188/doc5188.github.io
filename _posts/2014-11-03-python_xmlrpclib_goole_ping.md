---
layout: post
title: "python xmlrpclib 完成google ping功能"
categories: python
tags: [python, xmlrpclib, seo ping功能]
date: 2014-11-03 22:45:21
---

最近在做SEO的时候，为了让发的外链能够快速的收录，想到了利用ping的功能，google和百度都有相关的ping介绍，有兴趣的朋友可以去看看相关的知识。实现ping功能除了可以用一些开源的博客程序，比如WP，它是可以在后台设置ping地址的，只要设置好以后，你发帖子，就会自动的通知搜索引擎，我的博客已经更新了，而今天我用的方法是不通过WP等带有ping功能的博客，自己用python 在本地去ping 搜索引擎，从而达到快速收录的效果。附上代码：

{% highlight bash %}
import re

urlinfo = '''http://www.cnpythoner.com/post/181.html
url2
url3
'''

def ping(webname,hosturl,linkurl):
    import xmlrpclib
    rpc_server = xmlrpclib.ServerProxy('http://blogsearch.google.com/ping/RPC2 ')
    result = rpc_server.weblogUpdates.extendedPing(webname,hosturl,linkurl)

    print result                                    
    if result.get('flerror', False) == True:
        print 'ping error'
    else:
        print 'ping success'


def get_url(url):
    '''获取标准的url'''
    
    host_re  = re.compile(r'^https?://(.*?)($|/)',
                       re.IGNORECASE
                   )
    
    return host_re.search(url).group(0)


info = urlinfo.split('\n')

for m in info:
    webname = m.split('.')[1]
    hosturl = get_url(m)
    ping(webname,hosturl,m)
{% endhighlight %}
如果返回的结果是{'message': 'Thanks for the ping.', 'flerror': False}，说明已经ping成功，恭喜你了，呵呵。

希望对大家有帮助。主要还是python xmlrpclib 的用法。


<pre>
referer: http://www.cnpythoner.com/post/182.html
</pre>
