---
layout: post
title: "mysql多表查询 查询A表中id不存在B表中id的结果"
categories: 数据库
tags: [mysql, mysql多表查询, 多表查询]
date: 2014-12-18 17:51:12
---

select * from a where id not in (select id from b)
