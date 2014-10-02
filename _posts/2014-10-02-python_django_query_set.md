---
layout: post
title: "Django中QuerySet的分片及Count效率思考"
categories: python
tags: [django, python, queryset]
date: 2014-10-02 23:15:49
---

在用Django做数据库查询并且分页的时候会有类似如下的代码：

self._object_list = Cancel_order.objects.filter(state=self._state)[5:10]

这时就有一个疑问：这是利用python的一个语法，对数组进行截取，以便取出其中的5到10各对象。但是这样不是每次都对数据表进行了select all，把结果全部存在QuerySet中，然后再分片？这样在实际应用中根本不可行啊。

查阅 www.djangoproject.com：
<pre>
“QuerySets are lazy

QuerySets are lazy — the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated.”

http://www.djangoproject.com/documentation/db-api/
</pre>

 

http://www.ibm.com/developerworks/cn/linux/l-django/ 这篇文章中有更明确的说明：

QuerySets 是惰性的，这一点非常不错。这意味着只在对数据库进行求值之后才会对它们执行查询，这会比立即执行查询的速度更快。

这种惰性利用了 Python 的分片（slicing）功能。下面的代码并没有先请求所有的记录，然后对所需要的记录进行分片，而是在实际的查询中使用了 5 作为 OFFSET、10 作为 LIMIT，这可以极大地提高性能。


清单 14. Python 分片

{% highlight python %}
>>> from jobs.models import Job
>>> for job in Job.objects.all()[5:15]
...     print job
{% endhighlight %}
      


注意：使用 count 方法可以确定一个 QuerySet 中有多少记录。Python 的 len 方法会进行全面的计算，然后统计那些以记录形式返回的行数，而 count 方法执行的则是真正的 SQL COUNT 操作，其速度更快。我们这样做，数据库管理员会感激我们的。


清单 15. 统计记录数

{% highlight python %}
>>> from jobs.models import Job
>>> print "Count = ", Job.objects.count()       # GOOD!
>>> print "Count = ", len(Job.objects.all())    # BAD!
      
{% endhighlight %}
