---
layout: post
categories: linux
title: "php添加pcntl扩展(Linux)"
tags: [linux, php, pcntl]
date: 2014-09-25 23:25:41
---

 pcntl扩展可以支持php的多线程操作（仅限linux）
原本需要重新编译PHP的后面configrue提示加上--enable-pcnt

由于我的php是采用yum安装的，所以不能采用上面的方式
下面介绍一个php动态添加扩展的方式 phpize

1、首先看下 phpize命令 所在的目录  （ps：我的目录/usr/bin/phpize）
如果没有找到的话 执行安装
{% highlight bash %}
# yum install php53_devel   （ps：请注意自己的版本)
{% endhighlight %}
安装完毕后。会生成phpize命令   

2、去php.net下载相应版本的php源文件
咱们以php-5.3.17 为例吧，解压后，进入相应的模块下
{% highlight bash %}
# cd ext/pcntl
#先执行phpize
# /usr/bin/phpize
# ./configure --with-php-config=/usr/bin/php-config   （ps:请正确的指定php-config的目录）
#编译、安装
# make && make install
{% endhighlight %}

这时候出了一个错误

./configure编译正常，但make出错
<pre>
error: ‘PHP_FE_END’ undeclared here (not in a function)
</pre>

解决方法：

源代码有错误，进入php-5.3.17目录
{% highlight bash %}
# sed -i 's|PHP_FE_END|{NULL,NULL,NULL}|' ./ext/**/*.c
# sed -i 's|ZEND_MOD_END|{NULL,NULL,NULL}|' ./ext/**/*.c
{% endhighlight %}
再重新make && make install

3、编译完毕后会生成了一个  pcntl.so的文件。在php的model目录里

编辑/etc/php.ini，加入
<pre>
extension=pcntl.so
</pre>

4、重启apache

{% highlight bash %}
# service httpd restart
{% endhighlight %}

5、测试是否安装成功

{% highlight php %}
<?php
    echo pcntl_fork();
?>
{% endhighlight %}

输出：23165

另附：

pcntl扩展可以支持php的多线程操作.
原本需要重新编译PHP的后面configrue提示加上--enable-pcntl
为了省事直接编译算鸟.
{% highlight bash %}
# cd /usr/local/src/php-5.2.6/ext/pcntl
# phpize
# ./configure --with-php-config=/usr/local/php/bin/php-config
# make && make install
{% endhighlight %}
pcntl.so  加到php.ini中OK 

