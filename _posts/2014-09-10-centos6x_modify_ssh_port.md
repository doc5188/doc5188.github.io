---
layout: post
title: "CentOS6.x 修改ssh远程连接端口"
categories: linux
tags: [sshd, linux, centos]
date: 2014-09-10 14:33:21
---

ssh默认端口22，我们这里改成8888
请使用root权限进行以下操作：

1、首先设置防火墙（这一步一定要先做，不然后面换了SSH端口进不去就麻烦）

{% highlight bash %}
# iptables -I INPUT 4 -p tcp --dport 8888 -j ACCEPT
# service iptables save
# service iptables restart
{% endhighlight %}



2、备份ssh端口配置文件

{% highlight bash %}
# cp /etc/ssh/ssh_config /etc/ssh/ssh_config.bak
# cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
{% endhighlight %}


3、修改SSH端口

{% highlight bash %}
# vi /etc/ssh/sshd_config
{% endhighlight %}

在#Port 22下面添加
<pre>
Port 8888
</pre>

{% highlight bash %}
# vi /etc/ssh/ssh_config
{% endhighlight %}

在#Port 22下面添加
<pre>
Port 8888
</pre>

4、重启SSH服务

{% highlight bash %}
# service sshd restart
{% endhighlight %}


5、防火墙中删除原来的SSH默认22端口
查看SSH端口顺序

{% highlight bash %}
# iptables -L -n --line-numbers
{% endhighlight %}


删除对应序列为5的22端口

{% highlight bash %}
# iptables -D INPUT 5
{% endhighlight %}

保存

{% highlight bash %}
# service iptables save
{% endhighlight %}

重启服务

{% highlight bash %}
# service iptables restart
{% endhighlight %}
