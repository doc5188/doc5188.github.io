---
layout: post
title: "简易的python web服务器用途"
categories: python 
tags: [python simplehttpserver]
date: 2014-10-28 09:17:46
---

我们在工作中经常会需要看下报表，如tsung的统计报表或者lcov的覆盖情况，这些报表通常为了方便都会作成html格式的。我们可以把这些html网页打包拉回去用浏览器慢慢看，但是每次都要打包，拉数据非常麻烦。我们可以架设个web服务器来做这个事情。

apache或者nginx都太庞大，设置起来太麻烦。简易Python服务器来帮忙了。

只要在你的html的目录下运行：
{% highlight bash %}
$ python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
localhost.localdomain - - [22/Jul/2011 10:39:52] "GET / HTTP/1.1" 200 -
...
{% endhighlight %}

服务器就架设起来了，我们来验证下：
{% highlight bash %}
$ telnet localhost 8000
Trying 127.0.0.1...
Connected to localhost.localdomain (127.0.0.1).
Escape character is '^]'.
GET / HTTP/1.1
 
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/2.4.3
Date: Fri, 22 Jul 2011 02:39:52 GMT
Content-type: text/html
Content-Length: 1247
 
<title>Directory listing for /</title>
<h2>Directory listing for /</h2>
<hr>
<ul>
<li><a href="filename">filename</a>
...
</ul>
<hr>
{% endhighlight %}

因为python几乎是所有服务器的标配，所以使用起来没有障碍。

这样是不是很方便?

祝玩得开心！

<pre>
原文: http://blog.yufeng.info/archives/1449
</pre>
