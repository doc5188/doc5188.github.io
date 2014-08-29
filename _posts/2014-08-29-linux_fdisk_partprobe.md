---
layout: post
title: "使用fdisk结合partprobe命令不重启系统添加 一块新的磁盘分区"
categories: linux
tags: [linux, fdisk, partprobe]
date: 2014-08-29 09:37:21
---

<p>主机自带硬盘超过300GB，目前只划分使用了3个主分区，不到70GB，如 下：<br>
[root@db2 ~]# df -h <br>
Filesystem Size Used Avail Use% Mounted on <br>
/dev/sda1 29G 3.7G&nbsp; 24G 14% / <br>
/dev/sda2 29G&nbsp; 22G 5.2G 81% /oracle <br>
tmpfs&nbsp;&nbsp;&nbsp; 2.0G&nbsp;&nbsp;&nbsp; 0 2.0G&nbsp; 0% /dev/shm <br>
<br>
[root@db2 ~]# cat /proc/partitions<br>
major minor&nbsp; #blocks&nbsp; name<br>
<br>
&nbsp;&nbsp; 8&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 311427072 sda<br>
&nbsp;&nbsp;&nbsp; sda1<br>
&nbsp;&nbsp; 8&nbsp;&nbsp;&nbsp;&nbsp; 2&nbsp;&nbsp; 30716280 sda2<br>
&nbsp;&nbsp; 8&nbsp;&nbsp;&nbsp;&nbsp; 3&nbsp;&nbsp;&nbsp; 8193150 sda3<br>
&nbsp;&nbsp; 8&nbsp;&nbsp;&nbsp; 16&nbsp;&nbsp;&nbsp;&nbsp; 976896 sdb<br>
&nbsp;&nbsp; 8&nbsp;&nbsp;&nbsp; 32&nbsp;&nbsp;&nbsp;&nbsp; 976896 sdc<br>
<br>
现在需要给系统添加1个100GB的空间存放数据文件，而又不影响现有系统上业务的运行，<br>
使用fdisk结合partprobe命令不重启系统添加 一块新的磁盘分区。操作步骤如下：</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p><strong><br>
</strong>
</p>
<p><strong>第1步，添加新的磁盘分区</strong>
<br>
[root@db2 ~]# fdisk /dev/sda<br>
The number of cylinders for this disk is set to 38770.<br>
There is nothing wrong with that, but this is larger than 1024,<br>
and could in certain setups cause problems with:<br>
1) software that runs at boot time (e.g., old versions of LILO)<br>
2) booting and partitioning software from other OSs<br>
&nbsp;&nbsp; (e.g., DOS FDISK, OS/2 FDISK)<br>
<br>
Command (m for help): p<br>
<br>
Disk /dev/sda: 318.9 GB, 318901321728 bytes<br>
255 heads, 63 sectors/track, 38770 cylinders<br>
Units = cylinders of 16065 * 512 = 8225280 bytes<br>
<br>
&nbsp;&nbsp; Device Boot&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Start&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; End&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Blocks&nbsp;&nbsp; Id&nbsp; System<br>
/dev/sda1&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3824&nbsp;&nbsp;&nbsp; 30716248+&nbsp; 83&nbsp; Linux<br>
/dev/sda2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3825&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7648&nbsp;&nbsp;&nbsp; 30716280&nbsp;&nbsp; 83&nbsp; Linux<br>
/dev/sda3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7649&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 8668&nbsp;&nbsp;&nbsp;&nbsp; 8193150&nbsp;&nbsp; 82&nbsp; Linux swap / Solaris<br>
<br>
Command (m for help): n<br>
Command action<br>
&nbsp;&nbsp; e&nbsp;&nbsp; extended<br>
&nbsp;&nbsp; p&nbsp;&nbsp; primary partition (1-4)<br>
p<br>
Selected partition 4<br>
First cylinder (8669-38770, default 8669):<br>
Using default value 8669<br>
Last cylinder or +size or +sizeM or +sizeK (8669-38770, default 38770): +100G&nbsp;&nbsp; <br>
Command (m for help): w<br>
The partition table has been altered!<br>
<br>
Calling ioctl() to re-read partition table.<br>
<br>
WARNING: Re-reading the partition table failed with error 16: <br>
<br>
<br>
Device or resource busy.<br>
The kernel still uses the old table.<br>
The new table will be used at the next reboot.<br>
Syncing disks.<br>
[root@db2 ~]#<br>
<br>
<br>
<strong>第2步，使用工具partprobe让kernel读取分区信息</strong>
<br>
[root@db2 ~]# partprobe<br>
使用fdisk工具只是将分区信息写到磁盘，如果需要mkfs磁盘分区则需要重启系统，<br>
而使用partprobe则可以使kernel重新读取分区 信息，从而避免重启系统。<br>
<br>
<br>
<br>
<strong>第3步，格式化文件系统</strong>
<br>
[root@db2 ~]# mkfs.ext3 /dev/sda4<br>
mke2fs 1.39 (29-May-2006)<br>
Filesystem label=<br>
OS type: Linux<br>
Block size=4096 (log=2)<br>
Fragment size=4096 (log=2)<br>
12222464 inodes, 24416791 blocks<br>
1220839 blocks (5.00%) reserved for the super user<br>
First data block=0<br>
Maximum filesystem blocks=4294967296<br>
746 block groups<br>
32768 blocks per group, 32768 fragments per group<br>
16384 inodes per group<br>
Superblock backups stored on blocks:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, <br>
&#12288;&#12288;&#12288;&#12288;2654208, 4096000, 7962624, 11239424, 20480000, 23887872<br>
<br>
Writing inode tables: done<br>
Creating journal (32768 blocks): done<br>
Writing superblocks and filesystem accounting information:<br>
<br>
done<br>
<br>
This filesystem will be automatically checked every 26 mounts or<br>
180 days, whichever comes first.&nbsp; Use tune2fs -c or -i to override.<br>
[root@db2 ~]#<br>
<br>
<br>
<br>
<strong>第4步，mount新的分区/dev/sda4</strong>
<br>
[root@db2 ~]# e2label&nbsp; /dev/sda4 /data<br>
[root@db2 ~]# mkdir /data<br>
[root@db2 ~]# mount /dev/sda4 /data<br>
[root@db2 ~]# df<br>
Filesystem&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1K-blocks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Used Available Use% Mounted on<br>
/dev/sda1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 29753556&nbsp;&nbsp; 3810844&nbsp; 24406900&nbsp; 14% /<br>
/dev/sda2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 29753588&nbsp; 11304616&nbsp; 16913160&nbsp; 41% /oracle<br>
tmpfs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2023936&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp; 2023936&nbsp;&nbsp; 0% /dev/shm<br>
/dev/sda4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 96132968&nbsp;&nbsp;&nbsp; 192312&nbsp; 91057300&nbsp;&nbsp; 1% /data<br>
[root@db2 ~]#<br>
<br>
<strong>总结：使用partprobe可以不用重启系统即可配合fdisk工具创建新的分区。</strong>
</p>
