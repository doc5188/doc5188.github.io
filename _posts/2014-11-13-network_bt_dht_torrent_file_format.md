---
layout: post
title: "Bt Torrent 文件格式"
categories: 网络
tags: [Bt Torrent, dht metadata]
date: 2014-11-13 11:18:36
---
<p>刚找到的，不敢独享，发来看看 &nbsp; <br>
&nbsp; Torrent文件格式 &nbsp; <br>
&nbsp; &nbsp; <br>
&nbsp; BT种子文件格式 &nbsp; <br>
&nbsp; &nbsp; <br>
&nbsp; BT种子文件使用了一种叫bencoding的编码方法来保存数据。 &nbsp; <br>
&nbsp; bencoding现有四种类型的数据：srings(字符串)，integers(整数)，lists(列表)，dictionaries(字典) &nbsp; <br>
&nbsp; 编码规则如下： &nbsp; <br>
&nbsp; strings(字符串)编码为：&lt;字符串长度&gt;：&lt;字符串&gt; &nbsp; <br>
&nbsp; 例如： &nbsp; 4:test &nbsp; 表示为字符串"test" &nbsp; <br>
&nbsp; 4:例子 &nbsp; 表示为字符串“例子” &nbsp; <br>
&nbsp; 字符串长度单位为字节 &nbsp; <br>
&nbsp; 没开始或结束标记 &nbsp; <br>
&nbsp; &nbsp; <br>
&nbsp; integers(整数)编码为：i&lt;整数&gt;e &nbsp; <br>
&nbsp; 开始标记i，结束标记为e &nbsp; <br>
&nbsp; 例如： &nbsp; i1234e &nbsp; 表示为整数1234 &nbsp; <br>
&nbsp; i-1234e &nbsp; 表示为整数-1234 &nbsp; <br>
&nbsp; 整数没有大小限制 &nbsp; <br>
&nbsp; i0e &nbsp; 表示为整数0 &nbsp; <br>
&nbsp; i-0e &nbsp; 为非法 &nbsp; <br>
&nbsp; 以0开头的为非法如： &nbsp; i01234e &nbsp; 为非法 &nbsp; <br>
&nbsp; &nbsp; <br>
&nbsp; lists(列表)编码为：l&lt;bencoding编码类型&gt;e &nbsp; <br>
&nbsp; 开始标记为l,结束标记为e &nbsp; <br>
&nbsp; 列表里可以包含任何bencoding编码类型，包括整数，字符串，列表，字典。 &nbsp; <br>
&nbsp; 例如： &nbsp; l4:test5abcdee &nbsp; 表示为二个字符串["test","abcde"] &nbsp; <br>
&nbsp; &nbsp; <br>
&nbsp; dictionaries(字典)编码为d&lt;bencoding字符串&gt;&lt;bencoding编码类型&gt;e &nbsp; <br>
&nbsp; 开始标记为d,结束标记为e &nbsp; <br>
&nbsp; 关键字必须为bencoding字符串 &nbsp; <br>
&nbsp; 值可以为任何bencoding编码类型 &nbsp; <br>
&nbsp; 例如： &nbsp; d3:agei20ee &nbsp; 表示为{"age"=20} &nbsp; <br>
&nbsp; d4:path3:C:/8:filename8:test.txte &nbsp; 表示为{"path"="C:/","filename"="test.txt"} &nbsp; <br>
&nbsp; &nbsp; <br>
&nbsp; 具体文件结构如下： &nbsp; <br>
&nbsp; 全部内容必须都为bencoding编码类型。 &nbsp; <br>
&nbsp; 整个文件为一个字典结构,包含如下关键字 &nbsp; <br>
&nbsp; announce:tracker服务器的URL(字符串) &nbsp; <br>
&nbsp; announce-list(可选):备用tracker服务器列表(列表) &nbsp; <br>
&nbsp; creation &nbsp; date(可选):种子创建的时间，Unix标准时间格式，从1970 &nbsp; 1月1日 &nbsp; 00:00:00到创建时间的秒数(整数) &nbsp; <br>
&nbsp; comment(可选):备注(字符串) &nbsp; <br>
&nbsp; created &nbsp; by(可选):创建人或创建程序的信息(字符串) &nbsp; <br>
&nbsp; info:一个字典结构，包含文件的主要信息，为分二种情况：单文件结构或多文件结构 &nbsp; <br>
&nbsp; 单文件结构如下： &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; length:文件长度，单位字节(整数) &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; md5sum(可选)：长32个字符的文件的MD5校验和，BT不使用这个值，只是为了兼容一些程序所保留!(字符串) &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name:文件名(字符串) &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; piece &nbsp; length:每个块的大小，单位字节(整数) &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; pieces:每个块的20个字节的SHA1 &nbsp; Hash的值(二进制格式) &nbsp; <br>
&nbsp; 多文件结构如下： &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; files:一个字典结构 &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; length:文件长度，单位字节(整数) &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; md5sum(可选):同单文件结构中相同 &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; path:文件的路径和名字，是一个列表结构，如/test/test.txt &nbsp; 列表为l4:test8test.txte &nbsp;
<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name:最上层的目录名字(字符串) &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; piece &nbsp; length:同单文件结构中相同 &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; pieces:同单文件结构中相同 &nbsp; &nbsp; <br>
&nbsp; 实例： &nbsp; <br>
&nbsp; 用记事本打开一个.torrent可以看来类似如下内容 &nbsp; <br>
&nbsp; d8:announce35:http://www.manfen.net:7802/announce13:creation &nbsp; datei1076675108e4:infod6:lengthi17799e4:name62:MICROSOFT.WINDOWS.2000.AND.NT4.SOURCE.CODE-SCENELEADER.torrent12:piece &nbsp; lengthi32768e6:pieces20:?W &nbsp; ?躐?緕排T酆ee &nbsp;
<br>
&nbsp; &nbsp; <br>
&nbsp; 很容易看出 &nbsp; <br>
&nbsp; announce＝http://www.manfen.net:7802/announce &nbsp; <br>
&nbsp; creation &nbsp; date＝1076675108秒(02/13/04 &nbsp; 20:25:08) &nbsp; <br>
&nbsp; 文件名=MICROSOFT.WINDOWS.2000.AND.NT4.SOURCE.CODE-SCENELEADER.torrent &nbsp; <br>
&nbsp; 文件大小＝17799字节</p>
