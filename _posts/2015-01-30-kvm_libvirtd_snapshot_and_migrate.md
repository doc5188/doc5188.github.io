---
layout: post
title: "virsh离线迁移带快照的虚拟机实验"
categories: 云计算
tags: [libvirt, virsh, kvm, 虚拟化]
date: 2015-01-30 15:57:34
---

目地：

从结点A上将虚拟机Vm-01迁移至结点B点。虚拟机Vm-01存在外部快照(内部快照也类似)

1. 在结点A上关闭Vm-01.

2. 复杂快照文件，镜像文件,配置文件，及快照配置文件(/var/lib/libvirt/qemu/snapshot/Vm-01/)到结点B点。
  注意快照文件，镜像文件的路径需要与结点A上的路径一致。

3. 若Vm-01所使用的虚拟网卡信息被其它VM占用，需要修改虚拟网卡的名称。

4. 创建Vm-01虚拟机, virsh define ...

5. 创建Vm-01快照配置文件。 virsh snapshot-create Vm-Gavin --redefine 1422602325.xml 

6. 启动虚拟机。
