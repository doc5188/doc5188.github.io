---
layout: post
title: "python保留小数点后几位"
categories: python
tags: [python]
date: 2014-10-02 01:45:01
---

<pre>
a,b=1,2
c = '%.5f'%(float(a)/b)
d = round(float(a)/b,5)
print c,d
0.50000 0.5
</pre>

round()在2.x版本里除尽是不能实现的
