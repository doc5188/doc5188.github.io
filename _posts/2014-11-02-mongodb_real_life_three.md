---
layout: post
title: "MongoDB实战系列之三：MongoDB的主从部署"
categories: 数据库
tags: [mongodb实战系列, mongodb主从部署]
date: 2014-11-02 21:46:58
---

主从同步：

<pre>
md01 10.0.0.11 master
md02 10.0.0.12 slave
md03 10.0.0.14 slave

#建立数据库目录

mkdir -p /elain/apps/mongodb/
mkdir -p /elain/data/mongodb/db/
mkdir -p /elain/logs/mongodb/
</pre>
注：
<pre>
1、不需要像mysql一样复制完整数据过去，丛库启动会制动复制主库完整数据。
2、丛库自动配置为只读。
3、mongodb第一次启动时间较长，需要注意等待。
4、管理命令多数都要在admin库中执行 use admin

相关参数：./mongod –help
–autoresync 当发现从服务器的数据不是最新时，开始从主服务器请求同步数据
–slavedelay 同步延迟，单位：秒
</pre>

* 主-从

作为主服务器启动

{% highlight bash %}
/elain/apps/mongodb/bin/mongod --fork --master --oplogSize=4096 --port 27001 --dbpath /elain/data/mongodb/db --logpath /elain/logs/mongodb/mongodb.log
{% endhighlight %}

作为从服务器启动，并指明主服务器地址。–autoresync为强制从主服务器同步全部数据

{% highlight bash %}
/elain/apps/mongodb/bin/mongod --fork --slave --source 10.0.0.11:27001 --port 27001 --dbpath /elain/data/mongodb/db --logpath /elain/logs/mongodb/mongodb.log
{% endhighlight %}
注：可以在启动从时加以下常用参数
<pre>
–slavedelay 10 #延时复制 单位为秒
–autoresync #自动重新同步
–only #复制指定的数据库，默认复制所有的库
–oplogSize #主节点的oplog日志大小，单位为M，建议设大点(更改oplog大小时，只需停主库，删除local.*，然后加–oplogSize=* 重新启动即可,*代表大小)
</pre>

如果发现主从不同步，从上手动同步

db.runCommand({"resync":1})

状态查询

db.runCommand({"isMaster":1})  #主还是从

在丛库上查询主库地址

<pre>
> use local;
switched to db local
> db.sources.find();
{ "_id" : ObjectId("4e9105515d704346c8796407"), "host" : "10.0.0.11:27001", "source" : "main", "syncedTo" : { "t" : 1318155992000, "i" : 1 } }
#查看各Collection状态

db.printCollectionStats();
#查看主从复制状态

db.printReplicationInfo();
</pre>

* 测试主从

在主服务器新建数据库

{% highlight bash %}
mongo --port 27001
>show dbs
>use elaindb
>db.blog.save({title:"new article"})

{% endhighlight %}

在从服务器上查看同步数据

{% highlight bash %}
mongo --port 27001
#在从库插入数据的操作 会提示 not master

> use elaindb;
switched to db elaindb
> db.blog.find();
{ "_id" : ObjectId("4e9174b48443c8ef12b30c56"), "title" : "new article" }
#查看主从同步信息：

> db.printReplicationInfo();
this is a slave, printing slave replication info.
source:   10.0.0.11:27001
syncedTo: Sun Oct 09 2011 18:37:12 GMT+0800 (CST)
= 19 secs ago (0.01hrs)

>db.printSlaveReplicationInfo();
#此为同步过来的数据，测试成功
{% endhighlight %}

附加：

* 添加及删除源：

启动从节点时可以用–source指定主节点，也可以在shell中配置这个源，

启动一个从，端口为27002

{% highlight bash %}
/elain/apps/mongodb/bin/mongod --fork --slave  --port 27002 --dbpath /elain/data/mongodb/testdb --logpath /elain/logs/mongodb/mongodb.log
{% endhighlight %}

登录：

mongo --port 27002

{% highlight bash %}
[root@md03 ~]# mongo --port 27002
MongoDB shell version: 2.0.0
connecting to: 127.0.0.1:27002/test
> show dbs
local   (empty)

添加到从节点上

>use local
>db.sources.insert({"host": "10.0.0.11:27001"});
#查看显示正在同步

> db.sources.find();
{ "_id" : ObjectId("4e9111e1c29bbd9b9cd31d4e"), "host" : "10.0.0.11:27001", "source" : "main", "syncedTo" : { "t" : 1318156782000, "i" : 246 }, "dbsNextPass" : { "testdb" : true, "testdb1" : true } }
#同步完成后

> db.sources.find();
{ "_id" : ObjectId("4e9111e1c29bbd9b9cd31d4e"), "host" : "10.0.0.11:27001", "source" : "main", "syncedTo" : { "t" : 1318156782000, "i" : 256 } }
更改源：(假设10.0.0.12也为主库)

db.sources.insert({"host": "10.0.0.12:27001"});
db.sources.remove({"host": "10.0.0.11:27001"});
若复制中使用了认证，需在local库中添加repl用户来复制

>user local;
> db.addUser("repl", "elain123");
{% endhighlight %}

* 附录一、Slave 顶替 Master

如果主服务器 10.0.0.11 宕机了,

此时需要用 10.0.0.12 机器来顶替 master 服务,

步骤如下:

<pre>
#停止 10.0.0.12 进程(mongod)

kill -2 `ps -ef|grep mongod|grep -v grep|awk ''''{print $2}''''`

#删除 10.0.0.12 数据目录中的 local.*

rm -rf /elain/data/mongodb/db/local.*
#以–master 模式启动 10.0.0.12

/elain/apps/mongodb/bin/mongod --fork --master --oplogSize=4096 --port 27001 --dbpath /elain/data/mongodb/db --logpath /elain/logs/mongodb/mongodb.log

</pre>


* 附录二、切换 Master/Slave 角色

切换主库10.0.0.11和从库10.0.0.12的角色

步骤如下:（命令略）

<pre>
用 fsync 命令暂停 主库 上的写操作,
关闭 从库 上的服务
清空 从库 上的 local.*文件
用-master 选项重启 从库 服务
在 从库 上执行一次写操作,初始化 oplog,获得一个同步起始点
关闭 从库 服务,此时 从库 已经有了新的 local.*文件
关闭 主库 服务,并且用 从库 上新的 local.*文件来代替 主库 上的 local.*文件(建议先压缩再COPY)
用-master 选项重启 从库 服务
在启动slave的选项上加一个-fastsync 选项来重启 主库 服务
</pre>





<pre>
referer: http://www.elain.org/?p=627
</pre>

