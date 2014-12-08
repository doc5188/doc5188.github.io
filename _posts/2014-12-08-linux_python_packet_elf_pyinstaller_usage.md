---
layout: post
title: "Linux Pyinstaller使用示例"
categories: linux
tags: [python, linux, pyinstaller]
date: 2014-12-08 12:33:28
---

* 1. 安装pyinstaller

<pre>
# pip install pyinstaller
</pre>


* 2. 切换普通使用

# su test

若没有普通用户，刚需先添加普通用户

<pre>
	# adduser test 
  	# passwd test
  	# su gavin
</pre>


* 3. 打包文件

<pre>
$ /usr/local/python/bin/pyinstaller --onefile test_bb.py 
</pre>

* 4. 运行

<pre>
$ ./dist/test_bb
</pre>


* 遇到的错误及解决方法：

1.
<pre>
Traceback (most recent call last):
  File "<string>", line 3, in <module>
  File "/usr/local/python/lib/python2.7/site-packages/PyInstaller/loader/pyi_importers.py", line 270, in load_module
    exec(bytecode, module.__dict__)
  File "/tmp/crawl/build/test_src/out00-PYZ.pyz/test_src", line 11, in <module>
  File "/usr/local/python/lib/python2.7/site-packages/PyInstaller/loader/pyi_importers.py", line 270, in load_module
    exec(bytecode, module.__dict__)
  File "/tmp/crawl/build/test_src/out00-PYZ.pyz/mysql", line 2, in <module>
  File "build/bdist.linux-x86_64/egg/MySQLdb/__init__.py", line 19, in <module>
  File "build/bdist.linux-x86_64/egg/_mysql.py", line 7, in <module>
  File "build/bdist.linux-x86_64/egg/_mysql.py", line 3, in __bootstrap__
ImportError: No module named pkg_resources

</pre>

解决方法:

<pre>
cp ~/.python-eggs/MySQL_python-1.2.3b1-py2.7-linux-x86_64.egg-tmp/_mysql.so dist/ -v
</pre>
