---
layout: post
title: "使用 GDB list 和 search 命令"
date: 2014-08-14 12:53:32
categories: gdb
tags: [gdb, linux]
---

<pre>
使用 GDB list 和 search 命令
 
list 命令用于列出源码
 
(gdb) help list # 查看list命令帮助

(gdb) list # 查看代码执行位置附近10行,假设 15-24

(gdb) list # 再显示10行，即25-34

(gdb) list 38 # 查看第38行周围的 10 行，即33 - 42

(gdb) list - # 查看上一个list命令查看的代码之前的10行，即23-32行

(gdb) list 3,19 # 查看3-19行

(gdb) list main # 查看main函数周围的10行代码

(gdb) list flow.c:23 # 查看flow.c文件第23行周围的10行

(gdb) list flow.c:hello # 查看flow.c文件中函数hello周围的10行

(gdb) list *0x12345678 # 查看地址为 0x12345678 的符号附近的10行代码
</pre>

search/forward-search/reverse-search 命令用于在源码中搜索

usage: search <regular expression>
<pre>
(gdb) help search #查看search命令帮助

(gdb) help forward-search #查看forward-search命令的帮助

(gdb) help reverse-search #查看reverse-search命令的帮助

(gdb) search hello #从当前位置向前查找含有"hello"的第一行

(gdb) search [0-9]\{1,\} #从当前位置向前查找含有数字的第一行

(gdb) reverse-search ^#  #从当前位置向后查找以‘#’开头的第一行
</pre>
