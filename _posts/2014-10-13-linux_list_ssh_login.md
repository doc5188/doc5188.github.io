---
layout: post
title: "在一个列表里选定主机名后直接SSH登陆"
categories: linux
tags: [ssh, csshx]
date: 2014-10-13 09:29:59
---

标题真拗口，详细一点应该是，在一个文本文件里有一个主机名（和 IP 地址）列表，通过 vi/vim 的上下键选择某个主机名（IP 地址）后，点击回车键就可以完成相应的 SSH 登陆。

不管 chef/puppet/salt/ansible 这类自动化配置工具多么智能，我们总有需要登陆到单台服务器上找问题的时候。总不能每次去翻 doc/txt 文档找相应的 IP 地址和用户名吧，找到 IP 地址和用户名后、copy 出来、切换窗口、再 ssh？有点累～～

机械的工作总是能找到替代的工具来完成，warp 就是这样一个小工具，确切的说是一个小 bash 脚本，warp 从 .warp 文本文件里读取主机名（IP 地址）信息，然后自动连上 ssh.

{% highlight bash %}
$ wget https://raw.githubusercontent.com/jpalardy/warp/master/warp
$ chmod +x warp
{% endhighlight %}

我们可以看到这个 .warp 文件格式很自由，只要保证第一列是主机名和 IP 地址（执行 ssh 命令格式的后半部分）就可以了，还可以用 — 和 # 当作注释方便我们区分和归类不同的服务器：

{% highlight bash %}
$ vi ~/.warp
# VIRTUAL MACHINE HOSTS

-- production servers

host101.vpsee.com -- xen host
host102.vpsee.com
root@host103.vpsee.com -- kvm host
user@host104.vpsee.com

-- development servers

172.20.2.101
172.20.2.102
root@172.20.2.103
user@172.20.2.104

# SUN GRID ENGINE HOSTS

sge101
sge102.cluster.vpsee.com
192.168.2.15 -- local datacenter
{% endhighlight %}

执行 warp 后会自动打开 vi/vim，然后使用 kj 键选择某行后回车即可：

{% highlight bash %}
$ ./warp
{% endhighlight %}

如果选择多行，warp 还支持 csshx 哦～

