---
layout: post
title: "centos 5.8安装pptpd"
categories: linux 
tags: [linux, pptpd]
date: 2015-01-13 01:11:14
---

centos 5.8

<pre>
http://www.onelone.com/tutorial/vpn.html
</pre>





1,查看版本

version

http://murray.cn/index.php/2011/03/chakan-linux-centos-var/

lsb_release -a



2,network设置

ip+dns

http://blog.csdn.net/iamfafa/article/details/6209009

centos的设置主要在/etc/sysconfig/里，跟debian有些不同



3,安装常用工具

screen+htop+iftop

http://zoomquiet.org/res/scrapbook/ZqFLOSS/data/20090313234155/


centos 安装程序相比debian，没有这么方便


更新yum源

wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.2-2.el5.rf.i386.rpm

yum update




4,安装pptpd

pptpd+iptables

http://net.chinaunix.net/6/2008/01/07/1147970.shtml

http://blog.ihipop.info/2010/06/1265.html


安装ppp

yum install ppp


更新yum源,安装pptpd

<pre>
vim /etc/yum.repos.d/Doylenet.repo

[doylenet]
name=Doylenet custom repository for CentOS
baseurl=http://files.doylenet.net/linux/yum/centos/5/i386/doylenet/
gpgcheck=1
gpgkey=http://files.doylenet.net/linux/yum/centos/RPM-GPG-KEY-rdoyle
enabled=1


yum update
# yum install pptpd
</pre>



设置ip

<pre>
vim /etc/pptpd.conf 
localip 10.0.0.2
remoteip 10.0.0.200-220
</pre>



设置权限

<pre>
vim /etc/ppp/chap-secrets
username * password *
</pre>


支持转发

/etc/sysctl.conf

将“net.ipv4.ip_forward”的值改为1


<pre>
    sysctl -p  
</pre>



设置iptables NAT

<pre>
iptables -I FORWARD -s 192.168.7.64/32 -m iprange --dst-range 192.168.7.1-192.168.7.20 -j DROP
iptables -I FORWARD -s 192.168.7.64/32 -m iprange --dst-range 192.168.7.23-192.168.7.254 -j DROP
</pre>



iptables的规则保存与debian有所不同


<pre>
    /etc/init.d/iptables save  
</pre>


设置自动启动服务


<pre>
    chkconfig pptpd on  


    chkconfig iptables on  
</pre>






5,关闭不用服务(主要是不知道如何删除)

http://blog.chinaunix.net/uid-24250828-id-3161214.html





