---
layout: post
title: "Linux系统下手动安装pdo_mysql 成功"
categories: linux 
tags: [linux, pdo_mysql]
date: 2014-10-09 15:53:23
---

原来在Linux系统下编译php的时候，没有把dpo_mysql相关的参数带上，安装完后才发现。再重新编译有点费时间，所以决定单独来安装。

先到http://pecl.php.net/找需要的版本，我用的是稳定的版本。要先看看说明，特别是要注意mysql的php的版本。

{% highlight bash %}
# wget http://pecl.php.net/get/PDO_MYSQL-1.0.2.tgz
# tar xzvf PDO_MYSQL-1.0.2.tgz
# cd PDO_MYSQL-1.0.2
# /usr/local/php/bin/phpize
 Configuring for:
 PHP Api Version: 20041225
 Zend Module Api No: 20060613
 Zend Extension Api No: 220060519
# ./configure --with-php-config=/usr/local/php/bin/php-config
{% endhighlight %}

经过configure就可以make了

make

make install注意pdo_mysql的全路径，我的是：

/usr/local/php/lib/php/extensions/debug-non-zts-20060613/pdo_mysql.so

然后在/usr/local/lib/php.ini

加上一句：

extension=/usr/local/php/lib/php/extensions/debug-non-zts-20060613/pdo_mysql.so

重新启动apache即可看到已经加载pdo_mysql成功。 
