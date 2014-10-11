---
layout: post
title: "echo 如何不换行"
categories: linux
tags: [shell, echo]
date: 2014-10-11 14:49:45
---

echo 如何不换行


<pre>
echo -e "please input a value:\c"
</pre>
echo的参数中, -e表示开启转义, /c表示不换行,
