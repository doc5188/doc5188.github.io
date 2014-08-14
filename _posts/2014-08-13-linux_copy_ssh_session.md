---
layout: post
date: 2014-08-13 17:53:00
title: "Linux下SSH Session复制"
categories: linux
---

羡慕Windows下secureCRT的Session Copy功能，一直在寻找Linux下类似的软件，殊不知SSH本身就支持此功能。

特别感谢阿干同学的邮件分享。

详细方法

Linux/mac下，在$HOME/.ssh/config中加入
{% highlight bash %}
Host *
ControlMaster auto
ControlPath /tmp/ssh-%r@%h
{% endhighlight %}
至此只要第一次SSH登录输入密码，之后同个Hosts则免登。

配置文件分析
{% highlight bash %}
man ssh_config 5
ControlPath
             Specify the path to the control socket used for connection sharing as described in the ControlMaster section
             above or the string “none” to disable connection sharing.  In the path, ‘%l’ will be substituted by the
             local host name, ‘%h’ will be substituted by the target host name, ‘%p’ the port, and ‘%r’ by the remote
             login username.  It is recommended that any ControlPath used for opportunistic connection sharing include at
             least %h, %p, and %r.  This ensures that shared connections are uniquely identified.
%r 为远程机器的登录名
%h 为远程机器名
{% endhighlight %}

原理分析

严格地讲，它并不是真正意义上的Session Copy，而只能说是共享Socket。

第一次登录的时候，将Socket以文件的形式保存到：/tmp/ssh-%r@%h这个路径

之后登录的时候，一旦发现是同个主机，则复用这个Socket

故，一旦主进程强制退出（Ctrl+C），则其他SSH则被迫退出。

可以通过ssh -v参数，看debug信息验证以上过程

备注

有同学说在linux上通过证书的形式，可以实现免登录，没错。

对于静态密码，完全可以这么干；对于动态密码（口令的方式），则上述手段可以方便很多。
