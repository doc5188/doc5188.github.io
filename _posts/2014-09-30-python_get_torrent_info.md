---
layout: post
title: "Python libtorrent提取种子文件中的信息"
categories: python
tags: [python, libtorrent, torrent]
date: 2014-09-30 12:47:21
---

Python libtorrent提取种子文件中的信息，有需要的朋友可以参考下。

种子文件最麻烦的就是提取种子文件的文件列表，有的种子文件数上百上千的，处理起来头疼死你。

这段脚本只提取种子文件中按文件大小排序最大的5个文件的文件名和大小，保存为字符串便于插入数据库

如：

Blood and Ties 2013 1080p BluRay x264 DTS HD MA 5.1-alrmothe.mkv$||$16264604081@||@cover.jpg$||$49333@||@nfo.nfo$||$3553@||@لأفضل جودة.txt$||$448@||@For better quality.txt$||$359

用的时候用 @||@$||$ 分割一下就可以了

{% highlight python %}
import libtorrent as lt
import os

info = lt.torrent_info('test.torrent')
info_hash = info.info_hash()
name = info.name()
total_size = info.total_size()
creation_date = info.creation_date()
num_files = info.num_files()
files = info.files()
items = dict([(file.size,file.path) for file in files]).items()
items.sort(reverse=True)
files = os.path.split(items[0][1])[-1]+"$||$"+str(items[0][0])
for i in items[1:5]:
    files = files+"@||@"+os.path.split(i[1])[-1]+"$||$"+str(i[0])
print info_hash, name, total_size, creation_date.date(), num_files ,file
{% endhighlight %}

输出：

f2143efa661c547126665877e1a071ca6932e945 Blood and Ties 2013 1080p BluRay x264 DTS HD MA 5.1-alrmothe 16264658397 None 21 Blood and Ties 2013 1080p BluRay x264 DTS HD MA 5.1-alrmothe.mkv$||$16264604081@||@cover.jpg$||$49333@||@nfo.nfo$||$3553@||@لأفضل جودة.txt$||$448@||@For better quality.txt$||$359
