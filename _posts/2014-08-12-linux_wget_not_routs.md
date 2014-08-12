---
layout: post
title:  "FTP错误ftp: connect: No route to host的解决办法"
date:   2014-08-12 17:37:11
categories: Linux
---

现象：


<pre>
ftp: connect: No route to host
 
ftp> ls
227 Entering Passive Mode (1,2,3,4,43,196)
ftp: connect: No route to host
ftp> passive
Passive mode off.
</pre>

 

停止ftp服务器上的iptables 则一切正常，于是判断是iptables的问题

FTP错误ftp: connect: No route to host的解决办法


<pre>
Try "modprobe ip_conntrack_ftp", if that helps. If yes, then you should
add that module to /etc/sysconfig/iptables-config.

In /etc/sysconfig/iptables-config try setting
IPTABLES_MODULES="ip_nat_ftp ip_conntrack_ftp"
and restart iptables.
</pre>

 

<pre>
[root@host335 ~]# service iptables stop
Flushing firewall rules: [  OK  ]
Setting chains to policy ACCEPT: filter [  OK  ]
Unloading iptables modules: [  OK  ]
[root@host335 ~]# service iptables start
Applying iptables firewall rules: [  OK  ]
Loading additional iptables modules: ip_nat_ftp ip_conntrack_ftp [  OK  ]
</pre>
