---
layout: post
title: "dhtspider使用Twig模板引擎"
categories: php
tags: [dhtspider, twig, php]
date: 2015-01-16 15:27:08
---

1. 安装Twig. dhtspider(演示站http://bt.doc5188.com)使用tarball安装方法.

a) 下载Twig. 

	wget https://github.com/twigphp/Twig/archive/v1.16.0.tar.gz
	tar vxf v1.16.0.tar.gz

b) 使用Twig.

{% hightlight bash %}
<?php
require_once 'Twig-1.16.0/lib/Twig/Autoloader.php';
Twig_Autoloader::register();

$loader = new Twig_Loader_Array(array(
    'index' => 'Hello {{ name }}!',
));
$twig = new Twig_Environment($loader);

echo $twig->render('index', array('name' => 'Fabien'));

?>
{% endhightlight %}
