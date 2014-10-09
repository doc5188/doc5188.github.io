---
layout: post
title: "iSCSI 卡和iSCSI HBA卡有什么区别啊"
categories: 存储
tags: [iSCSI, iSCSI HBA]
date: 2014-10-09 15:34:58
---

iSCSI 卡和iSCSI HBA卡有什么区别啊



不知道你所说的iscsi卡是什么意思,是不是用来做iscsi的网卡.

区别在于:

1, iscsi hba卡, 卡的firmware带有iscsi 的initiator, 同时卡上有足够的CPU资源(有的是单独的处理器来负责, 而不是用网卡芯片来处理)来做TCP/IP以及ISCSI解包的工作, 而且在卡上有非常大的buffer来作为该卡的缓冲. 这个卡是可以物理上做到boot from iscsi的.(同样需要OS的support.

2, iscsi卡, 我姑且认为是用iscsi的网卡, 这种网卡的一个特点是a, 它是一个网卡, 使用网卡的芯片(intel, broadcom, maxwell), b, 卡上没有单独的buffer, 而是使用网卡芯片上少的可怜的cache, 一般32k-64k, 最多到128k,

这种网卡是用的是软件的iscsi initiator. 我所见到的有3种:

第一种, 网卡, 没有任何的TOE, 和TOE on iscsi. 这种网卡有的是主板集成, 有的是单独的. 属于最便宜的解决方案, 一般CPU的占用率在8-9%左右.

第二种, TOE的网卡. 支持TOE, 但不支持TOE on iscsi, 这种网卡不支持boot from iscsi.

第三种TOE on iscsi. 网卡firmware中带有iscsi initiator, 支持boot from iscsi. 
