---
layout: post
title: "ubuntu 14.04 安装qq"
categories: linux
tags: [linux, ubuntu, wine]
date: 2014-09-15 21:53:00
---

 本人系统为Ubuntu 14.04 LTS 64bit，各种google下成功wine安装了QQ用用

1.首先安装最新版的wine1.6，没记错版本号应该是这个

{% highlight bash %}
# add-apt-repository ppa:ubuntu-wine/ppa
# apt-get update
# apt-get install wine1.6
# apt-get install winetricks
{% endhighlight %}

输入这些命令你要耐心等后。。。。。。。


注意：

64位Ubuntu 可以安装ia32-libs 32位兼容支持库来运行：
{% highlight bash %}
# apt-get install libgtk2.0-0:i386
{% endhighlight %}


2.下载安装包

http://www.longene.org/download/WineQQ2013SP6-20140102-Longene.deb

安装命令


{% highlight bash %}
# dpkg -i WineQQ2013SP6-20140102-Longene.deb
{% endhighlight %}
