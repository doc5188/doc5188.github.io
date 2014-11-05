---
layout: post
title: "第六天:centos6.5下&nbsp;samba&nbsp;服务器的安装"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:26
---

<p>今天下雨，闲来无事，学习了下 samba服务器的安装。暂时没包含打印机的共享.</P>
<p>先说下：Windows访问linux分区，和liunx访问windows的ntfs分区</P>
<p>fdisk -l 查看 ntfs Windows分区</P>
<p>&nbsp;<wbr> 挂载win分区<br />
&nbsp;<wbr> mkdir /mnt/windir<br />
&nbsp;<wbr> mount -t auto /dev/hda1&nbsp;<wbr>
/mnt/windir<br />
umount /mnt/windir 不挂在<br />
windows下访问Linux分区可以使用 explore2fs这个软件 很方便的。</P>
<p>再说下&nbsp;<wbr> <strong>/bin,/sbin,/usr/sbin,/usr/bin
目录</STRONG></P>
<p>&nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>这些目录都是存放命令的，首先区别下/sbin和/bin：</P>
<p>&nbsp;<wbr> &nbsp;<wbr> 从命令功能来看，/sbin
下的命令属于基本的系统命令，如shutdown，reboot，用于启动系统，修复系统，/bin下存放一些普通的基本命令，如ls,chmod等，这些命令在Linux系统里的配置文件脚本里经常用到。</P>
<p>&nbsp;<wbr> &nbsp;<wbr>
从用户权限的角度看，/sbin目录下的命令通常只有管理员才可以运行，/bin下的命令管理员和一般的用户都可以使用。</P>
<p>&nbsp;<wbr> &nbsp;<wbr>
从可运行时间角度看，/sbin,/bin能够在挂载其他文件系统前就可以使用。</P>
<p>&nbsp;<wbr> &nbsp;<wbr>而/usr/bin,/usr/sbin与/sbin
/bin目录的区别在于：</P>
<p>&nbsp;<wbr> &nbsp;<wbr>
/bin,/sbin目录是在系统启动后挂载到根文件系统中的，所以/sbin,/bin目录必须和根文件系统在同一分区；</P>
<p>&nbsp;<wbr> &nbsp;<wbr>
/usr/bin,usr/sbin可以和根文件系统不在一个分区。</P>
<p>&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>/usr/sbin存放的一些非必须的系统命令；/usr/bin存放一些用户命令，如led(控制LED灯的)。</P>
<p>&nbsp;<wbr> &nbsp;<wbr> 转下一位网友的解读，个人认为诠释得很到位：</P>
<p><strong>&nbsp;<wbr> &nbsp;<wbr>
/bin</STRONG>是系统的一些指令。bin为binary的简写主要放置一些系统的必备执行档例如:cat、cp、chmod
df、dmesg、gzip、kill、ls、mkdir、more、mount、rm、su、tar等。<br />
<strong>&nbsp;<wbr> &nbsp;<wbr>
/sbin</STRONG>一般是指超级用户指令<strong>。</STRONG>主要放置一些系统管理的必备程式例如:cfdisk、dhcpcd、dump、e2fsck、fdisk、halt、ifconfig、ifup、
ifdown、init、insmod、lilo、lsmod、mke2fs、modprobe、quotacheck、reboot、rmmod、
runlevel、shutdown等。<br />
<strong>&nbsp;<wbr> &nbsp;<wbr>
/usr/bin</STRONG>　是你在后期安装的一些软件的运行脚本。主要放置一些应用软体工具的必备执行档例如c++、g++、gcc、chdrv、diff、dig、du、eject、elm、free、gnome*、
gzip、htpasswd、kfm、ktop、last、less、locale、m4、make、man、mcopy、ncftp、
newaliases、nslookup passwd、quota、smb*、wget等。</P>
<p><strong>&nbsp;<wbr> &nbsp;<wbr>
/usr/sbin&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></STRONG>放置一些用户安装的系统管理的必备程式例如:dhcpd、httpd、imap、in.*d、inetd、lpd、named、netconfig、nmbd、samba、sendmail、squid、swap、tcpd、tcpdump等。<br />

&nbsp;<wbr> &nbsp;<wbr>
如果新装的系统，运行一些很正常的诸如：shutdown，fdisk的命令时，悍然提示：bash:command not
found。那么<br />
&nbsp;<wbr> &nbsp;<wbr> 首先就要考虑root
的$PATH里是否已经包含了这些环境变量。<br />
&nbsp;<wbr> &nbsp;<wbr>
可以查看PATH，如果是：PATH=$PATH:$HOME/bin则需要添加成如下：<br />
&nbsp;<wbr> &nbsp;<wbr>
PATH=$PATH:$HOME/bin:/sbin:/usr/bin:/usr/sbin<br />
============================================================</P>
<p>我使用yum install samba来安装 也可以使用swat实现smb服务器</P>
<p>我首先查了下 yum list samba,名字正确 然后</P>
<p>我 敲入 yum install samba</P>
<p>出现了这些东西:</P>
<p>installing:<br />
samba&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i686&nbsp;<wbr>&nbsp;<wbr>
3.6.9-168.el6_5&nbsp;<wbr> 5.0m<br />
Updating for dependencies:<br />
&nbsp;<wbr>libsmbclient&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i686&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
3.6.9-168.el6_5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
updates&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>&nbsp;<wbr> 1.6 M<br />
&nbsp;<wbr>samba-client&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i686&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
3.6.9-168.el6_5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
updates&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> 11
M<br />
&nbsp;<wbr>samba-common&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i686&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
3.6.9-168.el6_5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
updates&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>&nbsp;<wbr> 9.9 M<br />
&nbsp;<wbr>samba-winbind&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i686&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
3.6.9-168.el6_5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
updates&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>&nbsp;<wbr> 2.1 M<br />
&nbsp;<wbr>samba-winbind-clients&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i686&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
3.6.9-168.el6_5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
updates&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>&nbsp;<wbr> 2.0 M<br />
安装ok后 ,查询下启动状态</P>
<p>service smb status&nbsp;<wbr> 已停<br />
service smb start&nbsp;<wbr>&nbsp;<wbr> 启动<br />
重新启动后 会&nbsp;<wbr> 停止启动smb 需要开机加入启动里<br />
chkconfig --level 345 smb on 加入开机自启动里面</P>
<p>smb打印机共享：/etc/samba/smb.conf&nbsp;<wbr>
,打印机驱动的安装需要安装cups</P>
<p>yum list cups<br />
Loaded plugins: downloadonly, fastestmirror, refresh-packagekit,
security<br />
Loading mirror speeds from cached hostfile<br />
&nbsp;<wbr>* base: mirrors.yun-idc.com<br />
&nbsp;<wbr>* extras: mirrors.yun-idc.com<br />
&nbsp;<wbr>* updates: mirrors.yun-idc.com<br />
Installed Packages<br />
cups.i686&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
1:1.4.2-50.el6_4.5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
@anaconda-CentOS-201311271240.i386/6.5 以后在安装.</P>
<p>&nbsp;<wbr>printcap name = /etc/printcap<br />
&nbsp;<wbr>loaad printers = yes 自动加载共享打印机<br />
默认打印系统是cups 打印机配置文件 /etc/cups/printers.conf<br />
性能配置文件/etc/printcap<br />
windows下访问 <a HREF="file://ip/">\\ip\</A></P>
<p>==============</P>
<p>samba的配置 有2种方式 ： 1.配置/etc/samba/smb.conf&nbsp;<wbr>
2种配置swat文件 我选用smb.conf配置:</P>
<p>我单位小，3部门，所以要有3个组，多少个部门就多少个组. 一个 linux管理组 用于管理,caiwu部门，办公部门. 起名为
linuxz组 ，caiwuz,officez
3个组名,希望每人不希望别人查看，lunuxz可以查看管理所有用户的，公司内有共享资源库给大家无偿使用，只读的，建一个大家随便添加删除的共享文件夹</P>
<p>客户机有多少台就 添加多少个用户名：5台电脑办公，那么就按照人名 pc1,pc2,pc3,pc4,pc5 建立用户名5个</P>
<p>1.每个用户有自有的文件夹：所以先建立每人的目录:</P>
<p>mkdir -p /opt/linuxz</P>
<p>cd /opt/linuxz</P>
<p>mkdir
pc1,pc2,pc3,c4,pc5,资源库单位(all_share_only),大家随便读写用的夹(all_rw)</P>
<p>比如 pc1--pc3 是财务组 那么 财务组名（caiwu）,pc4-pc5 是
销售组(xiaoshou)组名,都需要建立对应的组.</P>
<p>2.添加组名，/usr/sbin/groupadd
linuxz&nbsp;<wbr>&nbsp;<wbr>
我没使用root登录，所以有些命令需要到/sbin下执行。只有普通管理员才能执行/sbin下的命令。</P>
<p>&nbsp;<wbr>其他的组都添加: groupadd pc1 pc2,pc3,pc4,pc5</P>
<p>添加用户名了:多少个电脑都多少个。</P>
<p>adduser -g pc1 -d /opt/linuxz/pc1 -s /sbin/nologin
pc1,明白把，我前面建立了目录这里-d 可以取消了</P>
<p>还有 -s 我加上的目的是不需要shell登录，为了安全把</P>
<p>还有 -G 我没有划分，如果你的单位电脑太多，就可以用他
登录到比如财务组内的成员可以读写的目录，pc1-5可以归类到某个组内&nbsp;<wbr></P>
<p>adduser -g linuxz -G linuxz,pc1,,,pc5 -s /sbin/nologin
linuxz</P>
<p>3.添加smb用户了，最简单的了。修改/etc/samba/smb.conf</P>
<p>&nbsp;<wbr> tdbsam认证 改为
sampasswd认证，其实用那个都可以。用smbpasswd认证存储数据</P>
<p>&nbsp;<wbr> passdb backend =
smbpasswd:/etc/samba/smbpasswd加入这一行,记住</P>
<p>刚才在系统内增加的用户就可以用于smb,只不过是 一个用户名，2套密码，一套系统密码 ，另一套smb密码。</P>
<p>smb这套密码存储在 /etc/samba/smbpasswd内。</P>
<p>service smb restart 就可以了，从新启动服务</P>
<p>修改 smb用户密码： smbpasswd -a 用户名(pc1,pc5,linuxz)</P>
<p>目录权限需要知道下：smb初始建立文件的权限：</P>
<p>&nbsp;<wbr>ll -i 查看下 开头的数字，</P>
<p>0777 4位权限:意思</P>
<p>create mask&nbsp;<wbr> 就是建立文件的预设值<br />
directory mask 就是建立目录的预设置</P>
<p><br />
chmod 755 /opt/linux&nbsp;<wbr>&nbsp;<wbr>
修改管理用户的目录权限<br />
&nbsp;<wbr>chown linuxz:linuxz /opt/linuxz
将/opt/下的linux目录文件的所有者改为用户</P>
<p>linuxz 组为linuxz</P>
<p>&nbsp;<wbr>chmod 2770 pc0*&nbsp;<wbr> 将pc01-pc05
5个目录的权限 2 为屏蔽写权限, 其他用</P>
<p>户没有权限<br />
chown pc01.linux pc01 将 目录pc01的所有者改为 pc01和 linuxz
这2个用户，因为linuxz用户要管理他.</P>
<p>chmod 755 共享资料库</P>
<p>4.修改/etc/samba/smb.conf</P>
<p>[global]</P>
<p>几行</P>
<p>security = share&nbsp;<wbr>
选这个模式，默认user模式，需要输入密码才能进入。费劲，隐私情况下用user行</P>
<p>[linuxz]用户</P>
<p>commnet =注释</P>
<p>path = /opt/linuxz</P>
<p>create mask = 0664</P>
<p>directory mask = 0775</P>
<p>writeable = yes</P>
<p>valid users = linuxz</P>
<p>browseable = yes</P>
<p>[资源库]</P>
<p>path = /opt/linuxz/资料库</P>
<p>writeable = yes</P>
<p>browseable = yes</P>
<p>guest ok = yes</P>
<p>[pc01]</P>
<p>comment =</P>
<p>path = /opt/linuxz/pc01</P>
<p>create mask = 0664</P>
<p>directory mask = 0775</P>
<p>writeable = yes</P>
<p>valid users = pc01,@linuxz （@是组名）</P>
<p>browseable = yes</P>
<p>ok了，重新驱动smb服务</P>
<p>可以看到共享了：但是不能写入文件</P>
<p>关闭防火墙和&nbsp;<wbr> selinux</P>
<p>/etc/selinux/config 关闭 SELINUX=disabled 前面是大写，。后面是小写.</P>
<p>重新启动smb服务。ok了，</P>
<p>还有一种方式不用这么麻烦：直接修改&nbsp;<wbr>smb.conf来设置smaba服务器:</P>
<p>不需要权限管理的简单。建立好要共享的目录，然后修改下smb.conf就可以了.</P>
<p>========打印机驱动的添加：</P>
<p>1.先安装 cups软件 yum install cups</P>
<p>我的安装centos6.5默认安装了 cups</P>
<p>提示我安装了，安装到那了呢？ rpm -qi cups 出现了位置配置等信息.没看出啥 rpm -qc cups
看出来了.</P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
