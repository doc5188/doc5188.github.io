---
layout: post
title: "第八天:centos&nbsp;6.5&nbsp;的&nbsp;vsftpd&nbsp;的配置,用的是pam验证"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:24
---

<p>搞了2天，才初步成功，历经磨难，请大家不要轻易相信百度的东西，天下文章一大抄，一点都不假。</P>
<p>使用 yum install vsftpd<br />
rpm -ql vsftpd<br />
/etc/logrotate.d/vsftpd<br />
/etc/pam.d/vsftpd<br />
/etc/rc.d/init.d/vsftpd<br />
/etc/vsftpd<br />
/etc/vsftpd/ftpusers<br />
/etc/vsftpd/user_list<br />
/etc/vsftpd/vsftpd.conf<br />
/etc/vsftpd/vsftpd_conf_migrate.sh<br />
/usr/sbin/vsftpd<br />
/usr/share/doc/vsftpd-2.2.2/COPYING<br />
/usr/share/doc/vsftpd-2.2.2/EXAMPLE<br />
/usr/share/doc/vsftpd-2.2.2/EXAMPLE/INTERNET_SITE/README<br />
/usr/share/doc/vsftpd-2.2.2/EXAMPLE/INTERNET_SITE/README.configuration<br />

/usr/share/doc/vsftpd-2.2.2/EXAMPLE/INTERNET_SITE/vsftpd.conf<br />
/usr/share/doc/vsftpd-2.2.2/EXAMPLE/INTERNET_SITE/vsftpd.xinetd<br />

/usr/share/doc/vsftpd-</P>
<p>2.2.2/EXAMPLE/INTERNET_SITE_NOINETD/README.configuration<br />
/usr/share/doc/vsftpd-2.2.2/FAQ<br />
/usr/share/doc/vsftpd-2.2.2/INSTALL<br />
/usr/share/doc/vsftpd-2.2.2/LICENSE<br />
/usr/share/doc/vsftpd-2.2.2/README<br />
/usr/share/doc/vsftpd-2.2.2/README.security<br />
/usr/share/doc/vsftpd-2.2.2/REWARD<br />
/usr/share/doc/vsftpd-2.2.2/vsftpd.xinetd<br />
/usr/share/man/man5/vsftpd.conf.5.gz<br />
/usr/share/man/man8/vsftpd.8.gz<br />
/var/ftp<br />
/var/ftp/pub<br />
有些文件省略了 ，看下：<br />
启动了 service vsftpd start<br />
设置为开机启动 chkconfig vsftpd on<br />
在windows看了下 <a HREF="ftp://192.168.0.238/">ftp://192.168.0.238</A>
后目录是pub 没有任何文件，也不能</P>
<p>管理，需要重新看下配置文件了。<br />
ftp首先需要一个管理员用于管理ftp目录内的文件<br />
/usr/sbin/vsftpd 是运行vsftpd的主程序.<br />
/etc/rc.d/init.d/vsftpd是启动脚本文件<br />
/etc/vsftpd/vsftpd.conf 配置文件<br />
/etc/pam.d/vsftpd 验证文件<br />
/etc/vsftpd/user_list 黑名单文件，禁止这里的用户名登录ftp<br />
/var/ftp 匿名用户主目录<br />
/var/ftp/pub 匿名用户下载目录，不需要用户名密码随便登录ftp服务器 的目</P>
<p>录文件<br />
/etc/rc.d/init.d/vsftpd restart
启动vsftpd服务器，这是什么启动方式我忘了，我用的是s启动方式<br />
查看下/var/ftp目录，是属于root用户，并且没有 w权限，安装的时候就已经设</P>
<p>置好了，注意安全。如果权限，用户属于别的组，那么需要 chown root.root</P>
<p>/var/ftp&nbsp;<wbr> 换用户，另外写权限 chmod og -w /var/ftp
注意不能有写权限。<br />
前面我直接登录ftp地址查看那么我就属于匿名用户，系统都建立好了目录. /var/ftp , /var/ftp/pub</P>
<p>还有虚拟用户登录，虚拟用户 映射 linux系统的一个账户来登录，当然了</P>
<p>linux下的账户设置nologin 不允许登录linux系统。<br />
保存一份vsftpd.conf的备份，第一次修改后改的乱七八糟。<br />
yum -y erase vsftpd 又重新安装了 呵呵<br />
&nbsp;<wbr>如果你的单位不需要太多的要求，只要启动vsftpd 就可以了。===ok了.</P>
<p>我就想用虚拟账户登录::</P>
<p>我用guest虚拟用户配置下vsftpd</P>
<p>过程:<br />
&nbsp;<wbr>1. 设置虚拟用户口令文件.acclogin.txt&nbsp;<wbr>
文件名随便起<br />
&nbsp;<wbr>&nbsp;<wbr>
内容:&nbsp;<wbr>&nbsp;<wbr> xiaofu /用户<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
123456 /密码<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
fuwei&nbsp;<wbr> /用于管理<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
123456 /对应密码<br />
&nbsp;<wbr>2.生成虚拟用户口令验证文件,将刚才的文件转换成系统识别的口令验证文件<br />
&nbsp;<wbr> pam认证，著名的linux下的认证系统，比较安全，好像是挺好的认证方式了。<br />
&nbsp;<wbr> db_load -T -t hash -f
/etc/vsftpd/acclogin.txt</P>
<p>/etc/vsftpd/acclogin.db<br />
&nbsp;<wbr> 生成了乱序的acclogin.db认证文件<br />
&nbsp;<wbr>3.编辑vsftpd的PAM认证文件<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
在/etc/pam.d目录下，<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
vi /etc/pam.d/vsftpd<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
将里面其他的都注释掉，添加下面这两行：<br />
auth required /lib/security/pam_userdb.so
db=/etc/vsftpd/account<br />
account required /lib/security/pam_userdb.so
db=/etc/vsftpd/account<br />
&nbsp;<wbr>不需要加入db&nbsp;<wbr><br />
注意：如果是本地用户登录ftp,就不需要添加这两行pam认证,如果是虚拟用户需</P>
<p>要加.因为虚拟用户用到了.db认证<br />
4.建立一个本地用户用于映射.并且设置宿主目录权限<br />
&nbsp;<wbr> 所有的 ftp用户 只需要使用一个系统用户，这个用户不能用于登录linux,所</P>
<p>以不用设置密码。<br />
.添加vsftpd映射用户,<br />
&nbsp;<wbr>useradd -d /var/virtual_usr -s /sbin/nologin
virtual_usr<br />
&nbsp;<wbr>chmod 700 /var/virtual_usr
&nbsp;<wbr><br />
/etc/passwd 看到最后一行加入了一个用户virtual_usr 。<br />
5.修改vim /etc/vsftpd/vsftpd.conf文件 配置guest虚拟用户选项</P>
<p>虚拟用户并不是系统用户，也就是说这些FTP的用户在系统中是不存在的。他们的权限<br />
其实是集中寄托在一个在系统中的某一个用户身上的，所谓Vsftpd的虚拟宿主用户，就是这样一个支持着所有虚拟用户的宿主用户。由于他支撑了FTP的所有虚拟的用户，那么他本身的权限将会影响着这些虚拟的用户，因此，处于安全性的考虑，也要<br />

注意对该用户的权限的控制，该用户也绝对没有登陆系统的必要，这里也设定他为不能登陆系统的用户。</P>
<p># Example config file /etc/vsftpd/vsftpd.conf<br />
# The default compiled in settings are fairly paranoid. This sample
file<br />
# loosens things up a bit, to make the ftp daemon more
usable.<br />
# Please see vsftpd.conf.5 for all compiled in defaults.<br />
#<br />
# READ THIS: This example file is NOT an exhaustive list of vsftpd
options.<br />
# Please read the vsftpd.conf.5 manual page to get a full idea of
vsftpd's<br />
# capabilities.<br />
#<br />
# Allow anonymous FTP? (Beware - allowed by default if you comment
this out).<br />
#anonymous_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">anonymous_enable=NO<br /></FONT>#设定不允许匿名访问,实际环境可以开放匿名用户的登录。<br />

# Uncomment this to allow local users to log in.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">local_enable=YES<br /></FONT>#设定本地用户可以访问。注意：主要是为虚拟宿主用户，如果该项目设定为NO那么所有虚拟用户将无法访问。<br />

#<br />
# Uncomment this to enable any form of FTP write command.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">write_enable=YES<br /></FONT>#设定可以进行写操作。<br />

#<br />
# Default umask for local users is 077. You may wish to change this
to 022,<br />
# if your users expect that (022 is used by most other
ftpd's)<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">local_umask=022</FONT><br />
#设定上传后文件的权限掩码。<br />
#<br />
# Uncomment this to allow the anonymous FTP user to upload files.
This only<br />
# has an effect if the above global write enable is activated.
Also, you will<br />
# obviously need to create a directory writable by the FTP
user.<br />
#anon_upload_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">anon_upload_enable=NO<br /></FONT>#禁止匿名用户上传。<br />

#<br />
# Uncomment this if you want the anonymous FTP user to be able to
create<br />
# new directories.<br />
#anon_mkdir_write_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">anon_mkdir_write_enable=NO<br /></FONT>#禁止匿名用户建立目录。<br />

#<br />
# Activate directory messages - messages given to remote users when
they<br />
# go into a certain directory.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">dirmessage_enable=YES<br /></FONT>#设定开启目录标语功能。<br />

#<br />
# Activate logging of uploads/downloads.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">xferlog_enable=YES</FONT><br />
#设定开启日志记录功能。<br />
#<br />
# Make sure PORT transfer connections originate from port 20
(ftp-data).<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">connect_from_port_20=YES</FONT><br />

#设定端口20进行数据连接。<br />
#<br />
# If you want, you can arrange for uploaded anonymous files to be
owned by<br />
# a different user. Note! Using "root" for uploaded files is
not<br />
# recommended!<br />
#chown_uploads=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chown_uploads=NO</FONT><br />
#设定禁止上传文件更改宿主。</P>
<p><br />
#chown_username=whoever</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chroot_local_user=YES<br /></FONT>#设定登陆后.只可以访问自己的属主目录.不可访问上一层目录文件</P>
<p># You may override where the log file goes if you like. The
default is shown<br />
# below.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">xferlog_file=/var/log/vsftpd.log<br />
</FONT>#设定Vsftpd的服务日志保存路径。注意，该文件默认不存在。必须要手动touch出来，并且由于这里更改了Vsftpd的服务宿主用户为手动建立的Vsftpd。必须注意给与该用户对日志的写入权限，否则服务将启动失败。<br />

#<br />
# If you want, you can have your log file in standard ftpd xferlog
format<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">xferlog_std_format=YES<br /></FONT>#设定日志使用标准的记录格式。<br />

#<br />
# You may change the default value for timing out an idle
session.<br />
#idle_session_timeout=600<br />
#设定空闲连接超时时间，这里使用默认。将具体数值留给每个具体用户具体指定，当然如果不指定的话，还是使用这里的默认值600，单位秒。<br />

#<br />
# You may change the default value for timing out a data
connection.<br />
#data_connection_timeout=120<br />
#设定单次最大连续传输时间，这里使用默认。将具体数值留给每个具体用户具体指定，当然如果不指定的话，还是使用这里的默认值120，单位秒。<br />

#<br />
# It is recommended that you define on your system a unique user
which the<br />
# ftp server can use as a totally isolated and unprivileged
user.<br />
#nopriv_user=ftpsecure<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">nopriv_user=vsftpd<br /></FONT>#设定支撑Vsftpd服务的宿主用户为手动建立的Vsftpd用户。注意，一旦做出更改宿主用户后，必须注意一起与该服务相关的读写文件的读写赋权问题。比如日志文件就必须给与该用户写入权限等。<br />

#<br />
# Enable this and the server will recognise asynchronous ABOR
requests. Not<br />
# recommended for security (the code is non-trivial). Not enabling
it,<br />
# however, may confuse older FTP clients.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">async_abor_enable=YES</FONT><br />

#设定支持异步传输功能。<br />
#<br />
# By default the server will pretend to allow ASCII mode but in
fact ignore<br />
# the request. Turn on the below options to have the server
actually do ASCII<br />
# mangling on files when in ASCII mode.<br />
# Beware that on some FTP servers, ASCII support allows a denial of
service<br />
# attack (DoS) via the command "SIZE /big/file" in ASCII mode.
vsftpd<br />
# predicted this attack and has always been safe, reporting the
size of the<br />
# raw file.<br />
# ASCII mangling is a horrible feature of the protocol.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">ascii_upload_enable=YES<br />
ascii_download_enable=YES<br /></FONT>#设定支持ASCII模式的上传和下载功能。<br />
#<br />
# You may fully customise the login banner string:<br />
<font STYLE="BACKGroUnD-CoLor: rgb(0,255,0)">#ftpd_banner=Welcome<br /></FONT>#设定Vsftpd的登陆语。<br />

#<br />
# You may specify a file of disallowed anonymous e-mail addresses.
Apparently<br />
# useful for combatting certain DoS attacks.<br />
#deny_email_enable=YES<br />
# (default follows)<br />
#banned_email_file=/etc/vsftpd/banned_emails<br />
#<br />
# You may specify an explicit list of local users to chroot() to
their home<br />
# directory. If chroot_local_user is YES, then this list becomes a
list of<br />
# users to NOT chroot().<br />
#chroot_list_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chroot_list_enable=NO</FONT><br />

#禁止用户登出自己的FTP主目录。<br />
# (default follows)<br />
#chroot_list_file=/etc/vsftpd/chroot_list<br />
#<br />
# You may activate the "-R" option to the builtin ls. This is
disabled by<br />
# default to avoid remote users being able to cause excessive I/O
on large<br />
# sites. However, some broken FTP clients such as "ncftp" and
"mirror" assume<br />
# the presence of the "-R" option, so there is a strong case for
enabling it.<br />
#ls_recurse_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">ls_recurse_enable=NO<br /></FONT>#禁止用户登陆FTP后使用"ls
-R"的命令。该命令会对服务器性能造成巨大开销。如果该项被允许，那么挡多用户同时使用该命令时将会对该服务器造成威胁。<br />
# When "listen" directive is enabled, vsftpd runs in standalone
mode and<br />
# listens on IPv4 sockets. This directive cannot be used in
conjunction<br />
# with the listen_ipv6 directive.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">listen=YES<br /></FONT>#设定该Vsftpd服务工作在StandAlone模式下。顺便展开说明一下，所谓StandAlone模式就是该服务拥有自己的守护进程支持，在ps
-A命令下我们将可用看到vsftpd的守护进程名。如果不想工作在StandAlone模式下，则可以选择SuperDaemon模式，在该模式下vsftpd将没有自己的守护进程，而是由超级守护进程Xinetd全权代理，与此同时，Vsftp服务的许多功能将得不到实现。<br />

#<br />
# This directive enables listening on IPv6 sockets. To listen on
IPv4 and IPv6<br />
# sockets, you must run two copies of vsftpd whith two
configuration files.<br />
# Make sure, that one of the listen options is commented !!<br />
#listen_ipv6=YES</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">pam_service_name=vsftpd.vu&nbsp;<wbr>
//我重新启动了认证文件，没用自带的.这要注意</FONT><br />
#设定PAM服务下Vsftpd的验证配置文件名。因此，PAM验证将参考/etc/pam.d/下的vsftpd文件配置。<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">userlist_enable=YES<br /></FONT>#设定userlist_file中的用户将不得使用FTP。<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">tcp_wrappers=YES<br /></FONT>#设定支持TCP
Wrappers。#KC: The following entries are added for supporting
virtual ftp
users.以下这些是关于Vsftpd虚拟用户支持的重要配置项目。默认Vsftpd.conf中不包含这些设定项目，需要自己手动添加配置。</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">guest_enable=YES<br /></FONT>设定启用虚拟用户功能。<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">guest_username=virtual_usr<br /></FONT>指定虚拟用户的宿主用户。<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">virtual_use_local_privs=YES<br />
</FONT>设定虚拟用户的权限符合他们的宿主用户。<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">user_config_dir=/etc/vsftpd/v_conf<br />
</FONT>设定虚拟用户个人Vsftp的配置文件存放路径。也就是说，这个被指定的目录里，将存放每个Vsftp虚拟用户个性的配置文件，<br />

一个需要注意的地方就是这些配置文件名必须和虚拟用户名相同。保存退出。</P>
<p>..看配置需要加个配置日志文件&nbsp;<wbr> touch /var/log/</P>
<p>6.对每个虚拟用户进行权限配置<br />
在末行加上 user_config_dir=每个用户配置文件目录&nbsp;<wbr> 我的就是<br />
eg:我的: user_config_dir=v_conf</P>
<p>7这就需要在/var/virtual_usr下 建立用户名我的fuwei 和 xiaofu<br />
&nbsp;<wbr>在/etc/vsftpd/v_conf下 建立对应的 用户名文件<br />
&nbsp;<wbr>6. 给虚拟用户配置权限文件<br />
/var/virtual_usr/fuwei：虚拟用户登录目录<br />
别忘了设置权限（文件是root用户创建虚拟用户没有写入权限）chown -R</P>
<p>virtual_usr.virtual_usr /var/virtual_usr/fuwei<br />
/etc/vsftpd/v_conf 下给每个用户创建个权限文件，这个文件要和虚拟用户名</P>
<p>称相同<br />
例子：</P>
<p>文件名：fuwei<br />
local_root=/var/virtual_usr/fuwei&nbsp;<wbr> (FTP用户fuwei
的登陆目录文件),就是各自回各自的家<br />
anonymous_enable=NO<br />
write_enable=YES<br />
local_umask=022<br />
anon_upload_enable=NO<br />
anon_mkdir_write_enable=NO<br />
idle_session_timeout=300<br />
data_connection_timeout=90<br />
max_clients=1<br />
max_per_ip=1<br />
local_max_rate=25000<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
======</P>
<p>文件名：xiaofu</P>
<p>local_root=/var/virtual_usr/xiaofu&nbsp;<wbr>
(FTP用户xiaofu的登陆目录文件)就是各自回各自的家里<br />
<br />
anonymous_enable=NO<br />
write_enable=YES<br />
local_umask=022<br />
anon_upload_enable=NO<br />
anon_mkdir_write_enable=NO<br />
idle_session_timeout=300<br />
data_connection_timeout=90<br />
max_clients=1<br />
max_per_ip=1<br />
local_max_rate=25000<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
======<br />
如果不能登录，查看 /var/log/secure日志</P>
<p>ls -a 显示隐藏文件<br />
/etc/vsftpd/下 建立 message</P>
<p>最后总结:
研究了二天，用于映射虚拟用户登录的宿主用户不能建立在/home目录下。这一点网上的文章都是在东抄西抄的，都没经过实战.
ok我的虚拟用户pam验证就结束了.</P>
<p>==单独配置每个虚拟用户的时候，发现不能上传，需要将各自的用户目录，chown virutual_usr
给这个ftp用户才能上传建立目录等。root所有者的话不行，不能上传，新建目录，切记.</P>
<p>&nbsp;<wbr></P>
<p><br />
========最后，我转摘一下网上的留作备份，</P>
<div STYLE="Line-HeiGHT: 160%; FonT-siZe: 14px">
<p>CentOS 6.3下安装Vsftp，虚拟用户<br />
一.安装：<br />
1.安装Vsftpd服务相关部件：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">yum install
vsftpd*<br /></FONT>Dependencies Resolved<br />
=============================================================================</P>
<p><br />
Package&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Arch&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Version&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Repository&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Size<br />
=============================================================================<br />

Installing:<br />
vsftpd&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i386&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
2.0.5-10.el5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
137 kTransaction Summary<br />
=============================================================================<br />

Install&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
1
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

Update&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

Remove&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0 Package(s)&nbsp;<wbr><br />
2.确认安装PAM服务相关部件：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">yum install pam*</FONT><br />
Dependencies Resolved<br />
=============================================================================<br />

Package&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Arch&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Version&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Repository&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Size<br />
=============================================================================<br />

Installing:<br />
pam-devel&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i386&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0.99.6.2-3.14.el5
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
186 kTransaction Summary<br />
=============================================================================<br />

Install&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
1
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

Update&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

Remove&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

开发包，其实不装也没有关系，主要的目的是确认PAM。<br />
3.安装DB4部件包：<br />
这里要特别安装一个db4的包，用来支持文件数据库。<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">yum install
db4*<br /></FONT>Dependencies Resolved<br />
=============================================================================<br />

Package&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Arch&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Version&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Repository&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
Size<br />
=============================================================================<br />

Installing:<br />
db4-devel&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i386&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
4.3.29-9.fc6&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
2.0 M<br />
db4-java&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i386&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
4.3.29-9.fc6&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
1.7 M<br />
db4-tcl&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i386&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
4.3.29-9.fc6&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
1.0 M<br />
db4-utils&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
i386&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
4.3.29-9.fc6&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
119 kTransaction Summary<br />
=============================================================================<br />

Install&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
4
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

Update&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

Remove&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
0
Package(s)&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr><br />

二.系统帐户<br />
1.建立Vsftpd服务的宿主用户：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">useradd vsftpd -s
/sbin/nologin</FONT></P>
<p>
默认的Vsftpd的服务宿主用户是root，但是这不符合安全性的需要。这里建立名字为vsftpd的用户，用他来作为支持Vsftpd的<br />

服务宿主用户。由于该用户仅用来支持Vsftpd服务用，因此没有许可他登陆系统的必要，并设定他为不能登陆系统的用户。</P>
<p>2.建立Vsftpd虚拟宿主用户：<br />
[root@linuxidc.com nowhere]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">useradd virtusers -s
/sbin/nologin</FONT></P>
<p>
本篇主要是介绍Vsftp的虚拟用户，虚拟用户并不是系统用户，也就是说这些FTP的用户在系统中是不存在的。他们的总体权限<br />
其实是集中寄托在一个在系统中的某一个用户身上的，所谓Vsftpd的虚拟宿主用户，就是这样一个支持着所有虚拟用户的宿主<br />
用户。由于他支撑了FTP的所有虚拟的用户，那么他本身的权限将会影响着这些虚拟的用户，因此，处于安全性的考虑，也要<br />
非分注意对该用户的权限的控制，该用户也绝对没有登陆系统的必要，这里也设定他为不能登陆系统的用户。</P>
<p>三.调整Vsftpd的配置文件：<br />
1.编辑配置文件前先备份<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">cp /etc/vsftpd/vsftpd.conf
/etc/vsftpd/vsftpd.conf.bak</FONT></P>
<p>编辑主配置文件Vsftpd.conf</P>
<p>[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">vi
/etc/vsftpd/vsftpd.conf</FONT></P>
<p>
这里我将原配置文件的修改完全记录，凡是修改的地方我都会保留注释原来的配置。其中加入我对每条配置项的认识，对于一些比较关键的配置项这里我做了我的观点，并且原本英语的说明我也不删除，供参考对比用。<br />

------------------------------------------------------------------------------<br />

# Example config file /etc/vsftpd/vsftpd.conf<br />
#<br />
# The default compiled in settings are fairly paranoid. This sample
file<br />
# loosens things up a bit, to make the ftp daemon more
usable.<br />
# Please see vsftpd.conf.5 for all compiled in defaults.<br />
#<br />
# READ THIS: This example file is NOT an exhaustive list of vsftpd
options.<br />
# Please read the vsftpd.conf.5 manual page to get a full idea of
vsftpd's<br />
# capabilities.<br />
#<br />
# Allow anonymous FTP? (Beware - allowed by default if you comment
this out).<br />
#anonymous_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">anonymous_enable=NO<br /></FONT>#设定不允许匿名访问,实际环境可以开放匿名用户的登录。<br />

#<br />
# Uncomment this to allow local users to log in.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">local_enable=YES<br /></FONT>#设定本地用户可以访问。注意：主要是为虚拟宿主用户，如果该项目设定为NO那么所有虚拟用户将无法访问。<br />

#<br />
# Uncomment this to enable any form of FTP write command.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">write_enable=YES<br /></FONT>#设定可以进行写操作。<br />

#<br />
# Default umask for local users is 077. You may wish to change this
to 022,<br />
# if your users expect that (022 is used by most other
ftpd's)<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">local_umask=022</FONT><br />
#设定上传后文件的权限掩码。<br />
#<br />
# Uncomment this to allow the anonymous FTP user to upload files.
This only<br />
# has an effect if the above global write enable is activated.
Also, you will<br />
# obviously need to create a directory writable by the FTP
user.<br />
#anon_upload_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">anon_upload_enable=NO<br /></FONT>#禁止匿名用户上传。<br />

#<br />
# Uncomment this if you want the anonymous FTP user to be able to
create<br />
# new directories.<br />
#anon_mkdir_write_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">anon_mkdir_write_enable=NO<br /></FONT>#禁止匿名用户建立目录。<br />

#<br />
# Activate directory messages - messages given to remote users when
they<br />
# go into a certain directory.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">dirmessage_enable=YES<br /></FONT>#设定开启目录标语功能。<br />

#<br />
# Activate logging of uploads/downloads.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">xferlog_enable=YES</FONT><br />
#设定开启日志记录功能。<br />
#<br />
# Make sure PORT transfer connections originate from port 20
(ftp-data).<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">connect_from_port_20=YES</FONT><br />

#设定端口20进行数据连接。<br />
#<br />
# If you want, you can arrange for uploaded anonymous files to be
owned by<br />
# a different user. Note! Using "root" for uploaded files is
not<br />
# recommended!<br />
#chown_uploads=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chown_uploads=NO</FONT><br />
#设定禁止上传文件更改宿主。</P>
<p><br />
#chown_username=whoever</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chroot_local_user=YES<br /></FONT>#设定登陆后.只可以访问自己的属主目录.不可访问上一层目录文件</P>
<p># You may override where the log file goes if you like. The
default is shown<br />
# below.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">xferlog_file=/var/log/vsftpd.log<br />
</FONT>#设定Vsftpd的服务日志保存路径。注意，该文件默认不存在。必须要手动touch出来，并且由于这里更改了Vsftpd的服务宿主用户为手动建立的Vsftpd。必须注意给与该用户对日志的写入权限，否则服务将启动失败。<br />

#<br />
# If you want, you can have your log file in standard ftpd xferlog
format<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">xferlog_std_format=YES<br /></FONT>#设定日志使用标准的记录格式。<br />

#<br />
# You may change the default value for timing out an idle
session.<br />
#idle_session_timeout=600<br />
#设定空闲连接超时时间，这里使用默认。将具体数值留给每个具体用户具体指定，当然如果不指定的话，还是使用这里的默认值600，单位秒。<br />

#<br />
# You may change the default value for timing out a data
connection.<br />
#data_connection_timeout=120<br />
#设定单次最大连续传输时间，这里使用默认。将具体数值留给每个具体用户具体指定，当然如果不指定的话，还是使用这里的默认值120，单位秒。<br />

#<br />
# It is recommended that you define on your system a unique user
which the<br />
# ftp server can use as a totally isolated and unprivileged
user.<br />
#nopriv_user=ftpsecure<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">nopriv_user=vsftpd<br /></FONT>#设定支撑Vsftpd服务的宿主用户为手动建立的Vsftpd用户。注意，一旦做出更改宿主用户后，必须注意一起与该服务相关的读写文件的读写赋权问题。比如日志文件就必须给与该用户写入权限等。<br />

#<br />
# Enable this and the server will recognise asynchronous ABOR
requests. Not<br />
# recommended for security (the code is non-trivial). Not enabling
it,<br />
# however, may confuse older FTP clients.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">async_abor_enable=YES</FONT><br />

#设定支持异步传输功能。<br />
#<br />
# By default the server will pretend to allow ASCII mode but in
fact ignore<br />
# the request. Turn on the below options to have the server
actually do ASCII<br />
# mangling on files when in ASCII mode.<br />
# Beware that on some FTP servers, ASCII support allows a denial of
service<br />
# attack (DoS) via the command "SIZE /big/file" in ASCII mode.
vsftpd<br />
# predicted this attack and has always been safe, reporting the
size of the<br />
# raw file.<br />
# ASCII mangling is a horrible feature of the protocol.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">ascii_upload_enable=YES<br />
ascii_download_enable=YES<br /></FONT>#设定支持ASCII模式的上传和下载功能。<br />
#<br />
# You may fully customise the login banner string:<br />
<font STYLE="BACKGroUnD-CoLor: rgb(0,255,0)">ftpd_banner=Welcome to
blah FTP service ^_^<br /></FONT>#设定Vsftpd的登陆标语。<br />
#<br />
# You may specify a file of disallowed anonymous e-mail addresses.
Apparently<br />
# useful for combatting certain DoS attacks.<br />
#deny_email_enable=YES<br />
# (default follows)<br />
#banned_email_file=/etc/vsftpd/banned_emails<br />
#<br />
# You may specify an explicit list of local users to chroot() to
their home<br />
# directory. If chroot_local_user is YES, then this list becomes a
list of<br />
# users to NOT chroot().<br />
#chroot_list_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chroot_list_enable=NO</FONT><br />

#禁止用户登出自己的FTP主目录。<br />
# (default follows)<br />
#chroot_list_file=/etc/vsftpd/chroot_list<br />
#<br />
# You may activate the "-R" option to the builtin ls. This is
disabled by<br />
# default to avoid remote users being able to cause excessive I/O
on large<br />
# sites. However, some broken FTP clients such as "ncftp" and
"mirror" assume<br />
# the presence of the "-R" option, so there is a strong case for
enabling it.<br />
#ls_recurse_enable=YES<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">ls_recurse_enable=NO<br /></FONT>#禁止用户登陆FTP后使用"ls
-R"的命令。该命令会对服务器性能造成巨大开销。如果该项被允许，那么挡多用户同时使用该命令时将会对该服务器造成威胁。<br />
# When "listen" directive is enabled, vsftpd runs in standalone
mode and<br />
# listens on IPv4 sockets. This directive cannot be used in
conjunction<br />
# with the listen_ipv6 directive.<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">listen=YES<br /></FONT>#设定该Vsftpd服务工作在StandAlone模式下。顺便展开说明一下，所谓StandAlone模式就是该服务拥有自己的守护进程支持，在ps
-A命令下我们将可用看到vsftpd的守护进程名。如果不想工作在StandAlone模式下，则可以选择SuperDaemon模式，在该模式下vsftpd将没有自己的守护进程，而是由超级守护进程Xinetd全权代理，与此同时，Vsftp服务的许多功能将得不到实现。<br />

#<br />
# This directive enables listening on IPv6 sockets. To listen on
IPv4 and IPv6<br />
# sockets, you must run two copies of vsftpd whith two
configuration files.<br />
# Make sure, that one of the listen options is commented !!<br />
#listen_ipv6=YES</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">pam_service_name=vsftpd</FONT><br />

#设定PAM服务下Vsftpd的验证配置文件名。因此，PAM验证将参考/etc/pam.d/下的vsftpd文件配置。<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">userlist_enable=YES<br /></FONT>#设定userlist_file中的用户将不得使用FTP。<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">tcp_wrappers=YES<br /></FONT>#设定支持TCP
Wrappers。#KC: The following entries are added for supporting
virtual ftp
users.以下这些是关于Vsftpd虚拟用户支持的重要配置项目。默认Vsftpd.conf中不包含这些设定项目，需要自己手动添加配置。</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">guest_enable=YES<br /></FONT>设定启用虚拟用户功能。<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">guest_username=virtusers<br /></FONT>指定虚拟用户的宿主用户。<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">virtual_use_local_privs=YES<br />
</FONT>设定虚拟用户的权限符合他们的宿主用户。<br />
<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">user_config_dir=/etc/vsftpd/vconf<br />
</FONT>设定虚拟用户个人Vsftp的配置文件存放路径。也就是说，这个被指定的目录里，将存放每个Vsftp虚拟用户个性的配置文件，<br />

一个需要注意的地方就是这些配置文件名必须和虚拟用户名相同。保存退出。</P>
<p>3.建立Vsftpd的日志文件，并更该属主为Vsftpd的服务宿主用户（这一步可以放在修改配置表前面）：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">touch
/var/log/vsftpd.log</FONT><br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chown vsftpd.vsftpd
/var/log/vsftpd.log</FONT></P>
<p>4.建立虚拟用户配置文件存放路径：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">mkdir
/etc/vsftpd/vconf/</FONT></P>
<p>三.制作虚拟用户数据库文件<br />
1.先建立虚拟用户名单文件：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">touch
/etc/vsftpd/virtusers<br /></FONT>建立了一个虚拟用户名单文件，这个文件就是来记录vsftpd虚拟用户的用户名和口令的数据文件，<br />

这里给它命名为virtusers。为了避免文件的混乱，我把这个名单文件就放置在/etc/vsftpd/下。</P>
<p>2.编辑虚拟用户名单文件：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">vi
/etc/vsftpd/virtusers</FONT><br />
----------------------------<br />
ftp001<br />
123456<br />
ftp002<br />
123456<br />
ftp003<br />
123456<br />
----------------------------<br />
编辑这个虚拟用户名单文件，在其中加入用户的用户名和口令信息。格式很简单：“一行用户名，一行口令”。3.生成虚拟用户数据文件：<br />

[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">db_load -T -t hash -f
/etc/vsftpd/virtusers /etc/vsftpd/virtusers.db</FONT><br />
这里我顺便把这个命令简单说明一下<br />
----------------------------------------------------------------------<br />

4.察看生成的虚拟用户数据文件<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">ll
/etc/vsftpd/virtusers.db<br /></FONT>-rw-r--r-- 1 root root 12288
Sep 16 03:51 /etc/vsftpd/virtusers.db<br />
需要特别注意的是，以后再要添加虚拟用户的时候，只需要按照“一行用户名，一行口令”的格式将新用户名和口令添加进虚拟用户名单文件。但是光这样做还不够，不会生效的哦！还要再执行一遍“
db_load -T -t hash -f 虚拟用户名单文件虚拟用户数据库文件.db ”的上述命令使其生效才可以！</P>
<p>四.设定PAM验证文件，并指定虚拟用户数据库文件进行读取<br />
1.察看原来的Vsftp的PAM验证配置文件：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">cat
/etc/pam.d/vsftpd</FONT><br />
----------------------------------------------------------------<br />

#%PAM-1.0<br />
session&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
optional&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
pam_keyinit.so&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
force revoke<br />
auth&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
pam_listfile.so item=user sense=deny file=/etc/vsftpd/ftpusers
onerr=succeed<br />
auth&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
pam_shells.so<br />
auth&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
include&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
system-auth<br />
account&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
include&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
system-auth<br />
session&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
include&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
system-auth<br />
session&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
pam_loginuid.so<br />
----------------------------------------------------------------</P>
<p>2.在编辑前做好备份：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">cp /etc/pam.d/vsftpd
/etc/pam.d/vsftpd.backup</FONT></P>
<p>3.编辑Vsftpd的PAM验证配置文件<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">vi
/etc/pam.d/vsftpd</FONT><br />
----------------------------------------------------------------<br />

#%PAM-1.0<br />
auth&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
/lib/security/pam_userdb.so&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
db=/etc/vsftpd/virtusers<br />
account
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
/lib/security/pam_userdb.so&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
db=/etc/vsftpd/virtusers<br />
以上两条是手动添加的，上面的全部加#注释了.内容是对虚拟用户的安全和帐户权限进行验证。<br />
!!!!!!!这里有个要注意说明的:如果系统是64位系统在这里的所有lib后面要加入64!!!!!!<br />
!!!!!!!如下这样才可以:</P>
<p>#%PAM-1.0<br />
auth&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
/lib64/security/pam_userdb.so&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
db=/etc/vsftpd/virtusers<br />
account
required&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
/lib64/security/pam_userdb.so&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
db=/etc/vsftpd/virtusers</P>
<p>五.虚拟用户的配置<br />
1.规划好虚拟用户的主路径：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">mkdir /var/ftp/</FONT></P>
<p>2.建立测试用户的FTP用户目录：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">mkdir /var/ftp/ftp001
/var/ftp/ftp002 /var/ftp/ftp003</FONT></P>
<p>3.建立虚拟用户配置文件模版：</P>
<p><br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">cp /etc/vsftpd/vsftpd.conf.bak
/etc/vsftpd/vconf/vconf.tmp4</FONT>.定制虚拟用户模版配置文件：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">vi
/etc/vsftpd/vconf/vconf.tmp<br /></FONT>--------------------------------<br />

<font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">local_root=/opt/vsftp/virtuser</FONT><br />

virtuser 这个就是以后要指定虚拟的具体主路径。<br />
anonymous_enable=NO<br />
设定不允许匿名用户访问。<br />
write_enable=YES<br />
设定允许写操作。<br />
local_umask=022<br />
设定上传文件权限掩码。<br />
anon_upload_enable=NO<br />
设定不允许匿名用户上传。<br />
anon_mkdir_write_enable=NO<br />
设定不允许匿名用户建立目录。<br />
idle_session_timeout=600&nbsp;<wbr>&nbsp;<wbr>
(根据用户要求.可选)<br />
设定空闲连接超时时间。<br />
data_connection_timeout=120<br />
设定单次连续传输最大时间。<br />
max_clients=10&nbsp;<wbr>&nbsp;<wbr>
(根据用户要求.可选)<br />
设定并发客户端访问个数。<br />
max_per_ip=5&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
(根据用户要求.可选)<br />
设定单个客户端的最大线程数，这个配置主要来照顾Flashget、迅雷等多线程下载软件。<br />
local_max_rate=50000&nbsp;<wbr>&nbsp;<wbr>
(根据用户要求.可选)<br />
设定该用户的最大传输速率，单位b/s。<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
--------------------------------</P>
<p>范例</P>
<p>local_root=/var/ftp/ftp001<br />
#这个就是以后要指定虚拟的具体主路径。<br />
anonymous_enable=NO<br />
#设定不允许匿名用户访问。<br />
write_enable=YES<br />
#设定允许写操作。<br />
local_umask=022<br />
#设定上传文件权限掩码。<br />
#anon_upload_enable=YES<br />
#设定不允许匿名用户上传。<br />
anon_mkdir_write_enable=YES<br />
#设定不允许匿名用户建立目录。<br />
idle_session_timeout=600<br />
#设定空闲连接超时时间。<br />
data_connection_timeout=120<br />
#设定单次连续传输最大时间。<br />
max_clients=10<br />
#设定并发客户端访问个数。<br />
max_per_ip=10<br />
#设定单个客户端的最大线程数，这个配置主要来照顾Flashget、迅雷等多线程下载软件。<br />
#local_max_rate=50000<br />
#设定该用户的最大传输速率，单位b/s。<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
virtual_use_local_privs=NO<br />
anon_world_readable_only=NO<br />
anon_upload_enable=YES<br />
local_root=/var/ftp/ftp001<br />
#这个就是以后要指定虚拟的具体主路径。<br />
anonymous_enable=NO<br />
#设定不允许匿名用户访问。<br />
write_enable=YES<br />
#设定允许写操作。<br />
local_umask=022<br />
#设定上传文件权限掩码。<br />
#anon_upload_enable=YES<br />
#设定不允许匿名用户上传。<br />
anon_mkdir_write_enable=YES<br />
#设定不允许匿名用户建立目录。<br />
idle_session_timeout=600<br />
#设定空闲连接超时时间。<br />
data_connection_timeout=120<br />
#设定单次连续传输最大时间。<br />
max_clients=10<br />
#设定并发客户端访问个数。<br />
max_per_ip=10<br />
#设定单个客户端的最大线程数，这个配置主要来照顾Flashget、迅雷等多线程下载软件。<br />
#local_max_rate=50000<br />
#设定该用户的最大传输速率，单位b/s。<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
virtual_use_local_privs=NO<br />
anon_world_readable_only=NO</P>
<p>特权用户：</P>
<p>local_root=/var/ftp/<br />
#这个就是以后要指定虚拟的具体主路径。<br />
anonymous_enable=NO<br />
#设定不允许匿名用户访问。<br />
write_enable=YES<br />
#设定允许写操作。<br />
local_umask=022<br />
#设定上传文件权限掩码。<br />
#anon_upload_enable=YES<br />
#设定不允许匿名用户上传。<br />
anon_mkdir_write_enable=YES<br />
#设定不允许匿名用户建立目录。<br />
idle_session_timeout=600<br />
#设定空闲连接超时时间。<br />
data_connection_timeout=120<br />
#设定单次连续传输最大时间。<br />
max_clients=10<br />
#设定并发客户端访问个数。<br />
max_per_ip=10<br />
#设定单个客户端的最大线程数，这个配置主要来照顾Flashget、迅雷等多线程下载软件。<br />
#local_max_rate=50000<br />
#设定该用户的最大传输速率，单位b/s。<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
anon_world_readable_only=NO<br />
virtual_use_local_privs=YES</P>
<p>&nbsp;<wbr></P>
<p>
anon_upload_enable=YES这里将原vsftpd.conf配置文件经过简化后保存作为虚拟用户配置文件的模版。这里将并不需要指定太多的配置内容，主要的<br />

框架和限制交由Vsftpd的主配置文件vsftpd.conf来定义，即虚拟用户配置文件当中没有提到的配置项目将参考主配置文件中的设定。而在这里作为虚拟用户的配置文件模版只需要留一些和用户流量控制，访问方式控制的配置项目就可以了。这里的关键项是local_root这个配置，用来指定这个虚拟用户的FTP主路径。5.更改虚拟用户的主目录的属主为虚拟宿主用户：<br />

[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chown -R virtusers.virtusers
/var/ftp/</FONT></P>
<p>6.检查权限：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">ll /var/ftp/<br /></FONT>total
24<br />
drwxr-xr-x 2 overlord overlord 4096 Sep 16 05:14 ftp001<br />
drwxr-xr-x 2 overlord overlord 4096 Sep 16 05:00 ftp002<br />
drwxr-xr-x 2 overlord overlord 4096 Sep 16 05:00 ftp003<br />
六.给测试用户定制：<br />
1.从虚拟用户模版配置文件复制：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">cp /etc/vsftpd/vconf/vconf.tmp
/etc/vsftpd/vconf/ftp001<br /></FONT>2.针对具体用户进行定制：<br />
[root@linuxidc.com ~]# <font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">vi
/etc/vsftpd/vconf/ftp001</FONT><br />
---------------------------------</P>
<p><br />
local_root=/opt/vsftp/ftp001&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
(FTP用户ftp001 的登陆目录文件)<br />
anonymous_enable=NO<br />
write_enable=YES<br />
local_umask=022<br />
anon_upload_enable=NO<br />
anon_mkdir_write_enable=NO<br />
idle_session_timeout=300<br />
data_connection_timeout=90<br />
max_clients=1<br />
max_per_ip=1<br />
local_max_rate=25000<br />
pam_service_name=vsftpd<br />
chroot_local_user=YES<br />
---------------------------------<br />
七.启动服务：<br />
[root@linuxidc.com ~]# service vsftpd start<br />
Starting vsftpd for
vsftpd:&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
[ OK ]<br />
八.测试：<br />
1.在虚拟用户目录中预先放入文件：<br />
[root@linuxidc.com ~]# touch /opt/vsftp/ftp001/test.txt<br />
2.从其他机器作为客户端登陆FTP：<br />
可以IE或FTP客户端软直接访问</P>
<p>ie里输入 <a HREF="ftp://127.0.0.1/"><font COLOR="#731808" SIZE="2">ftp://127.0.0.1</FONT></A> (服务器IP)</P>
<p>弹出对话框后.输入FTP用户名和密码<br />
---------------------------------------------</P>
<p><br />
注意:<br />
在/etc/vsftpd/vsftpd.conf中，local_enable的选项必须打开为Yes，使得虚拟用户的访问成为可能，否则会出现以下现象：<br />

----------------------------------<br />
[root@linuxidc.com ~]# ftp<br />
ftp&gt; open 192.168.1.22<br />
Connected to 192.168.1.22.<br />
500 OOPS: vsftpd: both local and anonymous access disabled!<br />
----------------------------------<br />
原因：虚拟用户再丰富，其实也是基于它们的宿主用户virtusers的，如果virtusers这个虚拟用户的宿主被限制住了，那么虚</P>
<p>拟用户也将受到限制。</P>
<p>补充：<br />
1.要查看服务器自带的防火墙有无挡住FTP 21端口 导致不能访问</P>
<p>vi /etc/sysconfig/iptables 后增加以下内容</P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">-A INPUT -m state
--state ESTABLISHED,RELATED -j ACCEPT</FONT></P>
<p><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">-A INPUT -m state
--state NEW -m tcp -p tcp --dport 21 -j ACCEPT</FONT></P>
<p>2.查看 SELinux 禁用没有.要禁用<br />
3.500 OOPS:错误 有可能是你的vsftpd.con配置文件中有不能被识别的命令，还有一种可能是命令的YES 或 NO
后面有空格。<br />
4.要仔细查看各个用到的文件夹权限,及用户属主权限等</P>
<p>5.vsftp的随系统启动自启动</P>
<p><span><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chkconfig
iptables on</FONT></SPAN></P>
<p><span><span><font STYLE="BACKGroUnD-CoLor: rgb(255,255,0)">chkconfig vsftpd
on</FONT></SPAN></SPAN></P>
<p><br />
1 如何新加FTP用户</P>
<p>打开密码文件里加入(一行是用户.一是密码.依次类推)<br />
#vi /etc/vsftpd/virtusers<br />
加入用户后 保存退出</P>
<p>#db_load -T -t hash -f /etc/vsftpd/virtusers
/etc/vsftpd/virtusers.db&nbsp;<wbr>&nbsp;<wbr>
(然后生成新的虚拟用数据文件)<br />
#cp /etc/vsftpd/vconf/vconf.tmp
d&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
(新建d用户,用虚拟用户模板vconf.tmp文件生成d虚拟用户文件)<br />
#vi
/etc/vsftpd/vconf/d&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
(打开D虚拟用户文件.在第一行最后加入该用户对应的FTP目录)<br />
#mkdir
/opt/vsftp/WWW&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
(新建WWW目录为d FTP用户登陆目录)<br />
#service vsftpd restart<br />
-------------------------------------------------------<br />
2 如何修改FTP 用户登陆密码</P>
<p>打开密码文件里加入(第一行是用户.第二是密码.依次类推,只要改对应用户下面的密码即可)<br />
#vi /etc/vsftpd/virtusers&nbsp;<wbr>&nbsp;<wbr><br />
#db_load -T -t hash -f /etc/vsftpd/virtusers
/etc/vsftpd/virtusers.db&nbsp;<wbr>&nbsp;<wbr>
(然后生成新的虚拟用数据文件)<br />
#service vsftpd restart</P>
</DIV>
<p>&nbsp;<wbr></P>
<p><span>2. 下面，问题就出来了。打开SELinux后，SELinux会阻止ftp
daemon读取用户home目录。所以FTP会甩出一句 “500 OOPS: cannot change
directory”。无法进入目录，出错退出。</SPAN><br />
<br />
<span>解决办法有两个：</SPAN><br />
<br />
<span>1.
降低SELinux安全级别，把enforcing降低到permissive<span>&nbsp;<wbr></SPAN></SPAN><br />
</P>
<div>vi /etc/sysconfig/selinux<br />
<br />
# This file controls the state of SELinux on the system.<br />
# SELINUX= can take one of these three values:<br />
#&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
enforcing - SELinux security policy is enforced.<br />
#&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
permissive - SELinux prints warnings instead of enforcing.<br />
#&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
disabled - SELinux is fully disabled.<br />
SELINUX=permissive<span>&nbsp;<wbr></SPAN><br /></DIV>
<p><br />
<span>这时FTP的登录功能就正常了。但降低整体系统安全作为代价来解决一个小问题，这总不是最佳方案。</SPAN><br />
<br />
<span>2.
经过研究，又找到了另一个更理想的办法。首先查看SELinux中有关FTP的设置状态：</SPAN><br /></P>
<div>getsebool -a|grep ftp<br />
<br />
allow_ftpd_anon_write --&gt; off<br />
allow_ftpd_full_access --&gt; off<br />
allow_ftpd_use_cifs --&gt; off<br />
allow_ftpd_use_nfs --&gt; off<br />
allow_tftp_anon_write --&gt; off<br />
ftp_home_dir --&gt; off<br />
ftpd_connect_db --&gt; off<br />
ftpd_disable_trans --&gt; on<br />
ftpd_is_daemon --&gt; on<br />
httpd_enable_ftp_server --&gt; off<br />
tftpd_disable_trans --&gt; off<br /></DIV>
<p><br />
<br />
<span>经过尝试发现，打开ftp_home_dir或者
ftpd_disable_trans。都可以达到在enforcing级别下，允许FTP正常登录的效果。</SPAN><br /></P>
<div>setsebool -P ftpd_disable_trans 1<br />
或者<br />
setsebool -P ftp_home_dir 1<br />
service vsftpd restart</DIV>
<p><br />
<span>加-P是保存选项，每次重启时不必重新执行这个命令了。最后别忘了在/etc/sysconfig/selinux中，修改SELINUX=enforcing。</SPAN><br />
</P>
<p>&nbsp;<wbr>=========</P>
<div><font FACE="微软雅黑"><font SIZE="3"><b>两种方式建立Vsftpd</B><b>虚拟用户</B></FONT></FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑">我们登录FTP有三种方式，匿名登录、本地用户登录和虚拟用户登录。</FONT></DIV>
<div><font FACE="微软雅黑">匿名登录：在登录FTP时使用默认的用户名，一般是ftp或anonymous。</FONT></DIV>
<div><font FACE="微软雅黑">本地用户登录：使用系统用户登录，在/etc/passwd中。</FONT></DIV>
<div><font FACE="微软雅黑">虚拟用户登录：这是FTP专有用户，有两种方式实现虚拟用户，本地数据文件和数据库服务器。</FONT></DIV>
<div><font FACE="微软雅黑">FTP虚拟用户是FTP服务器的专有用户，使用虚拟用户登录FTP，只能访问FTP服务器提供的资源，大大增强了系统的安全。</FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑">本文实验的Linux系统是CentOS 5 update2</FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><b><font SIZE="3" FACE="微软雅黑">一、本地数据文件方式</FONT></B></DIV>
<div><font FACE="微软雅黑"><b>1.</B> <b>添加虚拟用户口令文件</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vftpuser.txt</FONT></DIV>
</DIV>
<div><font FACE="微软雅黑">添加虚拟用户名和密码，一行用户名，一行密码，以此类推。奇数行为用户名，偶数行为密码。</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">bobyuan #用户名</FONT></DIV>
<div><font FACE="微软雅黑">123456 #密码</FONT></DIV>
<div><font FACE="微软雅黑">markwang #用户名</FONT></DIV>
<div><font FACE="微软雅黑">123456 #密码</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>2.</B> <b>生成虚拟用户口令认证文件</B></FONT></DIV>
<div><font FACE="微软雅黑">将刚添加的vftpuser.txt虚拟用户口令文件转换成系统识别的口令认证文件。</FONT></DIV>
<div><font FACE="微软雅黑">首先查看系统有没有安装生成口令认证文件所需的软件db4-utils。</FONT></DIV>
<div>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#rpm &ndash;qa
|grep db4-utils</FONT></FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 /]#rpm &ndash;ivh
db4-utils-4.3.29-9.fc6.i386.rpm</FONT></DIV>
</DIV>
</DIV>
</DIV>
<div><font FACE="微软雅黑">下面使用db_load命令生成虚拟用户口令认证文件。</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">[root@CentOS5 /]#db_load &ndash;T &ndash;t hash &ndash;f
/etc/vsftpd/vftpuser.txt /etc/vsftpd/vftpuser.db</FONT></DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>3.</B>
<b>编辑vsftpd的PAM认证文件</B></FONT></DIV>
<div><font FACE="微软雅黑">在/etc/pam.d目录下，</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/pam.d/vsftpd</FONT></DIV>
</DIV>
<div><font FACE="微软雅黑">将里面其他的都注释掉，添加下面这两行：</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">auth required /lib/security/pam_userdb.so
db=/etc/vsftpd/vftpuser</FONT></DIV>
<div><font FACE="微软雅黑">account required /lib/security/pam_userdb.so
db=/etc/vsftpd/vftpuser</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>4.</B>
<b>建立本地映射用户并设置宿主目录权限</B></FONT></DIV>
<div><font FACE="微软雅黑">所有的FTP虚拟用户需要使用一个系统用户，这个系统用户不需要密码。</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">[root@CentOS5 /]#useradd &ndash;d /home/vftpsite
&ndash;s /sbin/nologin vftpuser</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 /]#chmod 700
/home/vftpsite</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>5.</B>
<b>配置vsftpd.conf（设置虚拟用户配置项）</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd.conf</FONT></FONT></DIV>
<div><font FACE="微软雅黑">guest_enable=YES #开启虚拟用户</FONT></DIV>
<div><font FACE="微软雅黑">guest_username=vftpuser
#FTP虚拟用户对应的系统用户</FONT></DIV>
<div><font FACE="微软雅黑">pam_service_name=vsftpd
#PAM认证文件</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>6.</B> <b>重启vsftpd服务</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">[root@CentOS5 /]#service vsftpd
restart</FONT></DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>7.</B> <b>测试虚拟用户登录FTP</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">C:\User\Administrator&gt;ftp
192.168.120.240</FONT></FONT></DIV>
<div><font FACE="微软雅黑">连接到192.168.120.240。</FONT></DIV>
<div><font FACE="微软雅黑">220 Welcome to BOB FTP server</FONT></DIV>
<div><font FACE="微软雅黑">用户(192.168.120.240(none)):markwang</FONT></DIV>
<div><font FACE="微软雅黑">331 Please specify the
password.</FONT></DIV>
<div><font FACE="微软雅黑">密码:</FONT></DIV>
<div><font FACE="微软雅黑">230 Login successful.</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><b><font SIZE="3" FACE="微软雅黑">二、数据库服务器（MySQL）方式</FONT></B></DIV>
<div><font FACE="微软雅黑"><b>1.</B> <b>安装MySQL</B></FONT></DIV>
<div><font FACE="微软雅黑">我使用的是Tar包安装的MySQL，版本号：mysql-6.0.8-alpha.tar.gz</FONT></DIV>
<div><font FACE="微软雅黑">具体安装方法，请查看我的另一篇文章“<a HREF="http://yuanbin.blog.51cto.com/363003/124826" TARGET="_blank">部署LAMP+Discuz！7.0</A>”。</FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>2.</B>
<b>建立本地映射用户并设置宿主目录权限</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#useradd
&ndash;d /home/vftpsite &ndash;s /sbin/nologin vftpuser</FONT></FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 /]#chmod 700
/home/vftpsite</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>3.</B>
<b>配置vsftpd.conf（设置虚拟用户配置项）</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd.conf</FONT></FONT></DIV>
<div><font FACE="微软雅黑">guest_enable=YES #开启虚拟用户</FONT></DIV>
<div><font FACE="微软雅黑">guest_username=vftpuser
#FTP虚拟用户对应的系统用户</FONT></DIV>
<div><font FACE="微软雅黑">pam_service_name=vsftpd
#PAM认证文件</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>4.</B>
<b>在MySQL中建立用户口令数据库</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#mysql &ndash;u
root &ndash;p</FONT></FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt; create database
vftpuser;&nbsp;<wbr>&nbsp;<wbr>
#建立虚拟用户数据库，库名vftpuser</FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt; use vftpuser;&nbsp;<wbr>
#进入vftpuser数据库</FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑">mysql&gt; create table users(name char(16)
binary,passwd char(16) binary);&nbsp;<wbr>
#建立虚拟用户口令表，表名users</FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑">mysql&gt; insert into users (name,passwd)
values ('bobyuan',password('111'));&nbsp;<wbr></FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt;&nbsp;<wbr> insert into
users (name,passwd) values
('markwang',password('111'));</FONT></DIV>
<div><font FACE="微软雅黑">#建立两个虚拟用户，bobyuan和markwang</FONT></DIV>
<div><strong><font COLOR="#FF0000">注：在这里我用这种方法添加的虚拟用户密码都是经过MySQL加密的，加密后的密码pam-mysql不能识别（MySQL和pam-mysql兼容性有些问题），因此本次实验使用明文保存密码。</FONT></STRONG><br />

<strong>添加明文密码：</STRONG><br />
<strong>方法一：单个添加用户</STRONG><br />
mysql&gt; insert into users (name,passwd) values ('bobyuan',
'111');<br />
mysql&gt; insert into users (name,passwd) values
('markwang',‘111');<br />
<strong>方法二：批量添加用户<br /></STRONG>新建vftpuser.txt文件<br />
[root@CentOS5 /]#vi vftpuser.txt<br />
添加用户名和密码，注意字段数据之间要用Tab键隔开。<br />
bobyuan&nbsp;<wbr> 111<br />
markwang 111<br />
mysql&gt;use vftpuser;<br />
mysql&gt;load data local infile “/vftpuser.txt”into table
users;</DIV>
<div>mysql&gt;flush privileges;</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑">mysql&gt; grant select&nbsp;<wbr>on
vftpuser.users to vftpuser@localhost identified by
'111111';&nbsp;<wbr>
#授权vftpuser这个账号可以读取vftpuser数据库的user表</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>5.</B> <b>验证第4步的设置是否成功</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#mysql &ndash;u
vftpuser &ndash;p</FONT></FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt;show databases;</FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt;use vftpuser;</FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt;show tables;</FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt;select * from users;</FONT></DIV>
<div><font FACE="微软雅黑">mysql&gt;quit</FONT></DIV>
</DIV>
</DIV>
<div><font FACE="微软雅黑">如下图：</FONT></DIV>
<div SIZCACHE08774206063853389="0" SIZSET="30"><a HREF="http://img1.51cto.com/attachment/200902/6/363003_1233940771XTd0.jpg" TARGET="_blank"></A><a HREF="http://img1.51cto.com/attachment/200902/6/363003_1233940773qBbv.jpg" TARGET="_blank"><img STYLE="BorDer-riGHT-WiDTH: 0px; DispLAY: inline; BorDer-Top-WiDTH: 0px; BorDer-BoTToM-WiDTH: 0px; BorDer-LeFT-WiDTH: 0px" TITLE="clip_image002" BORDER="0" ALT="clip_image002" src="http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif" real_src ="http://img1.51cto.com/attachment/200902/6/363003_1233940774ZKsE.jpg" WIDTH="650" HEIGHT="503" BLOG.51CTO.COM="" HTTP:="" /></A></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>6.</B>
<b>编译MySQL的PAM认证模块</B></FONT></DIV>
<div><font FACE="微软雅黑">查看/lib/security目录下有没有MySQL对应的PAM模块。</FONT></DIV>
<div SIZCACHE08774206063853389="0" SIZSET="31"><a HREF="http://img1.51cto.com/attachment/200902/6/363003_1233940775cokk.jpg">
</A><a HREF="http://img1.51cto.com/attachment/200902/6/363003_1233940776qJ3K.jpg" TARGET="_blank"><img STYLE="BorDer-riGHT-WiDTH: 0px; DispLAY: inline; BorDer-Top-WiDTH: 0px; BorDer-BoTToM-WiDTH: 0px; BorDer-LeFT-WiDTH: 0px" TITLE="clip_image004" BORDER="0" ALT="clip_image004" src="http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif" real_src ="http://img1.51cto.com/attachment/200902/6/363003_1233940776QNHv.jpg" HEIGHT="45" BLOG.51CTO.COM="" HTTP:="" /></A></DIV>
<div><font FACE="微软雅黑">如果没有则下载pam-mysql安装（</FONT><a HREF="http://sourceforge.net/projects/pam-mysql"><font FACE="微软雅黑">http://sourceforge.net/projects/pam-mysql</FONT></A><font FACE="微软雅黑">），</FONT></DIV>
<div><font FACE="微软雅黑">我下载的是pam_mysql-0.7RC1.tar.gz。</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">[root@CentOS5 /]#cd
/usr/local/src</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 src]#tar &ndash;zxvf
pam_mysql-0.7RC1.tar.gz</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 src]#cd
pam_mysql-0.7RC1</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 pam_mysql-0.7RC1]# ./configure
--with-mysql=/usr/local/mysql/
--with-pam-mods-dir=/lib/security/</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5
pam_mysql-0.7RC1]#make</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 pam_mysql-0.7RC1]#make
install</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>7.</B>
<b>编辑vsftpd的PAM认证文件</B></FONT></DIV>
<div><font FACE="微软雅黑">在/etc/pam.d目录下，</FONT></DIV>
<div>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/pam.d/vsftpd</FONT></DIV>
</DIV>
</DIV>
<div><font FACE="微软雅黑">将里面其他的都注释掉，添加下面这两行：</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">auth required pam_mysql.so user=vftpuser
passwd=111111 host=localhost db=vftpuser table=users
usercolumn=name passwdcolumn=passwd crypt=0</FONT></DIV>
<div><font FACE="微软雅黑">account required pam_mysql.so user=vftpuser
passwd=111111 host=localhost db=vftpuser table=users
usercolumn=name passwdcolumn=passwd crypt=0</FONT></DIV>
</DIV>
</DIV>
<div><font FACE="微软雅黑">crypt=0：表示口令使用明文方式保存在数据库中<br />
crypt=1：表示口令使用UNIX的DES加密方式加密后保存在数据库中<br />
crypt=2：表示口令使用MySQL的password()函数加密后保存在数据库中<br />
crypt=3：表示口令使用MD5散列值的方式保存在数据库中</FONT></DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>8.</B> <b>重启vsftpd服务</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">[root@CentOS5 /]#service vsftpd
restart</FONT></DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>9.</B> <b>测试虚拟用户登录FTP</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>C:\User\Administrator&gt;ftp 192.168.120.240</DIV>
<div>Connected to 192.168.120.240.<br />
220 Welcome to BOB FTP server<br />
User (192.168.120.240:(none)): bobyuan<br />
331 Please specify the password.<br />
Password:<br />
230 Login successful.<br />
ftp&gt; quit<br />
221 Goodbye.</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><b><font SIZE="3" FACE="微软雅黑">三、虚拟用户高级设置</FONT></B></DIV>
<div><font FACE="微软雅黑"><b>1.</B>
<b>virtual_use_local_privs</B><b>参数</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">当virtual_use_local_privs=YES时，虚拟用户和本地用户有相同的权限；</FONT></FONT></DIV>
<div><font FACE="微软雅黑">当virtual_use_local_privs=NO时，虚拟用户和匿名用户有相同的权限，默认是NO。</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div><font FACE="微软雅黑">当virtual_use_local_privs=YES，write_enable=YES时，虚拟用户具有写权限（上传、下载、删除、重命名）。</FONT></DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">当virtual_use_local_privs=NO，write_enable=YES，anon_world_readable_only=YES，</FONT></FONT></DIV>
<div><font FACE="微软雅黑">anon_upload_enable=YES时，虚拟用户不能浏览目录，只能上传文件，无其他权限。</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">当virtual_use_local_privs=NO，write_enable=YES，anon_world_readable_only=NO，</FONT></FONT></DIV>
<div><font FACE="微软雅黑">anon_upload_enable=NO时，虚拟用户只能下载文件，无其他权限。</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">当virtual_use_local_privs=NO，write_enable=YES，anon_world_readable_only=NO，</FONT></FONT></DIV>
<div><font FACE="微软雅黑">anon_upload_enable=YES时，虚拟用户只能上传和下载文件，无其他权限。</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">当virtual_use_local_privs=NO，write_enable=YES，anon_world_readable_only=NO，</FONT></FONT></DIV>
<div><font FACE="微软雅黑">anon_mkdir_write_enable=YES时，虚拟用户只能下载文件和创建文件夹，无其他权限。</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">当virtual_use_local_privs=NO，write_enable=YES，anon_world_readable_only=NO，</FONT></FONT></DIV>
<div><font FACE="微软雅黑">anon_other_write_enable=YES时，虚拟用户只能下载、删除和重命名文件，无其他权限。</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>2.</B>
<b>建立各个虚拟用户自身的配置文件</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd.conf</FONT></FONT></DIV>
<div><font FACE="微软雅黑">添加：</FONT></DIV>
<div><font FACE="微软雅黑">user_config_dir=/etc/vsftpd/vsftpd_user_conf</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 /]#mkdir
/etc/vsftpd/vsftpd_user_conf</FONT></DIV>
</DIV>
</DIV>
<div><font FACE="微软雅黑">编辑bobyuan的配置文件</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd_user_conf/bobyuan</FONT></DIV>
<div><font FACE="微软雅黑">添加：</FONT></DIV>
<div><font FACE="微软雅黑">anon_world_readable_only=NO
#开放bobyuan的下载权限（只能下载）。注意这个地方千万不能写成YES，否则bobyuan将不能列出文件和目录。</FONT></DIV>
</DIV>
</DIV>
<div><font FACE="微软雅黑">编辑markwang的配置文件</FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd_user_conf/markwang</FONT></DIV>
<div><font FACE="微软雅黑">添加：</FONT></DIV>
<div><font FACE="微软雅黑">write_enable=YES
#开放markwang的写权限</FONT></DIV>
<div><font FACE="微软雅黑">anon_world_readable_only=NO
#开放markwang的下载权限</FONT></DIV>
<div><font FACE="微软雅黑">anon_upload_enable=YES
#开放markwang的上传权限</FONT></DIV>
<div><font FACE="微软雅黑">anon_mkdir_write_enable=YES
#开放markwang创建目录的权限</FONT></DIV>
<div><font FACE="微软雅黑">anon_other_write_enable=YES
#开放markwang删除和重命名的权限</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><b><font SIZE="3" FACE="微软雅黑">四、虚拟用户配置文件（实验）</FONT></B></DIV>
<div><font FACE="微软雅黑"><b>1.</B> <b>所有虚拟用户使用统一配置</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd.conf</FONT></FONT></DIV>
<div><font FACE="微软雅黑">write_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">anonymous_enable=NO</FONT></DIV>
<div><font FACE="微软雅黑">local_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">guest_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">guest_username=vftpuser</FONT></DIV>
<div><font FACE="微软雅黑">virtual_use_local_privs=NO</FONT></DIV>
<div><font FACE="微软雅黑">pam_service_name=vsftpd</FONT></DIV>
<div><font FACE="微软雅黑">anon_world_readable_only=NO
#可以下载</FONT></DIV>
<div><font FACE="微软雅黑">anon_upload_enable=NO（默认值）
#不能上传</FONT></DIV>
<div><font FACE="微软雅黑">anon_mkdir_write_enable=NO（默认值）
#不能新建文件夹</FONT></DIV>
<div><font FACE="微软雅黑">anon_other_write_enable=NO（默认值）
#不能删除和重命名文件</FONT></DIV>
<div><font FACE="微软雅黑">ftpd_banner=Welcome to BOB FTP
server</FONT></DIV>
<div><font FACE="微软雅黑">xferlog_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">xferlog_file=/var/log/vsftpd.log</FONT></DIV>
<div><font FACE="微软雅黑">xferlog_std_format=YES</FONT></DIV>
<div><font FACE="微软雅黑">ascii_upload_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">ascii_download_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">tcp_wrappers=NO</FONT></DIV>
<div><font FACE="微软雅黑">setproctitle_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">listen_port=21</FONT></DIV>
<div><font FACE="微软雅黑">connect_from_port_20=YES</FONT></DIV>
<div><font FACE="微软雅黑">idle_session_timeout=600</FONT></DIV>
<div><font FACE="微软雅黑">data_connection_timeout=120</FONT></DIV>
<div><font FACE="微软雅黑">max_clients=0</FONT></DIV>
<div><font FACE="微软雅黑">max_per_ip=3</FONT></DIV>
<div><font FACE="微软雅黑">local_max_rate=512000</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div><font FACE="微软雅黑"><b>2.</B> <b>各个虚拟用户使用自身配置</B></FONT></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd.conf</FONT></FONT></DIV>
<div><font FACE="微软雅黑">write_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">anonymous_enable=NO</FONT></DIV>
<div><font FACE="微软雅黑">local_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">guest_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">guest_username=vftpuser</FONT></DIV>
<div><font FACE="微软雅黑">virtual_use_local_privs=NO</FONT></DIV>
<div><font FACE="微软雅黑">pam_service_name=vsftpd</FONT></DIV>
<div><font FACE="微软雅黑">user_config_dir=/etc/vsftpd/vsftpd_user_conf</FONT></DIV>
<div><font FACE="微软雅黑">ftpd_banner=Welcome to BOB FTP
server</FONT></DIV>
<div><font FACE="微软雅黑">xferlog_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">xferlog_file=/var/log/vsftpd.log</FONT></DIV>
<div><font FACE="微软雅黑">xferlog_std_format=YES</FONT></DIV>
<div><font FACE="微软雅黑">ascii_upload_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">ascii_download_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">tcp_wrappers=NO</FONT></DIV>
<div><font FACE="微软雅黑">setproctitle_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">listen_port=21</FONT></DIV>
<div><font FACE="微软雅黑">connect_from_port_20=YES</FONT></DIV>
<div><font FACE="微软雅黑">idle_session_timeout=600</FONT></DIV>
<div><font FACE="微软雅黑">data_connection_timeout=120</FONT></DIV>
<div><font FACE="微软雅黑">max_clients=0</FONT></DIV>
<div><font FACE="微软雅黑">max_per_ip=3</FONT></DIV>
<div><font FACE="微软雅黑">local_max_rate=512000</FONT></DIV>
</DIV>
</DIV>
<div>&nbsp;<wbr></DIV>
<div STYLE="BorDer-BoTToM: #aaaaaa 1px solid; BorDer-LeFT: #aaaaaa 1px solid; pADDinG-BoTToM: 5px; BACKGroUnD-CoLor: #d3d3d3; pADDinG-LeFT: 5px; pADDinG-riGHT: 5px; BorDer-Top: #aaaaaa 1px solid; BorDer-riGHT: #aaaaaa 1px solid; pADDinG-Top: 5px">
<div>
<div><font FACE="微软雅黑"><font FACE="微软雅黑">[root@CentOS5 /]#mkdir
/etc/vsftpd/vsftpd_user_conf</FONT></FONT></DIV>
<div><font FACE="微软雅黑">编辑bobyuan（FTP匿名用户）的配置文件</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd_user_conf/bobyuan</FONT></DIV>
<div><font FACE="微软雅黑">anon_world_readable_only=NO</FONT></DIV>
<div><font FACE="微软雅黑">编辑ftpadmin（FTP匿名管理员）的配置文件</FONT></DIV>
<div><font FACE="微软雅黑">[root@CentOS5 /]#vi
/etc/vsftpd/vsftpd_user_conf/ftpadmin</FONT></DIV>
<div><font FACE="微软雅黑">anon_world_readable_only=NO</FONT></DIV>
<div><font FACE="微软雅黑">anon_upload_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">anon_mkdir_write_enable=YES</FONT></DIV>
<div><font FACE="微软雅黑">anon_other_write_enable=YES</FONT></DIV>
</DIV>
</DIV>
