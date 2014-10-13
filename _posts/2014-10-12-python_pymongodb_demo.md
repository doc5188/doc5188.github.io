---
layout: post
title: "pymongo 使用小结"
categories: python
tags: [pymongo]
date: 2014-10-12 23:58:11
---

pymongo 使用小结

1、安装pymongo

{% highlight bash %}
# easy_install pymongo
{% endhighlight %}

2、连接mongodb

{% highlight bash %}
>>> import pymongo
>>> conn = pymongo.Connection('localhost', 27017)
{% endhighlight %}

3、获取数据库列表

{% highlight bash %}
>>> conn.database_names()
[u'test1', u'test2', u'admin', u'local']
{% endhighlight %}

4、连接数据库

{% highlight bash %}
>>> db = conn.test1
或
>>> db = conn['test1']
{% endhighlight %}

5、权限验证

{% highlight bash %}
>>> db.authenticate('username', 'password')
True
{% endhighlight %}

6、获取聚集列表 (聚集的概念类似于关系型数据库中的表)

{% highlight bash %}
>>> db.collection_names()
[u'account', u'role', u'item', u'online']
{% endhighlight %}

7、连接聚集

{% highlight bash %}
>>> account = db.account
或
>>> account = db['account']
{% endhighlight %}

8、查看聚集的一条记录

{% highlight bash %}
>>> account.find_one()
{% endhighlight %}

9、查看聚集的所有key (类似于关系型数据库中的字段)

{% highlight bash %}
>>> account.find_one().keys()
{% endhighlight %}

10、查看聚集的所有记录

{% highlight bash %}
>>> for i in account.find():
... print i
{% endhighlight %}

11、查看记录总数

{% highlight bash %}
>>> account.find().count()
{% endhighlight %}

12、根据条件查询多条记录

{% highlight bash %}
>>> for i in account.find({"name": "xxx"}):
... print i
{% endhighlight %}

13、对查询结果进行排序 (默认升序ASCENDING)

{% highlight bash %}
>>> account.find().sort("name", pymongo.ASCENDING)
>>> account.find().sort([("name", pymongo.ASCENDING), ("active_time", pymongo.DESCENDING)])
{% endhighlight %}

14、新增记录

{% highlight bash %}
>>> account.insert({"name": "mike", "active_time": "20130408"})
{% endhighlight %}

15、更新记录

{% highlight bash %}
>>> account.update({"name": "mike"}, {"$set": {"active_time": "20130408120000"}})
{% endhighlight %}

16、删除记录 (不带条件表示全部删除)

{% highlight bash %}
>>> account.remove({"name": "mike"})
{% endhighlight %}

