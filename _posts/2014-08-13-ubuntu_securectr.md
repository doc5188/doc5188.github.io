---
layout: post
title: "打造ubuntu底下的SecureCRT（引用）"
categories: linux ubuntu
date: 2014-08-13 17:49:00
---

其实也就是就简单用gnome-terminal实现ssh列表管理,CRT分组等复杂功能没有.起码比linux putty,sshmenu等等工具好使,也比敲ssh Host,配置.ssh/config文件好用.有tabs就方便太多了.


1.打开gnome-terminal

2.菜单->编辑->配置文件->新建->输入192.168.1.3 ->标题和命令

3.标题写192.168.1.3

4.勾上运行自定义命令,自定义命令输入ssh 192.168.1.3

5.菜单->文件->打开标签页  就可以看到列表了

6.点192.168.1.3 会ssh连服务器, telnet和终端应该也是一样

可怜我找半天linux ssh client 最后是这样解决了.配合~/.ssh/config更灵活些.配合FileZilla和在win环境管理服务器已经差不了多少了

ubuntu底下gnome-terminal 的--tab 参数bug什么时候才能修复阿.....

我原来想用脚本 myssh + ssh_config 来开标签页可惜有bug
{% highlight bash %}
   #!/bin/sh
   echo $1
   if ! [ -z $1 ] ; then
           gnome-terminal --tab -t $1 -x ssh $1
   else
           echo "arg count less 1.\n"
   fi
{% endhighlight %}

（另外，linux下的终端 putty 也还行）
