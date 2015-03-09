---
layout: post
date: 2014-09-21 23:01:38
title: "ubuntu 安装php模块pcntl"
categories: linux
tags: [pcntl, php, ubuntu]
---

环境:

ubuntu 14.04 amd64

php-5.5.9

1. 下载php5源码

{% highlight bash %}
# cd /tmp
# apt-get install dpkg-dev php5-dev
# apt-get source php5
{% endhighlight %}

2. 编译安装

{% highlight bash %}
# cd php5-5.5.9+dfsg/ext/pcntl/
# phpize #若没有这个命令需要安装php5-dev
# ./configure && make && make install
{% endhighlight %}

3. 启用模块

{% highlight bash %}
vi /etc/php5/cli/conf.d/pcntl.ini
extension=pcntl.so
{% endhighlight %}
