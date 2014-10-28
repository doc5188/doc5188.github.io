---
layout: post
title: "Linux使用diff和patch制作及打补丁"
categories: linux
tags: [diff, patch]
date: 2014-10-28 16:50:53
---
<div>
在做开发的过程中难免需要给内核及下载的一些源码打补丁，所以我们先学习下Linux下使用如如何使用diff制作补丁以及如何使用patch打补丁。<br>
<br>
首先介绍一下diff和patch。</span>
</div>
<div style="text-indent: 21.75pt;">
	<strong><span style="font-size: small;">1、diff</span></strong>
</div>
<table class="ke-zeroborder" align="center" border="0" width="97%">
	<tbody>
		<tr>
			<td colspan="3">
				<div align="center">
				</div>
			</td>
		</tr>
	</tbody>
</table>
<div style="text-indent: 21.75pt;">
	<span style="font-size: small;">－－－－－－－－－－－－－－－－－－－－</span>
</div>
<div style="text-indent: 21.75pt;">
	<span style="font-size: small;">NAME</span>
</div>
<div style="text-indent: 21.75pt;">
	<span><span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; diff - find differences between two files</span></span>
</div>
<div style="text-indent: 21.75pt;">
	<span style="font-size: small;">SYNOPSIS</span>
</div>
<div style="text-indent: 21.75pt;">
	<span><span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; diff [options] from-file to-file</span></span>
</div>
<div style="text-indent: 21.75pt;">
	<span style="font-size: small;">－－－－－－－－－－－－－－－－－－－－</span>
</div>
<div style="text-indent: 21.75pt;">
	<span style="font-size: small;">简单的说，diff的功能就是用来比较两个文件的不同，然后记录下来，也就是所谓的diff补丁。语法格式：diff 【选项】 <span style="color: green;">源文件（夹）</span> <span style="color: fuchsia;">目的文件（夹）</span>，就是要给<span style="color: green;">源文件（夹）打个补丁，使之变成<span style="color: fuchsia;">目的文件（夹）</span>，术语也就是“升级”。下面介绍三个最为常用选项：</span></span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">-r 是一个递归选项，设置了这个选项，diff会将两个不同版本源代码目录中的所有对应文件全部都进行一次比较，包括子目录文件。 </span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">-N 选项确保补丁文件将正确地处理已经创建或删除文件的情况。</span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">-u 选项以统一格式创建补丁文件，这种格式比缺省格式更紧凑些。</span>
</div>
<div style="text-indent: 21pt;">
	<strong><span style="font-size: small;">2、patch</span></strong>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">－－－－－－－－－－－－－－－－－－</span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">NAME</span>
</div>
<div style="text-indent: 21pt;">
	<span><span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; patch - apply a diff file to an original</span></span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">SYNOPSIS</span>
</div>
<div style="text-indent: 21pt;">
	<span><span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; patch [options] [originalfile [patchfile]]</span></span>
</div>
<div style="text-indent: 21pt;">
	<span><span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; but usually just</span></span>
</div>
<div style="text-indent: 21pt;">
	<span><span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; patch -pnum &lt;patchfile&gt;</span></span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">－－－－－－－－－－－－－－－－－－</span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">简单的说，patch就是利用diff制作的补丁来实现<span style="color: green;">源文件（夹）和<span style="color: fuchsia;">目的文件（夹）</span>的转换。这样说就意味着你可以有<span style="color: green;">源文件（夹）</span>――</span>&gt;<span style="color: fuchsia;">目的文件（夹）</span>，也可以<span style="color: fuchsia;">目的文件（夹）――</span>&gt;<span style="color: green;">源文件（夹）。</span>下面介绍几个最常用选项：</span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">-p0 选项要从当前目录查找目的文件（夹）</span>
</div>
<div style="text-indent: 21pt;">
	<span style="font-size: small;">-p1 选项<span style="color: black;">要忽略掉第一层目录，从当前目录开始查找。</span></span>
</div>
<div style="text-align: left;" align="left">
	<span style="font-size: 12pt; color: olive;">************************************************************</span>
</div>
n style="font-size: 12pt; color: olive;"> 
<div style="text-indent: 21pt;">
	<span style="color: rgb(255, 102, 0);">在这里以实例说明：</span>
</div>
<div style="text-align: left;" align="left">
	<span style="font-size: 12pt; color: rgb(255, 102, 0);">--- old/modules/pcitable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Mon Sep 27 11:03:56 1999</span>
</div>
<div style="text-align: left;" align="left">
	<span style="font-size: 12pt; color: rgb(255, 102, 0);">+++ new/modules/pcitable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tue Dec 19 20:05:41 2000</span>
</div>
<div style="text-align: left;" align="left">
	<span style="font-size: 12pt; color: rgb(255, 102, 0);">&nbsp;&nbsp;&nbsp; 如果使用参数-p0，那就表示从当前目录找一个叫做old的文件夹，在它下面寻找modules下的pcitable文件来执行patch操作。</span>
</div>
<div style="text-align: left;" align="left">
	<span style="font-size: 12pt; color: rgb(255, 102, 0);">&nbsp;&nbsp;&nbsp; 如果使用参数-p1，那就表示忽略第一层目录（即不管old），从当前目录寻找modules的文件夹，在它下面找pcitable。这样的前提是当前目录必须为modules所在的目录。而diff补丁文件则可以在任意位置，只要指明了diff补丁文件的路径就可以了。当然，可以用相对路径，也可以用绝对路径。不过我一般习惯用相对路径。</span>
</div>
<div style="text-indent: 21pt;">
	-E&nbsp;选项说明如果发现了空文件，那么就删除它
</div>
<div style="text-indent: 21pt;">
	-R&nbsp;选项说明在补丁文件中的“新”文件和“旧”文件现在要调换过来了（实际上就是给新版本打补丁，让它变成老版本）
</div>
<div style="text-indent: 21pt;">
	下面结合具体实例来分析和解决，分为两种类型：为单个文件打补丁和为文件夹内的多个文件打补丁。
</div>
<div>
	环境：在<a title="RedHat" href="http://www.linuxidc.com/topicnews.aspx?tid=10">RedHat</a> 9.0下面以armlinux用户登陆。
</div>
<div>
	目录树如下：
</div>
<div>
	|-- bootloader
</div>
<div>
	|-- debug
</div>
<div>
	|-- images
</div>
<div>
	|-- kernel
</div>
<div>
	|-- program
</div>
<div>
	|-- rootfiles
</div>
<div>
	|-- software
</div>
<div>
	|-- source
</div>
<div>
	|-- sysapps
</div>
<div>
	|-- tmp
</div>
<div>
	`-- tools
</div>
<div>
	下面在program文件夹下面建立patch文件夹作为实验用，然后进入patch文件夹。
</div>
</span>
</div>
<div>
	<span style="font-size: small;"></span>&nbsp;
</div>
<div>
	<div id="content">
		<span style="font-size: small;">一、为单个文件进行补丁操作<br>
1、建立测试文件test0、test1<br>
[www.linuxidc.com@linuxidc patch]$ cat &gt;&gt;test0&lt;&lt;EOF<br>
&gt; 111111<br>
&gt; 111111<br>
&gt; 111111<br>
&gt; EOF<br>
[www.linuxidc.com@linuxidc patch]$ more test0 </span> 
		<table class="ke-zeroborder" align="center" border="0" width="97%">
			<tbody>
				<tr>
					<td colspan="3">
						<div align="center">
						</div>
					</td>
				</tr>
			</tbody>
		</table>
<br>
<span style="font-size: small;">111111<br>
111111<br>
111111<br>
[www.linuxidc.com@linuxidc patch]$ cat &gt;&gt;test1&lt;&lt;EOF<br>
&gt; 222222<br>
&gt; 111111<br>
&gt; 222222<br>
&gt; 111111<br>
&gt; EOF<br>
[www.linuxidc.com@linuxidc patch]$ more test1<br>
222222<br>
111111<br>
222222<br>
111111<br>
2、使用diff创建补丁test1.patch<br>
[www.linuxidc.com@linuxidc patch]$ diff -uN test0 test1 &gt; test1.patch<br>
【注：因为单个文件，所以不需要-r选项。选项顺序没有关系，即可以是-uN，也可以是-Nu。】<br>
[www.linuxidc.com@linuxidc patch]$ ls<br>
test0 test1 test1.patch<br>
[www.linuxidc.com@linuxidc patch]$ more test1.patch<br>
************************************************************<br>
patch文件的结构<br>
补丁头<br>
补丁头是分别由---/+++开头的两行，用来表示要打补丁的文件。---开头表示旧文件，+++开头表示新文件。<br>
一个补丁文件中的多个补丁<br>
一个补丁文件中可能包含以---/+++开头的很多节，每一节用来打一个补丁。所以在一个补丁文件中可以包含好多个补丁。<br>
块<br>
块是补丁中要修改的地方。它通常由一部分不用修改的东西开始和结束。他们只是用来表示要修改的位置。他们通常以@@开始，结束于另一个块的开始或者一个新的补丁头。<br>
块的缩进<br>
块会缩进一列，而这一列是用来表示这一行是要增加还是要删除的。<br>
块的第一列<br>
+号表示这一行是要加上的。<br>
-号表示这一行是要删除的。<br>
没有加号也没有减号表示这里只是引用的而不需要修改。<br>
************************************************************<br>
***diff命令会在补丁文件中记录这两个文件的首次创建时间，如下***<br>
--- test0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2006-08-18 09:12:01.000000000 +0800<br>
+++ test1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2006-08-18 09:13:09.000000000 +0800<br>
@@ -1,3 +1,4 @@<br>
+222222<br>
&nbsp;111111<br>
-111111<br>
+222222<br>
&nbsp;111111<br>
[www.linuxidc.com@linuxidc patch]$ patch -p0 &lt; test1.patch<br>
patching file test0<br>
[www.linuxidc.com@linuxidc patch]$ ls<br>
test0 test1 test1.patch<br>
[www.linuxidc.com@linuxidc patch]$ cat test0<br>
222222<br>
111111<br>
222222<br>
111111<br>
3、可以去除补丁，恢复旧版本<br>
[www.linuxidc.com@linuxidc patch]$ patch -RE -p0 &lt; test1.patch<br>
patching file test0<br>
[www.linuxidc.com@linuxidc patch]$ ls<br>
test0 test1 test1.patch<br>
[www.linuxidc.com@linuxidc patch]$ cat test0<br>
111111<br>
111111<br>
111111<br>
二、为多个文件进行补丁操作<br>
1、创建测试文件夹<br>
[www.linuxidc.com@linuxidc patch]$ mkdir prj0<br>
[www.linuxidc.com@linuxidc patch]$ cp test0 prj0<br>
[www.linuxidc.com@linuxidc patch]$ ls<br>
prj0 test0 test1 test1.patch<br>
[www.linuxidc.com@linuxidc patch]$ cd prj0/<br>
[www.linuxidc.com@linuxidc prj0]$ ls<br>
test0<br>
[www.linuxidc.com@linuxidc prj0]$ cat &gt;&gt;prj0name&lt;&lt;EOF<br>
&gt; --------<br>
&gt; prj0/prj0name<br>
&gt; --------<br>
&gt; EOF<br>
[www.linuxidc.com@linuxidc prj0]$ ls<br>
prj0name test0<br>
[www.linuxidc.com@linuxidc prj0]$ cat prj0name<br>
--------<br>
prj0/prj0name<br>
--------<br>
[www.linuxidc.com@linuxidc prj0]$ cd ..<br>
[www.linuxidc.com@linuxidc patch]$ mkdir prj1<br>
[www.linuxidc.com@linuxidc patch]$ cp test1 prj1<br>
[www.linuxidc.com@linuxidc patch]$ cd prj1<br>
[www.linuxidc.com@linuxidc prj1]$ cat &gt;&gt;prj1name&lt;&lt;EOF<br>
&gt; ---------<br>
&gt; prj1/prj1name<br>
&gt; ---------<br>
&gt; EOF<br>
[www.linuxidc.com@linuxidc prj1]$ cat prj1name<br>
---------<br>
prj1/prj1name<br>
---------<br>
[www.linuxidc.com@linuxidc prj1]$ cd ..</span>
</div>
<div>
	<span style="font-size: small;"></span>&nbsp;
</div>
<div>
	<div id="content">
		<div>
			<strong><span style="font-size: small;">2、创建补丁</span></strong>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm patch]$ diff -uNr prj0 prj1 &gt; prj1.patch</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm patch]$ more prj1.patch</span>
		</div>
		<div>
			<span style="font-size: small;"></span>&nbsp;
		</div>
		<div>
			<span style="font-size: small;">diff -uNr prj0/prj0name prj1/prj0name</span>
		</div>
		<table class="ke-zeroborder" align="center" border="0" width="97%">
			<tbody>
				<tr>
					<td colspan="3">
						<div align="center">
						</div>
					</td>
				</tr>
			</tbody>
		</table>
		<div>
			<span style="font-size: small;">--- prj0/prj0name<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2006-08-18 09:25:11.000000000 +0800</span></span>
		</div>
		<div>
			<span style="font-size: small;">+++ prj1/prj0name<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1970-01-01 08:00:00.000000000 +0800</span></span>
		</div>
		<div>
			<span style="font-size: small;">@@ -1,3 +0,0 @@</span>
		</div>
		<div>
			<span style="font-size: small;">---------</span>
		</div>
		<div>
			<span style="font-size: small;">-prj0/prj0name</span>
		</div>
		<div>
			<span style="font-size: small;">---------</span>
		</div>
		<div>
			<span style="font-size: small;">diff -uNr prj0/prj1name prj1/prj1name</span>
		</div>
		<div>
			<span style="font-size: small;">--- prj0/prj1name<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1970-01-01 08:00:00.000000000 +0800</span></span>
		</div>
		<div>
			<span style="font-size: small;">+++ prj1/prj1name<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2006-08-18 09:26:36.000000000 +0800</span></span>
		</div>
		<div>
			<span style="font-size: small;">@@ -0,0 +1,3 @@</span>
		</div>
		<div>
			<span style="font-size: small;">+---------</span>
		</div>
		<div>
			<span style="font-size: small;">+prj1/prj1name</span>
		</div>
		<div>
			<span style="font-size: small;">+---------</span>
		</div>
		<div>
			<span style="font-size: small;">diff -uNr prj0/test0 prj1/test0</span>
		</div>
		<div>
			<span style="font-size: small;">--- prj0/test0&nbsp;2006-08-18 09:23:53.000000000 +0800</span>
		</div>
		<div>
			<span style="font-size: small;">+++ prj1/test0&nbsp;1970-01-01 08:00:00.000000000 +0800</span>
		</div>
		<div>
			<span style="font-size: small;">@@ -1,3 +0,0 @@</span>
		</div>
		<div>
			<span style="font-size: small;">-111111</span>
		</div>
		<div>
			<span style="font-size: small;">-111111</span>
		</div>
		<div>
			<span style="font-size: small;">-111111</span>
		</div>
		<div>
			<span style="font-size: small;">diff -uNr prj0/test1 prj1/test1</span>
		</div>
		<div>
			<span style="font-size: small;">--- prj0/test1&nbsp;1970-01-01 08:00:00.000000000 +0800</span>
		</div>
		<div>
			<span style="font-size: small;">+++ prj1/test1&nbsp;2006-08-18 09:26:00.000000000 +0800</span>
		</div>
		<div>
			<span style="font-size: small;">@@ -0,0 +1,4 @@</span>
		</div>
		<div>
			<span style="font-size: small;">+222222</span>
		</div>
		<div>
			<span style="font-size: small;">+111111</span>
		</div>
		<div>
			<span style="font-size: small;">+222222</span>
		</div>
		<div>
			<span style="font-size: small;">+111111</span>
		</div>
		<div>
			<span style="font-size: small;"></span>&nbsp;
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm patch]$ ls</span>
		</div>
		<div>
			<span style="font-size: small;">prj0&nbsp;prj1&nbsp;prj1.patch&nbsp;test0&nbsp;test1&nbsp;test1.patch</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm patch]$ cp prj1.patch ./prj0</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm patch]$ cd prj0</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm prj0]$ patch -p1 &lt; prj1.patch </span>
		</div>
		<div>
			<span style="font-size: small;">patching file prj0name</span>
		</div>
		<div>
			<span style="font-size: small;">patching file prj1name</span>
		</div>
		<div>
			<span style="font-size: small;">patching file test0</span>
		</div>
		<div>
			<span style="font-size: small;">patching file test1</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm prj0]$ ls</span>
		</div>
		<div>
			<span style="font-size: small;">prj1name&nbsp;prj1.patch&nbsp;test1</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm prj0]$ patch -R -p1 &lt; prj1.patch </span>
		</div>
		<div>
			<span style="font-size: small;">patching file prj0name</span>
		</div>
		<div>
			<span style="font-size: small;">patching file prj1name</span>
		</div>
		<div>
			<span style="font-size: small;">patching file test0</span>
		</div>
		<div>
			<span style="font-size: small;">patching file test1</span>
		</div>
		<div>
			<span style="font-size: small;">[armlinux@lqm prj0]$ ls</span>
		</div>
		<div>
			<span style="font-size: small;">prj0name&nbsp;prj1.patch&nbsp;test0</span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">－－－－－－－－－－－－－－－－－－－</span></span>
		</div>
n> 
		<div>
			<span style="color: red;"><span style="font-size: small;">总结一下：</span></span>
		</div>
an><span> 
		<div>
			<span style="color: red;"><span style="font-size: small;">单个文件</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">diff –uN &nbsp;from-file &nbsp;to-file &nbsp;&gt;to-file.patch</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">patch –p0 &lt; to-file.patch</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">patch –RE –p0 &lt; to-file.patch</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">多个文件</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">diff –uNr &nbsp;from-docu &nbsp;to-docu&nbsp;&gt;to-docu.patch</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">patch –p1 &lt; to-docu.patch</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">patch –R –p1 &lt;to-docu.patch</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;">－－－－－－－－－－－－－－－－－－－</span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;"></span></span>
		</div>
		<div>
			<span style="color: red;"><span style="font-size: small;"></span></span>
		</div>
		<div>
			<strong><span style="font-size: small;">三、应用</span></strong>
		</div>
		<div style="text-indent: 21.75pt;">
			<span style="font-size: small;">为内核打补丁。</span>
		</div>
		<div style="text-indent: 21.75pt;">
			<span style="font-size: small;">1、首先是解压，因为发布的补丁文件都是使用gzip压缩的。</span>
		</div>
		<div style="text-indent: 21pt;">
			<span style="font-size: small;">$gunzip ../setup-dir/ patch-2.4.21-rmk1.gz </span>
		</div>
		<div style="text-indent: 21pt;">
			<span style="font-size: small;">2、然后进入你的内核源代码目录</span>
		</div>
		<div style="text-indent: 21pt;">
			<span style="font-size: small;">$cd linux-2.4.21</span>
		</div>
		<div style="text-indent: 21pt;">
			<span style="font-size: small;">3、打补丁</span>
		</div>
		<div style="text-indent: 21pt;">
			<span style="font-size: small;">$patch –p1 &lt; ../../setup-dir/patch-2.4.21-rmk1 </span>




















<pre>
referer: http://m.blog.chinaunix.net/uid-21768364-id-186039.html
</pre>

