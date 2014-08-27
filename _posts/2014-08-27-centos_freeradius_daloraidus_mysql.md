---
layout: post
title: "Centos安装Freeradius+daloRADIUS配合ROS PPPOE验证"
categories: linux
tags: [linux, centos, freeradius, daloradius, pppoe]
date: 2014-08-27 16:21:23
---

LAMP环境安装：

{% highlight bash %}
# yum -y install httpd httpd-devel mysql mysql-server mysql-devel
# yum -y install php php-devel php-mysql php-common php-gd php-mbstring php-mcrypt php-xml
# /etc/init.d/httpd start
# /etc/init.d/mysqld start
# chkconfig httpd on
# chkconfig mysqld on
# mysqladmin -u root password 'newpassowrd'
{% endhighlight %}


Freeradius安装：

{% highlight bash %}
# yum install freeradius2 freeradius2-mysql freeradius2-utils
# /etc/init.d/radiusd start
# chkconfig radiusd on
{% endhighlight %}


测试Freeradius：

{% highlight bash %}
# radiusd -X
Listening on authentication address * port 1812
Listening on accounting address * port 1813
Listening on command file /var/run/radiusd/radiusd.sock
Listening on authentication address 127.0.0.1 port 18120 as server inner-tunnel
Listening on proxy address * port 1814
Ready to process requests.
{% endhighlight %}


配置Freeradius支持sql：

<pre>
cat /etc/raddb/radiusd.conf 
$INCLUDE sql.conf #调用sql.conf配置，去除之前的#
</pre>

<pre>
cat /etc/raddb/sites-enabled/default #下两段中添加sql
authorize {
	preprocess
	chap
	mschap
	digest
	suffix
	eap {
		ok = return
	}
	files
	sql
	expiration
	logintime
	pap
}
accounting {
	detail
	unix
	radutmp
	sql
	exec
	attr_filter.accounting_response
}
</pre>


设置Freeradius sql连接信息：

<pre>
cat /etc/raddb/sql.conf 
	database = "mysql"
	driver = "rlm_sql_${database}"
	server = "localhost"
	#port = 3306
	login = "radius"
	password = "radiupass"
  	radius_db = "radius"
</pre>


安装DaloRADIUS：

{% highlight bash %}
# wget http://downloads.sourceforge.net/project/daloradius/daloradius/daloradius0.9-9/daloradius-0.9-9.tar.gz
# tar zxvf daloradius-0.9-9.tar.gz 
# mv daloradius-0.9-9 /var/www/html/daloradius
# chown -R apache:apache /var/www/html/daloradius
{% endhighlight %}


创建数据库并导入：

{% highlight bash %}
# mysql -u root -p
mysql>create database radius;
mysql>grant all on radius.* to radius@localhost identified by "radpass"; 
mysql>exit;
# mysql -uroot -p radius < /var/www/html/daloradius/contrib/db/mysql-daloradius.sql 
# mysql -uroot -p radius < /var/www/html/daloradius/contrib/db/fr2-mysql-daloradius-and-freeradius.sql
{% endhighlight %}


配置DaloRADIUS：

<pre>
cat /var/www/html/daloradius/library/daloradius.conf.php
$configValues['CONFIG_DB_ENGINE'] = 'mysql';
$configValues['CONFIG_DB_HOST'] = 'localhost';
$configValues['CONFIG_DB_PORT'] = '3306';
$configValues['CONFIG_DB_USER'] = 'radius';
$configValues['CONFIG_DB_PASS'] = 'radpass';
$configValues['CONFIG_DB_NAME'] = 'radius';
$configValues['CONFIG_PATH_DALO_VARIABLE_DATA'] = '/var/www/daloradius/var'; #如在别目录需修改
</pre>


添加RADIUS客户端：

<pre>
cat /etc/raddb/clients.conf
client 192.168.1.21 {
	secret		= root
	shortname	= ROS
}
</pre>


通过浏览器访问http://www.doc5188.com/daloradius即可登录管理，默认账号：administrator，密码：radius。
<img src="/upload/images/2663906113.png" >


通过Daloradius管理界面可查看在线用户：

<img src="/upload/images/1922219599.png" >
