---
layout: post
title: "linux ssh 连接很慢的解决办法"
categories: linux
tags: [linux, ssh]
date: 2014-10-09 17:32:01
---

周海汉 /文
ablozhou # gmail.com
http://blog.csdn.net/ablo_zhou
2009.12.25 圣诞快乐！
 
=============

现象：

在局域网内，能ping通目标机器，并且时延是微秒级。

用ssh连局域网内其他linux机器，会等待10-30秒才有提示输入密码。严重影响工作效率。

 

========================

客户端操作系统版本：

{% highlight bash %}
zhouhh@zhhofs:~$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=9.10
DISTRIB_CODENAME=karmic
DISTRIB_DESCRIPTION="Ubuntu 9.10"
{% endhighlight %}

 

========================

调试信息：

{% highlight bash %}

    zhouhh@zhhofs:~$ ssh -v 192.168.12.16  
    OpenSSH_5.1p1 Debian-6ubuntu2, OpenSSL 0.9.8g 19 Oct 2007  
    debug1: Reading configuration data /etc/ssh/ssh_config  
    debug1: Applying options for *  
    debug1: Connecting to 192.168.12.16 [192.168.12.16] port 22.  
    debug1: Connection established.  
    debug1: identity file /home/zhouhh/.ssh/identity type -1  
    debug1: identity file /home/zhouhh/.ssh/id_rsa type -1  
    debug1: identity file /home/zhouhh/.ssh/id_dsa type -1  
    debug1: Remote protocol version 2.0, remote software version OpenSSH_4.3  
    debug1: match: OpenSSH_4.3 pat OpenSSH_4*  
    debug1: Enabling compatibility mode for protocol 2.0  
    debug1: Local version string SSH-2.0-OpenSSH_5.1p1 Debian-6ubuntu2  
    debug1: SSH2_MSG_KEXINIT sent  
    debug1: SSH2_MSG_KEXINIT received  
    debug1: kex: server->client aes128-cbc hmac-md5 none  
    debug1: kex: client->server aes128-cbc hmac-md5 none  
    debug1: SSH2_MSG_KEX_DH_GEX_REQUEST(1024<1024<8192) sent  
    debug1: expecting SSH2_MSG_KEX_DH_GEX_GROUP  
    debug1: SSH2_MSG_KEX_DH_GEX_INIT sent  
    debug1: expecting SSH2_MSG_KEX_DH_GEX_REPLY  
    debug1: Host '192.168.12.16' is known and matches the RSA host key.  
    debug1: Found key in /home/zhouhh/.ssh/known_hosts:1  
    debug1: ssh_rsa_verify: signature correct  
    debug1: SSH2_MSG_NEWKEYS sent  
    debug1: expecting SSH2_MSG_NEWKEYS  
    debug1: SSH2_MSG_NEWKEYS received  
    debug1: SSH2_MSG_SERVICE_REQUEST sent  
    debug1: SSH2_MSG_SERVICE_ACCEPT received  
    debug1: Authentications that can continue: publickey,gssapi-with-mic,password  
    debug1: Next authentication method: gssapi-with-mic  
    debug1: An invalid name was supplied  
    Cannot determine realm for numeric host address  
    debug1: An invalid name was supplied  
    Cannot determine realm for numeric host address  
    debug1: An invalid name was supplied  
    debug1: Next authentication method: publickey  
    debug1: Trying private key: /home/zhouhh/.ssh/identity  
    debug1: Trying private key: /home/zhouhh/.ssh/id_rsa  
    debug1: Trying private key: /home/zhouhh/.ssh/id_dsa  
    debug1: Next authentication method: password  
    zhouhh@192.168.12.16's password:   
    debug1: Authentication succeeded (password).  
    debug1: channel 0: new [client-session]  
    debug1: Entering interactive session.  
    debug1: Sending environment.  
    debug1: Sending env LANG = zh_CN.UTF-8  
    Last login: Fri Dec 25 13:35:04 2009 from 192.168.11.146  
{% endhighlight %}

 

可以看到如下的错误信息：

<pre>
debug1: Next authentication method: gssapi-with-mic
debug1: An invalid name was supplied
Cannot determine realm for numeric host address
</pre>

 

事实上，正是从gssapi-with-mic这一行开始，开始耗时间。

 

====================

失败的尝试：


有人说是在目标机器中修改/etc/ssh/sshd_conf文件

将UseDNS 的缺省值由yes修改为no，并重启sshd。我试了，对这种情况不管用。但不排除对别的延迟情况管用。

 

====================

有效的解决办法：

1. 修改本地机器的hosts文件，将目标机器的IP和域名加上去。或者让本机的DNS 服务器能解析目标地址。

vi /etc/hosts

 

192.168.12.16  ourdev

 

其格式是“目标机器IP 目标机器名称”这种方法促效。没有延迟就连上了。不过如果给每台都加一个域名解析，挺辛苦的。但在windows下用putty或secure-crt时可以采用这种方法。

 

2.修改本机的客户端配置文件ssh_conf，注意，不是sshd_conf

vi /etc/ssh/ssh_conf

 

找到

GSSAPIAuthentication yes

改为

GSSAPIAuthentication no

保存。

 

再连目标机器，速度就飞快了。

GSSAPI ( Generic Security Services Application Programming Interface) 是一套类似Kerberos 5 的通用网络安全系统接口。该接口是对各种不同的客户端服务器安全机制的封装，以消除安全接口的不同，降低编程难度。但该接口在目标机器无域名解析时会有问题。我看到有人给ubuntu提交了相关bug， 说要将GSSAPIAuthentication的缺省值设为no，不知为何，ubuntu9.10的缺省值还是yes。

 

修改完毕，此时的连接调试数据变为了：

{% highlight bash %}

    zhouhh@zhhofs:~$ ssh -v 192.168.12.16  
    OpenSSH_5.1p1 Debian-6ubuntu2, OpenSSL 0.9.8g 19 Oct 2007  
    debug1: Reading configuration data /etc/ssh/ssh_config  
    debug1: Applying options for *  
    debug1: Connecting to 192.168.12.16 [192.168.12.16] port 22.  
    debug1: Connection established.  
    debug1: identity file /home/zhouhh/.ssh/identity type -1  
    debug1: identity file /home/zhouhh/.ssh/id_rsa type -1  
    debug1: identity file /home/zhouhh/.ssh/id_dsa type -1  
    debug1: Remote protocol version 2.0, remote software version OpenSSH_4.3  
    debug1: match: OpenSSH_4.3 pat OpenSSH_4*  
    debug1: Enabling compatibility mode for protocol 2.0  
    debug1: Local version string SSH-2.0-OpenSSH_5.1p1 Debian-6ubuntu2  
    debug1: SSH2_MSG_KEXINIT sent  
    debug1: SSH2_MSG_KEXINIT received  
    debug1: kex: server->client aes128-cbc hmac-md5 none  
    debug1: kex: client->server aes128-cbc hmac-md5 none  
    debug1: SSH2_MSG_KEX_DH_GEX_REQUEST(1024<1024<8192) sent  
    debug1: expecting SSH2_MSG_KEX_DH_GEX_GROUP  
    debug1: SSH2_MSG_KEX_DH_GEX_INIT sent  
    debug1: expecting SSH2_MSG_KEX_DH_GEX_REPLY  
    debug1: Host '192.168.12.16' is known and matches the RSA host key.  
    debug1: Found key in /home/zhouhh/.ssh/known_hosts:1  
    debug1: ssh_rsa_verify: signature correct  
    debug1: SSH2_MSG_NEWKEYS sent  
    debug1: expecting SSH2_MSG_NEWKEYS  
    debug1: SSH2_MSG_NEWKEYS received  
    debug1: SSH2_MSG_SERVICE_REQUEST sent  
    debug1: SSH2_MSG_SERVICE_ACCEPT received  
    debug1: Authentications that can continue: publickey,gssapi-with-mic,password  
    debug1: Next authentication method: publickey  
    debug1: Trying private key: /home/zhouhh/.ssh/identity  
    debug1: Trying private key: /home/zhouhh/.ssh/id_rsa  
    debug1: Trying private key: /home/zhouhh/.ssh/id_dsa  
    debug1: Next authentication method: password  
    zhouhh@192.168.12.16's password:   
{% endhighlight %}

 

