---
layout: post
title: "MySQL修改字段默认值"
categories: 数据库
tags: [mysql]
date: 2014-12-25 09:09:49
---

环境


MySQL 5.1 + 命令行工具


问题


MySQL修改字段默认值


解决


alter table topic alter column cateId set default '2';


语法


alter table表名alter column字段名drop default; (若本身存在默认值，则先删除)


alter table 表名 alter column 字段名 set default 默认值;(若本身不存在则可以直接设定)
