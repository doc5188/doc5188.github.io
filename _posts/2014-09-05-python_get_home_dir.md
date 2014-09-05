---
layout: post
title: "Python 获取用户主目录$HOME"
date: 2014-09-05 13:02:12
categories: python
tags: [linux, python]
---

{% highlight python %}
import os
usr_home = os.path.expanduser(’~')
{% endhighlight %}

