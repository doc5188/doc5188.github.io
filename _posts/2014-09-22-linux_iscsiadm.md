---
layout: post
title "iscsiadm主要操作命令"
categories: linux
tags: [iscsiadm, linux, iscsi]
date: 2014-09-22 15:54:32
---


当前包含磁盘
{% highlight bash %}
[root@xifenfei ~]# fdisk -l
 
Disk /dev/sda: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1        2355    18916506   83  Linux
/dev/sda2            2356        2610     2048287+  82  Linux swap / Solaris
 
Disk /dev/sdb: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1               1        2610    20964793+  83  Linux
 
Disk /dev/sdc: 2147 MB, 2147483648 bytes
255 heads, 63 sectors/track, 261 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
Disk /dev/sdc doesn't contain a valid partition table
 
Disk /dev/sdd: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sdd1               1         100      803218+  83  Linux
/dev/sdd2             101        1000     7229250   83  Linux

查看iscsi运行情况
[root@xifenfei ~]# rpm -aq|grep iscsi
iscsi-initiator-utils-6.2.0.872-10.0.1.el5
[root@xifenfei ~]#  chkconfig --list |grep iscsi
iscsi           0:off   1:off   2:on    3:on    4:on    5:on    6:off
iscsid          0:off   1:off   2:off   3:on    4:on    5:on    6:off
[root@xifenfei ~]# ps -ef|grep iscs
root      2753     2  0 Jun21 ?        00:00:00 [iscsi_eh]
root     15793     1  0 09:08 ?        00:00:00 brcm_iscsiuio
root     15800     1  0 09:08 ?        00:00:00 iscsid
root     15802     1  0 09:08 ?        00:00:00 iscsid
root     19533 15269  0 10:11 pts/1    00:00:00 grep iscs

配置iscsi存储
[root@xifenfei ~]# iscsiadm -m discovery -t sendtargets -p 192.168.1.254:3260
192.168.1.254:3260,1 iqn.2006-01.com.openfiler:tsn.32b32087937b
[root@xifenfei ~]# iscsiadm -m node –T iqn.2006-01.com.openfiler:tsn.32b32087937b -p 192.168.1.254:3260 -l
Logging in to [iface: default, target: iqn.2006-01.com.openfiler:tsn.32b32087937b, portal: 192.168.1.254,3260]
Login to [iface: default, target: iqn.2006-01.com.openfiler:tsn.32b32087937b, portal: 192.168.1.254,3260] successful.
[root@xifenfei ~]# iscsiadm -m node –T iqn.2006-01.com.openfiler:tsn.32b32087937b -p 192.168.1.254:3260
>--op update -n node.startup -v automatic

当前包含磁盘
[root@xifenfei ~]# fdisk -l
 
Disk /dev/sda: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1        2355    18916506   83  Linux
/dev/sda2            2356        2610     2048287+  82  Linux swap / Solaris
 
Disk /dev/sdb: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1               1        2610    20964793+  83  Linux
 
Disk /dev/sdc: 2147 MB, 2147483648 bytes
255 heads, 63 sectors/track, 261 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
Disk /dev/sdc doesn't contain a valid partition table
 
Disk /dev/sdd: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sdd1               1         100      803218+  83  Linux
/dev/sdd2             101        1000     7229250   83  Linux
 
Disk /dev/sde: 1073 MB, 1073741824 bytes
34 heads, 61 sectors/track, 1011 cylinders
Units = cylinders of 2074 * 512 = 1061888 bytes
 
Disk /dev/sde doesn't contain a valid partition table
 
Disk /dev/sdf: 1073 MB, 1073741824 bytes
34 heads, 61 sectors/track, 1011 cylinders
Units = cylinders of 2074 * 512 = 1061888 bytes
 
Disk /dev/sdf doesn't contain a valid partition table
 
Disk /dev/sdg: 1073 MB, 1073741824 bytes
34 heads, 61 sectors/track, 1011 cylinders
Units = cylinders of 2074 * 512 = 1061888 bytes
 
Disk /dev/sdg doesn't contain a valid partition table

卸载iscsi存储
[root@xifenfei ~]# iscsiadm -m node --logoutall=all
Logging out of session [sid: 3, target: iqn.2006-01.com.openfiler:tsn.32b32087937b, portal: 192.168.1.254,3260]
Logout of [sid: 3, target: iqn.2006-01.com.openfiler:tsn.32b32087937b, portal: 192.168.1.254,3260] successful.
[root@xifenfei ~]# iscsiadm -m node --op delete --targetname iqn.2006-01.com.openfiler:tsn.32b32087937b

当前包含磁盘
[root@xifenfei ~]# fdisk -l
 
Disk /dev/sda: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1        2355    18916506   83  Linux
/dev/sda2            2356        2610     2048287+  82  Linux swap / Solaris
 
Disk /dev/sdb: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1               1        2610    20964793+  83  Linux
 
Disk /dev/sdc: 2147 MB, 2147483648 bytes
255 heads, 63 sectors/track, 261 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
Disk /dev/sdc doesn't contain a valid partition table
 
Disk /dev/sdd: 21.4 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
 
   Device Boot      Start         End      Blocks   Id  System
/dev/sdd1               1         100      803218+  83  Linux
/dev/sdd2             101        1000     7229250   83  Linux

iscsi操作总结
增加iscsi存储
(1)发现iscsi存储:iscsiadm -m discovery -t st -p ISCSI_IP
(2)查看iscsi发现记录:iscsiadm -m node
(3)登录iscsi存储:iscsiadm -m node -T LUN_NAME -p ISCSI_IP -l
(4)开机自动: iscsiadm -m node –T LUN_NAME -p ISCSI_IP --op update -n node.startup -v automatic
 
删除iscsi存储
(1)登出iscsi存储 iscsiadm -m node -T LUN_NAME -p ISCSI_IP -u
(2)对出iscsi所有登录 iscsiadm -m node --logoutall=all
(3)删除iscsi发现记录:iscsiadm -m node -o delete -T LUN_NAME -p ISCSI_IP
 
登入需验证码的节点
(1)开启认证
iscsiadm -m node -T LUN_NAME -o update --name node.session.auth.authmethod --value=CHAP
*.使用-o同--op
(2)添加用户
iscsiadm -m node -T LUN_NAME --op update --name node.session.auth.username --value=[用户名]
(3)添加密码
iscsiadm –m node –T LUN_NAME –op update –name node.session.auth.password –value=[密码]

<pre>
链接：http://www.xifenfei.com/3420.html
</pre>
