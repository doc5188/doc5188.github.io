---
layout: post
title: "PHP网站地图生成类(二)"
categories: php
tags: [网站地图生成]
date: 2014-10-20 10:15:07
---
给大家一个例子参考一下，首先创建一个文件，名字叫做sitemap-generator.php, 内容如下：

{% highlight bash %}
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
    <head>
        <title></title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
    <body>
        <?php
    include 'SitemapGenerator.php';
    $sitemap = new SitemapGenerator("http://www.smartwei.com/");

    //添加url，如果你的url是通过程序生成的，这里就可以循环添加了。
    $sitemap->addUrl("http://www.smartwei.com/", date('c'), 'daily', '1');
    $sitemap->addUrl("http://www.smartwei.com/speed-up-firefox.html", date('c'), 'daily',    '0.5');
    $sitemap->addUrl("http://www.smartwei.com/php-form-check-class.html", date('c'), 'daily');
    $sitemap->addUrl("http://www.smartwei.com/32-userful-web-design-blogs.html", date('c'));

    //创建sitemap
    $sitemap->createSitemap();

    //生成sitemap文件
    $sitemap->writeSitemap();

    //更新robots.txt文件
    $sitemap->updateRobots();

    //提交sitemap到搜索引擎
    $sitemap->submitSitemap();
        ?>
    </body>
</html>
{% endhighlight %}
 
如果你的网站每天新增页面数量较少，基本上每天执行一次就可以了。如果比较多的话，可以根据你的需求创建定时执行的任务。这样，就可以使你想各大搜索引擎提交的sitemap始终是最新的了。

转自：http://www.smartwei.com/php-sitemap-generator-class.html
