---
layout: post
title: "mysql 中sql 语句查询今天、昨天、7天、近30天、本月、上一月 数据"
categories: 数据库
tags: [mysql, mysql查询历史数据]
date: 2014-12-30 14:30:13
---

今天

<pre>
select * from 表名 where to_days(时间字段名) = to_days(now());
</pre>

昨天

<pre>
SELECT * FROM 表名 WHERE TO_DAYS( NOW( ) ) - TO_DAYS( 时间字段名) <= 1
</pre>

7天

<pre>
SELECT * FROM 表名 where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(时间字段名)
</pre>

近30天

<pre>
SELECT * FROM 表名 where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(时间字段名)
</pre>

本月

<pre>
SELECT * FROM 表名 WHERE DATE_FORMAT( 时间字段名, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )
</pre>

上一月

<pre>
SELECT * FROM 表名 WHERE PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( 时间字段名, '%Y%m' ) ) =1 
</pre>


<pre>
referer:http://blog.csdn.net/ve_love/article/details/19685399
</pre>
