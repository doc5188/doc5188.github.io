---
layout: post
title: "Python搭建BT资源搜索站（四）"
categories: python
tags: [python, BT资源搜索站]
date: 2014-10-10 12:00:59
---

前文中已经下载到了一些BT种子文件，其实聪明的孩子已经发现我之前写过一篇使用Python将BT种子转换为磁力链接的文章，其中会有一些办法解析BT种子的info信息，然后提取出来转换成磁力链接格式。

因为暂时咱们只拿到了一些BT种子文件，所以最简单的方式获取BT文件的信息就是要解析BT种子文件，获取文件本身包含的一些信息。

参考之前的文章，我建议是使用python-libtorrent来解析文件，效率高而且通过apt-get方式安装出问题的几率小。

因为是Windows下开发，安装包请自行Google下载，本人下载到的版本为python-libtorrent-0.16.10.win32，安装过程一路Next即可。

安装完成后就可以参考我之前在Debian环境的代码，轻松的将现有的种子文件转换成磁力链接。

除了可以转换成磁力链接外，通过解析一个种子文件咱们可以获取到的信息有：

    1. 这个种子中包含的文件列表

    2. 文件列表包含文件名称、文件大小

    3. 通过文件名称咱们可以分析到文件类型等等

    4. Tracker信息等等

解析BT种子并更新种子某些信息到Mongo的代码:https://gist.github.com/Chairo/6366846/raw/30e988f9244e62ecd12cfd1c5283933857c90175/file_info.py


<pre>
referer: http://www.au92.com/archives/P-y-t-h-o-n-da-jian-B-T-zi-yuan-sou-suo-zhan-si.html
</pre>
