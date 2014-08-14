---
layout: post
title:  "kvm虚拟机磁盘文件读取小结"
date:   2014-08-12 11:38:11
categories: 虚拟化
tags: [虚拟化, Linux]
---


kvm虚拟机磁盘挂载还真不是一帆风顺的。xen虚拟化默认就raw格式的磁盘，可以直接挂载，kvm如果采用raw也可以直接挂载，与xen磁盘挂载方式一致。

本文出自：http://koumm.blog.51cto.com

1.kvm虚拟化相比xen虚拟化来说，工具与方法众多，本文列举思路如下：

(1)raw格式的磁盘可以直接挂载，可以将qcow2磁盘转换成raw格式并挂载

转换示例:
{% highlight bash %}
$ qemu-img convert -fraw -O qcow2 /data/raw.img/data/qcow2.img
{% endhighlight %}


(2)通过编译安装qemu-nbd工具挂载qcows格式的磁盘

qemu-nbd工具默认没有安装，需要编译安装，该内容待测试，如确实需要也可以参考思路1去解决。

(3)通过创建KVM环境创建kvm虚拟机配置文件挂载虚拟磁盘启动虚拟机


(4)通过libguestfs-tools工具直接修改与读取qcow2虚拟磁盘文件

 

本文主要测试libguestfs-tools工具来进行测试。

2.libguestfs-tools工具的使用示例

(1)确认libguestfs-tools工具的安装，没有安装可以yum进行安装。

安装完成后，会安装很多virt-开头的命令，下面将大概介绍使用这些命令。

{% highlight bash %}
[root@node1 ~]# vir
virsh                  virt-df                virt-inspector2        virt-p2v-server        virt-tar-in
virt-alignment-scan    virt-edit              virt-install           virt-pki-validate      virt-tar-out
virt-cat               virt-filesystems       virt-list-filesystems  virt-rescue            virt-v2v
virt-clone             virt-format            virt-list-partitions   virt-resize            virt-viewer
virt-convert           virt-host-validate     virt-ls                virt-sparsify          virt-what
virt-copy-in           virt-image             virt-make-fs           virt-sysprep           virt-win-reg
virt-copy-out          virt-inspector         virt-manager           virt-tar               virt-xml-validate
{% endhighlight %}

(2)命令使用参数格式

 
{% highlight bash %}
virt-df  [--options] -d domname
virt-df [--options] -a disk.img [-a disk.img ...]
{% endhighlight %}

通常两种方式：-d是采用域名称方式，-a是直接获取的磁盘文件方式。

 
3.virt-cat命令

直接查看虚拟机里面的/etc/passwd文件，类似于cat命令。

{% highlight bash %}
[root@node1 ~]# virt-cat -d oeltest01 /etc/passwd
{% endhighlight %}


<img src="/upload/images/20130924123007226.jpg" >

4.virt-edit命令

直接编辑虚拟机里面的文件，类似于vi命令。

注：虚拟机必须处于关机状态，否则会出现如下提示：

{% highlight bash %}
libguestfs: error: error: domain is a live virtual machine.
Writing to the disks of a running virtual machine can cause disk corruption.
Either use read-only access, or if the guest is running the guestfsd daemon
specify live access.  In most libguestfs tools these options are --ro or
--live respectively.  Consult the documentation for further information.
{% endhighlight %}

<img src="/upload/images/20130924123008349.jpg" >


 
{% highlight bash %}
[root@node1 ~]# virt-edit -d oeltest01 /etc/rc.local
{% endhighlight %}

可以通过vi命令进行编辑。

<img src="/upload/images/20130924123010879.jpg" >

5.virt-df命令

直接查看虚拟机里面的磁盘使用情况，类似于df-h命令。

{% highlight bash %}
[root@node1 ~]# virt-df  -h oeltest01
{% endhighlight %}

<img src="/upload/images/20130924123011730.jpg" >

virt-filesystems命令也与上面内容类似

{% highlight bash %}
[root@node1 ~]# virt-filesystems -d oeltest01
/dev/sda1
/dev/vg/root
{% endhighlight %}
6.virt-copy-out命令

直接复制虚拟机里面的磁盘文件到本地磁盘上，类似于cp命令。

(1)拷贝oeltest01虚拟机中的passwd文件到本地/root目录下

{% highlight bash %}
[root@node1 ~]# virt-copy-out -d oeltest01 /etc/passwd /root/
{% endhighlight %}

(2)拷贝oeltest01虚拟机中的/etc/到本地/root目录下

 
{% highlight bash %}
[root@node1 ~]# virt-copy-out -d oeltest01 /etc /root/
{% endhighlight %}

<img src="/upload/images/20130924123011198.jpg" >

该命令很有用，也可以直接指定虚拟机磁盘文件进行命令。

#查看虚拟机所有磁盘文件

<img src="/upload/images/20130924123013552.jpg" >

通过直接读取磁盘文件中的内容。

{% highlight bash %}
[root@node1 ~]# virt-copy-out -a /data/test01.qcow2 -a /data/test01_add01.qcow2 /etc/sysconfig/network-scripts/ifcfg-eth0 /root/
{% endhighlight %}

7.virt-copy-in命令

直接复制虚拟化平台上本地磁盘文件到虚拟机磁盘上，类似于cp命令。

拷贝本地/root/etc.tar.gz文件到虚拟机/root目录下

{% highlight bash %}
[root@node1 ~]# virt-copy-in -d oeltest01 /root/etc.tar.gz /root/
{% endhighlight %}

注：虚拟化必须处于关机状态，可以开机验证。
 
{% highlight bash %}
[root@node1 ~]# virsh start oeltest01
域 oeltest01 已开始
[root@node1 ~]#
[root@node1 ~]#
[root@node1 ~]# virsh console oeltest01
连接到域 oeltest01
Escape character is ^]
Oracle Linux Server release 5.8
Kernel 2.6.18-308.el5 on an x86_64
test01 login: root
Pass word:
Last login: Wed Sep 11 05:21:11 on ttyS0
[root@test01 ~]# ll
total 10828
-rw------- 1 root root     1225 Sep 11 03:54 anaconda-ks.cfg
drwxr-xr-x 2 root root     4096 Sep 11 04:17 Desktop
-rw-r--r-- 1 root root 11006264 Sep 16  2013 etc.tar.gz
-rw-r--r-- 1 root root    36587 Sep 11 03:54 install.log
-rw-r--r-- 1 root root     3828 Sep 11 03:53 install.log.syslog
{% endhighlight %}

文读取虚拟机磁盘文件的内容到此，还有很多命令的命令，可以进行测试。
