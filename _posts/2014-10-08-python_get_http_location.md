---
layout: post
title: "python httplib获取location"
categories: python
tags: [python, httplib, http location]
date: 2014-10-08 23:18:38
---

<pre>

#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import httplib
 
httplib.HTTPConnection.debuglevel = 1
'''
200正常状态码不会有跳转 也就不会有location
conn = httplib.HTTPConnection("tu.duowan.com") #这里是host
conn.request('GET', '/m/meinv/index.html')#上面是分支 注意是GET
'''
#访问跳转的302页面就可以在headers中找到location
conn = httplib.HTTPConnection("localhost") #这里是host
conn.request('GET', '/yesearch/index.php?r=site/index')#上面是分支 注意是GET
for item in conn.getresponse().getheaders(): 
if item[0]=='location':
print item[1]
conn.close()

</pre>
