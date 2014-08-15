---
layout: post
categories: linux
title: "VIM用行号参与替换"
tags: [linux, vim]
date: 2014-08-15 12:55:46
---

一个小技巧。Vim有好处千种，”替换”只是其中一个。

除了强大的正则表达式,\=也是一个好用的工具。
比如要生成这么一个文件

<pre>
This is number 1
This is number 2
This is number 3
This is number 4
This is number 5
This is number 6
This is number 7
This is number 8
This is number 9
This is number 10
</pre>

方法当然有很多。用\=可以这么做:
先输入一行

<pre>
This is number X
</pre>

复制出另外9行

<pre>
yy9p
</pre>

得到

<pre>
This is number X
This is number X
This is number X
This is number X
This is number X
This is number X
This is number X
This is number X
This is number X
</pre>

然后冒号进入Command-line模式 (关于Vim的几种模式)

<pre>
	:%s@X@\=line('.')
</pre>

	就得到了

<pre>
	This is number 1
	This is number 2
	This is number 3
	This is number 4
	This is number 5
	This is number 6
	This is number 7
	This is number 8
	This is number 9
	This is number 10
</pre>

	\=其实就是对\=之后的表达式求值用来做替换。line(‘.’)是一个返回数值的函数，返回当前行的行号，所以每一行的行号被作为\=的返回值，用来替换X，就得到了需要的结果。

	其他方法比如做一个宏(Macro)来逐行递增也可以达到效果，但是不如用这个\=方便。
	因为\=后面的部分是作为表达式来处理的，所以更复杂一些的替换都可以很简单的得到实现，比如 (先撤销掉之前的改动，下同):

<pre>
		:%s@X@\=line('.')*line('.')
</pre>

		就可以得到

<pre>
		This is number 1
		This is number 4
		This is number 9
		This is number 16
		This is number 25
		This is number 36
		This is number 49
		This is number 64
		This is number 81
		This is number 100
</pre>

		我个人觉得最好用的是这个功能

<pre>
		:%s@X@\=printf("%03d", line('.'))
</pre>

		可以得到

<pre>
		This is number 001
		This is number 002
		This is number 003
		This is number 004
		This is number 005
		This is number 006
		This is number 007
		This is number 008
		This is number 009
		This is number 010
</pre>

		printf的加入又带来了太多种可能的玩法，非常称手。
	
<pre>
	来源：http://haoxiang.org/2013/11/vim-replace-by-line-number/
</pre>

