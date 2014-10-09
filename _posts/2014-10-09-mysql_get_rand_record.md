---
layout: post
title: "MYSQL随机获得一条数据"
categories: 数据库
tags: [mysql, 随机取数据]
date: 2014-10-09 21:56:37
---

<pre>
select * from `user` where`Sex`='男' order by rand() limit 1
</pre>

我原本是这么写的,

感觉效率不高!,.

是否有更好的办法,提高效率实现随机获取一条数据!

还有就是假如 这随机的我需要满足2个条件,第一是 `Sex`='男' 和`Ctiy`='广州'  这又要怎么写?


====================解答===============================

order by rand()  就是随机排序

order by rand() limit 1  就是随机获取一行数据.

满足2个条件,第一是 `Sex`='男' 和`Ctiy`='广州'

<pre>
select * from `user` where`Sex`='男'  AND  `Ctiy`='广州'    order by rand() limit 1
</pre>
