---
layout: post
title: "安装 psycopg2 的问题：pg_config executable not found"
categories: linux 
tags: [python-psycopg2, postgresql]
date: 2014-10-15 08:55:48
---

使用 pip install psycopg2，特么报错，Error: pg_config executable not found。

网上搜索下，说需要安装 pg 和 py 的驱动：
Debian系:

<pre>
    apt-get install libpq-dev python-dev
</pre>

RedHat系：

<pre>
    yum install libpqxx-devel python-devel
</pre>

安装完成，再使用 pip install psycopg2，OK，一切顺利。

有的时候 pip 还经常出现 timeout,不省心啊！可以下载后安装：

<pre>
$ wget https://pypi.python.org/packages/source/p/psycopg2/psycopg2-2.5.2.tar.gz
$ tar -zxvf psycopg2-2.5.2.tar.gz
$ cd psycopg2-2.5.2/
$ ~/venv/bin/python setup.py build #我使用的是虚拟环境
$ ~/venv/bin/python setup.py install
</pre>
