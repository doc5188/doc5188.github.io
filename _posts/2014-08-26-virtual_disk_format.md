---
layout: post
title: "qcow2/raw/vmdk等镜像格式的比较和基本转换"
date: 2014-08-26 17:43:02
categories: 虚拟化
tags: [linux, 虚拟化]
---


注：本文转自http://www.cnblogs.com/feisky/archive/2012/07/03/2575167.html


云计算用一个朋友的话来说:”做云计算最苦逼的就是得时时刻刻为一些可能一辈子都碰不到的事做

好准备。更苦逼的就是刚以为一个问题不会遇到，立刻就发生了。。。“。这个还真的没有办法，

谁让哥我是搞云计算的呢，简单一个虚拟化就搞的你蛋疼，你还能想其它的吗？一直纠结在做虚

拟化使用什么镜像格式，刚刚开始用了raw的file，后来发现LVM的很多特性对于虚拟化还是有比较

理想的能力，而且性能也很不错就用了LVM。后来被VMware骗了跑去搞Esxi接触了VMDK，最近

研究openstack发现了qcow2格式，貌似现在很流行呀。也说不上分析这些镜像格式的能力，就简单

说说自己的一些使用心得。


目前主要有那些格式来作为虚拟机的镜像：

raw


(default) the raw format is a plain binary image of the disc image, and is very portable. On filesystems that suppor

t sparse files, images in this format only use the space actually used by the data recorded in them.

老牌的格式了，用一个字来说就是裸，也就是赤裸裸，你随便dd一个file就模拟了一个raw格式的镜

像。由于裸的彻底，性能上来说的话还是不错的。目前来看，KVM和XEN默认的格式好像还是这

个格式。因为其原始，有很多原生的特性，例如直接挂载也是一件简单的事情。


裸的好处还有就是简单，支持转换成其它格式的虚拟机镜像对裸露的它来说还是很简单的（如果

其它格式需要转换，有时候还是需要它做为中间格式），空间使用来看，这个很像磁盘，使用多

少就是多少（du -h看到的大小就是使用大小），但如果你要把整块磁盘都拿走的话得全盘拿了

（copy镜像的时候），会比较消耗网络带宽和I/O。接下来还有个有趣的问题，如果那天你的硬盘

用着用着不够用了，你咋办，在买一块盘。但raw格式的就比较犀利了，可以在原来的盘上追加空间：
dd if=/dev/zero of=zeros.raw bs=1024k count=4096（先创建4G的空间）


cat foresight.img zeros.raw > new-foresight.img（追加到原有的镜像之后）


当然，好东西是吹出来的，谁用谁知道，还是有挺多问题的。由于原


生的裸格式，不支持snapshot也是很正常的。传说有朋友用版本管理软件对raw格式的文件做版本管


理从而达到snapshot的能力，估计可行，但没试过，这里也不妄加评论。但如果你使用LVM的裸设


备，那就另当别论。说到LVM还是十分的犀利的，当年用LVM做虚拟机的镜像，那性能杠杠的

。

而且现在好多兄弟用虚拟化都采用LVM来做的。在LVM上做了很多的优化，国外听说也有朋友在


LVM增量备份方面做了很多的工作。目前来LVM的snapshot、性能、可扩展性方面都还是有相当的

效果的。目前来看的话，备份的话也问题不大。就是在虚拟机迁移方面还是有很大的限制。但目


前虚拟化的现状来看，真正需要热迁移的情况目前需求还不是是否的强烈。虽然使用LVM做虚拟

机镜像的相关公开资料比较少，但目前来看牺牲一点灵活性，换取性能和便于管理还是不错的选择。

对于LVM相关的特性及使用可以参考如下链接：

http://www.ibm.com/developerworks/linux/library/l-lvm2/index.html

cow
copy-on-write format, supported for historical reasons only and not available to QEMU on Windows


曾经qemu的写时拷贝的镜像格式，目前由于历史遗留原因不支持窗口模式。从某种意义上来说是


个弃婴，还没得它成熟就死在腹中，后来被qcow格式所取代。

qcow
the old QEMU copy-on-write format, supported for historical reasons and superseded by qcow2


一代的qemu的cow格式，刚刚出现的时候有比较好的特性，但其性能和raw格式对比还是有很大的

差距，目前已经被新版本的qcow2取代。其性能可以查看如下链接：


http://www.linux-kvm.org/page/Qcow2

qcow2
QEMU copy-on-write format with a range of special features, including the ability to take multiple snapshots,

 smaller images on filesystems that don’t support sparse files, optional AES encryption, and optional zlib compression


现在比较主流的一种虚拟化镜像格式，经过一代的优化，目前qcow2的性能上接近raw裸格式的性

能，这个也算是redhat的官方渠道了，哈哈，希望有朋友能拍他们砖：


https://fedoraproject.org/wiki/Features/KVM_qcow2_Performance


对于qcow2的格式，几点还是比较突出的，qcow2的snapshot，可以在镜像上做N多个快照：

    更小的存储空间，即使是不支持holes的文件系统也可以（这下du -h和ls -lh看到的就一样了）
    Copy-on-write support, where the image only represents changes made to an underlying disk

     image（这个特性SUN ZFS表现的淋漓尽致）

    支持多个snapshot，对历史snapshot进行管理
    支持zlib的磁盘压缩

    支持AES的加密

vmdk 
VMware 3 & 4, or 6 image format, for exchanging images with that product
VMware的格式，这个格式说的蛋疼一点就有点牛X，原本VMware就是做虚拟化起家，自己做了一

个集群的VMDK的pool，做了自己的虚拟机镜像格式。又拉着一些公司搞了一个OVF的统一封包

。从性能和功能上来说，vmdk应该算最出色的，由于vmdk结合了VMware的很多能力，目前来看，

KVM和XEN使用这种格式的情况不是太多。但就VMware的Esxi来看，它的稳定性和各方面的能力

还是可圈可点。


vdi
VirtualBox 1.1 compatible image format, for exchanging images with VirtualBox.


SUN收购了VirtualBox，Oracle又收购了SUN，这么说呢，vdi也算虚拟化这方面的一朵奇葩，可惜的

是入主的两家公司。SUN太专注于技术（可以说是IT技术最前端也不为过），Oracle又是开源杀手

（mysql的没落）。单纯从能力上来说vdi在VirtualBox上的表现还是不错的。也是不错的workstation

级别的产品。

说了这么多虚拟机镜像格式，这么多虚拟化，做云计算的伤不起呀，得为长期发展考虑，也有朋

友对镜像的转换做了很多事情，简单看看几种镜像的转化：

raw->qcow2

此步骤使用qemu-img工具实现，如果机器上没有，可以通过rpm或yum进行安装，包名为qemu-img。

qemu-img是专门虚拟磁盘映像文件的qemu命令行工具。

具体命令如下：

{% highlight bash%}
     # qemu-img convert -f raw centos.img -O qcow2 centos.qcow2
{% endhighlight %}

<pre>
     参数说明：convert   将磁盘文件转换为指定格式的文件

                     -f   指定需要转换文件的文件格式

                    -O  指定要转换的目标格式

     转换完成后，将新生产一个目标映像文件，原文件仍保存。
</pre>

VMDK–>qcow2:


{% highlight bash%}
kevin@kevin:~# qemu-img convert -f vmdk -O qcow2 SLES11SP1-single.vmdk SLES11SP1-single.img
{% endhighlight %}

http://www.ibm.com/developerworks/cn/linux/l-cn-mgrtvm3/index.html


qcow2–>raw:
{% highlight bash%}
kevin@kevin:~$ qemu-img convert -O qcow2 image-raw.raw image-raw-converted.qcow
{% endhighlight %}

本文转自：http://blog.prajnagarden.com/?p=248
