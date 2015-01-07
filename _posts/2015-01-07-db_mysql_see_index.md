---
layout: post
title: "mysql 查看索引"
categories: 数据库 
tags: [mysql, 查看索引]
date: 2015-01-07 09:49:54
---

查看索引
<pre>
mysql> show index from tblname;
mysql> show keys from tblname;

· Table
表的名称。
· Non_unique
如果索引不能包括重复词，则为0。如果可以，则为1。
· Key_name
索引的名称。
· Seq_in_index
索引中的列序列号，从1开始。
· Column_name
列名称。
· Collation
列以什么方式存储在索引中。在MySQL中，有值‘A’（升序）或NULL（无分类）。
· Cardinality
索引中唯一值的数目的估计值。通过运行ANALYZE TABLE或myisamchk -a可以更新。基数根据被存储为整数的统计数据来计数，所以即使对于小型表，该值也没有必要是精确的。基数越大，当进行联合时，MySQL使用该索引的机 会就越大。
· Sub_part
如果列只是被部分地编入索引，则为被编入索引的字符的数目。如果整列被编入索引，则为NULL。
· Packed
指示关键字如何被压缩。如果没有被压缩，则为NULL。
· Null
如果列含有NULL，则含有YES。如果没有，则该列含有NO。
· Index_type
用过的索引方法（BTREE, FULLTEXT, HASH, RTREE）。
· Comment
</pre>
