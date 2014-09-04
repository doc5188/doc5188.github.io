---
layout: post
title: "比较SCSI、ISCSI、FC"
categories: 存储
tags: [scsi, iscsi, fc, 存储]
date: 2014-09-04 14:50:12
---
　　其历史顺序应该SCSI->FC(用于SCSI)->ISCSI;

　　最初是从SCSI开始的，它也是存储领域最为广泛的协议;SCSI的命令和数据，可以直接在SCSI接口中传输，也可以通过封装进行传输，比如用USB，1394，FC，以及iSCSI等方式。

　　由于在传统的SCSI接口中，其传输的距离有限;因此用FC来扩大传输距离就应运而生，从而封装SCSI的FC接口流行起来，物理上它只是加上的FC的电路，其核心的SCSI部分基本不做修改，因此软件上移植SCSI HBA到FC的HBA实现难度并不大。

　　同样，由于FC的成本和传输距离问题，iSCSI横空出世，它用TCP/IP协议来封装和传输，物理上加上TOE电路(或者用软件来实现这部分)，同样其核心仍然是SCSI的处理，方式和FC查不错。至于iSCSI的流行，这和软硬件厂商的推广(需要在存储的各个应用环境中都加入iSCSI的支持)，以及市场的接受程度相关。

　　从物理上来讲，对于FC和iSCSI需要特殊的IC来完成处理;而软件上，改变会比较小，在windows下面，PCI RAID卡、FC卡、iSCSI卡的驱动，都是采用Port/MiniPort驱动架构，其中Port driver(是硬件无关的)由微软提供(在2003以前叫SCSIPORT,现在叫StorPort，在windows的系统目录下可以看见这该驱动)，而Miniport包含了上面所说的三种卡，其架构都一样，只是要针对各种卡做对应的处理而已。对于其他的操作系统，这3种卡的软件处理方面也是类似的。因为最主要的差别都在物理传输上，所以基本在硬件上完成;而软件上，都是以处理SCSI命令和数据为核心，然后围绕传输接口做相关的处理。

　　存储介质厂商基本都没有加入iSCSI接口，而存储的其他部分host, network,以及阵列厂商都强烈支持

　　iSCSI。应该成本是个大问题，如果说硬盘要支持iSCSI接口，那么硬盘上应该加入个TOC的IC，同时要在硬盘的Firmware里面加入TCP/IP协议栈，在Firmware中实现这个，一是Firmware的大小限制(Firmware增加容量，成本增加还是比较高的)，还有就是硬盘的整体性能会因为处理TCP/IP协议而受到影响。

　　PATA/FATA/SCSI/FC/SAS这些是硬盘的连接技术。比如PC级硬盘连接常用PATA，但有被SATA取代的趋势;而阵列应该说，这些硬盘通信协议接口技术，主要是应用在后端设计中，通常低端的设备会用到PATA、FATA、或者SATA;但是通常中高端通常都是FC接口，至于SAS它只是SCSI的串行连接协议而已，相对于传统的并行SCSI接口实现高速传输，主要是物理层上和Media层的改变。而且存储介质的在性能上的提高，主要还是其机械性能，其他除了接口技术外，还有一些专用的加速IC chip，以及Firmware中的技术(比如采用Queue的硬盘就会好些，当然要全部实现queue，必须要Adapter配合才行)。

　　总的来说，应该是在SAN环境下，乱谈FC和 iSCSI;特别是Host, SAN network, 以及Array之间的连接技术。
