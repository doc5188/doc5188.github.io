---
layout: post
title: "coreseek索引更新机制"
categories: linux
tags: [coreseek]
date: 2014-11-23 23:35:03
---

* 1、首先是建立索引

/usr/local/coreseek/bin/indexer --all --config /data/coreseek/conf/post.conf

* 2、启动守护进程

/usr/local/coreseek/bin/searchd --config /data/coreseek/conf/post.conf

* 3、+记录

* 4、更新增量索引，这个写在脚本里，因为需要每分钟更新。

文件名：/data/coreseek/sh/build_delta_index.sh

内容：/usr/local/coreseek/bin/indexer post_delta --config /data/coreseek/conf/post.conf --rotate

* 5、合并索引，这个也要写在脚本里，每天合并一次

文件名：/data/coreseek/sh/build_main_index.sh

内容：/usr/local/coreseek/bin/indexer --merge post_main post_delta --rotate --config /data/coreseek/conf/post.conf  //合并索引

/usr/local/mysql/bin/mysql -hhostname -uusername -ppassword -Ddbname -e 'REPLACE INTO sph_counter SELECT 1, MAX(PostId) FROM Post' //更改maxid

/usr/local/coreseek/bin/indexer post_delta --config /data/coreseek/conf/post.conf --rotate >>/var/log/coreseek/deltaindexlog //重建增量索引

再贴下crontab规则

<pre>
*/1 * * * * /bin/sh /data/coreseek/sh/build_delta_index.sh
30 1 * * * /bin/sh /data/coreseek/sh/build_main_index.sh
</pre>

***************************************************************************
 
在实际应用中往往有这么一种情况，数据库数据很大，比如我们的歌曲表，如果我们每次都去更新整个表的索引，对系统得开销将非常大，显然这是不合适，这时我们会发现，每天我们需要更新的数据相比较而言较少，在这种情况下我们就需要使用“主索引+增量索引”的模式来实现实时更新的功能。

这个模式实现的基本原理是设置两个数据源和两个索引，为那些基本不更新的数据建立主索引，而对于那些新增的数据建立增量索引。主索引的更新频率我们可以设置的长一些(可以设置在每天的午夜进行更新)，而增量索引的更新频率，我们可以将时间设置的很短(几分钟左右)，这样在用户搜索的时候，我们可以同时查询这两个索引的数据。

下面，我们通过一个简单的例子来描述一下怎样实现这种模式

以sphinx.conf中默认的数据为例:

1.先在mysql中插入一个计数表和两个索引表

<pre>
CREATE TABLE sph_counter(
counter_id INTEGER PRIMARY KEY NOT NULL,
max_doc_id INTEGER NOT NULL
);

//主索引使用(确认之前是否已经建立过该表，如果已经建立，这里就不需要重新建了)

CREATE TABLE `sphinx` (  
`id` int(11) NOT NULL,  
`weight` int(11) NOT NULL,  
`query` varchar(255) NOT NULL,  
`CATALOGID` INT NOT NULL,  
`EDITUSERID` INT NOT NULL,  
`HITS` INT NULL,  
`ADDTIME` INT NOT NULL,   KEY
`Query` (`Query`)
) ENGINE=SPHINX DEFAULT CHARSET=utf8 CONNECTION=‘sphinx://localhost:3312/test1‘
//增量索引使用
CREATE TABLE `sphinx1` (
`id` int(11) NOT NULL,
`weight` int(11) NOT NULL,
`query` varchar(255) NOT NULL,
`CATALOGID` INT NOT NULL,
`EDITUSERID` INT NOT NULL,
`HITS` INT NULL,
`ADDTIME` INT NOT NULL, KEY
`Query` (`Query`)
)ENGINE=SPHINX DEFAULT CHARSET=utf8 CONNECTION=’sphinx://localhost:3312/ test1stemmed ‘

</pre>

* 2.修改sphinx.conf

<pre>
source src1
{
sql_query_pre = SET NAMES utf8
sql_query_pre = SET SESSION query_cache_type=OFF
sql_query_pre = REPLACE INTO sph_counter SELECT 1, MAX(id) FROM documents
sql_query = SELECT id, group_id, UNIX_TIMESTAMP(date_added) AS date_added, title, content FROM documents \
WHERE id<=( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )
… //其他可以默认
}
// 注意：sql_query_pre的个数需和src1对应，否则可能搜索不出相应结果
source src1throttled : src1
{
sql_ranged_throttle = 100
sql_query_pre = SET NAMES utf8
sql_query_pre = SET SESSION query_cache_type=OFF
sql_query_pre =
   sql_query = SELECT id, group_id, UNIX_TIMESTAMP(date_added) AS date_added, title, content FROM documents \
WHERE id>( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )
}
index test1 //主索引
{
source = src1
…
}
index test1stemmed : test1 //增量索引
{
source = src1throttled
…
}

</pre>

* 3.重建索引

<pre>
/usr/local/sphinx/bin/searchd –stop
/usr/local/sphinx/bin/indexer –config /usr/local/sphinx/etc/sphinx.conf –all
/usr/local/sphinx/bin/searchd –config /usr/local/sphinx/etc/sphinx.conf

</pre>
插入测试数据

<pre>
INSERT INTO `test`.`documents` (
`id` ,
`group_id` ,
`group_id2` ,
`date_added` ,
`title` ,
`content`
)
VALUES (
NULL , ‘3‘, ‘11‘, NOW( ) , ‘索引合并‘, ‘合并两个已有的索引比重新对所有数据做索引更有效率，而且有时候必须这样做（例如在“ 主索引＋增量索引”分区模式中应合并主索引和增量索引，而不是简单地重新索引“主索引对应的数据）。因此indexer有这个选项。合并索引一般比重新索引快，但在大型索引上仍然不是一蹴而就。基本上，待合并的两个索引都会被读入内存一次，而合并后的内容需要写入磁盘一次。例如，合并100GB和1GB的两个索引将导致202GB的IO操作（但很可能还是比重新索引少）‘
);

</pre>

执行

<pre>
SELECT doc . *
FROM documents doc
JOIN sphinx ON ( doc.id = sphinx.id )
WHERE query = ‘索引‘

</pre>

你会发现你刚添加的数据没有被检索出来

然后执行：

SELECT doc.* FROM documents doc join sphinx1 on (doc.id=sphinx1.id) where query=‘索引‘

你会发现数据是空的，这时我们就需要来更新增量索引了。

通过执行：

/usr/local/sphinx/bin/indexer –rotate –config /usr/local/sphinx/etc/sphinx.conf test1stemmed

命令来更新增量索引(正式使用时，我们可以将该命令配置到系统计划任务中，每隔几分钟执行一次)

–rotate: 该参数可以使我们在不需要停止searchd的情况下，直接加载索引

执行完命令该命令后，我们再来查看一下增量索引的数据

SELECT doc.* FROM documents doc join sphinx1 on (doc.id=sphinx1.id) where query=‘索引‘

你会发现新添加的数据被检索出来的。

主索引的更新：

<pre>
/usr/local/sphinx/bin/indexer –rotate –config /usr/local/sphinx/etc/sphinx.conf test1
collected 997 docs, 1.4 MB
sorted 0.3 Mhits, 100.0% done
total 997 docs, 1430054 bytes
total 1.428 sec, 1001459.38 bytes/sec, 698.19 docs/sec

</pre>

(我们可以设置成每天的午夜执行)

只有在更新了主索引后，结果才会被更新

SELECT doc.* FROM documents doc join sphinx on (doc.id=sphinx.id) where query=‘索引‘

我们也可以通过合并索引的方式使主索引的数据保持更新

/usr/local/sphinx/bin/indexer –merge test1 test1stemmed –rotate

可以将增量索引test1stemmed合并到主索引test1中去

为创建2个shell脚本，一个用来创建主索引、一个用来创建增量索引（此步可以省略）

1.创建主索引脚本build_main_index.sh

<pre>
#!/bin/sh
#/usr/local/sphinx/bin/searchd –stop
/usr/local/sphinx/bin/indexer test1 –config /usr/local/sphinx/etc/sphinx.conf >> /var/log/sphinx/mainindexlog
#/usr/local/sphinx/bin/searchd
</pre>

2.创建增量索引脚本build_delta_index.sh

<pre>
#!/bin/sh
#/usr/local/sphinx/bin/searchd –stop
/usr/local/sphinx/bin/indexer test1stemmed –config /usr/local/sphinx/etc/sphinx.conf –rotate>> /var/log/sphinx/deltaindexlog
/usr/local/sphinx/bin/indexer –merge test1 test1stemmed –config /usr/local/sphinx/etc/sphinx.conf –rotate >> /var/log/sphinx/deltaindexlog
#/usr/local/sphinx/bin/searchd

</pre>
每隔5分钟进行索引增量合并，每天2：30重建索引
<pre>
*/5 * * * * /bin/sh /opt/shell/build_delta_index.sh > /dev/null 2>&1
30 2* * * /bin/sh /opt/shell/build_main_index.sh > /dev/null 2>&1
</pre>
每周一至周六上早6点增量合并，同日重建索引

<pre>
1 6 * * 1-6 /bin/sh /opt/shell/build_delta_index.sh > /dev/null 2>&1
1 6 * * 7 /bin/sh /opt/shell/build_main_index.sh > /dev/null 2>&1

</pre>
