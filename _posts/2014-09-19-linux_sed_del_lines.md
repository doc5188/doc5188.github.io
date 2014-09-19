---
layout: post
title: "sed删除多行"
categories: linux
tags: [linux, sed]
date: 2014-09-19 14:40:21
---


sed删除以某标记开始，某标记截止的多行内容：
{% highlight bash %}
# sed '/<tag_begin>/, /<tag_end>/d'  <filename>
{% endhighlight %}
