---
layout: post
title: "在ubuntu 12.04中使用openvswitch+kvm构建虚拟环境"
date: 2014-08-12 17:43:43
categories: kvm openvswitch linux
---
<pre>
最近使用基于netfpga的openflow交换机做了一个实验，实验不大却也用了六台计算机，配置起来十分麻烦，做实验的时候实验室买了两台性能比较强悍的工作站，索性就把实验转移到虚拟环境中，一来可以减少给各个机器做配置的时间，把一个机器做好，其它的只需要clone即可，二来还可以学习一些虚拟化的东西，对自己也是一种提高，废话到此结束，下面进入正题。

下边所有步骤都假设你可以使用root权限执行命令，本文中的命令均使用root用户执行。

一、安装所需软件

①安装kvm

#apt-get install kvm virtinst libvirt-bin

②安装openvswitch

# apt-get install openvswitch-datapath-source openvswitch-controller openvswitch-brcompat openvswitch-switch

③安装其它相关软件

#apt-get install virt-top virt-manager python-libvirt

其中virt-manager是gui界面管理虚拟机的，建议安装，本文就是使用virt-manager操作的，当然也可是不安装使用命令行运行kvm，virt-top是查看虚拟机运行状态的，本文中没有用到，python-libvirt是是用python管理虚拟机的类库，安装它是因为我要使用程序获取虚拟机的一些运行信息，如果你习惯用java写程序，需要安装libjna-java，然后下载java版的libvirt，当然安装过程中也会遇到一些问题，这不属于本文的范畴，请自行百度。

 

二、配置openvswitch

①首先删除默认的网桥，名字是virtbr0，这个网桥是linux的birdge模块建立的，如果使用openvswitch就用不到，而且还可能引起一些不兼容的问题，命令如下：

#virsh net-destroy default

#virsh net-autostart --disable default

②删除bridge模块，因为我们使用了openvswitch的，所有用不到bridge，而且这个模块的存在会引起一些错误。命令：

#apt-purge ebtables

③启用brcompat模块

打开/etc/default/openvswitch-switch文件，把#BRCOMPAT=no改为BRCOMPAT=yes，保存退出

④编译openvswitch-datapath模块

#module-assistant auto-install openvswitch-datapath

这一步并非必须，如果在安装openvswitch前就把virbr0删除，可能就不需要这一步了，如果启动openvswitch-switch服务时出现错误，就需要运行此命令。

⑤添加网桥

使用openvswitch建立网桥，kvm使用，命令如下：

建立网桥br

#ovs-vsctl add-br br0

把eth0(物理机上网的网卡)添加到br0

#ovs-vsctl add-port br0 eth0

如果不出意外的话现在机器就不能上网了，可以按照以下方法解决

删除eth0的配置

#ifconfig eth0 0

为br0分配ip

#dhclient br0

因为我使用的是dhcp获取ip的，所以执行了此命令，如果你的ip是自己手动配置的，请把eth0的配置写到br0上。

⑥需要注意的一些问题

启动openvswitch-switch服务的时候看一下有没有出现bridge module is loaded not load brcompat，这一行提示，可以运行modprobe -r bridge命令，然后运行#apt-purge ebtables，之后再次启动该服务即可

启动openvswitch-switch服务前可以使用lsmod | grep brcompat命令看一下brcompat模块有没有加载，如果没有加载，请确认一下前四步是否都正确的执行了。

 

三、安装虚拟机

打开virt-manager，新建虚拟机，因为是图形界面操作，过程比较简单，不做过多的介绍，按照提示信息一步一步进行即可

①填写虚拟机名称

②选择安装光盘的镜像、选择操作系统类型

③填写cpu、内存信息

④创建新的磁盘

⑤配置网络

在Advanced options中默认的网络配置是NAT方式，点击下拉菜单，选择Specify shared deivce name将网络改为桥接方式，在下边的bridge 那么中填写br0（刚才用openvswitch建立的网桥），点击finish开始装系统即可。

注意：如果在配置openvswitch的时候有些地方没有做好，这里可能会出现错误，说是找不到br0。错误信息为：Unable to complete install:'Cannot get interface MUT on 'br;':No such device'。出现这个错误提示有两种可能，一种是系统中确实没有br0，也就是说你没用使用openvswitch建立br0，可是用ifconfig br0，或者ovs-vsctl show命令看一下，如果确实没有br0，回到配置openvswitch中的第五步；另一种是系统加载了bridge模块，而不是brcompat模块，你用openvswitch建立的网桥bridge是找不到的，此时可使用lsmod | grep brcompat看看，如果没有加载brcompat模块，回到配置openvswitch中，重新配置。

 

四、总结

使用openvswitch + kvm可以很快的建立一个虚拟环境，而且该环境支持openflow，这也是我使用这个方法的原因，毕竟我是做openflow的，当然你也可以使用mininet以更快的方式建立一个openflow环境，但是mininet还是太单薄了，只能用来测试网络的通与不同，其它许多东西都没法做。

使用openvswitch + kvm的时候主要问题在与openvswitch的配置，因为linux系统中已经有了一个bridge模块，该模块引起openvswitch出现一些问题，本文的主要内容也是来解决这些问题的。希望能够帮助有需要的人。
</pre>
