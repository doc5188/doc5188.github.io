---
layout: post
title: "PostgreSQL一些简单问题以及解决办法"
categories: 数据库
tags: [postgresql常见问题解决]
date: 2014-10-15 09:06:33
---

* 问题：

org.postgresql.util.PSQLException: Connection refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.

* 解决办法：Edit /var/lib/pgsql/data/postgresql.conf file
<pre>
Change

#listen_addresses = 'localhost'

to
listen_addresses = '*'
</pre>

* 问题：

org.postgresql.util.PSQLException: FATAL: no pg_hba.conf entry for host "<host_ip>", user "fkong", database "fkong", SSL off

* 解决办法：

<pre>
Edit /var/lib/pgsql/data/pg_hba.conf file
Add below line under "# IPv4 local connections:"
"host    all         all         <host_ip>/32         password"
</pre>

* 问题：

org.postgresql.util.PSQLException: FATAL: Ident authentication failed for user "fkong"

* 解决办法：

<pre>
Edit /var/lib/pgsql/data/pg_hba.conf file
Change
"host    all         all         <host_ip>/32         ident"
to
"host    all         all         <host_ip>/32         password"
</pre>
