---
layout: post
title: "mongoengine教程(1)——概述"
categories: python
tags: [mongoengine]
date: 2014-10-16 00:25:21
---

MongoEngine是MongoDB的一个ODM(Object-Document Mapper)框架，它提供了类似Django的语法来操作MongoDB数据库。

* 安装

安装 MongoEngine 需要先安装 PyMongo。

使用pip安装

<pre>
$ sudo pip install mongoengine
</pre>

通过源代码安装

先从 PyPi 或者 Github 下载源代码。然后再进行安装。

<pre>
$ [sudo] python setup.py install
</pre>

* 使用

首先启动 mongodb 服务器：

<pre>
$ mongod
</pre>

* 连接服务器

使用 connect 方法进行数据库链接，与pymongo的用法相似，其参数可以是多种型式的。

<pre>
from mongoengine import connect
connect('project1')
connect('project1', host='mongodb://localhost:27017/test_database')
</pre>

从 MongoEngine 0.6 开始增加了多数据库的支持， connect 的第二个参数可以为每个链接设置一个别名。

* 定义数据模型

mongoengine的 Document 与django的 Model 相似。

<pre>
class User(mongoengine.Document):
    name = mongoengine.StringField()
    meta = {"db_alias": "default"}
</pre>

* 数据操作

数据的添加过程也与django相似：

<pre>
User.objects.create(name="test1")
User.objects.create(name="test2")
User(name="test3").save()
</pre>

* 查询数据：

User.objects.filter(name="test2")

* 删除数据：

User.objects.filter(name="test2").delete()

MongoEngine虽然提供了ODM，但是我们同样还是可以直接对数据库进行操作。

获取 pymongo 的 collection 对象：

User.objects._collection

然后就可以使用原生的pymongo操作了。
