---
layout: post
title: "Python搭建BT资源搜索站（二）"
categories: python
tags: [python, BT资源搜索站]
date: 2014-10-10 11:54:59
---

前文中从torrage下载了一个info_hash的数据文件下来，但下载的文件仅仅是一个txt文档，需要将这个文档解析成一条一条的数据，保存进咱们的数据库，方便以后的数据库搜索以及一些其他处理。

首先，要用Python读取下载下来的文件内容，并且将文件内容保存进数据库中。虽然以前我是坚决抵制使用nosql作为主要的存储工具，但因为公司的项目的核心数据是在Mongodb中存储，之后必然要接触一些Mongo的工作，所以干脆搞一些小项目从头开始方便我熟悉Mongo。

读取文件的Python函数如下：

{% highlight bash %}
def read_data():
	_file = open('20130820.txt', 'rb').readlines()

	for _item in _file:

		print _item
{% endhighlight %}

这个函数就可以简单的将一个txt文件读取出来，并且逐行输出。

然后，下载Windows版本的Mongo（个人使用的32位系统，开发环境仅供开发使用，服务器上必然会采用64位）。下载完成后解压到硬盘，并将对应的文件夹加入环境变量中。

接下来，e:\python\01hg\bt-search新建一个名字为『data』的文件夹，在『命令提示符』中cd到e:\python\01hg\bt-search目录，输入mongod --dbpath data --setParameter textSearchEnabled=true启动mongo数据库。

然后，下载pymongo这个第三方插件用来支持python操作mongo数据库，下载完成后一路Next安装即可。

然后，需要改造前边的readdata函数，将读取到的文件内容保存到Mongo数据库中去…改造后的readdate函数为：

{% highlight bash %}
from pymongo import Connection #引入Mongo支持

#连接Mongo

mongo = Connection(host='127.0.0.1', port=27017)

db = mongo.bt #连接bt这个数据库，没有会自动新建

#读取下载的文件内容

def read_data():
	_file = open('20130820.txt', 'rb').readlines()

	for _item in _file:
		db.info_hash.insert({"info_hash":_item})

if __name__ == "__main__":
	read_data()
{% endhighlight %}

我写的完整的文件下载：https://gist.github.com/Chairo/6306780/download

在命令行（bt-search）目录下执行python txt.py，然后如果无任何提示输出，表示数据已经存入Mongodb中了。需要查看数据可以安装MongoVUE这个软件（自己搜索，有xx版，我用的是xx版1.5.3）

我执行文件操作后，MongoVUE中可以看到保存了一共5970条数据，如图：

<img src="/upload/images/09d29ae819a913de470ab3f65adec0d3_600.jpg" />

<pre>
source: http://www.au92.com/archives/P-y-t-h-o-n-da-jian-B-T-zi-yuan-sou-suo-zhan-er.html
</pre>
