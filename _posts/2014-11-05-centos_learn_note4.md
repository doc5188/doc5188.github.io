---
layout: post
title: "第十天：centos6.5下安装denyhosts"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:20
---

<p>1.ntsysv 配置启动项目服务的<br />
2. ls /etc/xinetd.d启动的服务<br />
3. /etc/inittab启动等级 telinit也可以修改<br />
4.ntsysv --level 345 修改运行等级<br />
5.日志管理。<br />
&nbsp;<wbr> /var/log下的 messages文件<br />
6.ac -p 每个用户的总连接时间<br />
7.lastlog 账户使用情况<br />
8.防火墙 setup设置<br />
9.禁止ping echo 1 &gt; /proc/sys/net/ipv4/icmp_echo_ignore_all<br />
&nbsp;<wbr> 允许ping echo 0 &gt;<br />
10. wget 从网上自主下载软件包的下载工具<br />
denyhosts的 安装配置:<br />
从denyhosts网站下载 DenyHosts-2.6.tar.gz tar -zxvf 解压<br />
&nbsp;<wbr>8 2006 CHANGELOG.txt<br />
-rwxr-xr-x 1 fuwei3006 fuwei3006&nbsp;<wbr> 4076
4月&nbsp;<wbr> 22 2006 daemon-control-dist<br />
drwxr-x--- 2 f&nbsp;<wbr> 4096 12月&nbsp;<wbr> 8 2006
DenyHosts<br />
-rw-r--r-- 1 f 20830 8月&nbsp;<wbr> 20 2006
denyhosts.cfg-dist<br />
-rwxr-xr-x 1 f&nbsp;<wbr> 6578
7月&nbsp;<wbr>&nbsp;<wbr> 8 2006 denyhosts.py<br />
-rw-r--r-- 1 f18009 12月 17 2005&nbsp;<wbr> LICENSE.txt<br />
-rw-r--r-- 1 f&nbsp;<wbr>&nbsp;<wbr> 353
4月&nbsp;<wbr>&nbsp;<wbr> 5 2006 MANIFEST.in<br />
-rw-r----- 1 f&nbsp;<wbr> 533 12月&nbsp;<wbr> 8
2006&nbsp;<wbr> PKG-INFO<br />
drwxr-x--- 2 f 4096 12月&nbsp;<wbr> 8 2006&nbsp;<wbr>
plugins<br />
-rw-r--r-- 1 f 3575 2月&nbsp;<wbr>&nbsp;<wbr> 3
2006&nbsp;<wbr> README.txt<br />
drwxr-x--- 2 f&nbsp;<wbr> 4096 12月&nbsp;<wbr> 8 2006
scripts<br />
-rw-r--r-- 1 f&nbsp;<wbr> 1522
4月&nbsp;<wbr>&nbsp;<wbr> 5 2006 setup.py<br />
解压这些文件： 观察:<br />
readme.txt 内 的&nbsp;<wbr>&nbsp;<wbr> python setup.py
install 就是安装命令。<br />
很快就完成了.<br />
安装在 /usr/share/denyhosts<br />
改名 denyhosts.cfg-dist 改为 denyhosts.cfg<br />
改名 daemon-control-dist 改为 daemon-control<br />
nano vi vim&nbsp;<wbr>
/usr/share/denyhosts/denyhosts.cfg修改</P>
<p>SECURE_LOG = /var/log/secure 安全日志存放文件<br />
HOSTS_DENY= /etc/hosts.deny&nbsp;<wbr>
发现非法用户，自动加入hosts.deny文件中屏蔽<br />
block_service =&nbsp;<wbr> sshd 需要检测的进程服务<br />
deny_threshold_invalid = 5 非法用户登录次数限制<br />
deny_threshold_valid = 10 合法用户登录次数限制<br />
deny_threshold_root = 1 root用户登录次数限制<br />
deny_threshold_restricted = 1 受限制用户登录次数限制<br />
work_dir = /usr/share/denyhosts/data
数据存储的文件夹，denyhosts将定期的检查这个文件下的数</P>
<p>据，分析非法数据并定期加入host.deny内<br />
lock_file = /var/lock/subsys/denyhosts 防止系统运行多个检测程序<br />
purge_deny = 过多久解除<br />
还有个 daemon-control 文件<br />
whereis&nbsp;<wbr> phthon看下安装位置<br />
看下 daemon-control 是 rooton用户的 并且 root用户 拥有rwx权限<br />
&nbsp;<wbr>cat /etc/hosts.deny 查看</P>
<p>将Denyhost启动脚本添加到自动启动中<br />
&nbsp;<wbr>echo ‘/usr/share/denyhosts/daemon-control
start’&gt;&gt;/etc/rc.d/rc.local<br />
启动Denyhost的进程<br />
&nbsp;<wbr>/usr/share/denyhosts/daemon-control start<br />
可以查看到Denyhost在运行中<br />
&nbsp;<wbr>ps -ef |grep deny<br />
在另外一台机器上使用Ssh进行连接，当在连续几次输入错误的密码后，会被自动阻止掉，在一定时内</P>
<p>不可以再连接<br />
Ssh连接记录的日志文件<br />
&nbsp;<wbr> tail /var/log/secure &ndash;f<br />
Denyhost日志文件<br />
&nbsp;<wbr> tail /var/log/denyhosts &ndash;f<br />
Denyhost将恶意连接的IP记录到Hosts.deny文件中，过一定时间后再从该文件中清除（Denyhost.cfg中</P>
<p>设定的时间）<br />
&nbsp;<wbr> vi /etc/hosts.deny</P>
<p>当我们需要在不同的目录，用到相同的文件时，我们不需要在每一个需要的目录下都放一个必须相同的</P>
<p>文件，我们只要在某个固定的目录，放上该文件，然后在其它的目录下用ln命令链接（link）它就可以</P>
<p>，不必重复的占用磁盘空间。例如：ln &ndash;s /bin/less /usr/local/bin/less<br />
　　-s 是代号（symbolic）的意思。<br />
　　这里有两点要注意：第一，ln命令会保持每一处链接文件的同步性，也就是说，不论你改动了哪一</P>
<p>处，其它的文件都会发生相同的变化；第二，ln的链接又软链接和硬链接两种，软链接就是ln &ndash;s **</P>
<p>**，它只会在你选定的位置上生成一个文件的镜像，不会占用磁盘空间，硬链接ln ** **，没有参数-s</P>
<p>， 它会在你选定的位置上生成一个和源文件大小相同的文件，无论是软链接还是硬链接，文件都保持</P>
<p>同步变化。<br />
　　如果你用ls察看一个目录时，发现有的文件后面有一个@的符号，那就是一个用ln命令生成的文件</P>
<p>，用ls &ndash;l命令去察看，就可以看到显示的link的路径了。<br />
&nbsp;<wbr>ln -s /usr/share/denyhosts/daemon-control
/etc/init.d/denyhosts 建立符号连接<br />
chkconfig -add denyhosts<br />
chkconfig denyhosts on 加入启动项目<br />
或者 /etc/rc.local 加入 /usr/share/denyhosts/daemon-control start<br />
==<br />
查看&nbsp;<wbr> /etc/hosts.deny 就可以<br />
===解除被封的ip:<br />
/etc/hosts.deny<br />
/usr/share/denyhosts/data<br />
/var/log下的 message 和 secure文件</P>
<p>&nbsp;<wbr></P>
