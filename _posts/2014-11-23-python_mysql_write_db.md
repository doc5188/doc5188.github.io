---
layout: post
title: "python MySQLdb中转义字符串的问题"
categories: python
tags: [python,]
date: 2014-11-23 14:58:16
---


<pre>
#-*-coding: utf8 -*-
from connectdb import connectDatabase; #connectDatabase是我自己定义的一个连接数据库的函数
import MySQLdb;
def escape():
    cnn = connectDatabase();
    cursor = cnn.cursor();
    name = "\\"; 
    name2 = "\""
    
    #name =  MySQLdb.escape_string(name);
    #name2 = MySQLdb.escape_string(name2);
    print name,name2;
    queryli = [(12,name),(12,name2)]
    print queryli;
    #cursor.executemany("insert into resource(cid,name) values(%s, %s)",queryli);
    cursor.execute("insert into resource(cid,name) values(%s, %s)" , (12,name) );
    cursor.close();
    
    cnn.commit();
    cnn.close();

if __name__ == "__main__":
    escape();
</pre>

<div><font COLOR="#E50000">注意：
cursor.execute()可以接受一个参数，也可以接受两个参数：</FONT></DIV>
<div><font COLOR="#E50000">(1) cursor.execute("insert into
resource(cid,name) values(%s, %s)" <b>,</B> (12,name)
);</FONT></DIV>
<div><font COLOR="#E50000">&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>这种格式是接受<b>两个参数</B>，MySQLdb会自动替你对字符串进行转义和加引号，不必再自己进行转义，执行完
&nbsp;<wbr> &nbsp;<wbr> 此语句之后，resource表中多了一条记录： 12
&nbsp;<wbr> \</FONT></DIV>
<div><font COLOR="#E50000">(2)&nbsp;<wbr>cursor.execute("insert into
resource(cid,name) values(%s, %s)" <b>%</B> (12,name)
);</FONT></DIV>
<div><font COLOR="#E50000">&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>这种格式是利用python的字符串格式化自己生成一个query，也就是传给execute<b>一个参数</B>，此时必须自己对
&nbsp;<wbr> &nbsp;<wbr>
字符串转义和增加引号，即上边的语句是错误的，应该修改为：</FONT></DIV>
<div><font COLOR="#E50000">&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>name = MySQLdb.escape_string(name);</FONT></DIV>
<div><font COLOR="#E50000">&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>cursor.execute("insert into resource(cid,name)
values(%s,
<b>'</B>%s<b>'</B>)"&nbsp;<wbr><b>%</B>&nbsp;<wbr>(12,name)
);</FONT></DIV>
<div><font COLOR="#E50000">&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>这样插入的记录才和(1)一样：12 &nbsp;<wbr>
\</FONT></DIV>
<div><br /></DIV>
<div>&nbsp;<wbr>&nbsp;<wbr> &nbsp;<wbr></DIV>
</DIV>	
