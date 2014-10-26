---
layout: post
title: "libtorrent下载metadata一直无法下载?"
categories: 网络
tags: [libtorrent, dht, magnet下载]
date: 2014-10-26 10:17:45
---

https://github.com/danfolkes/Magnet2Torrent/blob/master/Magnet_To_Torrent2.py 这是源码

在windows和ubuntu中执行的结果一样 

输出 Downloading Metadata (this may take a while)  然后就没有下文了 ， 看了下代码，到了 has_metadata() 就一直返回false

http://www.oschina.net/code/snippet_267866_20835 这里也有个车不多的，但也遇到了评论里的情况

有人说是libtorrent依赖的boost版本问题

求大神如果能运行出结果，求环境版本和依赖库，或者知道哪里出问题了请指出

我用的python 和libtorrent是ubuntu14.04 apt源中的


============================================

试了你上面连接等很久下不到，自己加几个tracker后就好了...

<pre>
C:\Users\User\Desktop\Magnet2Torrent-master>Magnet_To_Torrent2.py "magnet:?xt=urn:btih:2BAF09E4FD7853F6355064B1DA077B7FFE556594"
Downloading Metadata (this may take a while)
Aborting...
Cleanup dir c:\users\user\appdata\local\temp\tmpstsodr

C:\Users\User\Desktop\Magnet2Torrent-master>Magnet_To_Torrent2.py "magnet:?xt=urn:btih:2BAF09E4FD7853F6355064B1DA077B7FFE556594&tr=http%3a%2f%2ftracker.ktxp.com%3a6868%2fannounce&tr=http%3a%2f%2ftracker.ktxp.com%3a7070%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=udp%3a%2f%2ftracker.publicbt.com%3a80%2fannounce&tr=udp%3a%2f%2ftracker.prq.to%3a80%2fannounce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2ft2.popgo.org%3a7456%2fannonce"
Downloading Metadata (this may take a while)
Done
Saving torrent file here : C:\Users\User\Desktop\Magnet2Torrent-master\22.Jump.S
treet.2014.1080p.WEB-DL.AAC2.0.H264-RARBG.torrent ...
Saved! Cleaning up dir: c:\users\user\appdata\local\temp\tmp9rbyei

</pre>
