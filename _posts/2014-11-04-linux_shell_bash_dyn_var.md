---
layout: post
title: "bash如何动态的获取变量名？"
categories: linux 
tags: [bash, shell, 动态变量名]
date: 2014-11-04 17:53:40
---

假设我有一组变量名称为a1,a2,a3，如果我写一个循环来打印变量值，应该怎么写呢？


<pre>
    foo='hello world'
    bar='foo'
    eval echo "\$$bar"
</pre>
