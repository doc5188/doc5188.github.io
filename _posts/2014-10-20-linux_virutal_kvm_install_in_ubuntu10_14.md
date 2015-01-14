---
layout: post
title: "ubuntu 10.04安装kvm"
categories: linux
tags: [kvm, linux, ubuntu]
date: 2014-10-20 13:13:45
---
 
==========================================================================================
研究了很久的KVM，感觉是我用过的最快的虚拟机。对比常用的虚拟机，Vmware的功能全面，设置简单，但其速度不是很好；VirtualBox的效率虽然比Vmware高一些，但是存在不少缺点，感觉在运行时比较抢CPU，现在virtualbox已经支持smp,和虚拟化技术，但整体效率还是没有KVM高（但是图形效率作的不错）；KVM（Kernel-based Virtual Machine），基于内核的虚拟机，是我用过的最快的虚拟机，需要CPU支持虚拟化技术，并且在BIOS里打开虚拟化选项，效率可达到物理机的80％以上，对SMP的支持很好。所以现在强烈吐血卖命推荐KVM。（注：在原文最下面添加了版虚拟化驱动（virtio)的使用方式）
（使用磁盘方式以更新，请大家注意！！！）

没有废话，以下是在UBUNTU 10.04.1 64BIT下的方法

* 获得KVM：

KVM的网站：http://sourceforge.net/projects/kvm/files/

下载最新的qemu-kvm-0.13.0.tar.gz

* 解压：
{% highlight bash %}
tar -xzvf qemu-kvm-0.13.0.tar.gz
{% endhighlight %}

需要用到的包：

在 UBUNTU 10.04中 ,可以使用
{% highlight bash %}
sudo apt-get build-dep qemu-kvm
{% endhighlight %}

来解决依赖关系。

三步曲：
{% highlight bash %}
cd qemu-kvm-0.13.0
/configure --prefix=/usr/local/kvm
make
sudo make install
{% endhighlight %}

安装好以后加载KVM模块
{% highlight bash %}
sudo modprobe kvm
sudo modprobe kvm-intel //如果你的是INTEL处理器就用这个
sudo modprobe kvm-amd //如果你的是AMD处理器就用这个
{% endhighlight %}

这样就装好了。

下面介绍配置KVM桥接网络的方法： \\特别注意，大部分不能桥接无线网卡。。。只能桥接PCI网卡。。。。

安装桥接工具：
{% highlight bash %}
sudo apt-get install bridge-utils
{% endhighlight %}

安装创建TAP界面的工具：
{% highlight bash %}
sudo apt-get install uml-utilities
{% endhighlight %}

编辑网络界面配置文件（
{% highlight bash %}
sudo vi /etc/network/interfaces
{% endhighlight %}
),根据你的情况加入以下内容：
{% highlight bash %}
auto eth0
iface eth0 inet manual

auto tap0
iface tap0 inet manual
up ifconfig $IFACE 0.0.0.0 up
down ifconfig $IFACE down
tunctl_user lm \\lm是我的用户名，在这里换为你的用户名

auto br0
iface br0 inet static \\当然这里也可以使用DHCP分配
bridge_ports eth0 tap0
address 192.168.1.3
netmask 255.255.255.0
gateway 192.168.1.1
{% endhighlight %}


激活tap0和br0: //有些时候会不奏效，但重启后就行了
{% highlight bash %}
sudo /sbin/ifup tap0
sudo /sbin/ifup br0
{% endhighlight %}

好了以后ifconfig看一下，多了一个tap0和br0, br0上的IP地址就是你本机的IP地址。

KVM的使用方法：

KVM的使用方法具体可以参考
{% highlight bash %}
/usr/local/kvm/bin/qemu-system-x86_64 --help
{% endhighlight %}

下面具体举几个例子：

创建虚拟磁盘(用qemu-img命令）：
{% highlight bash %}
mkdir kvm
cd kvm
/usr/local/kvm/bin/qemu-img create -f qcow2 winxp.img 10G
{% endhighlight %}

创建虚拟机：
{% highlight bash %}
sudo /usr/local/kvm/bin/qemu-system-x86_64 -m 512 -drive file=/home/lm/kvm/winxp.img,cache=writeback -localtime -net nic,vlan=0,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tap0,script=no -boot d -cdrom /home/lm/iso/winxp.iso -smp 2 -soundhw es1370
{% endhighlight %}


这里对各个参数说明一下：
<pre>
-m 512

分配512MB的内存给GUEST OS

-drive file=/home/lm/kvm/winxp.img,cache=writeback

使用虚拟磁盘的文件和路径，并启用writeback缓存。
-localtime

使用本地时间（一定要加这个参数，不然虚拟机时间会有问题）
-net nic,vlan=0,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tapo,script=no

使用网络，并连接到一个存在的网络设备tap0,注意mac地址一定要自己编一个，特别是如果你虚拟了多个系统并且要同时运行的话，不然就MAC冲突了，在
-boot d

从光盘启动 （从硬盘启动则为 -boot c )
-cdrom /home/lm/iso/winxp.iso

使用的光盘镜像，如果要使用物理光驱的话就是 -cdrom /dev/cdrom
-smp 2

smp处理器个数为2个，如果你是4核处理器，后面的数字就为4（如果不开启此选项，则只能以单核模式运行）
</pre>

开始启动装系统了吧？是不是非常的快？如果你机器可以的话大概在15分钟左右就把XP装好了。

启动装好的虚拟机（很简单，上面的命令改两个参数就行）：
{% highlight bash %}
sudo /usr/local/kvm/bin/qemu-system-x86_64 -m 512 -drive file=/home/lm/kvm/winxp.img,cache=writeback -localtime -net nic,vlan=0,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tap0,script=no -boot c -smp 2 -soundhw es1370
{% endhighlight %}


然后在客户端里设置好IP地址就可以使用了，但是KVM的显卡能力不行，可以通过rdesktop远程连接解决
{% highlight bash %}
rdesktop 192.168.1.4:3389 -u administrator -p ****** -g 1280x750 -D -r sound:local \\分辨率可以自行设定，是不是比VirtualBox的无缝连接模式要爽？？
{% endhighlight %}



补充：

如果同时运行多个GUEST OS ，则网络设置要改一下，在/etc/network/interfaces 里加几个tap界面就行了，每个GUEST OS单独使用一个TAP，比如说现在要同时运行3个GUEST OS ，则配置文件如下：
{% highlight bash %}
auto tap0
iface tap0 inet manual
up ifconfig $IFACE 0.0.0.0 up
down ifconfig $IFACE down
tunctl_user lm \\lm是我的用户名，在这里换为你的用户名

auto tap1
iface tap1 inet manual
up ifconfig $IFACE 0.0.0.0 up
down ifconfig $IFACE down
tunctl_user lm \\lm是我的用户名，在这里换为你的用户名

auto tap2
iface tap2 inet manual
up ifconfig $IFACE 0.0.0.0 up
down ifconfig $IFACE down
tunctl_user lm \\lm是我的用户名，在这里换为你的用户名

auto br0
iface br0 inet static \\当然这里也可以使用DHCP分配
bridge_ports eth0 tap0 tap1 tap2
address 192.168.1.3
netmask 255.255.255.0
gateway 192.168.1.1
{% endhighlight %}

启动GUEST OS
{% highlight bash %}
sudo /usr/local/kvm/bin/qemu-system-x86_64 -m 512-drive file=/home/lm/kvm/winxp.img,cache=writeback -localtime -net nic,vlan=0,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tap0,script=no -boot c -smp 2 -soundhw es1370
{% endhighlight %}


把ifname=tap0换为你要tap1或者tap2就行了,MAC也要改噢。。

要注意，系统重启后要重新加载kvm内核模块：
{% highlight bash %}
sudo modprobe kvm
sudo modprobe kvm-amd //如果使用AMD处理器
sudo modprobe kvm-intel //如果是用INTEL处理器
{% endhighlight %}

当然，你也可以修改系统相关设置在启动时自动加载该模块。

同理，可以用此方法安装LINUX。装完了可以对比一下，是不是比VB和VM要爽得多呢？

其他比如像USB连接问题可以参考论坛里的帖子

我已经在我的系统里同时运行了4个CentOS 4.8 1个winxp sp3 1个win2003 sp2 5个FreeBSD 8.0

速度太快了，难以置信。

系统配置为：Athlon X2 5000+ 8G RAM 跑的Ubuntu 10.04.1 64bit

其实KVM的安装和使用都很方便简单的，大家要理解KVM各个参数的含义。最关键的就是KVM的网络桥接的设置，在这里大家要多看软件自身的文档，会有很大的帮助。

以上是KVM的最基础的实现方法，望大家多看文档，以便掌握更多更灵活的功能。

BTW：

[b]现在已经找到了原来磁盘性能糟糕的原因，按照以往的方法是用 -hda disk.img 的方法来使用虚拟磁盘，现在版本更新以后时候 -drive file=/home/lm/kvm/winxp.img,cache=writeback 来使用虚拟磁盘，请广大使用KVM的用户注意这里的变化。

注：Ubuntu 10.04 LTS 下的安装源里的KVM的方法(qemu-kvm 0.12.3)：

直接
{% highlight bash %}
sudo apt-get install qemu-kvm
{% endhighlight %}

网络配置如上，是一样的。

大家注意一个问题，如果你虚拟的是WIN2003，那么切勿在－net参数中使用model=e1000,否则HOST和GUEST之间不能PING通

添加：半虚拟化驱动使用方式如下

WIN系统需要下载的驱动程序：

http://www.linux-kvm.com

在左手边有一个Windows Guest Drivers,下载cdrom image和floppy image

使用版虚拟化驱动（virtio)可以得到更好的磁盘性能和网络性能，使用版虚拟化驱动的时候，KVM的启动参数如下(安装WIN时）：
{% highlight bash %}
sudo /usr/local/kvm/bin/qemu-system-x86_64 -m 512 -drive file=/home/lm/kvm/winxp.img,if=virtio,boot=on,cache=writeback -localtime -net nic,vlan=0,model=virtio,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tap0,script=no -boot d -cdrom /home/lm/iso/winxp.iso -fda=/disk/virtio-win-1.1.11-0.vfd -smp 2
{% endhighlight %}

说明一下新的参数：
<pre>
在file=/home/lm/kvm/winxp.img,if=virtio,boot=on,cache=writeback中

添加了if=virtio,通过virio来使用磁盘
在 -net nic,vlan=0,model=virtio,macaddr=52-54-00-12-34-01中

添加了model=virtio,通过virtio来使用网络
-fda=/disk/virtio-win-1.1.11-0.vfd

驱动程序的软盘镜像，-fda为添加一个软盘驱动器
</pre>

在安装WINDOWS的时候需要注意：在虚拟机启动从光盘引导启动WINDOWS安装的时候（最开始的时候）会提示你，按F6选择第三方驱动程序，按F6以后过几秒钟，它会出现选择第三方驱动的画面，按下S，会让你选择你要加载的第三方驱动。（网络太慢，图传不上来，大家可参考：http://www.linux-kvm.org/page/WindowsGuestDrivers/viostor/installation）

在WINDOWS安装完成以后，还要安装virtio网络驱动程序，修改KVM启动参数：

{% highlight bash %}
sudo /usr/local/kvm/bin/qemu-system-x86_64 -m 512 -drive file=/home/lm/kvm/winxp.img,if=virtio,boot=on,cache=writeback -localtime -net nic,vlan=0,model=virtio,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tap0,script=no -boot c -cdrom /home/lm/iso/virtio-win-1.1.11-0.iso -smp 2
{% endhighlight %}

启动虚拟机，启动好WIN系统以后，在WIN中安装网卡驱动程序（在设备管理器中安装），驱动程序就在虚拟机的光驱中。有时在安装过程中会出现问题，那么去掉cache=writeback重新安装试试。

现在主流的LINUX系统的内核都集成了virtio驱动，所以在使用半虚拟化驱动安装LINUX的时候可以直接安装，无需加载virtio驱动来安装。

注：

如果你使用的是raw文件系统或LVM分区，则应该将cache=writeback改为cache=none

建议大家使用LVM分区方式，这样虚拟机的磁盘性能可以接近物理机的磁盘性能。关于LVM的创建大家可以去查找相关文章，在这里给大家一个KVM使用LVM分区的示例：
{% highlight bash %}
sudo /usr/local/kvm/bin/qemu-system-x86_64 -m 512 -drive file=/dev/vg0/lv1,if=virtio,boot=on,cache=none -localtime -net nic,vlan=0,model=virtio,macaddr=52-54-00-12-34-01 -net tap,vlan=0,ifname=tap0,script=no -boot c -smp 2
{% endhighlight %}

