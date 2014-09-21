---
layout: post
title: "如何设置mysql远程访问"
tags: [mysql]
date: 2014-09-20 17:52:12
categories: 数据库
---

Mysql默认是不可以通过远程机器访问的,通过下面的配置可以开启远程访问

在MySQL Server端：

执行mysql 命令进入mysql 命令模式，

{% highlight sql %}
mysql> use mysql;
mysql> GRANT ALL ON *.* TO admin@'%' IDENTIFIED BY 'admin' WITH GRANT OPTION;
#这句话的意思 ，允许任何IP地址（上面的 % 就是这个意思）的电脑 用admin帐户  和密码（admin）来访问这个MySQL Server
#必须加类似这样的帐户，才可以远程登陆。 root帐户是无法远程登陆的，只可以本地登陆
{% endhighlight %}


那么如何远程访问呢？

在另一台MySQL 客户端（装有mysql程序包的pc ，windows或者是linux均可）

执行命令：

{% highlight sql %}

mysql -h172.21.5.29 -uadmin -padmin   即可了
//172.21.5.29就是MySQL Server的IP地址，admin admin就是刚才在 172.21.5.29上设置的远程访问帐户

{% endhighlight %}


我发现一个问题， 如果上面的命令你执行完毕， 你在 本地就是localhost ， 执行 :

{% highlight sql %}

mysql -hlocalhost -uadmin -padmin 
{% endhighlight %}



结果是失败的。

原来 上面的 % 竟然不包括localhost

所以你还必须加上这样的 命令 

{% highlight sql %}
mysql>GRANT ALL ON *.* TO admin@'localhost'  IDENTIFIED BY 'admin' WITH GRANT OPTION; 
{% endhighlight %}
