---
layout: post
title: "第九天&nbsp;:&nbsp;centos6.5的简单命令"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:21
---

<p>centos6.5的简单命令<br />
yum erase httpd 卸载系统自带的httpd和 mysql<br />
1.history 显示脚本执行的1000个命令<br />
显示的是 用户下的 .bash_history文件<br />
2.pwd<br />
显示当前的工作目录<br />
3.hostname<br />
显示当前的电脑名称。可以通过 ifconfig修改电脑名称<br />
也可以通过hostname 修改电脑名称</P>
<p>&nbsp;<wbr>涉及2个文件/etc/hosts<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
/etc/sysconfig/network</P>
<p>4.uname -a<br />
&nbsp;<wbr>显示centos的版本号码<br />
5. cat /etc/issue 查看centos发行版本号<br />
6.whoami<br />
&nbsp;<wbr> 当前使用者<br />
7.id username(用户名) 用户的标识组等信息。<br />
8.date 查看当前日期&nbsp;<wbr> time 查看当前时间 或者可以修改<br />
9.uptime 系统运行的时间<br />
10.free 内存使用信息<br />
11.df -al 查看文件系统的磁盘使用情况<br />
12. du / -bh 输出文件 结合more 因为太多了&nbsp;<wbr> du / -bh |
more<br />
&nbsp;<wbr> 列出 /目录下 每个子目录的硬盘的具体使用情况<br />
13.cat /proc/cpuinfo&nbsp;<wbr> 处理器信息</P>
<p>14.cat /proc/version&nbsp;<wbr> 查看版本<br />
15. cat /proc/filesystems 查看文件系统类型<br />
16.lsmod 查看加载的内核模块<br />
17.set&nbsp;<wbr> 显示当前用户环境变量<br />
18.echo $path 显示环境变量 path内容<br />
19.quota 显示磁盘空间配额<br />
20. sysctl -a 显示可以设置的内核参数<br />
21.runlevel 运行等级<br />
22.ls . dir ll ls-l ls-al 显示隐藏文件。<br />
&nbsp;<wbr> 通过putty终端的,
深蓝色的是目录，绿色的是可执行文件,紫色的图形文件，红色的是压缩文件，浅蓝色的是链接文件，黄色的是设备文件。<br />
23.cd 改变目录， cd .. cd \&nbsp;<wbr> clear清除终端内容，<br />
24.su 用户名，用于切换用户，默认是 root用户。<br />
25.&nbsp;<wbr> ./script 在当前目录下运行一个可执行文件。<br />
26.cp 复制文件 -r 复制整个目录,<br />
27.mv 改名移动文件,<br />
28.&nbsp;<wbr> ./当前目录<br />
29.ln 软连接，类似于快捷方式，硬链接建立一个文件指向<br />
30.rm 删除 -r 删除目录下的,-f删除指定的目录<br />
31.mkdir 建立目录<br />
32.rmdir删除一个空目录<br />
33.cat 查看文件 配合 more<br />
34.more 显示输出，用于多行<br />
35.vi,vim 编辑器<br />
36.diff 比较2个文件不同之处<br />
37. shutdown -r now -h&nbsp;<wbr>&nbsp;<wbr>
,poweroff 关机 重新启动。<br />
38.file 显示文件的类型,是那种类型的文件<br />
39.grep 搜索指定的字符串<br />
40.touch 修改文件时间日期的，也可以建立文件<br />
41.find 查找文件<br />
42.locate 地位文件，用于从数据库内查找,刚加入的找不到，因为没添加到数据库内，使用之前需要线更新下定位数据库<br />
43. man help info 指定命令的帮助信息<br />
44.whereis 命令&nbsp;<wbr> ， 查找一个命令都在那些位置,比较实用，加上-m
查找这个命令的帮助信息&nbsp;<wbr> 看到后 可以用man /var/路径名 查看 或者 直接 man
.gz前的名字就可以.</P>
<p>==========</P>
<p>习惯于用yum安装卸载了，方便</P>
<p>&nbsp;<wbr></P>
<p><br />
&nbsp;<wbr></P>
