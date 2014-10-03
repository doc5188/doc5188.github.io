---
layout: post
title: "mysql导入导出数据中文乱码解决方法小结"
categories: 数据库
tags: [mysql, 数据库乱码]
date: 2014-10-03 19:48:56
---

本文章总结了mysql导入导出数据中文乱码解决方法，出现中文乱码一般情况是导入导入时编码的设置问题，我们只要把编码调整一致即可解决此方法，下面是搜索到的一些方法总结,方便需要的朋友
linux系统中

linux默认的是utf8编码，而windows是gbk编码，所以会出现上面的乱码问题。

解决mysql导入导出数据乱码问题

首先要做的是要确定你导出数据的编码格式，使用mysqldump的时候需要加上--default-character-set=utf8，

例如下面的代码：
{% highlight bash %}
# mysqldump -uroot -p --default-character-set=utf8 dbname tablename > bak.sql
{% endhighlight %}



那么导入数据的时候也要使用--default-character-set=utf8：

{% highlight bash %}
# mysql -uroot -p --default-character-set=utf8 dbname < bak.sql
{% endhighlight %}


这样统一编码就解决了mysql数据迁移中的乱码问题了


我使用windows作为导出数据源，并导入 freebsd环境下的mysql库

* 解决方法：

导出数据

一、首先在windows平台下mysql用作导出数据库源。查看字符编码的系统变量：

{% highlight bash %}

mysql> show variables like ‘%char%';
+————————–+—————————-+
| Variable_name | Value |
+————————–+—————————-+
| character_set_client | latin1 |
| character_set_connection | latin1 |
| character_set_database | latin1 |
| character_set_filesystem | binary |
| character_set_results | latin1 |
| character_set_server | gbk |
| character_set_system | utf8 |
| character_sets_dir | D:mysqlsharecharsets |

+————————–+—————————-+
{% endhighlight %}


查看character_set_database，这里是latin1，latin1是装不了多字节字符集的

二、在windows下设置系统变量为utf8

{% highlight bash %}
mysql>set character_set_database=utf8; ##设置默认的字符集为utf8
{% endhighlight %}


三、导出数据

{% highlight bash %}
mysql> select * from table into outfile ‘c:table.txt' where +条件
{% endhighlight %}


这时导出了我想要的部分数据，并以txt文件存在 table.txt中。

导入数据

在freebsd平台下

一、同样设置字符编码的系统变量

{% highlight bash %}

mysql> show variables like ‘%char%';

+————————–+—————————-+
| Variable_name | Value |
+————————–+—————————-+
| character_set_client | latin1 |
| character_set_connection | latin1 |
| character_set_database | latin1 |
| character_set_filesystem | binary |
| character_set_results | latin1 |
| character_set_server | gbk |
| character_set_system | utf8 |

+————————–+—————————-+

mysql>set character_set_database=utf8; ##设置默认的字符集为utf8
{% endhighlight %}


二、转载数据

{% highlight bash %}
mysql>load data local infile ‘/home/table.txt' into table `table`;
{% endhighlight %}

至此、条件数据完整导入导出，并处理了乱码的情况。

总之，两台mysql服务器导入导出时，一定要确保两台服务器的character_set_database参数相同，这样才能防止一些 乱码的情况。当然我们还可以使用其他字符集，如gbk来进行调整。视情况操作了


* 解决方法三

乱码解决方法

导入数据后，在命令行查看发现中文乱码

使用以下命令查看系统字符集

{% highlight bash %}
show variables like 'char%';
{% endhighlight %}


如果不是GBK或UTF8，则停止mysql服务，然后到安装目录修改my.ini文件，

将文件中下面的变量改成如下，如果没有这个变量则增加这些变量

{% highlight bash %}

[mysql]
default-character-set=gbk

[mysqld]
character-set-server=utf8
{% endhighlight %}


重新启动服务，重新导入数据，如果还乱码，

最后得出经验时只要把导入与导出编码统一一下就没问题了。 
