---
layout: post
title: "awk怎么输出1到n列"
categories: linux
tags: [awk]
date: 2014-10-13 12:43:24
---

比如一个文件有m列，但我只想输出n列，n <= m，怎么弄？


{% highlight bash %}
##比如输出2到n列
# awk -F: 'BEGIN{n=4}{for(i=2;i<n;i++)printf $i":";print $i}' /etc/passwd
##输出所有列
# awk -F: '{for(i=1;i<=NF;i++)print $i}' /etc/passwd

{% endhighlight %}
