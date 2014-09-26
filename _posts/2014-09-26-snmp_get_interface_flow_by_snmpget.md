---
layout: post
date: 2014-09-26 15:03:28
title: "如何用snmpwalk/snmpget获取网卡流量"
categories: linux
tags: [linux, snmp, net-snmp, snmpget, snmpwalk]
---

<pre>
本机已经yum安装过了net-snmp套件了，但是使用了
snmpwalk -v 2c -c public localhost RFC1213-MIB::ifInOctets
结果是

IF-MIB::ifInOctets = No Such Object available on this agent at this OID

请问要做什么配置才可以获取流量信息，可以指定网卡么？


默认安装net-snmp是没有打开获取网卡流量等信息的权限的，为了能获取到流量需要对/etc/snmp/snmpd.conf做两处修改，
参考这篇文章，http://os.51cto.com/art/201103/252149.htm
1)去掉注释，打开这个名字为mib2的view，在89行

#view mib2 included .iso.org.dod.internet.mgmt.mib-2 fc  

2)修改access，将view从原来的systemview改成mib2

access notConfigGroup "" any noauth exact systemview none none  
access notConfigGroup "" any noauth exact mib2 none none  

重启snmpd就可以了使用最开始的命令了。

snmpwalk -v 2c -c public localhost RFC1213-MIB::ifInOctets
IF-MIB::ifInOctets.1 = Counter32: 167493
IF-MIB::ifInOctets.2 = Counter32: 84133
IF-MIB::ifInOctets.3 = Counter32: 12726861


</pre>
