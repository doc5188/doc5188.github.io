---
layout: post
categories: linux
tags: [linux, ubuntu, net-snmp]
title: "Ubuntu下安装net-snmp5.7.1步骤"
date: 2014-09-26 14:23:28
---

NET-SNMP的官方网站是:http://www.net-snmp.org

Ubuntu下安装net-snmp,具体步骤如下：

1、获取net-snmp的安装包，这里我们选择源代码的安装方式，当然你也可以选择ubuntu的网络下载方式安装，如：
{% highlight bash %}
# apt-get install net-snmp
{% endhighlight %}
或者是自己从网络down下来手动编译安装，这里我选择最新版本的net-snmp5.7.1,下载下来的格式为net-snmp-5.7.1.tar.gz

2、我们先必须要源代码安装包进行解压，如下：

我们可以先建一个snmp的目录 
{% highlight bash %}
# mkdir snmptemp
# cd snmptemp
# mv net-snmp-5.7.1.tar.gz ./
# tar -zxvf net-snmp-5.7.1.tar.gz
{% endhighlight %}
解压之后我们就把目录名字更改如下：
{% highlight bash %}
# mv net-snmp-5.7.1 ./net-snmp
{% endhighlight %}

3、安装Ubuntu下的snmp的依赖包，具体如下：
{% highlight bash %}
# apt-get install libperl-dev
{% endhighlight %}
以上的安装方式是先下载，后自动安装


4、进入到解压目录，开始配置
{% highlight bash %}
# cd net-snmp
# ./configure --with-default-snmp-version="3" --prefix="/usr/local/net-snmp" --with-sys-contact="@@no.where" --with-sys-location="Unknown" --with-logfile="/var/log/snmpd.log"   --with-persistent-directory="/var/net-snmp"
{% endhighlight %}

关于配置参数说明：

prefix:安装路径

<pre>
with-default-snmp-version(3): 3（在这里版本通常有三种形式：1,2c,3）
with-sys-contact（配置该设备的联系信息）: heaven（也可以是邮箱地址）
with-sys-location(该系统设备的地理位置):BEIJING P.R China
Location to write logfile (日志文件位置): /var/log/snmpd.log
Location to Write persistent(数据存储目录): /var/net-snmp
</pre>


配置完成之后，可以看如下关于Net-snmp的配置信息：
<pre>
---------------------------------------------------------
            Net-SNMP configuration summary:
---------------------------------------------------------
</pre>

5、编译和安装
{% highlight bash %}
# cd net-snmp
# make
# make install
{% endhighlight %}

如果安装后想卸载可以执行sudo make uninstall.

6、设置任何目录下可以运行snmp的命令，需做一下设置：
{% highlight bash %}
# echo export LD_LIBRARY_PATH=/usr/local/lib >> .bashrc
# source .bashrc
{% endhighlight %}

7、验证安装是否成功，如下所示：
{% highlight bash %}
# snmpget --version
{% endhighlight %}
如果成功，则显示当前的安装版本号，NET-SNMP version: 5.7.1

或者可以进入安装路径 /usr/local/net-snmp/bin目录下，直接执行snmpget --version
如果提示如下错误：
snmpget: error while loading shared libraries: libnetsnmp.so.30: cannot open shared object file: No such file or directory

则解决方案如下： cp /usr/local/lib/libnetsnmp.so.30 /usr/lib

或者将/usr/local/lib下所有的包都copy到/usr/lib下即可，再次运行以上获取版本的命令，即可正确输出版本号，表示Ubuntu下安装net-snmp成功!


8、配置snmpd.conf

参考官方说明：http://www.net-snmp.org/docs/man/snmpd.conf.html

一种方式是用命令snmpconf -g basic_setup生成snmpd.conf文件，但需要回答很多没用的问题，比较费时，我这里用了一种较简便的方法生成配置文件,就是把解压后的那个文件目录下的EXAMPLE.conf文件拷在我们的安装路径下并修改，命令格式如下：
cp EXAMPLE.conf /usr/local/net-snmp/share/snmp/snmpd.conf //cp样例配置到安装目录下

具体修改可以参考官方说明。

或者可以直接创建一个最简单的配置文件，如下：

<pre>
vi /usr/local/net-snmp/share/snmp/snmpd.conf
rocommunity public 192.168.1.100
rocommunity public 127.0.0.1
<pre>

9、设置net-snmp自启动

手动启动服务
{% highlight bash %}
# /usr/local/net-snmp/sbin/snmpd
{% endhighlight %}

设置系统自启动
{% highlight bash %}
# cp dist/snmpd-init.d /etc/init.d/snmpd
# vi /etc/init.d/snmpd
{% endhighlight %}
修改

prog="/usr/local/sbin/snmpd" 

为

prog="/usr/local/net-snmp/sbin/snmpd"

<pre>
修改
[ -x $prog -a -f /usr/local/share/snmp/snmpd.conf ] || exit 0
为
[ -x $prog -a -f /usr/local/net-snmp/share/snmp/snmpd.conf ] || exit 0
</pre>

{% highlight bash %}
# chkconfig snmpd on
# service snmpd start
{% endhighlight %}


检查

使用 ps -aux | grep snmpd查看snmpd的进程是否启动

使用如下命令从本机检查snmp是否得到系统数据

{% highlight bash %}
# snmpwalk -v 2c -c public localhost
{% endhighlight %}

如果返回的不是Time out,而是系统信息就说明net-snmp安装成功。

<pre>
来源: http://blog.csdn.net/shanzhizi/article/details/16967343
</pre>
