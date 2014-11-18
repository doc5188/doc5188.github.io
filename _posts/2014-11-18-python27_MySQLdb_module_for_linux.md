---
layout: post
title: "python2.7之MySQLdb模块 for linux安装"
categories: python
tags: [python27, MySQLdb模块安装]
date: 2014-11-18 14:53:01
---

<span style="font-size: 14px;">python2.7之MySQLdb模块 for linux安装</span><br>
<br>
<span style="font-size: 14px;">1.下载:MySQL-python</span><br>
<span style="font-size: 14px;">http://sourceforge.net/projects/mysql-python/files/mysql-python-test/1.2.3b1/MySQL-python-1.2.3b1.tar.gz/download</span><br>
<span style="font-size: 14px;">tar -zxf MySQL-python-1.2.3b1.tar.gz</span><br>
<span style="font-size: 14px;">cd MySQL-python-1.2.3b1</span><br>
<span style="font-size: 14px;">python setup.py build</span><br>
<span style="font-size: 14px;">==&gt;ImportError: No module named setuptools</span><br>
<br>
<span style="font-size: 14px;">2.下载setuptools</span><br>
<span style="font-size: 14px;">http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c8.tar.gz</span><br>
<span style="font-size: 14px;">tar -zxf setuptools-0.6c8.tar.gz</span><br>
<span style="font-size: 14px;">cd setuptools-0.6c8</span><br>
<span style="font-size: 14px;">python setup.py build</span><br>
<span style="font-size: 14px;">python setup.py install</span><br>
<br>
<span style="font-size: 14px;">3.回到MySQL-python-1.2.3b目录</span><br>
<span style="font-size: 14px;">cd MySQL-python-1.2.3b1</span><br>
<span style="font-size: 14px;">在运行时python setup.py build &amp;&amp; python setup.py install没有如下错误:</span><br>
<br>
<span style="font-size: 14px;">有类似错误，处理方式如下:</span><br>
<span style="font-size: 14px;">python setup.py build #若,报错:mysql_config not found</span><br>
<span style="font-size: 14px;">找出mysql 安装目录:/opt/mysql/</span><br>
<span style="font-size: 14px;">vi MySQL-python-1.2.3b1/setup_posix.py</span><br>
<span style="font-size: 14px;">行 &nbsp; &nbsp; 26 #mysql_config.path = "mysql_config"</span><br>
<span style="font-size: 14px;">改成如下: </span><br>
<span style="font-size: 14px;">行 &nbsp; &nbsp; 27 mysql_config.path = "/opt/mysql/bin/mysql_config"</span><br>
<br>
<span style="font-size: 14px;">再次运行&nbsp;</span><br>
<span style="font-size: 14px;">python setup.py build #报错:/usr/bin/ld:cannot find -lmysqlclient_r</span><br>
<span style="font-size: 14px;">root下:</span><br>
<span style="font-size: 14px;">echo "/opt/mysql/lib/mysql" &gt;&gt; /etc/ld.so.conf #请主意这个/etc/ld.so.conf，</span><br>
<span style="font-size: 14px;">这个是ld的默认配置文件，视系统不同而不同。 /opt/mysql/lib/mysql与mysql安装目录相关。</span><br>
<span style="line-height: 1.5;"><br>
<span style="font-size: 14px;"></span><span style="font-size: 14px;">刷新ld配置文件让其生效,使用:ldconfig</span></span><br>
<br>
<span style="font-size: 14px;">接着运行 python setup.py install</span><br>
<span style="line-height: 1.5;"><br>
<span style="font-size: 14px;"></span><span style="font-size: 14px;">检验是否已经安装成功MySQLdb时,提示如下错误:</span></span><br>
<span style="font-size: 14px;">&gt;&gt;&gt; import MySQLdb</span><br>
<span style="font-size: 14px;">/usr/lib/python2.4/site-packages/MySQL_python-1.2.3b1-py2.4-linux-i686.egg/_mysql.py:3: UserWarning: Module _mysql was already imported from /usr/lib/python2.4/site-packages/MySQL_python-1.2.3b1-py2.4-linux-i686.egg/_mysql.pyc, but /data/MySQL-python-1.2.3b1 is being added to sys.path</span><br>
<span style="font-size: 14px;">Traceback (most recent call last):</span><br>
<span style="font-size: 14px;">&nbsp; File "&lt;stdin&gt;", line 1, in ?</span><br>
<span style="font-size: 14px;">&nbsp; File "MySQLdb/__init__.py", line 19, in ?</span><br>
<span style="font-size: 14px;">&nbsp; &nbsp; import _mysql</span><br>
<span style="font-size: 14px;">&nbsp; File "build/bdist.linux-i686/egg/_mysql.py", line 7, in ?</span><br>
<span style="font-size: 14px;">&nbsp; File "build/bdist.linux-i686/egg/_mysql.py", line 6, in __bootstrap__</span><br>
<span style="font-size: 14px;">ImportError: libmysqlclient_r.so.16: cannot open shared object file: No such file or directory</span><br>
<span style="font-size: 14px;">解决方法:</span><br>
<span style="font-size: 14px;">vi /etc/profile下加:</span><br>
<span style="font-size: 14px;">export LD_LIBRARY_PATH=/opt/mysql/lib/mysql:$LD_LIBRARY_PATH</span><br>
