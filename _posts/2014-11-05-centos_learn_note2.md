---
layout: post
title: "第十二天:centos6.5下&nbsp;安装配置iredmail"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:18
---

<p>今天闲来无事，配置了下iredmail服务.</P>
<p>安装 iremail 需要事先 卸载掉 mysql apache</P>
<p>我看了下属性将地址复制.bz2&nbsp;<wbr> 然后 centos下 wget <a HREF="http://www.iredmail.com/iRedMail-0.8.7.tar.bz2">http://www.iredmail.com/iRedMail-0.8.7.tar.bz2</A></P>
<p>就下载到了 我的当前工作目录内.</P>
<p>&nbsp;<wbr>tar -jxvf iRedMail-0.8.7.bz2</P>
<p>[root@fwcent iRedMail-0.8.7]# bh iRedMail.sh</P>
<p>-bash: bh: command not found</P>
<p>[root@fwcent iRedMail-0.8.7]# bash iRedMail.sh</P>
<p>hostname: Unknown host</P>
<p>hostname: Unknown host</P>
<p>&lt; ERROR &gt; Please configure a fully qualified domain name
(FQDN) in</P>
<p>/etc/hosts before we go further.</P>
<p>&nbsp;<wbr>Example:</P>
<p>&nbsp;<wbr>127.0.0.1&nbsp;<wbr>&nbsp;<wbr>
imail.iredmail.org imail localhost</P>
<p>出现这样的错误，看来是计算机名称需要xxx.xxx.xxx的形式</P>
<p>修改计算机名需要2个文件： /etc/hosts&nbsp;<wbr>&nbsp;<wbr>
,/etc/sysconfig/network</P>
<p>重新启动电脑后，开始安装 bash iRedMail.sh</P>
<p>&nbsp;<wbr>#bash iRedMail.sh</P>
<p>&lt; SKIP &gt; Function: check_new_iredmail.</P>
<p>&lt; INFO &gt; Generating yum repository ...</P>
<p>&lt; INFO &gt; Clean metadata of yum repositories.</P>
<p>Loaded plugins: downloadonly, fastestmirror,
refresh-packagekit,</P>
<p>security</P>
<p>Cleaning repos: Webmin base extras iRedMail tmp_epel updates</P>
<p>11 metadata files removed</P>
<p>3 sqlite files removed</P>
<p>0 metadata files removed</P>
<p>&lt; INFO &gt; Install epel yum repo.</P>
<p>&lt; INFO &gt; Installing package(s): epel-release</P>
<p>Loaded plugins: downloadonly, fastestmirror,
refresh-packagekit,</P>
<p>security</P>
<p>Loading mirror speeds from cached hostfile</P>
<p>
tmp_epel/metalink&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>|
4.6
kB&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:07</P>
<p>&nbsp;<wbr>* base: centos.ustc.edu.cn</P>
<p>&nbsp;<wbr>* extras: centos.ustc.edu.cn</P>
<p>&nbsp;<wbr>* tmp_epel: mirrors.neusoft.edu.cn</P>
<p>&nbsp;<wbr>* updates: centos.ustc.edu.cn</P>
<p>
Webmin&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
|&nbsp;<wbr> 951
B&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:00</P>
<p>
Webmin/primary&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>|&nbsp;<wbr>
23
kB&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:00</P>
<p>
Webmin&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>182/182</P>
<p>
base&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
| 3.7
kB&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:00</P>
<p>
base/primary_db&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>|
3.5
MB&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:07</P>
<p>
extras&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
| 3.4
kB&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:00</P>
<p>
extras/primary_db&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
|&nbsp;<wbr> 18
kB&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>00:00</P>
<p>http://iredmail.org/yum/rpms/6/repodata/repomd.xml: [Errno 14]
PYCURL</P>
<p>ERROR 56 - "Failure when receiving data from the peer"</P>
<p>Trying other mirror.</P>
<p>Error: Cannot retrieve repository metadata (repomd.xml) for</P>
<p>repository: iRedMail. Please verify its path and try again</P>
<p>&lt; ERROR &gt; Installation failed, please check the terminal
output.</P>
<p>&lt; ERROR &gt; If you're not sure what the problem is, try to
get help in</P>
<p>iRedMail</P>
<p>&lt; ERROR &gt; forum: http://www.iredmail.org/forum/</P>
<p>&nbsp;<wbr>又出错了， 估计是文件没下载下来，按照网上的换了ip
173.254.22.21好了，</P>
<p>那个pkgs下有个get -all.sh文件。不需要翻页就看到了。</P>
<p>然后又是一番下载等待，最后进入了，"welcome and thanks for your use"界</P>
<p>面。yes后进入了"default mail storage path"默认的邮件存储路径.默认</P>
<p>是/var/vmail 我就不改了。我这个目录下空间够大。</P>
<p>下一步， "choose your preferred backend used to store mail
accounts"选</P>
<p>择你的后台管理的email账户。我选择"mysql",输入用于以后通过mysql管理</P>
<p>iredmail的密码 ,"your firest virtual domain name"你的第一个虚拟域名,我</P>
<p>输入 fw.org 我的主机名后半部分。"password for the admimnistrator of</P>
<p>your domain" 管理员管理邮箱的密码,"optional components"组件,全选 安装,</P>
<p>y安装。下载116个文件。</P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>
[UNCOMPL&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
ETED]</P>
<p>&nbsp;<wbr>iRedMail:_Open_Source_Mail_Server_Solution</P>
<p>&nbsp;<wbr></P>
<p>
qqqqqqqqqqqqqqqqqqqqqqqq<wbr>qqqqqqqqqqqqqqqqqqqqqqqq<wbr>qqqqqqqqqqqqqqqqqqqqqq</P>
<p>qqqqqqqq</P>
<p>&nbsp;<wbr></P>
<p>&lt; Question &gt; Continue? [y|N]y</P>
<p>&lt; INFO &gt; Installing package(s): mysql-server mysql httpd
mod_ssl php</P>
<p>&nbsp;<wbr> httpd-tools.i686
0:2.2.15-30.el6.centos&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
mysql-libs.i686</P>
<p>0:5.1.73-3.el6_5</P>
<p>&nbsp;<wbr></P>
<p>Complete!</P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>
********************************************************************</P>
<p>* Start iRedMail Configurations</P>
<p>
********************************************************************</P>
<p>&lt; INFO &gt; Create self-signed SSL certification files.</P>
<p>&lt; INFO &gt; Create required system accounts: vmail, iredapd,
iredadmin.</P>
<p>&lt; INFO &gt; Configure Apache web server and PHP.</P>
<p>&lt; INFO &gt; Configure MySQL database server.</P>
<p>&lt; INFO &gt; Configure Postfix (Message Transfer Agent).</P>
<p>&lt; INFO &gt; Configure Cluebringer (postfix policy
server).</P>
<p>&lt; INFO &gt; Configure Dovecot (pop3/imap/managesieve
server).</P>
<p>&lt; INFO &gt; Configure ClamAV (anti-virus toolkit).</P>
<p>&lt; INFO &gt; Configure Amavisd-new (interface between MTA and
content</P>
<p>checkers).</P>
<p>&lt; INFO &gt; Configure SpamAssassin (content-based spam
filter).</P>
<p>&lt; INFO &gt; Configure iRedAPD (postfix policy daemon).</P>
<p>&lt; INFO &gt; Configure iRedAdmin (official web-based admin
panel).</P>
<p>&lt; INFO &gt; Configure Fail2ban (authentication failure
monitor).</P>
<p>&lt; INFO &gt; Configure Awstats (logfile analyzer for mail and
web server).</P>
<p>&lt; INFO &gt; Configure Roundcube webmail.</P>
<p>&lt; INFO &gt; Configure phpMyAdmin (web-based MySQL management
tool).</P>
<p>&nbsp;<wbr></P>
<p>
**********************************************************************</P>
<p>***</P>
<p>* iRedMail-0.8.7 installation and configuration complete.</P>
<p>
**********************************************************************</P>
<p>***</P>
<p>&nbsp;<wbr></P>
<p>&lt; INFO &gt; Mail sensitive administration info to
postmaster@fw.org.</P>
<p>&lt; INFO &gt; Disable SELinux in /etc/selinux/config.</P>
<p>&lt; Question &gt; Would you like to use firewall rules provided
by iRedMail</P>
<p>now?</P>
<p>&lt; Question &gt; File: /etc/sysconfig/iptables, with SSHD
port: 22. [Y|n]y</P>
<p>&lt; INFO &gt; Copy firewall sample rules:
/etc/sysconfig/iptables.</P>
<p>&lt; Question &gt; Restart firewall now (with SSHD port 22)?
[y|N]n</P>
<p>&lt; Question &gt; Would you like to use MySQL configuration
file shipped</P>
<p>within iRedMail now?</P>
<p>&lt; Question &gt; File: /etc/my.cnf. [Y|n]y</P>
<p>&lt; INFO &gt; Copy MySQL sample file: /etc/my.cnf.</P>
<p>&lt; INFO &gt; Enable SSL support for MySQL server.</P>
<p>&lt; INFO &gt; Updating ClamAV database (freshclam), please wait
...</P>
<p>ClamAV update process started at Mon Jun&nbsp;<wbr> 2
16:02:18 2014</P>
<p>main.cvd is up to date (version: 55, sigs: 2424225, f-level:
60,</P>
<p>builder: neo)</P>
<p>WARNING: getfile: daily-18955.cdiff not found on remote server
(IP:</P>
<p>200.236.31.1)</P>
<p>WARNING: getpatch: Can't download daily-18955.cdiff from</P>
<p>db.cn.clamav.net</P>
<p>Trying host db.cn.clamav.net (202.118.1.66)...</P>
<p>WARNING: getfile: daily-18955.cdiff not found on remote server
(IP:</P>
<p>202.118.1.66)</P>
<p>WARNING: getpatch: Can't download daily-18955.cdiff from</P>
<p>db.cn.clamav.net</P>
<p>WARNING: getpatch: Can't download daily-18955.cdiff from</P>
<p>db.cn.clamav.net</P>
<p>WARNING: Incremental update failed, trying to download
daily.cvd</P>
<p>Downloading daily.cvd [100%]</P>
<p>daily.cvd updated (version: 19053, sigs: 974792, f-level: 63,
builder:</P>
<p>neo)</P>
<p>Downloading bytecode.cvd [100%]</P>
<p>bytecode.cvd updated (version: 241, sigs: 46, f-level: 63,
builder:</P>
<p>dgoddard)</P>
<p>Database updated (3399063 signatures) from db.cn.clamav.net
(IP:</P>
<p>200.236.31.1)</P>
<p>
********************************************************************</P>
<p>* URLs of installed web applications:</P>
<p>*</P>
<p>* - Webmail: httpS://imail.fw.org/mail/</P>
<p>* - Admin Panel (iRedAdmin): httpS://imail.fw.org/iredadmin/</P>
<p>*&nbsp;<wbr>&nbsp;<wbr> + Username:
postmaster@fw.org, Password: 123456</P>
<p>*</P>
<p>&nbsp;<wbr></P>
<p>
********************************************************************</P>
<p>* Congratulations, mail server setup completed successfully.
Please</P>
<p>* read below file for more information:</P>
<p>*</P>
<p>*&nbsp;<wbr>&nbsp;<wbr> -
/root/iRedMail-0.8.7/iRedMail.tips</P>
<p>*</P>
<p>* And it's sent to your mail account .</P>
<p>*</P>
<p>* Please reboot your system to enable mail services.</P>
<p>*</P>
<p>
********************************************************************</P>
<p>===以上是安装的流程。。</P>
<p>重新启动电脑后:。</P>
<p>也可以启动相关服务</P>
<p>service iredapd start</P>
<p>service policyd start</P>
<p>service amavisd start</P>
<p>service dovecot start</P>
<p>service fail2ban start</P>
<p>service postfix start</P>
<p>service iptables start</P>
<p>我选择重新启动电脑</P>
<p>输入ip 192.168.0.238 打开了邮件前台服务器&nbsp;<wbr> roundcube
webmail 界面</P>
<p>输入ip https://192.168.0.238/iredadmin 打开了 Login To Manage
Your</P>
<p>Mail Domains &amp; Accounts&nbsp;<wbr>
意味着&nbsp;<wbr> webmail控制端也ok了。这是邮件管理员后</P>
<p>台。</P>
<p>数据库管理图形界面工具phpmyadmin ，https://192.168.0.238/phpmyadmin也</P>
<p>打开了.</P>
<p>但是我通过 https://域名形式没打开，</P>
<p>* URLs of installed web applications:</P>
<p>*</P>
<p>* - Webmail: httpS://imail.fw.org/mail/</P>
<p>* - Admin Panel (iRedAdmin): httpS://imail.fw.org/iredadmin/</P>
<p>*&nbsp;<wbr>&nbsp;<wbr> + Username:
postmaster@fw.org, Password: 123456</P>
<p>&nbsp;<wbr></P>
<p>
&nbsp;<wbr>phpmyadmin的用户名是root密码就是我设置的123456,也就是mysql的root用户</P>
<p>，和我安装时设置的mysql用户密码.</P>
<p>&nbsp;<wbr>管理邮箱后台的用户是 postmaster@fw.org 密码123456</P>
<div>
<p>&nbsp;<wbr>前台邮箱由于没有通过管理员设置还没有用户使用。</P>
</DIV>
<p>装完iredmail后，重新启动服务器， sftpd 和 samba都不好用了</P>
<p>，重新运行setup设置防火墙，禁用，确定。然后又好用了。</P>
<p>&nbsp;<wbr>我现在只能用ip访问，主要是内网网络使用，可以了.</P>
<p>总结：安装完iredmail后，在安装目录下有个 iredmail.tips文件，记录了配置信息。什么的mail server
,apache,php,mysql,virtual users,backup mysql database都在这里可以看到。</P>
<p>&nbsp;<wbr></P>
