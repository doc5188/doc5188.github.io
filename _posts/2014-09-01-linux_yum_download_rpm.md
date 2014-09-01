---
layout: post
title: "使用yum只获取rpm包不自动安装"
categories: linux
tags: [linux, yum]
date: 2014-09-01 15:20:31
---

一、使用 yum-downloadonly 插件

参考文章：ghosTzone 的博客

http://ghostm55.is-programmer.com/posts/6422.html
 

yum是一个优秀的软件获取与系统更新的工具，主要应用于redhat系列的发行版本上。但是这样一个优秀的工具却没有原生提供只下载不安装的功能，而这样的功能在pacman与aptitude下都有。今天在CentOS的邮件列表上看到有人在讨论这个问题，了解到了这个问题要解决起来非常方便。

　　yum有一个plugin叫做yum-downloadonly，它就可以为用户实现只下载软件包的功能：

{% highlight bash%}
# yum install yum-downloadonly
{% endhighlight %}

<pre>
　　完成安装后，yum就多了两个命令参数，分别是：

    --downloadonly
    --downloaddir=/path/to/dir

　　这两个命令参数的含义非常明确，不用多作解释了，这样，用户就可以做到使用yum只下载软件包，不自动安装了。
</pre>

示例：

{% highlight bash%}
# yum install unixODBC --downloadonly --downloaddir=/var
{% endhighlight %}

就会自动把对应系统的 unixODBC 版本下载到目录 /var 下。

注意：如果系统中已经安装了unixODBC，那么就不会下载成功。

 

 

二、不使用yum-downloadonly 插件。(但会自动安装或升级)

yum 默认情况下，升级或者安装后，会删除下载的rpm包。

可以设置升级后不删除下载的rpm包

vi /etc/yum.conf
<pre>
[main]
cachedir=/var/cache/yum
keepcache=0
</pre>

将 keepcache=0 修改为 keepcache=1， 安装或者升级后，在目录 /var/cache/yum 下就会有下载的 rpm 包。

 
