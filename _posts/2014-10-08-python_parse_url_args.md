---
layout: post
title: "python获取url地址中的参数"
categories: python 
tags: [python, urlparse]
date: 2014-10-08 23:15:42
---

现在需要用python获取GET发送的url请求比如这样http://localhost/test.py?a=hello&b=world 
如何在python中获取参数a和b的值


============================
{% highlight python %}
>>> url="http://localhost/test.py?a=hello&b=world "  
>>> result=urlparse.urlparse(url)  
>>> result  
ParseResult(scheme='http', netloc='localhost', path='/test.py', params='', query='a=hello&b=world ', fragment='')  
>>> urlparse.parse_qs(result.query,True)  
{'a': ['hello'], 'b': ['world ']}  
>>> params=urlparse.parse_qs(result.query,True)  
>>> params  
{'a': ['hello'], 'b': ['world ']}  
>>> params['a'],params['b']  
(['hello'], ['world '])  

{% endhighlight %}


用urlparse模块就可以解析出来了
