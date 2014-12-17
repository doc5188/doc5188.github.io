---
layout: post
title: "UPDATE INNER JOIN 在 MYSQL 怎么用"
categories: 数据库
tags: [mysql]
date: 2014-12-17 12:41:58
---

update A,B set A.A2 = B.B2 where A.A1 = B.B1 and B.B2 = "XXX"


<a href='http://www.juhelian.com'>聚合链</a>后台修改数据库的语句

update file_info, hash_info set file_info.hash=hash_info.id where file_info.hash=hash_info.hash;


ALTER TABLE file_info MODIFY COLUMN hash bigint;
