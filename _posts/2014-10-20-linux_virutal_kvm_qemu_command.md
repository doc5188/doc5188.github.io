---
layout: post
title: "qemu-kvm 命令"
categories: 虚拟化
tags: [qemu-kvm]
date: 2014-10-20 12:55:39
---

<pre>
kvm -cpu qemu64 -drive file=/sdn/ubuntu11.10-desktop64-big.img -hdb /var/mnt/yfs/test.disk1 -hdc /var/mnt/yfs/test.disk2 -hdd /var/mnt/yfs/test.disk3 -m 16000 -vnc :11
</pre>

这样启动了一台ubuntu11.10，并在里面安装了openstack，stack虚拟机实例却无法连接网络。 后怀疑实例通过dhcp获得了不正确的ip

借此学习qemu的网络配置：

* KVM/QEMU桥接网络设置

配置kvm的网络有2种方法。

其一，默认方式为用户模式网络(Usermode Networking)，数据包由NAT方式通过主机的接口进行传送。

其二，使用桥接方式(Bridged Networking)，外部的机器可以直接联通到虚拟机，就像联通到你的主机一样。

第一，用户模式

虚拟机可以使用网络服务，但局域网中其他机器包括宿主机无法连接它。比如，它可以浏览网页，但外部机器不能访问架设在它里面的web服务器。
默认的，虚拟机得到的ip空间为10.0.2.0/24，主机ip为10.0.2.2供虚拟机访问。可以ssh到主机(10.0.2.2)，用scp来拷贝文件。

第二，桥接模式

这种模式允许虚拟机就像一台独立的主机一样拥有网络。这种模式需要网卡支持，一般的有线网卡都支持，绝大部分的无线网卡都不支持

A) 在主机上创建一个网络桥

1）安装bridge-utils

{% highlight bash %}
sudo apt-get install bridge-utils
{% endhighlight %}

2）改变网络设置，先停止网络

{% highlight bash %}
sudo invoke-rc.d networking stop
{% endhighlight %}

如果是用远程连接进行设置，设置完后，重启网络sudo invoke-rc.d networking restart，如果中途有一步错误，将不能连接

3）修改/etc/network/interfaces，直接用下面的替换。

a) 静态ip模式

<pre>
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet manual

auto br0
iface br0 inet static
address 192.168.0.10
network 192.168.0.0
netmask 255.255.255.0
broadcast 192.168.0.255
gateway 192.168.0.1
bridge_ports eth0
bridge_stp off
bridge_fd 0
bridge_maxwait 0
</pre>

b) DHCP模式

<pre>
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet manual

auto br0
iface br0 inet dhcp
bridge_ports eth0
bridge_stp off
bridge_fd 0
bridge_maxwait 0
</pre>

4）重启网络

{% highlight bash %}
sudo /etc/init.d/networking restart
{% endhighlight %}

B) 随机生成一个KVM的MAC地址

{% highlight bash %}
MACADDR="52:54:$(dd if=/dev/urandom count=1 2>/dev/null | md5sum | sed 's/^/(../)/(../)/(../)/(../).*$//1:/2:/3:/4/')"; echo $MACADDR
{% endhighlight %}

可以指定一个mac地址，但要注意，第一个字节必须为偶数，如00，52等，不能为奇数(01)，否则会有不可预料的问题。因为奇数保留为多播使用。如，KVM可以接收ARP包并回复，但这些回复会使其他机器迷惑。这是以太网的规则，而非KVM的问题。

如直接将网卡地址设置为MACADDR="32:32:32:32:32:32"

C) 将以前安装的虚拟机网络改为桥接方式或者安装新的虚拟机使用桥接网络

一个脚本文件
<pre>
#start kvm.winxp
USERID=`whoami`
MACADDR="32:32:32:32:32:32"
model=e1000e
iface=`sudo tunctl -b -u $USERID`
kvm -net nic,vlan=0,macaddr=$MACADDR -net tap,vlan=0,ifname=$iface $@
sudo tunctl -d $iface
#end kvm.winxp

</pre>

使用iso文件安装winxp，运行如下命令：
{% highlight bash %}
sudo ./kvm.bridge -m 512 -hda winxp.img -cdrom /home/software/zh-hans_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-74070.iso -boot d
{% endhighlight %}

运行安装完的虚拟机，运行如下命令：

{% highlight bash %}
sudo ./kvm.bridge -m 512 -hda winxp.img -boot c
{% endhighlight %}

===================================================================================
linux中Kvm桥接网络成功的关键

KVM在LINUX中的重要作用，速度等，我不再评价，我只能说，快！

但是，如果你要在一个服务器中使用多个虚拟机，并且想让这些虚拟机提供服务，那么，桥接网络是必不可少的，可是，网上流传的三四个版本中，关于桥接网络的，你试一下，会发现，很难成功,这是何道理？看起来他们似乎都配置成功了，也有可能是软件版本的问题，总之，你亲自尝试的时候，会发现，这其实很难实现。
当然，如果无法实现的话，也就没有此文了！

先说一下我的软件配置：

Linux 2.6.28-11-server #42-Ubuntu SMP X86＿64位Ubuntu服务器版9.04

KVM内核是自带的。

真实网络接口名称：eth0

KVM的安装方法我就不写了，网上有一大堆，注意，KVM有两个部分，一个部分是内核部分，这在9.04中是自带的，您要安装的KVM是管理部分（我也不知道这样理解是否正确，总之，你要安装KVM及QEMU）

不安装QEMU也可以用，因为KVM带一个修改版本的QEMU

成功的关键是配置网络及路由（这个在网上流传的版本中没有提到）

请生成一个文件(qemu-ifup),将这个文件加上可执行属性,文件内容如下：

<pre>
#!/bin/sh
set -x
switch=br0
if [ -n "$1" ];then
/usr/bin/sudo /usr/sbin/tunctl -u `whoami` -t $1
/usr/bin/sudo /sbin/ip link set $1 up
sleep 0.5s
/usr/bin/sudo /usr/sbin/brctl addif $switch $1
exit 0
else
echo "Error: no interface specified"
exit 1
fi
</pre>
将这个文件保存在你的HOME目录下，或者其它的目录也行。

修改你的/etc/network/interfaces文件如下：
<pre>
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).
# The loopback network interface
auto lo
iface lo inet loopback
auto br0
iface br0 inet static
bridge_ports eth0 //注意这个eth0,这是你的计算机的实际网卡，请根据你的网络修改，也可能跟我的这个一样。
address 192.168.1.242 //根据你的需要设置从这里到下面的参数，这个网络跟你的实现网络在一个子网内，不然无法桥接
netmask 255.255.255.0
network 192.168.1.0
broadcast 192.168.1.255
gateway 192.168.1.1
dns-nameserver 192.168.1.1 219.141.136.10
dns-search Office
</pre>

此时，重新启动计算机即可。

你可能注意到， 这个文件里可能有关于eth0的配置，请删除它即可，也就是说，不能对eth0进行任何配置，这个接口在重新启动后，应该是没有配置IP的，否则不能工作。

重新启动完成后，请比照一下你的接口配置是否跟我的一样：
<pre>
＃ifconfig
br0 Link encap:以太网 硬件地址 00:21:5e:4e:33:e2
inet 地址:192.168.1.242 广播:192.168.1.255 掩码:255.255.255.0
inet6 地址: fe80::221:5eff:fe4e:33e2/64 Scope:Link
UP BROADCAST RUNNING MULTICAST MTU:1500 跃点数:1
接收数据包:48324758 错误:0 丢弃:0 过载:0 帧数:0
发送数据包:25261650 错误:0 丢弃:0 过载:0 载波:0
碰撞:0 发送队列长度:0
接收字节:63199826111 (63.1 GB) 发送字节:5380518900 (5.3 GB)
eth0 Link encap:以太网 硬件地址 00:21:5e:4e:33:e2
inet6 地址: fe80::221:5eff:fe4e:33e2/64 Scope:Link
UP BROADCAST RUNNING MULTICAST MTU:1500 跃点数:1
接收数据包:48903854 错误:0 丢弃:0 过载:0 帧数:0
发送数据包:28125512 错误:0 丢弃:0 过载:0 载波:0
碰撞:0 发送队列长度:1000
接收字节:64152739997 (64.1 GB) 发送字节:6185466883 (6.1 GB)
中断:16

</pre>

请注意，只有br0有地址，而eth0是没有地址的，再比照一下你的路由表：
<pre>
# route
内核 IP 路由表
目标 网关 子网掩码 标志 跃点 引用 使用 接口
localnet * 255.255.255.0 U 0 0 0 br0
default bogon 0.0.0.0 UG 100 0 0 br0
请注意，如果你的路由表与我的不一样，例如出现四行，即又加上了
localnet * ................... eth0
default bogon ..................eth0
那么，你八成是不能成功桥接的，出现这样的问题应该是由于你的ETH0网络被配置了IP，处理的办法就是想办法去掉eth0的IP，可以使用这个方法：
#ifconfig eth0 0.0.0.0
比较一下，你的桥接网络接口：
#brctl show
bridge name bridge id STP enabled interfaces
br0 8000.00215e4e33e2 no eth0
tap0
tap1
tap2

</pre>

应该有这行存在（了可能还会出现其它的行，例如pan0),后面的tapX是不同的虚拟机的接口，这里可以看出，我桥接了三个虚拟接口到一个直接的接口。

如果你的IP地址配置与路由表跟我的一样，那么，应该是可以桥接成功的。

接下来就是启动你的虚拟机，启动前需要创建虚拟机的磁盘（即下面的u_ubuntu.img,可以参照网上的方法，这里就不重复了)，启动虚拟机的方法：

{% highlight bash %}
＃sudo kvm -hda u_ubuntu.img -boot c -net nic,model=virtio,macaddr=DE:AD:AF:22:33:22 -net tap,script=qemu-ifup -m 1024 -smp 2 -clock rtc -localtime
{% endhighlight %}

当然，有很的参数可用，我就不介绍了（其实我也不是很懂，嘿嘿），关键的问题就是macaddr和script两项，如果你有多个虚拟机，那么一样要配置不同的macaddr,script一定要指向你刚才保存的那个文件，可以使用绝对路径指明。

启动后，你应该可以正常安装操作系统了，安装完成后，如果虚拟机操作系统网络配置成DHCP，那么应该可以获取一个192.168.1.0网络内的地址，如果你不能获取地址，那么说明配置不成功。

在虚拟机工作的情况下，在宿主计算机上运行ifconfig，应该可以看到一个自动增加的接口tapX（其中X从0开始）。

小结一下：
<pre>
1）eth0（宿主计算机连接到网络的真实网络接口）不能有IP地址！
2)路由表一定要正确，可以去找一找关于路由方面的介绍，了解一下这个路由信息的意思
</pre>

 
