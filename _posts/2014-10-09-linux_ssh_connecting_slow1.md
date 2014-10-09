---
layout: post
title: "linux SSH 连接缓慢问题处理"
categories: linux
tags: [linux, ssh]
date: 2014-10-09 17:37:10
---

SSH 连接缓慢问题处理

问题现象：

我们有时候会遇到ssh连接服务器的时候非常慢，经常是要等30秒以上，甚至更长的时间。但是通过telent没有问题可以实现秒登，ping都没有问题返回都是几毫秒。


问题原因：

原因是因为ssh在连接的时候会去寻找DNS记录进行查找访问，那么这个时候DNS又正好没有开启或者说DNS里面没有需要sshd访问的相关记录，所有DNS在轮训的时候就会耗费大量的时间。


解决办法：

1、在服务器上配置ip及hostname对应解析

2、修改sshd配置文件UseDNS参数，将其禁用即可

3、修改ssh配置文件GSSAPIAuthentication 参数，将其禁用即可

4、修改名称搜索优先级，配置nsswitch.conf文件

5、重启sshd服务及network服务


步骤如下：

{% highlight bash %}
    1、在服务器上配置ip及hostname对应解析   
    [root@standby ~]# echo 192.168.7.60 stanby >>/etc/hosts  

      
    2、修改/etc/ssh/sshd_config文件，添加如下两个参数   
    [root@standby ~]# echo UseDNS=no >>/etc/ssh/ssh_config  
    [root@standby ~]# echo GSSAPIAuthentication no >>/etc/ssh/ssh_config  
    [root@standby ~]#  
      
    3、修改/etc/nsswitch.conf保证hosts参数files在前面   
    [root@standby ~]# cat /etc/nsswitch.conf |grep hosts  
    #hosts: db files nisplus nis dns  
    hosts: files dns  
      
    4、重启sshd和network服务   
    [root@standby ~]# service sshd restart  
    Stopping sshd: [ OK ]  
    Starting sshd: [ OK ]  
      
    [root@standby ~]# service network restart  
    Shutting down interface eth0: [ OK ]  
    Shutting down loopback interface: [ OK ]  
    Bringing up loopback interface: [ OK ]  
    Bringing up interface eth0: [ OK ]  
    [root@standby ~]#  


{% endhighlight %}

<pre>
http://blog.csdn.net/wuweilong/article/details/22443987
</pre>
