---
layout: post
title: "mysql 添加索引 mysql 如何创建索引"
categories: 数据库
tags: [mysql, 数据库索引]
date: 2014-12-29 23:55:22
---

1.添加PRIMARY KEY（主键索引） 
<pre>
mysql>ALTER TABLE `table_name` ADD PRIMARY KEY ( `column` ) 
</pre>

2.添加UNIQUE(唯一索引) 

<pre>
mysql>ALTER TABLE `table_name` ADD UNIQUE ( `column` ) 
</pre>

3.添加INDEX(普通索引) 

<pre>
mysql>ALTER TABLE `table_name` ADD INDEX index_name ( `column` ) 
</pre>

4.添加FULLTEXT(全文索引) 
<pre>
mysql>ALTER TABLE `table_name` ADD FULLTEXT ( `column`) 
</pre>

5.添加多列索引 

<pre>
mysql>ALTER TABLE `table_name` ADD INDEX index_name ( `column1`, `column2`, `column3` )
</pre>
