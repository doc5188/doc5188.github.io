---
layout: post
categories: linux
tags: [linux, unix, coredump]
title: "UNIX下core文件的分析"
date: 2014-09-12 17:36:21
---

<pre>
　1、lquerypv -h core文件 6b1，可以查看到Core文件中报错的进程名字。例如：lquerypv -h core_20041210 6b1得到如下的结果，可以看到core_20041210的core文件是exe_CustInfo可执行文件产生的：
　　000006B0 7FFFFFFF FFFFFFFF 7FFFFFFF FFFFFFFF |................|
　　000006C0 00000000 000007D0 7FFFFFFF FFFFFFFF |................|
　　000006D0 00120000 06DC7F50 00000000 0000000A |.......P........|
　　000006E0 735F4375 73745365 72766572 00000000 |exe_CustInfo....|
　　000006F0 00000000 00000000 00000000 00000000 |................|
　　00000700 00000000 00000000 00000000 00000261 |...............a|
　　00000710 00000000 00000058 00000000 00000261 |.......X.......a|
　　00000720 00000000 00000000 00000000 000346B7 |..............F.|
　　00000730 00000000 001B70F0 00000000 00000000 |......p.........|
　　00000740 00000000 00000000 00000000 00000001 |................|
　　00000750 00000000 00000000 00000000 00000001 |................|
　　00000760 00000000 00000000 00000000 00000000 |................|
　　00000770 00000000 00000000 00000000 00000000 |................|
　　00000780 00000000 00000000 00000000 00000000 |................|
　　00000790 00000000 00000000 00000000 00000000 |................|
　　000007A0 00000000 00000000 00000000 00000001 |................|
　　2、采用file命令，直接 file core文件 即可
　　$ file core_20041210
　　core_20041210 AIX core file fulldump 32-bit, exe_CustInfo
　　3、可以采用strings命令，直接将core文件中的所有垃圾提示去掉，只提取有用的信息，比如采用：strings 文件 | awk '{if (NR<=5) print $0}'，可以看到第二行就是产生core文件的可执行文件。如下：
　　%s(
　　exe_CustInfo
　　HHHHHH
　　,>exe_CustInfo
　　4、在AIX下可以采用adb,dbx工具。
　　5、在Linux下可以采用gdb工具。

</pre>