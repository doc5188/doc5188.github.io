---
layout: post
title: "第二天：centos6.5的简单了解"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:30
---

<p>我装的是是desktop模式，主机直接启动进入desktop桌面。</P>
<p>1.centos6.5运行 有还几个等级模式：</P>
<p>查看当前运行等级模式 : runlevel命令。</P>
<p>2.查看运行的服务状态： chkconfig --list</P>
<p>可以查看每个服务在不同的等级下运行状态。</P>
<p>3.chkconfig 用于查看系统服务的启动和停止命令</P>
<p>chkconfig 调用的是
/etc/init.d目录下的文件，chkconfig查看的服务都是在这个目录下的。这些都是linux在启动的过程中调用的,/etc/rc.d系列的都是在系统启动完成之后才读取的这个文件的，所以rc.系列的只是启动系统后读取的，和系统启动没有任何关系。</P>
<p>man - chkconfig 可以查看用法：</P>
<p>比如: chkconfig --list&nbsp;<wbr> 服务名&nbsp;<wbr>
就可以单独查看他的状态。</P>
<p>如果要修改在不同运行等级下的服务的状态，那么使用 chkconfig --level 2345 httpd off
这个命令的意思就是，改变运行等级 2/3/4/5的
httpd服务为不启动。就是关闭这个httpd服务在运行等级是2/3/4/5下。</P>
<p>比如关闭开机启动iptables服务,那么 chkconfig iptables off
就可以了.&nbsp;<wbr></P>
<p>chkconfig 修改服务状态，不会像Windows那样，立即执行，需要：使用 service
服务名字&nbsp;<wbr> start/reset/stop</P>
<p>4.用普通的帐号管理，如果要切换到root账户，输入su,su的意思就是super user的意思。</P>
<p>5.centos6.5的分区，/boot分区是单独独立于
/分区的，也就是说，/根分区挂载了所有的分区（除了/boot）分区.</P>
<p>6.install.log是记录了安装时候的所有的日志信息，没事的时候看看。</P>
<p>7.查看电脑上都安装了几块磁盘：fdisk -l 已经非常详细了。</P>
<p>&nbsp;<wbr> 列出来之后，选择要操作的磁盘，注意，就可以用parted命令删除</P>
<p>如果修改了分区，那么退出parted后，会提示 you may need to update /etc/fstab</P>
<p>这是一个分区开机自动挂载的文件，就是看看刚才的删除或者增加的分区是否删除或者自动挂载了。</P>
<p>可以 通过 list -l /dev/sda* 我操作的就是sda 160g磁盘来实验的。 一看正确就ok了</P>
<p>fstab文件 每次系统启动时候，挂载的信息。</P>
<p>8.格式化命令：mkfs</P>
<p>使用这个格式化分区，必须先卸载分区或者保持分区不再使用状态中。</P>
<p>9.查看电脑名称: hostname</P>
<p>&nbsp;<wbr></P>
<p>===========</P>
<p>10.学的有点乱：看看centos6.5的启动过程吧：(多注意观察屏幕出来的提示)</P>
<p>1.主板bios启动,引导硬盘上的mbr装系统的时候,主引导扇区。</P>
<p>2.mbr 进入grub,启动，bootloader自举程序，分区表.是/etc/grub.conf文件，启东linux
内核。<a HREF="http://photo.blog.sina.com.cn/showpic.html#blogid=685c0ea30101fg32&url=http://album.sina.com.cn/pic/001UurAfzy6Iu219qrH25" TARGET="_blank"><img NAME="image_operate_50011398753519250" src="http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif" real_src ="http://s6.sinaimg.cn/mw690/001UurAfzy6Iu219qrH25&amp;690" WIDTH="480" HEIGHT="50"  ALT="第二天：centos6.5的简单了解"  TITLE="第二天：centos6.5的简单了解" /></A><br />
ls /boot可以看下。解压内核</P>
<p>3.读取kernel,内核文件：/boot/vmlinuz-2.6.32.....</P>
<p>4.读取init的镜像文件，/boot/initrd</P>
<p>5.通过init去读取/etc/inittab</P>
<p>6.读取系统启动运行级别 id:5:initdefault::</P>
<p>
7.系统读取/etc/rc.d/rc.sysinit,设置时间，电脑名称，挂载分区表,是通过/etc/fstab来完成的。</P>
<p>
8.读取/etc/rc.d/rc脚本,其实这个脚本就相当于windows开机批处理,比如前面我的是启动了运行等级5，那么就启动/etc/rc.d/rc5.d目录下以s开头的服务，不启动k开头的服务，看我的图</P>
<p><a HREF="http://photo.blog.sina.com.cn/showpic.html#blogid=685c0ea30101fg32&url=http://album.sina.com.cn/pic/001UurAfzy6Iu3nf1jqd0" TARGET="_blank"><img NAME="image_operate_70761398754076796" src="http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif" real_src ="http://s1.sinaimg.cn/mw690/001UurAfzy6Iu3nf1jqd0&amp;690" WIDTH="461" HEIGHT="209"  ALT="第二天：centos6.5的简单了解"  TITLE="第二天：centos6.5的简单了解" /></A><br />
<br />
<a HREF="http://photo.blog.sina.com.cn/showpic.html#blogid=685c0ea30101fg32&url=http://album.sina.com.cn/pic/001UurAfzy6Iu3nu1Vx93" TARGET="_blank"><img NAME="image_operate_46351398754076906" src="http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif" real_src ="http://s4.sinaimg.cn/mw690/001UurAfzy6Iu3nu1Vx93&amp;690" WIDTH="690" HEIGHT="207"  ALT="第二天：centos6.5的简单了解"  TITLE="第二天：centos6.5的简单了解" /></A><br />
<br />
9.然后，系统就自动进入登录的界面了。登录结束了。</P>
<p>&nbsp;<wbr>休息休息在学习.</P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
