---
layout: post
title: "kvm的使用和配置"
categories: 虚拟化
tags: [kvm, linux, 虚拟化]
date: 2014-08-18 12:51:22
---

之前用的是低端本本，32位的u还不支持vt，虚拟机用的是virtualbox，虽然挺好用，但是每次升级内核都得重新编译一遍模块，有时还不一定能编译过，所以尽管vb版本升到4.0，一直在用的都是1.6.6版，虽然简陋点，但是写写文档用用网银还是能满足的。

买了新本第一时间就把kvm装上了。kvm的全称是kernel-based virtual machine，从2.6.20开始集成到内核中。不过kvm需要cpu的vt技术支持，图形性能也不如virtualbox和vmware的好，但是cpu和内存的占用个人感觉要比前两者好。

刚装的时候用的是深度的精简版xp，结果风扇狂转，cpu占用率100%，这个和网上说的像打了鸡血一样不相符啊……到论坛去问了一下，发现是iso的问题，重新装了个win7就好多了。

要看cpu是否支持vt技术，可以google搜cpu的型号到官网去看相关信息，也可以执行下面的命令：

egrep '(vmx|svm)' /proc/cpuinfo

如果有输出则说明可以使用kvm，否则的话先到bios中检查一下是否有vt的设置并且打开了，如果这个也没有的话只能用virtualbox或者vmware了。

创建一个虚拟机文件的命令是：

qemu-img create os.img 10G

先贴个完整的启动命令：

kvm -localtime -m 1024 -vga std -net nic -net user -boot c -smp 2 -usb -usbdevice tablet -drive file=/path/to/img,cache=writeback

选项的具体含义可以man一下kvm(其实是参数选项太多我也说不清楚……)这里和这里有两篇讲解得挺详细的文章，可以参考一下。

快照(2012.01.01更新)

kvm默认的文件格式是raw，也就是使用文件来模拟实际的硬盘(当然也可以使用一块真实的硬盘或一个分区)，不过raw格式只支持内存快照(就是启动的时候加-snapshot，所有更改都写到内存)，重启之后就没了。raw格式不支持磁盘快照，因此要使用qcow或qcow2文件格式。

要创建qcow2格式的虚拟机文件的命令是：

qemu-img create -f qcow2 /path/to/os.img 10G

参数-f指定格式，如果不指定默认的是raw。

要查看文件格式使用命令

qemu-img info /path/to/os.img

把raw格式转换成qcow2格式：

qemu-img convert -f raw -O qcow2 /path/to/os.img /path/to/new-fmt.img

创建一个快照：

qemu-img snapshot -c snapshot-name /path/to/os.img

这条命令并不会创建一个新的文件，而是把快照的信息记录在/path/to/os.img中。要查看某个文件有几个快照使用命令

qemu-img snapshot -l /path/to/os.img

把虚拟机恢复到某个快照的状态：

qemu-img snapshot -a snapshot-name /path/to/os.img

删除某个快照：

qemu-img snapshot -d snapshot-name /path/to/os.img

桥接

主要是想记录一下虚拟机中使用桥接上网的问题(上面命令中使用的是NAT方式)。在网上搜了很多教程，发现都需要写好多脚本好多命令。本着精简的原则，经过多次尝试发现只要修改一下/etc/network/interfaces就行了(以下情况在本人机器上测试通过，debian 6.0，qemu-kvm 0.12.5)。下面是我机器上的/etc/network/interfaces的内容：

<pre>
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
#allow-hotplug eth0
#iface eth0 inet dhcp

# for kvm bridged networking

auto eth0
iface eth0 inet manual

auto br0
iface br0 inet dhcp
bridge_ports eth0
</pre>

最后的部分是对网卡的设置，大概就是禁用eth0，然后新增一个接口br0。然后重启网络：/etc/init.d/networking restart，不行的话重启机器。下面是启动命令，只是和使用NAT方式在网络参数方面有些不一样：

kvm -localtime -m 1024 -vga std -net nic -net tap -usbdevice tablet -boot c -smp 2 -drive file=/path/to/img,cache=writeback

如果需要启动多台机器需要为不同的机器指定不同的mac地址，要不然会出现冲突，像下面这样：

kvm -localtime -m 1024 -vga std -net nic,macaddr=52:54:00:12:34:56 -net tap -usbdevice tablet -boot c -smp 2 -drive file=/path/to/img,cache=writeback

在host中执行ifconfig会发现多出来一个br0，还有一个供guest使用的接口tap0，如果启动多台机器的话还会有tap1，tap2等等。虽然能连上网络，但是在托盘的gnome-network-manager却是显示断开的，因为它只监视eth0……

这条命令需要使用root权限执行，否则会报错：

could not configure /dev/net/tun: Operation not permitted

但是看了下/dev/net/tun的权限是666，具体原因不明。总而言之就是用root就行了，不管你信不信，反正我是信了，事情就是这样，它就是发生了……

使用usb(2012.08.07更新)

在网上搜到一些老文章都说可以用usb和网银u盾，但是在我机器上死活用不了，时间一长就忘了。今天更新kvm到1.1.0，看到安装了一个新的包libusbredirparser0，一试之下果然可以用u盾了。

在插入u盾前运行命令lsusb看看有多少个usb设备：

root@debian:~# lsusb
Bus 002 Device 003: ID 04b3:310b IBM Corp. Red Wheel Mouse
Bus 002 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 05c8:030d Cheng Uei Precision Industry Co., Ltd (Foxlink) 
Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

每一个usb设备编号由两部分组成：vendor_id:product_id，通过这个编号访问usb设备。插入u盾后再运行一次lsusb：

root@debian:~# lsusb
Bus 002 Device 013: ID xxxx:xxxx
Bus 002 Device 003: ID 04b3:310b IBM Corp. Red Wheel Mouse
Bus 002 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 05c8:030d Cheng Uei Precision Industry Co., Ltd (Foxlink) 
Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

多出来的那一行就是u盾的设备信息，即xxxx:xxxx(这里显示的是实际的设备编号)。然后在启动虚拟机的时候加上选项：

-usb -usbdevice host:xxxx:xxxx

就行了。如果想在虚拟机启动后使用usb设备(即启动的时候没有指定)，可以按Ctrl-Alt-2进入控制台，然后执行

usb_add host:xxxx:xxxx

就可以动态添加新的usb设备。要移除usb设备则执行

usb_del host:xxxx:xxxx

使用命令

info usb

可以查看当前虚拟机上连接的usb设备。

要回到虚拟机界面，按Ctrl-Alt-1。

注意启动kvm的时候要用root运行，否则会出现”husb: open /dev/bus/usb/002/004: Permission denied”之类的错误。

使用招行u盾不能远程登录，否则老报错，但是又不说为啥错。在网上找了好久才发现问题，因为一般人都不会远程登录用u盾……

端口映射(2011.08.20更新)

-redir tcp:host_port::guest_port

表示把主机上的端口host_port映射到虚拟机的端口guest_port。

其它(2011.12.4更新)

在host中可以通过下面的命令来挂载虚拟机文件：

mount -o loop,offset=32256 /path/to/img /mnt

在虚拟机起不来的时候可以使用这个方法备份里面的数据。

更多配置后续补充。

参考资料

[1] 操作系统虚拟化之KVM http://www.staratlas.cn/archive/kvm-windows.html

