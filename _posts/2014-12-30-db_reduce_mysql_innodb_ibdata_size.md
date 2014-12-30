---
layout: post
title: "缩小mysql数据库的ibdata1文件"
categories: 数据库
tags: [mysql, ibdata1文件]
date: 2014-12-30 16:46:31
---

ibdata1是mysql使用InnoDB引擎的时候需要使用的文件。这个文件有的时候会变得很大，并且在你删除数据的时候，文件也不减小。今天就碰到了一次，导致所有的/var分区都被占用光了。

下面是处理超大ibddata1文件的步骤：

1. 对每张表使用单独的innoDB文件, 修改/etc/my.cnf文件

[mysqld]

innodb_file_per_table

目的很明确，我们可以单独删除每个文件

2. 导出所有的数据，重建数据库，然后恢复数据：

<pre>
# /usr/bin/mysqldump -R -q --all-databases > /temp/all.sql
# service mysqld stop
# rm -fr /var/lib/mysql/*
# /usr/bin/mysql_install_db
# service mysqld restart
# mysql < /tmp/all.sql
</pre>

3. /var/lib/mysql的每个数据库下面，都有会很多的.ibd文件。这些分散的.ibd文件取代了原来的那个ibddata1。

以后删除数据库的时候，直接删除某个数据库的目录就可以了。

————-华丽的分隔符————-

mysql 使用的引擎：

<pre>
mysql> show engines;
+------------+---------+----------------------------------------------------------------+
| Engine     | Support | Comment                                                        |
+------------+---------+----------------------------------------------------------------+
| MyISAM     | DEFAULT | Default engine as of MySQL 3.23 with great performance         |
| MEMORY     | YES     | Hash based, stored in memory, useful for temporary tables      |
| InnoDB     | YES     | Supports transactions, row-level locking, and foreign keys     |
| BerkeleyDB | YES     | Supports transactions and page-level locking                   |
| BLACKHOLE  | NO      | /dev/null storage engine (anything you write to it disappears) |
| EXAMPLE    | NO      | Example storage engine                                         |
| ARCHIVE    | NO      | Archive storage engine                                         |
| CSV        | NO      | CSV storage engine                                             |
| ndbcluster | NO      | Clustered, fault-tolerant, memory-based tables                 |
| FEDERATED  | NO      | Federated MySQL storage engine                                 |
| MRG_MYISAM | YES     | Collection of identicalMyISAM tables                          |
| ISAM       | NO      | Obsolete storage engine                                        |
+------------+---------+----------------------------------------------------------------+

12 rows in set (0.00 sec)
</pre>

For InnoDB tables, OPTIMIZE TABLE is mapped to ALTER TABLE, which rebuilds the table to update index statistics and free unused space in the clustered index.

所以不会直接来减少ibdata的文件尺寸。

减少ibdata的方法如下

- 1. 用mysqldump等工具导出数据

- 2. 停止 mysqld

- 3. 删除ibdata*, ib_logfile* 文件

- 4. 重新启动 mysqld（这时mysqld就会自动创建 idbdata*, ib_logfile* 文件）

- 5. 将到出来的数据导回去，体积才会减小。
