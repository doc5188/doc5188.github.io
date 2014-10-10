---
layout: post
title: "Python搭建BT资源搜索站（三）"
categories: python
tags: [python, BT资源搜索站]
date: 2014-10-10 11:59:59
---

前文中已经用Python将一个从torrage.com上采集下来的文件解析并且保存进了Mongo数据库中，但此时Mongo数据库中仅仅是一些字符串，和咱们期望的BT资源站貌似完全不相关。

当然聪明的小伙伴是已经知道torrage.com这个网站就是托管一些BT种子的网站，从网站主页就可以看到可以简单的通过访问『http://torrage.com/torrent/info_hash.torrent』下载一个BT种子。

所以再一次祭出requests这个神器，通过遍历之前保存进Mongo中的info_hash来下载BT种子文件。

<b>首先</b>，在bt-search目录新建一个文件夹『torrents』用来保存BT种子文件。

<b>然后</b>，使用requests抓取torrage的文件并保存到torrents文件夹中，具体代码可以参考我写完的代码：https://gist.github.com/Chairo/6329285/download

代码中包含自动创建目录、下载BT文件、从Mongo中根据指定条件查询数据、更新Mongo、删除Mongo数据等操作…

没有特别指明，请小伙伴自己发挥主观能动性，Google或者百度一下。

<pre>
referer: http://www.au92.com/archives/P-y-t-h-o-n-da-jian-B-T-zi-yuan-sou-suo-zhan-san.html
</pre>
