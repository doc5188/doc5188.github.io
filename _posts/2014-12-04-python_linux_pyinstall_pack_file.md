---
layout: post
title: "Linux下安装pyinstaller用于将py文件打包生成一个可执行文件 "
categories: linux
tags: [python, linux, pyinstaller, python打包]
date: 2014-12-04 13:12:32
---


<p>听说pyinstaller多平台支持的比较好，考虑在linux(redhat 6 32-bit)上装个pyinstall,<br>
</p>
不过真的是遇到太多问题了。。。下面是安装和使用流程：
<div><br>
</div>
<div>
<div><span style="font-size: 32px;">安装使用流程</span></div>
<div><br>
</div>
<div><span style="font-size: 14px;"><span style="font-size: 13px;">1. 首先给系统装个easy_install， 如果装了的可以跳过这步<br>
到pypi官方网址 https://pypi.python.org/pypi/setuptools 去download最新版本<br>
<br>
2. 官网上下载pyinstaller,当前的最新版本是2.1</span></span></div>
<div><span style="font-size: 14px;"><span style="font-size: 13px;">(1) 网址 http://www.pyinstaller.org/</span></span></div>
<div><br>
</div>
<div><span style="font-size: 14px;"><span style="font-size: 13px;">3.解包进入源码目录 </span>
</span></div>
<div><span style="font-size: 14px;"><span style="font-size: 13px;">(1)tar -zxvf pyinstaller_2.1.tar.gz
</span></span></div>
<div><span style="font-size: 14px;"><span style="font-size: 13px;">(2)cd pyinstaller-2.1 运行 python setup.py install<br>
<br>
4. 拷贝py文件<br>
将需打包的py文件如test.py 拷贝到当前目录<br>
<br>
5. 生成可执行文件<br>
cd到pyinstaller目录， 执行&nbsp; python pyinstaller.py test.py<br>
<br>
<span style="font-size: 32px;">可能遇到的问题</span><br>
<br>
</span></span>1. 用户权限<br>
直接在root用户下运行pyinstaller会报错 “cannot run pyinstaller as user root"...<br>
所以需新增另外一个用户，并给用户对pyinstaller所在的目录及所有父目录添加读写权限，避免运行后报‘mkdir’ permission denied...<br>
<br>
2. 找不到python lib动态库 <br>
su切换到新增用户后，<br>
pyinstaller报错找不到python动态库<br>
raise IOError("Python library not found!")<br>
IOError: Python library not <br>
<br>
执行python --version查看当前版本，并查找/usr/local/lib 下有没有对应版本的libpython*.*.so文件，<br>
如果有则跳过这步，如果没有则需要重新安装python，在python安装配置中一定要加上--enable-shared参数就可以生成对应动态链接库，如：<br>
#./configure --enable-shared --prefix=/usr/local<br>
#make<br>
#make install<br>
我环境中更新过python版本，导致/usr/lib下不是最新版本的库文件，需要将新版本拷贝到对应的/usr/lib目录下，注意有两个文件：<br>
#cp libpython*.so /usr/lib/<br>
#ln -s /usr/lib/libpython*.so.1.0 /usr/lib/libpython*.so<br>


<pre>
referer:http://blog.csdn.net/linda1000/article/details/12946297
</pre>
