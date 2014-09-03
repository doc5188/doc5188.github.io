---
layout: post
title: "CentOS开机自动运行程序的脚本"
categories: linux
tags: [script, centos, linux]
date: 2014-09-03 12:54:23
---

CentOS开机自动运行程序的脚本
 
有些时候我们需要在服务器里设置一个脚本，让他一开机就自己启动。方法如下：
{% highlight bash %}
# cd /etc/init.d
# vi youshell.sh   #将youshell.sh修改为你自己的脚本名
{% endhighlight %}
编写自己的脚本后保存退出。
在编写脚本的时候，请先加入以下注释
<pre>
#add for chkconfig
#chkconfig: 2345 70 30
#description: the description of the shell   #关于脚本的简短描述
#processname: servicename                    #第一个进程名，后边设置自启动的时候会用到
说明：
2345是指脚本的运行级别，即在2345这4种模式下都可以运行，234都是文本界面，5就是图形界面X
70是指脚本将来的启动顺序号，如果别的程序的启动顺序号比70小（比如44、45），则脚本需要等这些程序都启动以后才启动。
30是指系统关闭时，脚本的停止顺序号。
</pre>
给脚本添加上可执行权限：
{% highlight bash %}
# chmod +x youshell.sh
{% endhighlight %}
利用chkconfig命令将脚本设置为自启动
{% highlight bash %}
# chkconfig --add servicename
{% endhighlight %}
这样你的脚本就可以在开机后自动运行了。

另外，在redhat里也可以使用这个方法来实现开机自启动。

chkconfig的使用方法
<pre>
chkconfig(check config)
功能说明：检查，设置系统的各种服务。
语　　法：chkconfig
[--add][--del][--list][系统服务]或chkconfig[--level<等级代号>][系统服务][on/off/reset]
补充说明：这是RedHat公司遵循GPL规则所开发的程序，它可查询操作系统在每一个执行等级中会执行哪些系统服务，其中包括各类常驻服务。
参数：
　–add　增加所指定的系统服务，让chkconfig指令得以管理它，并同时在系统启动的叙述文件内增加相关数据。
　–del　删除所指定的系统服务，不再由chkconfig指令管理，并同时在系统启动的叙述文件内删除相关数据。
　–level<等级代号>　指定读系统服务要在哪一个执行等级中开启或关毕
1：chkconfig 命令也可以用来激活和解除服务。chkconfig –list 命令显示系统服务列表，以及这些服务在运行级别0到6中已被启动（on）还是停止（off）。
chkconfig –list
chkconfig –list httpd
httpd 0:off 1:off 2:on 3:on 4:on 5:on 6:off
2：chkconfig 还能用来设置某一服务在某一指定的运行级别内被启动还是被停运。譬如，要在运行级别3、4、5中停运 nscd 服务，使用下面的命令：
chkconfig –level 345 nscd off
3：由 xinetd 管理的服务会立即被 chkconfig 影响。譬如，如果 xinetd 在运行，finger 被禁用，那么执行了 chkconfig finger on 命令后，finger 就不必手工地重新启动 xinetd 来立即被启用。对其它服务的改变在使用 chkconfig 之后不会立即生效。必须使用service servicename start/stop/restart命令来重起服务
 
</pre>

第二种方法

编辑  /etc/rc.d/rc.local文件 

格式为  程序名  程序路径

例如  a.sh  /home/a.sh

