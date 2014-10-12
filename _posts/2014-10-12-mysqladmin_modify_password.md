---
layout: post
title: "使用mysqladmin命令修改MySQL密码与忘记密码"
categories: 数据库
tags: [mysqladmin]
date: 2014-10-12 21:14:52
---

修改密码：

1.例如你的 root用户现在没有密码，你希望的密码修改为123456，那么命令是：

{% highlight bash %}
# mysqladmin -u root password 123456
{% endhighlight %}

2.如果你的root现在有密码了（123456），那么修改密码为abcdef的命令是：

{% highlight bash %}
# mysqladmin -u root -p password abcdef 
{% endhighlight %}

注意，命令回车后会问你旧密码，输入旧密码123456之后命令完成，密码修改成功。

3.如果你的root现在有密码了（123456），那么修改密码为abcdef的命令是：

{% highlight bash %}
# mysqladmin -u root -p123456 password abcdef (注意-p 不要和后面的密码分
{% endhighlight %}

开写，要写在一起,不然会出错,错误如下所示)

4.使用phpmyadmin，这是最简单的了，修改mysql库的user表，

不过别忘了使用PASSWORD函数。


忘记密码：

下面我们提供了6种不同的修改mysql root用户的密码，与增加mysql用户的方法。

方法一 

使用phpmyadmin，这是最简单的了，修改mysql库的user表， 

不过别忘了使用PASSWORD函数。 

方法二 

使用mysqladmin，这是前面声明的一个特例。 

mysqladmin -u root -p password mypasswd 

输入这个命令后，需要输入root的原密码，然后root的密码将改为mypasswd。 

把命令里的root改为你的用户名，你就可以改你自己的密码了。 

当然如果你的mysqladmin连接不上mysql server，或者你没有办法执行mysqladmin， 

那么这种方法就是无效的。 

而且mysqladmin无法把密码清空。 

下面的方法都在mysql提示符下使用，且必须有mysql的root权限： 

方法三 

mysql> INSERT INTO mysql.user (Host,User,Password) 
VALUES('%','jeffrey',PASSWORD('biscuit')); 
mysql> FLUSH PRIVILEGES 

确切地说这是在增加一个用户，用户名为jeffrey，密码为biscuit。 

在《mysql中文参考手册》里有这个例子，所以我也就写出来了。 

注意要使用PASSWORD函数，然后还要使用FLUSH PRIVILEGES。 

方法四 

和方法三一样，只是使用了REPLACE语句 

mysql> REPLACE INTO mysql.user (Host,User,Password) 
VALUES('%','jeffrey',PASSWORD('biscuit')); 
mysql> FLUSH PRIVILEGES 

方法五 

使用SET PASSWORD语句， 

mysql> SET PASSWORD FOR jeffrey@"%" = PASSWORD('biscuit'); 

拟也必须使用PASSWORD()函数， 

但是不需要使用FLUSH PRIVILEGES。 

方法六 

使用GRANT ... IDENTIFIED BY语句 
<pre>
mysql> GRANT USAGE ON *.* TO jeffrey@"%" IDENTIFIED BY 'biscuit'; 
</pre>


这里PASSWORD()函数是不必要的，也不需要使用FLUSH PRIVILEGES。 

注意： PASSWORD() [不是]以在Unix口令加密的同样方法施行口令加密。

MySQL 忘记口令的解决办法

如果 MySQL 正在运行，首先杀之： killall -TERM mysqld。 

启动 MySQL ：bin/safe_mysqld --skip-grant-tables & 

就可以不需要密码就进入 MySQL 了。 

然后就是
<pre>
>use mysql
>update user set password=password("new_pass") where user="root";
>flush privileges;
</pre>
重新杀 MySQL ，用正常方法启动 MySQL 。
