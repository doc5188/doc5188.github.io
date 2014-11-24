---
layout: post
title: "coreseek实现字段排序"
categories: linux
tags: [linux, coreseek]
date: 2014-11-24 17:47:55
---

* 0. 修改config

<pre>
sql_attr_uint            = pt_order
sql_attr_timestamp        = stime
</pre>


* 1. stop searchd

* 2. indexer

* 3. start searchd

* 4. $sl->SetSortMode(SPH_SORT_EXTENDED,'pt_order DESC');
