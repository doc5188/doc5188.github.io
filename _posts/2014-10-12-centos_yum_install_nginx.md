---
layout: post
title: "CentOS6.5使用yum命令方便快捷安装Nginx"
categories: linux
tags: [nginx]
date: 2014-10-12 21:45:13
---

 当然，首先要求是可以联网的系统，因为yum安装需要互联网连接。 

1.为了追加 nginx 的 yum 仓库，需要创建一个文件 /etc/yum.repos.d/nginx.repo，并将下面的内容复制进去： 
<pre>
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=0
enabled=1
</pre>

2.编辑并保存/etc/yum.repos.d/nginx.repo文件后，在命令行下执行 

{% highlight bash %}
[root@localhost ~]# yum list | grep nginx
nginx.i386                               1.4.7-1.el6.ngx               @nginx   
nginx-debug.i386                         1.4.7-1.el6.ngx               nginx
{% endhighlight %}

会发现就是最新的稳定版 

于是直接执行 
{% highlight bash %}
# yum -y install nginx
{% endhighlight %}

安装即可 

3.这种安装和从源代码编译Nginx的安装完全不一样，安装完执行下面的命令 

{% highlight bash %}
[root@localhost ~]# find / -name *nginx*
/etc/nginx/nginx.conf
[root@localhost ~]# whereis nginx
nginx: /usr/sbin/nginx /etc/nginx /usr/share/nginx
{% endhighlight %}

你会发现主要文件安装到了/etc/nginx下 

接下来是启动Nginx服务，可以执行 

{% highlight bash %}
[root@localhost ~]# service nginx start
正在启动 nginx：                                           [确定]
{% endhighlight %}

启动成功。 

接着 

{% highlight bash %}
[root@localhost ~]# netstat -lntp | grep nginx
tcp        0      0 0.0.0.0:80                  0.0.0.0:*                   LISTEN      7910/nginx          
 
[root@localhost ~]# ps -ef | grep nginx
root      7910     1  0 23:43 ?        00:00:00 nginx: master process /usr/sbin/nginx -c 
/etc/nginx/nginx.conf
nginx     7912  7910  0 23:43 ?        00:00:00 nginx: worker process                   
root      7942  2459  0 23:52 pts/1    00:00:00 grep nginx
{% endhighlight %}

缺省是一个master，一个slave，可以在配置nginx.conf文件里调整 

4.设置开机自动启动 

在centos6.5下测试了一下，不用设置 

{% highlight bash %}
# chkconfig nginx on 
{% endhighlight %}

可以自行开机自动启动 
