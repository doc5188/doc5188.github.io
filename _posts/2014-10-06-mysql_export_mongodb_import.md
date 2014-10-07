---
layout: post
title: "将mysql数据导入mongodb"
categories: 数据库
tags: [mysql, mongodb, mongodbimport]
date: 2014-10-06 17:25:41
---

1、进入Mysql，将数据导成CVS

{% highlight bash %}
select * from test_info into outfile '/tmp/test.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
{% endhighlight %}

2、将CVS导入到Mongodb中
{% highlight bash %}
# mongoimport -h "127.0.0.1:16688" -u"username" -p "password" -d "hdms" -c "MS_Updatelog" -f "Up_id,Up_content,Up_Updatetime" -type=csv -file=/tmp/test/csv
{% endhighlight %}
