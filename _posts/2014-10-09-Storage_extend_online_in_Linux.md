---
layout: post
title: "Storage extend online in Linux"
categories: 存储
tags: [存储]
date: 2014-10-09 16:25:16
---

* 环境 : CentOS 5.x X64 Linux系统.


* HBA : 
<pre>
15:00.0 Fibre Channel: QLogic Corp. ISP2432-based 4Gb Fibre Channel to PCI Express HBA (rev 03)
15:00.1 Fibre Channel: QLogic Corp. ISP2432-based 4Gb Fibre Channel to PCI Express HBA (rev 03)
</pre>

* 存储 : HP MSA2312FC

* 需求 : 存储扩容后分配给CentOS 5.x X64 Linux系统.

* 操作 : 

1. HP MSA2312FC操作

创建新卷 : 
<pre>
create volume vdisk vd01 size 758G vd01vol5
create volume vdisk vd02 size 918G vd02vol1
create volume vdisk vd02 size 580G vd02vol2
</pre>

创建卷和主机的映射关系

<pre>
map volume access rw lun 5 host 192168001009_0 vd01vol5
map volume access rw lun 6 host 192168001009_0 vd02vol1
map volume access rw lun 7 host 192168001009_0 vd02vol2
map volume access rw lun 5 host 192168001009_1 vd01vol5
map volume access rw lun 6 host 192168001009_1 vd02vol1
map volume access rw lun 7 host 192168001009_1 vd02vol2
</pre>

查看映射关系
<pre>
# show host-maps 

Host View [ID (2101001B32BC4C82) Name (192168001009_1) Profile (Standard) ] Mapping:
   Name      Serial Number                    LUN   Access       Ports       
   --------------------------------------------------------------------------
   vd01vol01 00c0ff105ac50000024f7d5001000000 1     read-write   A1,A2,B1,B2 
   vd02vol1  00c0ff105a6a0000b280f35001000000 6     read-write   A1,A2,B1,B2 
   vd01vol02 00c0ff105ac500000a4f7d5001000000 2     read-write   A1,A2,B1,B2 
   vd02vol2  00c0ff105a6a00004481f35001000000 7     read-write   A1,A2,B1,B2 
   vd01vol03 00c0ff105ac50000264f7d5001000000 3     read-write   A1,A2,B1,B2 
   vd01vol04 00c0ff105ac500002f4f7d5001000000 4     read-write   A1,A2,B1,B2 
   vd01vol5  00c0ff105ac50000a380f35001000000 5     read-write   A1,A2,B1,B2 

Host View [ID (2100001B329C4C82) Name (192168001009_0) Profile (Standard) ] Mapping:
   Name      Serial Number                    LUN   Access       Ports       
   --------------------------------------------------------------------------
   vd01vol01 00c0ff105ac50000024f7d5001000000 1     read-write   A1,A2,B1,B2 
   vd02vol1  00c0ff105a6a0000b280f35001000000 6     read-write   A1,A2,B1,B2 
   vd01vol02 00c0ff105ac500000a4f7d5001000000 2     read-write   A1,A2,B1,B2 
   vd02vol2  00c0ff105a6a00004481f35001000000 7     read-write   A1,A2,B1,B2 
   vd01vol03 00c0ff105ac50000264f7d5001000000 3     read-write   A1,A2,B1,B2 
   vd01vol04 00c0ff105ac500002f4f7d5001000000 4     read-write   A1,A2,B1,B2 
   vd01vol5  00c0ff105ac50000a380f35001000000 5     read-write   A1,A2,B1,B2 
</pre>


2. 系统层面

配置完存储后, 通过 fdisk -l 看不到新加的存储.

通过dmesg信息可以看出, Linux SCSI 层不能自动remap LUN的关系. 具体信息如下 : 
<pre>
sd 6:0:1:1: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:1: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:4: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:3: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:2: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:2: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:3: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:4: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:3: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:1: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:4: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:1: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:2: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:2: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:3: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:4: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:3: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:1: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:1: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:4: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:0:2: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:2: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:3: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
sd 6:0:1:4: Warning! Received an indication that the LUN assignments on this target have changed. The Linux SCSI layer does not automatically remap LUN assignments.
</pre>

解决办法 : 
重新扫描设备, 执行以下命令, 执行完后设备就找到了.

{% highlight bash %}
# find /sys/class/scsi_host/host*/scan | while read line; do echo '- - -' > $line; done
{% endhighlight %}

dmesg输出 : 
<pre>
  Vendor: IBM-ESXS  Model: CBRCA146C3ETS0 N  Rev: C370
  Type:   Direct-Access                      ANSI SCSI revision: 06
  Vendor: IBM-ESXS  Model: CBRCA146C3ETS0 N  Rev: C370
  Type:   Direct-Access                      ANSI SCSI revision: 06
ata1: hard resetting link
ata1: SATA link down (SStatus 0 SControl 300)
ata1: EH complete
ata2: hard resetting link
ata2: SATA link down (SStatus 0 SControl 300)
ata2: EH complete
ata3: hard resetting link
ata3: SATA link down (SStatus 0 SControl 300)
ata3: EH complete
ata4: hard resetting link
ata4: SATA link down (SStatus 0 SControl 300)
ata4: EH complete
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdj: 195312480 512-byte hdwr sectors (100000 MB)
sdj: Write Protect is off
sdj: Mode Sense: 93 00 00 08
SCSI device sdj: drive cache: write back
SCSI device sdj: 195312480 512-byte hdwr sectors (100000 MB)
sdj: Write Protect is off
sdj: Mode Sense: 93 00 00 08
SCSI device sdj: drive cache: write back
 sdj: unknown partition table
sd 5:0:0:1: Attached scsi disk sdj
sd 5:0:0:1: Attached scsi generic sg13 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdk: 351562496 512-byte hdwr sectors (180000 MB)
sdk: Write Protect is off
sdk: Mode Sense: 93 00 00 08
SCSI device sdk: drive cache: write back
SCSI device sdk: 351562496 512-byte hdwr sectors (180000 MB)
sdk: Write Protect is off
sdk: Mode Sense: 93 00 00 08
SCSI device sdk: drive cache: write back
 sdk: unknown partition table
sd 5:0:0:2: Attached scsi disk sdk
sd 5:0:0:2: Attached scsi generic sg14 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdl: 312500000 512-byte hdwr sectors (160000 MB)
sdl: Write Protect is off
sdl: Mode Sense: 93 00 00 08
SCSI device sdl: drive cache: write back
SCSI device sdl: 312500000 512-byte hdwr sectors (160000 MB)
sdl: Write Protect is off
sdl: Mode Sense: 93 00 00 08
SCSI device sdl: drive cache: write back
 sdl: unknown partition table
sd 5:0:0:3: Attached scsi disk sdl
sd 5:0:0:3: Attached scsi generic sg15 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdm: 546874976 512-byte hdwr sectors (280000 MB)
sdm: Write Protect is off
sdm: Mode Sense: 93 00 00 08
SCSI device sdm: drive cache: write back
SCSI device sdm: 546874976 512-byte hdwr sectors (280000 MB)
sdm: Write Protect is off
sdm: Mode Sense: 93 00 00 08
SCSI device sdm: drive cache: write back
 sdm: unknown partition table
sd 5:0:0:4: Attached scsi disk sdm
sd 5:0:0:4: Attached scsi generic sg16 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdn: 1480468736 512-byte hdwr sectors (758000 MB)
sdn: Write Protect is off
sdn: Mode Sense: 93 00 00 08
SCSI device sdn: drive cache: write back
SCSI device sdn: 1480468736 512-byte hdwr sectors (758000 MB)
sdn: Write Protect is off
sdn: Mode Sense: 93 00 00 08
SCSI device sdn: drive cache: write back
 sdn: unknown partition table
sd 5:0:0:5: Attached scsi disk sdn
sd 5:0:0:5: Attached scsi generic sg17 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdo: 1792968736 512-byte hdwr sectors (918000 MB)
sdo: Write Protect is off
sdo: Mode Sense: 93 00 00 08
SCSI device sdo: drive cache: write back
SCSI device sdo: 1792968736 512-byte hdwr sectors (918000 MB)
sdo: Write Protect is off
sdo: Mode Sense: 93 00 00 08
SCSI device sdo: drive cache: write back
 sdo: unknown partition table
sd 5:0:0:6: Attached scsi disk sdo
sd 5:0:0:6: Attached scsi generic sg18 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdp: 1132812480 512-byte hdwr sectors (580000 MB)
sdp: Write Protect is off
sdp: Mode Sense: 93 00 00 08
SCSI device sdp: drive cache: write back
SCSI device sdp: 1132812480 512-byte hdwr sectors (580000 MB)
sdp: Write Protect is off
sdp: Mode Sense: 93 00 00 08
SCSI device sdp: drive cache: write back
 sdp: unknown partition table
sd 5:0:0:7: Attached scsi disk sdp
sd 5:0:0:7: Attached scsi generic sg19 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdq: 195312480 512-byte hdwr sectors (100000 MB)
sdq: Write Protect is off
sdq: Mode Sense: 93 00 00 08
SCSI device sdq: drive cache: write back
SCSI device sdq: 195312480 512-byte hdwr sectors (100000 MB)
sdq: Write Protect is off
sdq: Mode Sense: 93 00 00 08
SCSI device sdq: drive cache: write back
 sdq: unknown partition table
sd 5:0:1:1: Attached scsi disk sdq
sd 5:0:1:1: Attached scsi generic sg20 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdr: 351562496 512-byte hdwr sectors (180000 MB)
sdr: Write Protect is off
sdr: Mode Sense: 93 00 00 08
SCSI device sdr: drive cache: write back
SCSI device sdr: 351562496 512-byte hdwr sectors (180000 MB)
sdr: Write Protect is off
sdr: Mode Sense: 93 00 00 08
SCSI device sdr: drive cache: write back
 sdr: unknown partition table
sd 5:0:1:2: Attached scsi disk sdr
sd 5:0:1:2: Attached scsi generic sg21 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sds: 312500000 512-byte hdwr sectors (160000 MB)
sds: Write Protect is off
sds: Mode Sense: 93 00 00 08
SCSI device sds: drive cache: write back
SCSI device sds: 312500000 512-byte hdwr sectors (160000 MB)
sds: Write Protect is off
sds: Mode Sense: 93 00 00 08
SCSI device sds: drive cache: write back
 sds: unknown partition table
sd 5:0:1:3: Attached scsi disk sds
sd 5:0:1:3: Attached scsi generic sg22 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdt: 546874976 512-byte hdwr sectors (280000 MB)
sdt: Write Protect is off
sdt: Mode Sense: 93 00 00 08
SCSI device sdt: drive cache: write back
SCSI device sdt: 546874976 512-byte hdwr sectors (280000 MB)
sdt: Write Protect is off
sdt: Mode Sense: 93 00 00 08
SCSI device sdt: drive cache: write back
 sdt: unknown partition table
sd 5:0:1:4: Attached scsi disk sdt
sd 5:0:1:4: Attached scsi generic sg23 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdu: 1480468736 512-byte hdwr sectors (758000 MB)
sdu: Write Protect is off
sdu: Mode Sense: 93 00 00 08
SCSI device sdu: drive cache: write back
SCSI device sdu: 1480468736 512-byte hdwr sectors (758000 MB)
sdu: Write Protect is off
sdu: Mode Sense: 93 00 00 08
SCSI device sdu: drive cache: write back
 sdu: unknown partition table
sd 5:0:1:5: Attached scsi disk sdu
sd 5:0:1:5: Attached scsi generic sg24 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdv: 1792968736 512-byte hdwr sectors (918000 MB)
sdv: Write Protect is off
sdv: Mode Sense: 93 00 00 08
SCSI device sdv: drive cache: write back
SCSI device sdv: 1792968736 512-byte hdwr sectors (918000 MB)
sdv: Write Protect is off
sdv: Mode Sense: 93 00 00 08
SCSI device sdv: drive cache: write back
 sdv: unknown partition table
sd 5:0:1:6: Attached scsi disk sdv
sd 5:0:1:6: Attached scsi generic sg25 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdw: 1132812480 512-byte hdwr sectors (580000 MB)
sdw: Write Protect is off
sdw: Mode Sense: 93 00 00 08
SCSI device sdw: drive cache: write back
SCSI device sdw: 1132812480 512-byte hdwr sectors (580000 MB)
sdw: Write Protect is off
sdw: Mode Sense: 93 00 00 08
SCSI device sdw: drive cache: write back
 sdw: unknown partition table
sd 5:0:1:7: Attached scsi disk sdw
sd 5:0:1:7: Attached scsi generic sg26 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdx: 1480468736 512-byte hdwr sectors (758000 MB)
sdx: Write Protect is off
sdx: Mode Sense: 93 00 00 08
SCSI device sdx: drive cache: write back
SCSI device sdx: 1480468736 512-byte hdwr sectors (758000 MB)
sdx: Write Protect is off
sdx: Mode Sense: 93 00 00 08
SCSI device sdx: drive cache: write back
 sdx: unknown partition table
sd 6:0:0:5: Attached scsi disk sdx
sd 6:0:0:5: Attached scsi generic sg27 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdy: 1792968736 512-byte hdwr sectors (918000 MB)
sdy: Write Protect is off
sdy: Mode Sense: 93 00 00 08
SCSI device sdy: drive cache: write back
SCSI device sdy: 1792968736 512-byte hdwr sectors (918000 MB)
sdy: Write Protect is off
sdy: Mode Sense: 93 00 00 08
SCSI device sdy: drive cache: write back
 sdy: unknown partition table
sd 6:0:0:6: Attached scsi disk sdy
sd 6:0:0:6: Attached scsi generic sg28 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdz: 1132812480 512-byte hdwr sectors (580000 MB)
sdz: Write Protect is off
sdz: Mode Sense: 93 00 00 08
SCSI device sdz: drive cache: write back
SCSI device sdz: 1132812480 512-byte hdwr sectors (580000 MB)
sdz: Write Protect is off
sdz: Mode Sense: 93 00 00 08
SCSI device sdz: drive cache: write back
 sdz: unknown partition table
sd 6:0:0:7: Attached scsi disk sdz
sd 6:0:0:7: Attached scsi generic sg29 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdaa: 1480468736 512-byte hdwr sectors (758000 MB)
sdaa: Write Protect is off
sdaa: Mode Sense: 93 00 00 08
SCSI device sdaa: drive cache: write back
SCSI device sdaa: 1480468736 512-byte hdwr sectors (758000 MB)
sdaa: Write Protect is off
sdaa: Mode Sense: 93 00 00 08
SCSI device sdaa: drive cache: write back
 sdaa: unknown partition table
sd 6:0:1:5: Attached scsi disk sdaa
sd 6:0:1:5: Attached scsi generic sg30 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdab: 1792968736 512-byte hdwr sectors (918000 MB)
sdab: Write Protect is off
sdab: Mode Sense: 93 00 00 08
SCSI device sdab: drive cache: write back
SCSI device sdab: 1792968736 512-byte hdwr sectors (918000 MB)
sdab: Write Protect is off
sdab: Mode Sense: 93 00 00 08
SCSI device sdab: drive cache: write back
 sdab: unknown partition table
sd 6:0:1:6: Attached scsi disk sdab
sd 6:0:1:6: Attached scsi generic sg31 type 0
  Vendor: HP        Model: MSA2312fc         Rev: M110
  Type:   Direct-Access                      ANSI SCSI revision: 05
SCSI device sdac: 1132812480 512-byte hdwr sectors (580000 MB)
sdac: Write Protect is off
sdac: Mode Sense: 93 00 00 08
SCSI device sdac: drive cache: write back
SCSI device sdac: 1132812480 512-byte hdwr sectors (580000 MB)
sdac: Write Protect is off
sdac: Mode Sense: 93 00 00 08
SCSI device sdac: drive cache: write back
 sdac: unknown partition table
sd 6:0:1:7: Attached scsi disk sdac
sd 6:0:1:7: Attached scsi generic sg32 type 0
</pre>

获取设备UUID : 

{% highlight bash %}
# for i in `cat /proc/partitions | awk '{print $4}' |grep sd`; do echo "### $i: `scsi_id -g -u -s /block/$i`"; done
{% endhighlight %}

配置/etc/multipath.conf, ( 可选 )
<pre>
vi /etc/multipath.conf

blacklist {
         devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
         devnode "^hd[a-z]"
         # IBM or DELL local disk filter, this example, only on disk local. is sda.
         devnode "^sda$"
         # HP local disk filter
         #devnode "^cciss!c[0-9]d[0-9]*"
}
defaults {
         udev_dir                 /dev
         polling_interval         10
         selector                 "round-robin 0"
         path_grouping_policy     failover
         getuid_callout           "/sbin/scsi_id -g -u -s /block/%n"
         prio_callout             /bin/true
         path_checker             readsector0
         rr_min_io                100
         rr_weight                priorities
         failback                 immediate
         no_path_retry            fail
         user_friendly_names      yes
         flush_on_last_del        yes
}
multipaths {
         multipath {
                 wwid     3600c0ff000105ac5024f7d5001000000
                 alias    d11_msa1_vd01vol01
        }
         multipath {
                 wwid     3600c0ff000105ac50a4f7d5001000000
                 alias    d11_msa1_vd01vol02
        }
         multipath {
                 wwid     3600c0ff000105ac5264f7d5001000000
                 alias    d11_msa1_vd01vol03
        }
         multipath {
                 wwid     3600c0ff000105ac52f4f7d5001000000
                 alias    d11_msa1_vd01vol04
        }
         multipath {
                 wwid     3600c0ff000105ac5a380f35001000000
                 alias    d11_msa1_vd01vol05
        }
         multipath {
                 wwid     3600c0ff000105a6ab280f35001000000
                 alias    d11_msa1_vd01vol06
        }
         multipath {
                 wwid     3600c0ff000105a6a4481f35001000000
                 alias    d11_msa1_vd01vol07
        }
}
</pre>


重载multipath配置

{% highlight bash %}
# service multipathd reload
{% endhighlight %}


检查多路径是否正常 : 

{% highlight bash %}
[root@db-192-168-001-009 ~]# multipath -ll
d11_msa1_vd01vol07 (3600c0ff000105a6a4481f35001000000) dm-10 HP,MSA2312fc
[size=540G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 5:0:1:7 sdw  65:96  [active][ready]
 \_ 6:0:1:7 sdac 65:192 [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 5:0:0:7 sdp  8:240  [active][ready]
 \_ 6:0:0:7 sdz  65:144 [active][ready]
d11_msa1_vd01vol06 (3600c0ff000105a6ab280f35001000000) dm-9 HP,MSA2312fc
[size=855G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 5:0:1:6 sdv  65:80  [active][ready]
 \_ 6:0:1:6 sdab 65:176 [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 5:0:0:6 sdo  8:224  [active][ready]
 \_ 6:0:0:6 sdy  65:128 [active][ready]
d11_msa1_vd01vol05 (3600c0ff000105ac5a380f35001000000) dm-8 HP,MSA2312fc
[size=706G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 5:0:0:5 sdn  8:208  [active][ready]
 \_ 6:0:0:5 sdx  65:112 [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 5:0:1:5 sdu  65:64  [active][ready]
 \_ 6:0:1:5 sdaa 65:160 [active][ready]
d11_msa1_vd01vol04 (3600c0ff000105ac52f4f7d5001000000) dm-3 HP,MSA2312fc
[size=261G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 6:0:0:4 sde  8:64   [active][ready]
 \_ 5:0:0:4 sdm  8:192  [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 6:0:1:4 sdi  8:128  [active][ready]
 \_ 5:0:1:4 sdt  65:48  [active][ready]
d11_msa1_vd01vol03 (3600c0ff000105ac5264f7d5001000000) dm-2 HP,MSA2312fc
[size=149G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 6:0:0:3 sdd  8:48   [active][ready]
 \_ 5:0:0:3 sdl  8:176  [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 6:0:1:3 sdh  8:112  [active][ready]
 \_ 5:0:1:3 sds  65:32  [active][ready]
d11_msa1_vd01vol02 (3600c0ff000105ac50a4f7d5001000000) dm-1 HP,MSA2312fc
[size=168G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 6:0:0:2 sdc  8:32   [active][ready]
 \_ 5:0:0:2 sdk  8:160  [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 6:0:1:2 sdg  8:96   [active][ready]
 \_ 5:0:1:2 sdr  65:16  [active][ready]
d11_msa1_vd01vol01 (3600c0ff000105ac5024f7d5001000000) dm-0 HP,MSA2312fc
[size=93G][features=1 queue_if_no_path][hwhandler=0][rw]
\_ round-robin 0 [prio=100][active]
 \_ 6:0:0:1 sdb  8:16   [active][ready]
 \_ 5:0:0:1 sdj  8:144  [active][ready]
\_ round-robin 0 [prio=20][enabled]
 \_ 6:0:1:1 sdf  8:80   [active][ready]
 \_ 5:0:1:1 sdq  65:0   [active][ready]
{% endhighlight %}

到这里存储设备添加就算完成了.

* 【其他】

1. 如果存储块设备是通过iscsi连接的, 可以使用iscsiadm.

* 【参考】
<pre>
1. man iscsiadm
2. find /sys/class/scsi_host/host*/scan | while read line; do echo - - - > $line; done
3. http://serverfault.com/questions/262586/the-linux-scsi-layer-does-not-automatically-remap-lun-assignments
</pre>
