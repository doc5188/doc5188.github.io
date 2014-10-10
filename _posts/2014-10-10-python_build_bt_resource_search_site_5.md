---
layout: post
title: "Python搭建BT资源搜索站（五）"
categories: python
tags: [python, BT资源搜索站]
date: 2014-10-10 12:05:35
---

通过前面四篇文章，我们已经采集到了N多BT种子，并且已经将种子中包含的一些信息保存在Mongo数据库中，接下来就是如何将Mongo中的数据通过WEB服务器提供给搜索引擎，提供给一些浏览者。即，如何使用Python搭建一个WEB站点了。

首先我之前的项目均采用Bottle这个Python框架，这次依然不例外。这个框架的好处只有一个：足够简单。

使用Bottle启动一个Web Server是一件非常简单的事，文件保存成app.py：

{% highlight bash %}
from bottle import Bottle, run

app = Bottle()

if __name__ == "__main__":

	#命令行交互模式

	import sys

	port = int(sys.argv[1] if len(sys.argv) > 1 else 8888)

	run(app, host='0.0.0.0', port=port, reloader=True)
{% endhighlight %}

当然bottle.py这个文件需要从官方下载到当前目录，这样才可以正常import。

执行脚本python app.py启动了Web Server后，默认的端口号为8888，但此时在浏览器输入http://localhost:8888会返回一个“Not found: '/'”的404错误。这是因为咱们只是启动了一个空白的Web Server，但没有设置对应的Url route。

设置一个经典的首页显示Hello world的route:

{% highlight bash %}
from bottle import Bottle, run

app = Bottle()

@app.get('/')
def index():
	return 'Hello world'

if __name__ == "__main__":

	# Interactive mode

	import sys

	port = int(sys.argv[1] if len(sys.argv) > 1 else 8888)

	run(app, host='0.0.0.0', port=port, reloader=True)
{% endhighlight %}

这时候再执行python app.py，在浏览器访问http://localhost:8888/就可以看到『Hello world』的字样了。

<pre>
referer: http://www.au92.com/archives/P-y-t-h-o-n-da-jian-B-T-zi-yuan-sou-suo-zhan-wu.html
</pre>


