---
layout: post
title: "centos下自动安装python2.7"
categories: python
tags: [linux, python, python2.7安装, 升级python2.7]
date: 2014-10-16 23:32:42
---

由于多次需要配置CentOS python，干脆写成一个脚本。

使用版本：CentOS release 6.3 (Final)，其他没测试过。

一句话安装（需要能sudo或root）：

<pre>
wget  https://gist.github.com/zagfai/9087397/raw/16b0765875764bfc61c79330fbd242f7551c010d/centpy.sh && sudo sh centpy.sh && rm centpy.sh
</pre>

详细代码如下：

<pre>
#!/bin/bash
 
# system packages =============================================================
yum -y install python-devel openssl openssl-devel gcc sqlite sqlite-devel mysql-devel libxml2-devel libxslt-devel
 
# Python ==================================================
wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar -xzf Python-2.7.6.tgz
cd Python-2.7.6
./configure --prefix=/usr/local/python2.7 --with-threads  
   --enable-shared
make && make altinstall
ln -s /usr/local/python2.7/lib/libpython2.7.so /usr/lib
ln -s /usr/local/python2.7/lib/libpython2.7.so.1.0 /usr/lib
ln -s /usr/local/python2.7/bin/python2.7 /usr/bin
ln -s /usr/bin/python2.7 /usr/bin/python27
/sbin/ldconfig -v
 
# easyinstall and pip =====================================
wget   
/distribute-0.6.49.tar.gz --no-check-certificate
tar xf distribute-0.6.49.tar.gz
cd distribute-0.6.49
python2.7 setup.py install
/usr/local/python2.7/bin/easy_install pip
ln -s /usr/local/python2.7/bin/pip /usr/bin
 
 
# preinstall packages =========================================
pip install mysql-python ipython requests readline beautifulsoup4 
 html5lib
ln -s /usr/local/python2.7/bin/ipython /usr/bin
 
wget https://github.com/zagfai/webtul/archive/v0.31.zip
unzip v0.31
cd webtul-0.31 && sudo python2.7 setup.py install
 
# Done
echo rm dirs.............
rm Python-2.7.6 Python-2.7.6.tgz -r
echo FinishInstall!!!!!!!!!!
python2.7 -V

</pre>
