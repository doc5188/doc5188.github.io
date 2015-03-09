---
layout: post
title: "Ubuntu 12.04 Use Jekyll"
date: 2014-08-11 10:59:11
categories: Linux
---

1. 升级ruby > 1.9.2

{% highlight bash %}
$ sudo apt-get remove ruby1.8
$ sudo apt-get install ruby1.9.3
{% endhighlight bash %}

2.安装jekyll

{% highlight bash %}
	$ sudo gem install jekyll
{% endhighlight bash %}

3. 创建jekyll项目

{% highlight bash %}
	$ jekyll new blog
	$ cd blog
{% endhighlight bash %}
4. 浏览项目

{% highlight bash %}
	$ jekyll server
{% endhighlight bash %}
