---
layout: post
title: "第一天:centos6.5的安装"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:31
---

<p>1.&nbsp;<wbr>&nbsp;<wbr>
从开源社区下载了,centos6.5_i386.bindvd1.iso 的 32位版本。</P>
<p>跟以往一样，使用ultraiso 写入u盘，u盘选择usb-hdd模式，写入后，设置为u盘启动，我用的是8g
u盘，开始安装。</P>
<p>出现 -press the key to begin installistion
process.等了很长时间，回车也没用。把u盘插到windows 7
机器上看了下，打包生成syslinux.cfg启动配置文件，内容第一行：default&nbsp;<wbr>
vesamenu.c32</P>
<p>原来是默认 使用 vesamenu.c32菜单来启动，没启动过去，说明vesamenu.c32有问题，是不是格式不对。然后看了下
centos6.5的那个自带的 vesamenu.c32是160k,然后从网上随便找了一个vesamenu.c32
比他小。把原有的改名vesamenu.c32.old 将下载的vesamenu.c32拷入，重新启动u盘，可以安装了.</P>
<p>2.选择中文，熟悉的可以选择english,安装模式选择 hard
drive我采用的是u盘，说明下，我的电脑挂了一块160g一个硬盘， 一个 2t
的一块硬盘，还用u盘启动，插了个u盘，给大家介绍下，我的环境第一个盘是sda&nbsp;<wbr>
就是160g那个盘，sdb是 2t那个盘,sdc是u盘。我选择的是sdc1 这个设备，你不确定的话，可以按f2
分别查看下。“安装基本的存储设备”，电脑名称，随便左下角的 “网络配置”给ip 等 都设置好，直接就能上网了。</P>
<p>
3.到了分区这一步，这一步比较复杂，术语很多，有个lvm我还没搞清楚，以后在慢慢学习吧。先解决安装问题吧。以前我有些印象，linux启动需要
/分区 和 &nbsp;<wbr>/boot,只要有这2个分区，就可以启动linux.</P>
<p>我想安装到sdb硬盘上， 所以呢：选择自定义分区：就是以前的手动分区：</P>
<p>/boot&nbsp;<wbr> 系统分区
ext4&nbsp;<wbr>&nbsp;<wbr> 200m&nbsp;<wbr></P>
<p>/分区&nbsp;<wbr> 根分区&nbsp;<wbr>&nbsp;<wbr>
ext4&nbsp;<wbr>&nbsp;<wbr> 0.9t</P>
<p>/swap&nbsp;<wbr>
交换分区&nbsp;<wbr>ext4&nbsp;<wbr>&nbsp;<wbr> 200m
资料介绍内存的2倍，我不知道干啥用的，默认分点得了.</P>
<p>/data&nbsp;<wbr> 数据分区
ext4&nbsp;<wbr>&nbsp;<wbr> 1t&nbsp;<wbr>
因为我要安装mysql数据库，单用一个分区。也可以不用，就分3个分区就可以了.</P>
<p>分区的时候，“包含设备”里面去掉 u盘，我这里也就是sdc一定要注意。</P>
<p>
4.分区后，提示启动系统安装到那里，不要选择u盘，我选择了2t盘也就是sdb来引导程序，写入到主引导mbr硬盘，一定看准了，这里还要说明一下：我装了后，不能启动，后采用修复安装将引导程序按照主板bios启动顺序，选择2t盘就可以了，千万别写入到u盘就行.否则只有靠u盘才能启动.</P>
<p>5.我选择了desktop 有桌面模式，新手，老手可以选择无桌面的basic
server模式，desktop模式rpm包默认1100多个.</P>
<p>
6.重新启动，centos6.5开始启动了，还有些事情要做,一般不允许使用root登录，在此需要建立一个维护账户，也没必要用root用户登录，普通用户登录后可以在"超级终端"里切换到root
用户，然后就ok了。系统装好了。</P>
<p>发现问题:</P>
<p>
1.进入系统，简单查看了下，各个文件夹和文件，上不了网，看见右上角的网络连接没有启动，点击启用网络连接，重新启动后，网络连接又禁用了，看来，centos6.5
每次重新启动，网络连接不会自动启动，需要配置。</P>
<p>配置网卡：ifconfig 看 多个网卡的主机 那个是 up running状态就是连接网线了，</P>
<p>打开 /etc/sysconfig/network-scripts/ifcfg-eth0
这个文件，我用的是绝对位置，你也可以一层cd 命令进入. cd ..
是返回上一层，怎么习惯怎么用，现在我的机器是2个网卡,ifconfig 看了下有一个是link的，所以ifconfig eth0
192.168.0.238 然后 service network restart 就可以了.</P>
<p>通过桌面方式查看ifcfg-eth0这个文件内容，有一行 onboot=no 改为 yes 就可以了。然后我shutdown
-r now</P>
<p>
重新启动下在看下，是否会自动启动网络连接。我重新启动了，嗯自动启动网络连接了，很好,我使用的是putty这个连接工具，我关闭了centos6.5防火墙,使用putty操作，机房远。比较方便.</P>
<p>
2.vi使用：这里如果是终端下，涉及到使用vi编辑器，关于vi的操作，我就会点简单的。不会的可以双击打开文件直接编辑.进入vi后，如果需要编辑那么按a
就可以输入，回车是下一行，下面显示 模式，按 i
也是进入输入模式，如果要返回命令输入模式，那么多按几次esc键，就可以输入命令了，:wq
是保存文件，:q!是退出vi,并且不保存修改，具体看vi的帮助.</P>
<p>=今天就到这里了，等过几天我在把其他方面的记录下来.我先通过桌面模式随便看看，都什么情况。</P>
<p>&nbsp;<wbr></P>
