---
layout: post
title: "怎么用 vps + squid 配代理服务器"
date: 2014-08-18 9:00:23
categories: linux
tags: [linux, squid]
---

一共 4 步：

1. 申请一个 VPS（Virtual Private Server）。

我申请了一个亚马逊的aws ec2，可以免费使用一年。也可以去其他的国外网站上买收费的vps，一个月5美元左右。

2. 配置 VPS。

1）登录ssh。ec2的ssh使用有点搞，我把aws的文档放在下面的链接里，大家可以参考。

http://pan.baidu.com/s/1qWDIhTq

2）安装各种需要的软件，缺啥就用yum来安装。
{% highlight bash %}
# yum install XXX
{% endhighlight %}

3）在security group里加一条新的rule，选择tcp，端口任意。这个端口就是下面的squid的服务端口。这里有两点需要注意：

a. 端口的选择。我选的是21端口，不知道为什么选其他端口的话，squid就没法正常工作，打开网页经常被reset。还有绝对不能选默认的3128端口，我发现GFW屏蔽了这个端口，客户端会根本收不到服务器的tcp ack。

b. 最好在"lanch-wizard" group里添加rule。或者选择与ssh端口相同的一个group添加也行。我之前犯了一个错，就是自己新建了一个security group添加rule，结果根本无效，浪费了很多时间。

3. 配置squid。

1）配置文件如下。

{% highlight bash %}
[ec2-user@ip-172-31-40-178 ~]# cat /etc/squid/squid.conf
http_port 0.0.0.0:21 #监听在 21 端口
cache_mem 64 MB      #缓存64M
cache_dir ufs /var/spool/squid 4096 16 256
cache_effective_user squid
cache_effective_group squid
cache_access_log /var/log/squid/access.log
cache_log /var/log/squid/cache.log
cache_store_log /var/log/squid/store.log
acl all src 0.0.0.0/0.0.0.0                             #允许所有ip访问端口
{% endhighlight %}

#很多网上的文章都用ncsa_auth，其实在新的squid版本中已经改名为basic_ncsa_auth

#ps：我发现basic auth的方法有很多选择不一定非要用ncsa，squid真心强大啊！
{% highlight bash %}
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 10                            #一个帐号可以10个用户同时使用
auth_param basic credentialsttl 2 hours                 #一次认证2小时有效
auth_param basic realm Welcome to my proxy, enjoy it :D #欢迎用语
acl auth_user proxy_auth REQUIRED 
http_access allow auth_user                             #通过认证才能走代理
{% endhighlight %}

2）配置/etc/squid/passwd。这个文件管理用户访问。

添加第一个帐号，用下面的命令。
{% highlight bash %}
# htpasswd -c /etc/squid/password user1
{% endhighlight %}
之后去掉 -c 添加新帐号
{% highlight bash %}
# htpasswd /etc/squid/password user2
{% endhighlight %}

3）调试。

# squid -k parse  验证配置文件，如果有不对的话会报错。

# squid -N -d1    开启调试模式。建议先在调试模式下运行，这样有啥错都可以看到。

其他调试技巧就是连不上的时候可以用 tcpdump 抓包，或者 telnet 连端口啥的。还有就是遇到无数权限问题，我的办法简单粗暴，就是统统chmod 777。

4）启动服务。
# /etc/init.d/squid restart

4. 客户端浏览器设置，就是配代理和端口。

最后，感谢这条微博的作者“左耳朵耗子”，一切方法来源于他，谢谢。
<pre>
引用: http://tassardge.blog.163.com/blog/static/17230170820146128261044/
</pre>
