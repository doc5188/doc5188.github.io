---
layout: post
title: "第五天:centos6.5的进程,磁盘，目录命令学习"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:27
---

<p>1.进程管理：进程大家都知道和windows的一样的意思：</P>
<p>进程号pid , 父进程号 ppid 内核自己启动的进程号为1, pstree列出进程树形，显示进程间关系。</P>
<p>&nbsp;<wbr>ps -x 显示所有的进程,ps -aux 具体自己看帮助吧。</P>
<p>程序可以启动到后台，这样做的好处是省去了前台的占用时间，放到后台执行。方法是尾行 加 &amp;符号。</P>
<p>例如 find / -name xx.bmp &gt; findresult.txzt
&amp;,这样会放到后台执行，屏幕显示进程号</P>
<p>2.|是管道符号，同时执行管道两边的进程。</P>
<p>3.调度命令at , cron at执行一次， cron是计划的，多次执行的，这2个命令以后在讲吧。</P>
<p>5.who命令 查看在线用户，w命令，显示当前用户正在执行的工作.</P>
<p>6.结束进程命令kill,pkill,xkill.killall</P>
<p>7.grep命令是文本搜索工具， 正则，很有用的命令。</P>
<p>8.文件系统：</P>
<p>1.&nbsp;<wbr>&nbsp;<wbr> .开头的是隐藏文件</P>
<p>&nbsp;<wbr>&nbsp;<wbr> file 文件名 确定文件的类型</P>
<p>2. 显示当前工作目录 pwd</P>
<p>3.链接文件： 软链接：是将一个路径 链接到一个文件。&nbsp;<wbr>硬链接，访问方便</P>
<p>&nbsp;<wbr> 查看链接的信息&nbsp;<wbr> ls -la</P>
<p>4.文件权限： r :4&nbsp;<wbr>&nbsp;<wbr>
只读&nbsp;<wbr> w :2 写&nbsp;<wbr>&nbsp;<wbr> x:1
运行权限</P>
<p>&nbsp;<wbr>一个文件 ：第一个是文件的类型， 第二个三个是
文件所有者权限&nbsp;<wbr> 第二个组3 是 组内其他用户权限，后一个是 其他用户的权限</P>
<p>5.chmod 更改文件权限&nbsp;<wbr>&nbsp;<wbr> chmod 777
x.txt,递归的为-R 将目录极其中的文件及目录的权限全部修改.</P>
<p>&nbsp;<wbr> chmod -R 777 /home/目录名等</P>
<p>6.chown 改变目录或者文件的所有者： chown 用户名 / :组名 文件名&nbsp;<wbr></P>
<p>7.分区工具：</P>
<p>&nbsp;<wbr> fdisk 增加删除分区 q不保存，w保存</P>
<p>8.e2fsck修复磁盘错误工具，修复后需要重新启动centos 例如 e2fsck -av /dev/hda</P>
<p>9.dd磁盘管理，就是diskcopy功能 dd if=输入文件或设备 of=输出文件或设备</P>
<p>10.df 查看磁盘空间使用情况</P>
<p>11.parted分区工具</P>
<p>12.安装新的磁盘（比如安装个新硬盘）</P>
<p>&nbsp;<wbr> 步骤：1.&nbsp;<wbr> fdisk /dev/hdx 分区</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>2.&nbsp;<wbr>
mke2fs /dev/hdx1 格式化成 ext2分区,</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
3.&nbsp;<wbr> mkdir /newdisk, mount -t ext2
/dev/hdx1&nbsp;<wbr> /newdisk 挂载， 就这三部曲。</P>
<p>&nbsp;<wbr></P>
