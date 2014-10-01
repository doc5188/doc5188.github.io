---
layout: post
title: "apache 开启 rewrite 重写规则"
categories: linux
tags: [apache, httpd, linux, rewrite]
date: 2014-10-01 11:22:08
---

* 第一步：找到apache的配置文件httpd.conf（文件在conf目录下）

* 第二步：你首先必须得让服务器支持mod_rewrite,如果你使用的是虚拟主机，请事先询问你的主机提供商。

　　打开httpd.conf，找到

　　#LoadModule rewrite_module modules/mod_rewrite.so

　　把#去掉

　　找到AllowOverride None 改成 AllowOverride All，

　　注：AllowOverride 的参数设置为ALL，表示整台服务器上都支持URL规则重写。Apache 服务器要读每个网站下目录下的 .htaccess 文件。如果没有这个文件，或者这个文档没有定义任何关于URL重写的规则就不会有任何效果。

　　对于不同的网址，需要在APACHE中增加如下内容

{% highlight bash %}
　　<Directory “E:/Apache Group/Apache2/htdocs/leapsoul”>
　　/*引号里代表你的web存放目录*/
　　/*如果是Linux，只要你定位到你网站目录即可*/
　　　Options FollowSymLinks
　　　AllowOverride None
　　</Directory>
{% endhighlight %}
* 第三步：重启apache服务器，先按stop再start。

* 第四步：在你需要URL重写的网站目录下放一个.htaccess文件，文件名是.htaccess，Windiws下不能直接建立，你可以用记事本另存为。

* 第五步：在.htaccess中通过正则表达式映射需要伪静态的页面。
   
    最土的的 重写规则在 rewrite 文件下

　　URL正则表达式如下：
<pre>
　　RewriteEngine on
　　RewriteRule index.html index.php
　　RewriteRule (\d+).html$ info\.php\?infoid=$1
</pre>
