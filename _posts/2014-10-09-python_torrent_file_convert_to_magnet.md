---
layout: post
title: "Python将BT种子文件转换为磁力链的两种方法"
categories: python
tags: [python BT种子转磁力链]
date: 2014-10-09 17:46:32
---

Python将BT种子文件转换为磁力链的两种方法


BT种子文件相对磁力链来说存储不方便，而且在网站上存放BT文件容易引起版权纠纷，而磁力链相对来说则风险小一些。而且很多论坛或者网站限制了文件上传的类型，分享一个BT种子还需要改文件后缀或者压缩一次，其他人需要下载时候还要额外多一步下载种子的操作。

所以将BT种子转换为占用空间更小，分享更方便的磁力链还是有挺大好处的。

首先一个方案是使用bencode这个插件，通过pip方式安装或者自行下载源文件https://pypi.python.org/pypi/bencode/1.0通过python setup.py install方式安装均可。

相应的将BT种子转换为磁力链代码为：

{% highlight bash %}
import bencode, hashlib, base64, urllib
torrent = open('ubuntu-12.04.2-server-amd64.iso.torrent', 'rb').read()
metadata = bencode.bdecode(torrent)
hashcontents = bencode.bencode(metadata['info'])
digest = hashlib.sha1(hashcontents).digest()
b32hash = base64.b32encode(digest)
params = {'xt': 'urn:btih:%s' % b32hash,
'dn': metadata['info']['name'],
'tr': metadata['announce'],
'xl': metadata['info']['length']}
paramstr = urllib.urlencode(params)
magneturi = 'magnet:?%s' % paramstr
print magneturi
{% endhighlight %}

还有另外一个效率相对较高，而且更方便的方案是安装libtorrent，在Debian只需要

apt-get install python-libtorrent即可

对应转换磁力链的代码为：

{% highlight bash %}
import libtorrent as bt

info = bt.torrent_info('test.torrent')

print "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
{% endhighlight %}

<pre>
原文:http://www.au92.com/archives/P-y-t-h-o-n-jiang-B-T-zhong-zi-wen-jian-zhuan-huan-wei-ci-li-lian-de-liang-zhong-fang-fa.html
</pre>
