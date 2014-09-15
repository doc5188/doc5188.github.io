---
layout: post
title: "centos 5.2 用 pptpd 架设并配置 vpn"
categories: linux
tags: [centos, pptpd, vpn, linux]
date: 2014-09-15 22:19:21
---

<div class="bct fc05 fc11 nbw-blog ztag">
<p><font color="#000000" face="Verdana" size="5"><strong>第一章：基本安装</strong></font></p>
<p><font color="#000000" face="Verdana">1、安装ppp和iptables<br>yum install -y ppp iptables </font></p>
<p><font color="#000000" face="Verdana">2、下载pptpd的rpm包并安装<br>wget http://poptop.sourceforge.net/yum/stable/packages/pptpd-1.3.4-1.rhel5.1.i386.rpm<br>rpm -ivh pptpd-1.3.4-1.rhel5.1.i386.rpm</font></p>
<p><font color="#000000" face="Verdana">3、编辑配置文件 vi /etc/pptpd.conf<br>需要有如下内容：<br>option /etc/ppp/options.pptpd<br>logwtmp<br>localip&nbsp; 172.16.195.1<br>remoteip 172.16.195.101-200<br>一般只需加入后两行即可，即分配服务器IP和客户端IP范围，可自己选择合适的IP</font></p>
<p><font color="#000000" face="Verdana">4、编辑配置文件 vi /etc/ppp/options.pptpd<br>需要如下内容：<br>name pptpd<br>refuse-pap<br>refuse-chap<br>refuse-mschap<br>require-mschap-v2<br>require-mppe-128<br>proxyarp<br>lock<br>nobsdcomp<br>novj<br>novjccomp<br>nologfd<br>ms-dns 208.67.222.222<br>ms-dns 208.67.220.220<br>一般只需设定后两行的dns服务器地址即可，即去掉#号，把IP改为服务器的dns IP供客户端使用</font></p>
<p><font color="#000000" face="Verdana">5、编辑配置文件 vi /etc/ppp/chap-secrets<br># Secrets for authentication using CHAP<br># client server secret&nbsp;&nbsp; IP addresses<br>(user) pptpd (passwd) *<br>四项分别为客户端用户名，vpn服务器名（一般不改动），登陆密码，IP分配址（*为自动），中间用空格或Tab键隔开<br>可加入多个用户，分行录入</font></p>
<p><font color="#000000" face="Verdana">6、开启ip转发功能（否则只能连到vpn服务器，不能通过vpn服务器访问外部网络），修改配置文件</font></p>
<p><font color="#000000" face="Verdana">vi /etc/sysctl.conf 中的相应内容如下<br>net.ipv4.ip_forward = 1<br>使配置立即生效：<br>/sbin/sysctl -p</font></p>
<p><font color="#000000" face="Verdana">7、启用日志 vi /etc/syslog.conf</font></p>
<p><font color="#000000" face="Verdana">追加一行：</font></p>
<p><font color="#000000" face="Verdana">daemon.debug /var/log/pptpd.log</font></p>
<p><font color="#000000" face="Verdana">重起syslog：</font></p>
<p><font color="#000000" face="Verdana">kill -SIGHUP `cat /var/run/syslogd.pid`</font></p>
<p><font color="#000000" face="Verdana">8、配置iptables<br></font></p>
<p><font color="#000000"></font>&nbsp;</p>
<p><font color="#000000" face="Verdana">/sbin/iptables -F FORWARD</font></p>
<p><font color="#000000" face="Verdana">/sbin/iptables -A FORWARD -p udp --dport 53 -j ACCEPT<br>/sbin/iptables -A FORWARD -p tcp&nbsp; --dport 1723 -j ACCEPT<br>/sbin/iptables -A FORWARD -p gre&nbsp; -j ACCEPT<br>/sbin/iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT</font></p>
<p><font color="#000000" face="Verdana">如果要为不同客户端IP段分配不同公网IP，可类似如下设置</font></p>
<p><font color="#000000" face="Verdana">/sbin/iptables&nbsp;<font face="Verdana">&nbsp;-t nat </font>-A POSTROUTING -s&nbsp;192.168.251.0/24 -j SNAT --to-source 204.13.64.251<br>/sbin/iptables&nbsp;<font face="Verdana">&nbsp;-t nat </font>-A POSTROUTING -s 192.168.252.0/24 -j SNAT --to-source 204.13.64.252</font></p>
<p><font color="#000000" face="Verdana">......</font></p><font face="Verdana">
<p><br><font color="#000000">/etc/init.d/iptables save<br>/etc/init.d/iptables restart<br>注意：防火墙一定要开启，否则无法通过vpn服务器访问外网</font></p>
<p><font color="#000000">8、设置iptables和pptpd开机自动启动：<br>chkconfig pptpd on<br>chkconfig iptables on</font></p>
<p><font color="#000000">启动pptpd</font></p>
<p><font color="#000000">service pptpd start</font></p>
<p><font face="Verdana"><font color="#000000" face="Verdana" size="5"><strong>第二章：进阶安装（多公网IP实现拨入那个出口为那个）</strong></font></font></p>
<p><font color="#000000">1. 要配置多公网ip,基本思路是启动多个pptpd进程，分别监听每一个公网IP,并设置不同的ip池段，最后通过snat实现不同网段映射到不同的公网ip</font></p>
<p><font color="#000000">2.设置第一个公网IP<br>vi /etc/pptpd.conf <br><br>localip&nbsp; 192.168.251.1<br>remoteip 192.168.251.2-254<br>#在最后面添加一行 第一个公网ip<br>listen 210.0.0.251</font></p>
<p><font color="#000000"><font face="Verdana">添加NAT映射:<br>/sbin/iptables&nbsp;<font face="Verdana">&nbsp;-t nat </font>-A POSTROUTING -s&nbsp;192.168.251.0/24 -j SNAT --to-source 210.0.0.251<br></font><br>3.设置第二个公网IP</font></p>
<p><font color="#000000">cp /etc/pptpd.conf /etc/pptpd1.conf </font></p>
<p><font color="#000000">vi /etc/pptpd1.conf </font></p>
<p><font color="#000000">localip&nbsp; 192.168.252.1<br>remoteip 192.168.252.2-254<br>#在最后面添加一行 第一个公网ip<br>listen 210.0.0.252<br><br></font><font color="#000000" face="Verdana">添加NAT映射:<br>/sbin/iptables&nbsp;<font face="Verdana">&nbsp;-t nat </font>-A POSTROUTING -s&nbsp;192.168.252.0/24 -j SNAT --to-source 210.0.0.252<br><br>4.重复3复制配置文件pptpd2.conf,pptpd3.conf.......pptpd[N].conf<br><br>5.启动方法：<br>#pptpd -c /etc/pptpd.conf 这个已经被作为系统服务了<br>pptpd -c /etc/pptpd1.conf<br>pptpd -c /etc/pptpd2.conf<br>pptpd -c /etc/pptpd3.conf<br>........</font></p>
<p><font color="#000000">pptpd -c /etc/pptpd[N].conf<br></font></p>
<p><font color="#000000">将以上命令放入初始启动文件中<br></font><font color="#000000" face="Verdana">linux 自动启动服务很简单,最简单的是把启动命令放到/etc/rc.d/rc.local文件里这样就可以每次启动的时候自动启动服务了<br></font></p>
<p><font face="Verdana"><font color="#000000" face="Verdana" size="5"><strong>第三章：查看服务是否启动</strong></font></font></p>
<p><font color="#000000">查看网络,查看我们设置的每个公网ip上的pptp[tcp:1723]是否启动<br>netstat -a|more<br><br>查看进程<br>ps -A</font></p>
<p><br><font color="#000000">启动vpn服务器<br>service pptpd start<br><br>停止vpn服务器，但已有连接不受影晌<br>service pptpd stop<br><br>重启vpn服务器，并切断已连接的客户端<br>service pptpd restart-kill<br><br>service pptpd start<br><br>查看本机dns服务器地址<br>cat /etc/resolv.conf<br><br>查看所有网卡的信息<br>ifconfig -a</font></p></font></div>
