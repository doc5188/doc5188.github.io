---
layout: post
title: "MongoEngine文档翻译__新手教程（一）安装MongoEngine&连接MongoDB"
categories: python
tags: [mongoengine]
date: 2014-10-16 00:29:43
---

PS：非常不错的mongoengine新手教程

最近开始做一个Python + MongoDB的项目，用到了MongoEngine这个非常不错的ORM工具，我将MongoEngine的文档翻译一部分出来，与大家分享。

* 安装MongoEngine

为了使用MongoEngine，我们首先需要先下载一个MongoDB并且确保它能正常运行，你还需要安装pymongo。

可以用pip安装MongoEngine:

<pre>
$ pip install mongoengine  
</pre>

但是如果你没有安装setuptool，那么下载一个 MongoEngine ，然后手动安装 

<pre>
$ python setup.py install  
</pre>


如果你想用最新得MongoEngine，可以从GitHub上下载源码，然后按如下安装：

<pre>
$ git clone git://github.com/hmarr/mongoengine  
$ cd mongoengine  
$ python setup.py install  
</pre>

ps:由于mongoengine底层使用的是pymongo库，所以安装mongoengine的时候一定要安装与其版本配套的pymongo版本，否则在使用的时候或出现调用pymongo上的错误。（一般建议安装最新版的pymongo,否则要上网查下版本匹配）。

* 连接MongoDB

 连接一个运行的MongoDB实例，可以使用connect( ) 函数。第一个参数是需要连接的数据库名称，如果该数据库不存在，那么就会新建一个相应的数据库。如果该数据库需要验证登录，那么用户名和密码这些参数也需要提供。

<pre>
from mongoengine import connect  
connect('project1', username='webapp', password='pwd123')  
</pre>

在默认情况下，MongoDB的实例是运行在localhost的27017端口上，如果MongoDB是运行于别的地方，那么就需要提供host和port参数：

<pre>
connect('project1', host='192.168.1.35', port=12345)  
</pre>

Uri方式的连接也是支持的
<pre>
connect('project1', host='mongodb://localhost/database_name')  
</pre>
     
在MongoEngine 0.6中添加了对多数据库的支持。使用多数据库的时候使用 connect( )，并且提供一个连接的别名，如果没有提供别名就使用default。

在后台里面会使用 register_connection(  )来存储那些前端需要的所有别名数据。

单个的文档也能通过在它们的元数据中提供一个db_alias来实现对多数据库的支持。下面这个例子就使用了3个不同数据库来存储数据。

<pre>
class User(Document):  
    name = StringField()  
  
    meta = {"db_alias": "user-db"}  
  
class Book(Document):  
    name = StringField()  
  
    meta = {"db_alias": "book-db"}  
  
class AuthorBooks(Document):  
    author = ReferenceField(User)  
    book = ReferenceField(Book)  
  
    meta = {"db_alias": "users-books-db"}  

</pre>
