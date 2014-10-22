---
layout: post
title: "为什么mongodb插入数据经常出现时间相同的情况"
categories: 数据库
tags: [mongodb]
date: 2014-10-22 11:21:38
---

用 mongoengine 建立 collection，其中时间是这么定义的

{% highlight bash %}
from mongoengine import Document, DateTimeField
import datetime

class Post(Document):
    created = DateTimeField(default=datetime.datetime.utcnow())
{% endhighlight %}

在插入数据的过程中，老是出现插入时间相同的情况，下面这几条都是我手动插入的数据，但是发现有些十句的时间居然是一模一样的，下面是读出来的数据，可以看到好几条时间一样的，而这几条数据中间都间隔了好几分钟的：

<pre>
50f2bf6c674d9a1136de4964 • 2013-01-13 14:06:33.717000 • root • 0

50f2bf9c674d9a1136de4965 • 2013-01-13 14:06:33.717000 • root • 0

50f2bfc6674d9a1136de4966 • 2013-01-13 14:06:33.717000 • root • 0

50f2c01f674d9a1136de4967 • 2013-01-13 14:06:33.717000 • admin • 0

50f2c1b8674d9a1136de4968 • 2013-01-13 14:06:33.717000 • admin • 0

50f2b909674d9a1118d57170 • 2013-01-13 13:37:03.176000 • root • 0

50f2b681674d9a11023af511 • 2013-01-13 13:28:07.676000 • root • 0
</pre>

==========================解决方法：=====================

将 datetime.datetime.utcnow() 改为 datetime.datetime.utcnow 即可，看清这里不要有括号
