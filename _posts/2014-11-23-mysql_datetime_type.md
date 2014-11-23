---
layout: post
title: "MySQL5日期类型DATETIME和TIMESTAMP相关问题详解"
categories: 数据库
tags: [mysql5, datetime, timestamp]
date: 2014-11-23 10:58:15
---

MySQL5日期类型DATETIME和TIMESTAMP相关问题详解<br>
 <br>
MySQL5的日期类型有三种：DATETIME、DATE和TIMESTAMP，除了DATE用来表示一个不带时分秒的是日期，另外两个都带时分秒。TIMESTAMP还可以精确到毫秒。<br>
 <br>
其次还有个共性，就是他们的格式“不严格”，很自由，一般你认为对的格式都可以正确插入到数据库中。<br>
 <br>
这里主要解决带时分秒日期的一些常见问题。<br>
 <br>
一、IMESTAMP<br>
 <br>
1、TIMESTAMP列必须有默认值，默认值可以为“0000-00-00 00:00:00”，但不能为null。<br>
2、TIMESTAMP列不可以设置值，只能由数据库自动去修改。<br>
3、一个表可以存在多个TIMESTAMP列，但只有一个列会根据数据更新而改变为数据库系统当前值。因此，一个表中有多个TIMESTAMP列是没有意义，实际上一个表只设定一个TIMESTAMP列。<br>
4、TIMESTAMP列的默认值是CURRENT_TIMESTAMP常量值。当纪录数据发生变化的时候，TIMESTAMP列会自动将其值设定为CURRENT_TIMESTAMP。<br>
5、TIMESTAMP列创建后的格式是：<br>
`a` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,<br>
这个语句含义，a字段的默认值是CURRENT_TIMESTAMP，当纪录更新时候，自动将a字段的值设置为CURRENT_TIMESTAMP。<br>
6、另外，下面的定义从语法角度是对的，但是没有意义，因为该字段的值不可更改，永远只能为默认值。<br>
`b` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',<br>
 <br>
 <br>
二、DATETIME<br>
 <br>
1、DATETIME列可以设置为多个，默认可为null，可以手动设置其值。<br>
2、DATETIME列不可设定默认值，这是很多人煞费苦心研究的成果，呵呵！<br>
3、DATETIME列可以变相的设定默认值，比如通过触发器、或者在插入数据时候，将DATETIME字段值设置为now()，这样可以做到了，尤其是后者，在程序开发中常常用到。<br>
 <br>
一般建表时候，创建时间用datetime，更新时间用timestamp。<br>
CREATE TABLE user (<br>
 &nbsp; id bigint(20) NOT NULL AUTO_INCREMENT,<br>
 &nbsp; name varchar(20) CHARACTER SET gbk NOT NULL,<br>
 &nbsp; sex tinyint(1) DEFAULT '1',<br>
 &nbsp; state smallint(2) DEFAULT '1',<br>
 &nbsp; createtime datetime NOT NULL,<br>
 &nbsp; updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,<br>
 &nbsp; PRIMARY KEY (id)<br>
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1<br>
 <br>
三、日期最大值范围的问题<br>
 <br>
日期最大范围的问题不是绝对的，很多人制定一个说不能查过20XX年，这是扯蛋，根本没这回事。日期的范围等问题与MySQL的运行模式有关。当然这个范围很宽广，足够祖宗十八代用了，不用担心这问题了。<br>
 <br>
相反，要注意的问题是，编程语言对日期范围的限制，不同的语言，有不同的限制，这里不做讨论了。<br>
 <br>
四、日期格式转换<br>
 <br>
1、字符串转日期<br>
select STR_TO_DATE('2010-03-03 16:41:16', '%Y-%m-%d %H:%i:%s')<br>
 <br>
2、日期转字符串<br>
select DATE_FORMAT('2010-03-03 16:41:16', '%Y-%m-%d %H:%i:%s')<br>
 <br>
五、日期的中年月日时分秒星期月份等获取方法<br>
 <br>
select TIMESTAMP('2010-03-03 16:41:16');<br>
<br>
select DATE('2010-03-03 16:41:16');<br>
<br>
select YEAR('2010-03-03 16:41:16');<br>
<br>
select MONTH('2010-03-03 16:41:16');<br>
<br>
select DAY('2010-03-03 16:41:16');<br>
<br>
select TIME('2010-03-03 16:41:16');<br>
<br>
select CURTIME();<br>
<br>
select CURDATE();<br>
<br>
select CURRENT_DATE;<br>
<br>
select CURRENT_TIME;<br>
<br>
select CURRENT_TIMESTAMP;<br>
 <br>
方式很多，这里简单列举一二。<br>
 <br>
六、日期的算术运算<br>
 <br>
相关的函数很多很多，用法也很简单，一看就会，建议查看MySQL参考手册。<br>
mysql&gt; SELECT DATE_ADD('1999-01-01', INTERVAL 1 DAY);<br>
<br>
 &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; -&gt; '1999-01-02'<br>
<br>
mysql&gt; SELECT DATE_ADD('1999-01-01', INTERVAL 1 HOUR);<br>
<br>
 &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; -&gt; '1999-01-01 01:00:00'<br>
<br>
mysql&gt; SELECT DATE_ADD('1998-01-30', INTERVAL 1 MONTH);<br>
<br>
 &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; -&gt; '1998-02-28'<br>
 <br>
七、日期的大小比较<br>
 <br>
拿着日当数字，拿着字符串当日期，呵呵，很简单的。<br>
 &nbsp;&nbsp;&nbsp;and update_time &gt; '2010-03-02 16:48:41'<br>
 &nbsp;&nbsp;&nbsp;and update_time &lt;= '2010-03-03 16:51:58'<br>
 <br>
搞明白这些，参考MySQL指南，日期问题轻松搞定。
