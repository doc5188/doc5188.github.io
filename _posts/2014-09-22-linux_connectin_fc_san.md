---
layout: post
categories: linux
title: "Linux 连接 FC SAN"
tags: [linux, fc-scan]
date: 2014-09-22 17:52:21
---

今天在公司做了在linux平台下连接到emc cx500存储,具体步骤如下:

1.安装hba卡到linux主机上

2.连接光钎到emc cx500存储上

3.安装linux操作系统

4.登录IE浏览器,检查存储是否认到linux主机的hba卡

linux主机下查hba卡物理地址

cd /sys/class/host2/

cat port_name

5.存储上划分lun给linux主机用

6.在linux主机上扫描磁盘,以便认到从存储上新划分过来的硬盘

rmmod lpfc

fdisk -l

modprobe lpfc

fdisk -l
