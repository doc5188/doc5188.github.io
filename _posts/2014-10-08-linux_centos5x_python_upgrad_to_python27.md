---
layout: post
title: "centos5.x升级python至python2.7"
categories: linux 
tags: [linux, 升级python2.7]
date: 2014-10-08 17:13:49
---

首先到官网下载python2.7.3版本，编译安装
	
{% highlight bash %}
$ wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
$ tar zxvf Python-2.7.3.tgz
$ cd Python-2.7.3
$ ./configure
$ make && make install
{% endhighlight %}

然后备份原来的python，并把python2.7做软连接到新的位置
	
{% highlight bash %}
$ mv /usr/bin/python /usr/bin/python.bak
$ ln -s /usr/local/bin/python2.7 /usr/bin/python
$ python -V
{% endhighlight %}

版本提示为2.7.3

更改yum,使其能正常运行
	
{% highlight bash %}
$ vim /usr/bin/yum
{% endhighlight %}

把#/usr/bin/python改成#/usr/bin/python2.4

这样yum可以正常运行了

* 安装easy_install
	
{% highlight bash %}
$ yum install python-setuptools
{% endhighlight %}


然后安装python-setuptools

到pypi网站下载python-setuptools,版本要和yum的时候版本一致，不然运行的时候会出现：
	
{% highlight bash %}
$ easy_install rsa
Traceback (most recent call last):
  File "/usr/bin/easy_install", line 5, in <module>
    from pkg_resources import load_entry_point
ImportError: No module named pkg_resources
	
$ wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c5.tar.gz
$ tar zxvf setuptools-0.6c5.tar.gz
$ cd setuptools-0.6c5
$ python setup.py install
{% endhighlight %}

安装成功

这样就可以方便的使用easy_install来安装python的库了。
