---
layout: post
title: "BitTorrent协议规范(BitTorrent Protocol Specification)系列之元信息文件结构(Metainfo File Structure)-第二部分"
categories: 网络
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范]
date: 2014-11-13 12:33:43
---

<p>元信息文件结构(Metainfo File Structure)<br />元信息文件里面的所有数据都以B编码方式编码，B编码规范请参考本系列文档之B编码。</p>
<p>元信息文件(就是平常咱们经常接触到的以.torrent为后缀的文件)的内容是一个B编码的dictionary，包含下面列出的键(key)，其中字符串类型的值均以UTF-8编码。</p>
<p>info：该键(key)对应的值是一个描述torrent文件的dictionary。该dictionary有两种可能的结构：一种对应于没有目录结构的单文件torrent(即种子文件中只包含一个文件)，另一种则对应于多文件torrent(详情请看下文)。(dictionary类型) <br />announce：改键对应的值是tracker的announce URL。(字符串类型) <br />announce-list：(可选)，这是对正式规范的一个扩展，目的是提供向后兼容性。(list of lists of strings类型) <br />creation date：(可选)，该键对应的值是torrent文件的创建时间，时间使用标准的UNIX时间格式。(整数类型，是从1970-01-01 00:00:00开始的秒数)&nbsp; <br />comment：(可选)，该键对应的值是torrent文件制作者的评论。(字符串类型) <br />create by：(可选)，该键对应的值是制作torrent文件的程序的名称和版本。(字符串类型) <br />encoding：(可选)，由上文可知，.torrent元文件中包含一个info dictionary，当该dictionary过大时，就需要对其分片(piece)，该编码就是用来生成分片的。(字符串类型) </p>
<p>Info Dictionary(即键Info对应的值) <br />这一节主要是讲述两种模式(单文件模式和多文件)所共有的键(key)</p>
<p>piece length: 该键对应的值是每一片(piece)的字节数。(整数类型) <br />pieces: 该键对应的值由所有的20字节SHA1散列值连接而成的字符串，每一片(piece)均含有一个唯一的SHA1散列值。(字节串类型) <br />private: (可选)，这个键(key)所对应值是整数类型，如果设置为1。客户端必须广播自己的存在，然后通过在元信息文件中显式描述的trackers得到其他的peers，如果设置为0或者不设置，则表明客户端可以通过其他的方式来得到其他的peers，例如：PEX peer exchange技术，DHT技术等。&#8220;private&#8221;可以解释为没有外部的peer源(如果客户端不提供PEX peer exchange技术、DHT技术等，那么BitTorrent客户端必须通过tracker来得到其他的peers)。(整数类型)</p>
<p>Info in Single File Mode(单文件模式下的Info键)</p>
<p>对应于单文件模式，info dictionary包含如下的结构：</p>
<p>name：文件名. 建议使用。(字符串类型) <br />length：文件的所占字节数。(整数类型) <br />md5sum：(可选)，相当于文件MD5和的32个字符的16进制串，BitTorrent根本就不使用这个键(key)，但是有些程序为了更大的兼容性而包含它。(字符串类型)</p>
<p>Info in Multiple File Mode(多文件模式下的Info键)<br />对应于多文件模式，info dictionary包含如下的结构：</p>
<p>name：存储所有文件的目录名，建议使用。 (字符串类型) <br />files：a list of dictionaries，每一个文件对应一个dictionary(其实下面的字段刚好对应单文件模式下键(key)，说得通俗点就是多文件模式是多个单文件模式的集合)。list下的每一个dictionary包含如下的结构： <br />length：参考单文件模式 <br />md5sum：参考单文件模式 <br />path：包含单个或多个元素的list，这些元素合成在一起表示文件路径和文件名。list中的每一个元素对应于一个目录名或者文件名(当是最后一个元素时对应文件名). 例如：文件"dir1/dir2/file.ext"由三个字符串元素组成："dir1"、"dir2"和"file.ext"。这三个元素会被编码成B编码的字符串list：l4:dir14:dir28:file.exte </p>
<p>注意(Notes)<br />键(key)piece length指出了片(piece)的正常大小，通常情况下2的n次方。一般根据torrent中文件数据的总大小来选择片(piece)大小，同时片(piece)太大导致低效，片(piece)太小，会使.torrent文件太大这两个因素也会影响片(piece)大小的选择。以前，选择的片(piece)大小，应该使.torrent文件不超过50-75KB(据推测这样能减轻存储.torrent文件的tracker的负载). <br />目前最好的做法是保持片(piece)大小为512KB或者更少，虽然对于8-10GB的文件，会使.torrent文件过大，但是片数量的增加有利于文件的共享。最常用的片(piece)大小事256 kB，512 kB和1 MB。 <br />除了最后一块，所有的块都具有同样的大小，最后一块的大小是不规则的。这样片(piece)的数量就由( total length / piece size )决定。 <br />对于多文件模式情况下的片边界，可以将文件数据当做是一个长的连续流，这个流由文件列表中的文件串连而成。这样多文件模式下片(piece)数量的决定方式和单文件模式下就一样了。片(piece)有可能跨越文件边界。 <br />每个片(piece)都含有一个对应于该片(piece)数据的SHA1散列值。这些散列值串连起来就形成了上述info dictionary中pieces键所对应的值(key-value)。需要注意的是这个值并不是一个由字符串组成的list，而是一个字符串，字符串的长度是20的倍数。</p>



<pre>
referer:http://www.cnblogs.com/MaxWoods/archive/2009/07/25/1530849.html
</pre>
