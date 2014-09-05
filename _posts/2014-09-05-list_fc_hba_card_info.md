---
layout: post
date: 2014-09-05 15:19:23
title: "FC HBA卡信息的方法  "
categories: 存储
tags: [fc, hba, fc-san,存储]
---

在讨论这个问题的时候，需要先说清楚一个问题：我们知道，在早期的SAN存储系统中，服务器与 交换机的数据传输是通过光纤进行的，因为服务器是把SCSI指令传输到存储设备上，不能走普通LAN网的IP协议，所以需要使用FC传输，因此这种SAN 就叫FC-SAN，而后期出现了用IP协议封装的SAN，可以完全走普通LAN网络，因此叫做IP-SAN，其中最典型的就是现在热门的ISCSI。 

这两种方式都需要对数据块进行繁重的读包解包操作，因此高性能的SAN系统是需要在服务器上安装一块专门负责解包工作以减轻处理器负担的网卡，这种网卡 大家就叫它HBA卡，它除了执行解包工作外当然还可以提供一个光纤接口（如果是iSCSI HBA卡就是提供普通的RJ45接口）以用于跟对应的交换机连接；另外，HBA物理上你可以把它当作网卡一样插在PCI或者PCI-E槽位里，因此这种设 备的用法非常相一张网卡，很多人也就把它跟普通网卡或普通的光纤网卡混淆了。当然，有的iSCSI HBA卡就可以当作普通网卡来用，不过从价格上考虑这是非常奢侈的。 

HBA的常规定义：就是连接主机I/O总线和计算机内存系统的 I/O适配器。按照这个定义，像显卡就是连接视频总线和内存，网卡就是连接网络总线和内存，SCSI-FC卡就是连接SCSI或者FC总线和内存的，它们 都应该算是HBA。HBA卡有FC-HBA和iSCSI HBA将来还有其他HBA卡，但是，HBA通常用在SCSI。Adapter(适配器)和NIC用于FC；而NIC也会用于以太网和令牌环网。 

其实，网卡是大家常提到的一个类型设备的总称，是指安装在主机里，通过网络连接线（双绞线、光纤线缆、同轴电缆等）与网络交换机（以太网交换机、FC交换机、ISCSI交换机等）、或与其它网络设备（存储设备、服务器、工作站等）连接，从而形成一个网络的硬件设备。 

那么，光纤网卡这个称呼到底是不是指光纤口HBA卡呢？ 

实际上大家常说的光纤网卡指的就是光纤通道网络里的HBA卡。 

因传输协议的不同的，网卡可分为三种，一是以太网卡，二是FC网卡，三是iSCSI网卡。 

? 以太网卡：学名Ethernet Adapter,传输协议为IP协议,一般通过光纤线缆或双绞线与以太网交换机连接。接口类型分为光口和电口。光口一般都是通过光纤线缆来进行数据传输， 接口模块一般为SFP（传输率2Gb/s）和GBIC（1Gb/s）,对应的接口为SC、ST和LC。电口目前常用接口类型为RJ45,用来与双绞线连 接，也有与同轴电缆连接的接口，不过现在已经用的比较少了。 

?FC网卡：一般也叫光纤网卡，学名Fibre Channel HBA。传输协议为光纤通道协议，一般通过光纤线缆与光纤通道交换机连接。接口类型分为光口和电口。光口一般都是通过光纤线缆来进行数据传输，接口模块一 般为SFP（传输率2Gb/s）和GBIC（1Gb/s）,对应的接口为SC和LC。电口的接口类型一般为DB9针或HSSDC。 

?ISCSI网卡：学名ISCSI HBA，传输ISCSI协议，接口类型与以太网卡相同。 

大家说的“光纤网卡”一般是指FC HBA卡，插在服务器上，外接存储用的光纤交换机；而光口的以太网卡一般都叫做“光纤以太网卡”，也是插在服务器上，不过它外接的是带光口的以太网交换机。 

总结： 

其实这些网卡还是很好区分的，看下表就清楚了： 

?HBA卡：FC-HBA卡（俗称：光纤网卡）、iSCSI-HBA卡（RJ45接口） 
?以太网卡：光纤接口的以太网卡（俗称：光纤以太网卡） 

不过这些都是大家的俗语或常用语，有一定的使用环境。我们建议大家不要使用光纤网卡这个称呼，而是直接说成FC-HBA卡，这样就绝对不会造成误解了。

现介绍如何查看FC HBA卡信息，在Windows、Linux、IBM AIX、SUN Solaris、HP-UX系统下如何查看FC HBA卡的信息作了介绍，供实施相关项目时参考。

        在配置磁盘阵列、虚拟带库以及其他带FC HBA卡的设备时，经常需要查看FC HBA卡的WWPN信息以便进行端口添加、ZONE划分等操作，正确查看FC HBA卡的信息是保证顺利施工的前提。

本文主要通过以下3个章节分别讲述在同种系统下查看FC HBA卡信息的方法作一介绍：
<pre>
1     FC HBA卡概述
2    Windows系统下查看FC HBA卡的信息
3    Linux系统下查看FC HBA卡的信息
4    UNIX系统下查看FC HBA卡的信息
</pre>
 
一.FC HBA卡概述
 
 
     FC HBA，也即Fibre Channel Host Bus Adapter，光纤通道主机适配器，简称光纤适配器。

在FC网络环境中，主机需要和FC网络、FC存储设备（SAN磁盘阵列）连接时需要使用一种接口卡，就如同连接以太网需要以太网卡一样，这种接口卡就叫做FC HBA，简称FC HBA卡。

和以太网卡的MAC地址一样，HBA上也有独一无二的标识，：WWN（World Wide Name），FC HBA上的WWN有两种：

① Node WWN（WWNN）：每块HBA有其独有的Node WWN；

② Port WWN（WWPN）：每块HBA卡上每个port有其独一无二的Port WWN。

由于通信是通过port进行的，因此多数情况下需要使用WWPN而不是WWNN。 WWN的长度为8bytes，用16进制表示并用冒号分隔，例如：50:06:04:81:D6:F3:45:42

二Windows系统下查看FC HBA卡的信息

QLOGIC和EMULEX是全球存储厂商产品配套使常见的FC HBA卡的制造厂商，下面就这两种类型的FC HBA卡在Windows系统下如何查看的方法作以介绍。

在Windows系统中，可以使用厂家提供GUI界面管理工具来查看和配置FC HBA卡，针对QLOGIC和EMULEX的FC HBA卡可以分别通过SANSurfer 和 HBAnywhere来查看和配置相关的FC HBA卡。

1、   QLOGIC SANSurfer

SANSurfer一款用于管理FC HBA卡的GUI软件，通过该软件可以修改FC HBA卡速率等其他参数，并可以看到关于FC HBA卡的详细信息。官方网站提供的下载链接为：

    http://driverdownloads.qlogic.com/QLogicDriverDownloads_UI/Product_detail.aspx?oemid=264
    获取到SANSurfer安装包后，内部的文件如图1所示，双击start_here.htm即可进行安装向导安装相应的驱动和图形化管理软件：
 


图1. SANSurfer安装包文件
SANSurfer的安装向导：
 


图2. SANSurfer安装向导
按照向导的提示完成安装后即可使用SANSurfer管理软件查看与配置FC HBA卡了。
另外，在Windows系统的开机自检过程中可以按照系统的提示按“Ctrl+Q”进行Qlogic FC HBA卡的字符模式的配置界面。
2、   EMULEX HBAnywhere
     HBAnywhere是EMULEX提供的一款用于管理EMULEX FC HBA卡的GUI软件，
    HBAnywhere的具体使用方法请参考使用手册，在此不作详细介绍。
三Linux系统下查看FC HBA卡的信息
             因为linux版本太多,我们就以主流的,为例,RedHat Linux AS4、RedHat Linux AS5、SuSe Linux 9和SuSe Linux 10为例介绍在Linux系统中如何查看FC HBA卡的信息。
在查看FC HBA卡前请确保FC HBA卡物理连接正常，指示灯正常。
1、RedHat Linux AS4 和 SuSE Linux 9
RedHat Linux AS4与SuSE Linux 9中查看FC HBA卡信息的方法基本一样，在此以RedHat AS4为例介绍如何查看FC HBA卡的信息。
在RedHat AS4或SuSE Linux 9系统的/proc/scsi/qla2xxx目录下一般存在两个文件：1、2或者3、4，这些文件包含FC HBA卡的配置信息。
[root@localhost qla2xxx]# pwd
/proc/scsi/qla2xxx
[root@localhost qla2xxx]# ls
3 4
[root@localhost qla2xxx]# cat 3
QLogic PCI to Fibre Channel Host Adapter for QLA2342:
        Firmware version 3.03.18 IPX, Driver version 8.01.02-d4
ISP: ISP2312, Serial# P21735
Request Queue = 0x11f580000, Response Queue = 0x11f4d0000
Request Queue count = 4096, Response Queue count = 512
Total number of active commands = 0
Total number of interrupts = 3354
    Device queue depth = 0x10
Number of free request entries = 4094
Number of mailbox timeouts = 0
Number of ISP aborts = 0
Number of loop resyncs = 0
Number of retries for empty slots = 0
Number of reqs in pending_q= 0, retry_q= 0, done_q= 0, scsi_retry_q= 0
Host adapter:loop state = <READY>, flags = 0x1a03
Dpc flags = 0x4000000
MBX flags = 0x0
Link down Timeout = 000
Port down retry = 035
Login retry count = 035
Commands retried with dropped frame(s) = 0
Product ID = 4953 5020 2020 0002
 
SCSI Device Information:
scsi-qla0-adapter-node=2000001882374738;
scsi-qla0-adapter-port=2100001882374738;
 
FC Port Information:
scsi-qla0-port-0=200000188237b206:210000188237b206:010a00:81;
 
SCSI LUN Information:
(Id:Lun) * - indicates lun is not registered with the OS.
其中，SCSI Device Information下面的scsi-qla0-adapter-port=2100001882374738便是主机光纤卡的WWN号。
2、RedHat Linux AS5和SuSE Linux 10
RedHat Linux AS5与SuSE Linux 10中查看FC HBA卡信息的方法基本一致，在此在RedHat Linux AS5为便介绍如何查看FC HBA卡信息。
RedHat AS5系统的 /sys/class/fc_host/host*/port_name 这个文件包含了所有已被系统发现的FC HBA卡的信息，使用查看命令查看该文件的内容即可看到FC HBA卡的信息。
查看WWPN：cat /sys/class/fc_host/host*/port_name
查看WWNN：cat /sys/class/fc_host/host*/node_name
四UNIX系统下查看FC HBA卡的信息
           最后就是Unix了,在此介绍实际应用较为广泛的UNIX系统中如何查看FC HBA卡信息，包括IBM AIX、SUN SOLARIS、HP-UNIX。
1、IBM AIX
    ① 查看AIX主机连接的光纤设备
       # lsdev -Cc adapter -S a | grep fcs
        fcs0      Available 09-08 FC Adapter
        fcs1      Available 09-09 FC Adapter
       上面的输出显示有2块光纤卡：fcs0和fcs1。
    ② 查看光纤卡fcs0的WWN号
       # lscfg -vpl fcs0
       fcs0             U787B.001.DNWG664-P1-C1-T1 FC Adapter
        Part Number.................10N8620
        Serial Number...............1B74404468
        Manufacturer................001B
        EC Level....................A
        Customer Card ID Number.....5759
        FRU Number.................. 10N8620
        Device Specific.(ZM)........3
        Network Address.............10000000C96E2898
        ROS Level and ID............02C82138
        Device Specific.(Z0)........1036406D
        Device Specific.(Z1)........00000000
        Device Specific.(Z2)........00000000
        Device Specific.(Z3)........03000909
        Device Specific.(Z4)........FFC01159
        Device Specific.(Z5)........02C82138
        Device Specific.(Z6)........06C12138
        Device Specific.(Z7)........07C12138
        Device Specific.(Z8)........20000000C96E2898
        Device Specific.(Z9)........BS2.10X8
        Device Specific.(ZA)........B1F2.10X8
        Device Specific.(ZB)........B2F2.10X8
        Device Specific.(ZC)........00000000
        Hardware Location Code......U787B.001.DNWG664-P1-C1-T1
上面命令的输出中，加粗红色的部分就是光纤卡的WWN号。
2、   SUN SOLARIS
    ① 查询现有存储设备和光纤设备，可以读到包括磁盘设备的WWN号
       # luxadm probe
    ② 查看HBA的prot，可以得到HBA卡的port值以及属性
      # luxadm -e port
      /devices/pci@0,0/pci1022,7450@2/pci1077,101@1/fp@0,0:devctl          NOT CONNECTED
      /devices/pci@0,0/pci1022,7450@2/pci1077,101@1,1/fp@0,0:devctl        CONNECTED
从中可以看到仅有一块光纤卡连接到存储设备。
③ 选择已经连接的HBA卡，查看其WWN号
       # luxadm -e dump_map /devices/pci@0,0/pci1022,7450@2/pci1077,101@1/fp@0,0:devctl
       Pos Port_ID Hard_Addr Port WWN         Node WWN         Type
       0    0       0        210000e08b19827a 200000e08b19827a 0x1f (Unknown Type,Host Bus Adapter)
3、HP-UNIX
    ① 列出HP机上连接的光纤卡设备
      # ioscan -fnC fc
Class  I H/W Path Driver S/W State   H/W Type   Description
=================================================================
fc 0 0/3/1/0  fcd CLAIMED   INTERFACE HP A6826-60001 2Gb Dual Port PCI/PCI-X Fibre Channel Adapter (FC Port 1)
                      /dev/fcd0
fc 1 0/3/1/1  fcd CLAIMED   INTERFACE HP A6826-60001 2Gb Dual Port PCI/PCI-X Fibre Channel Adapter (FC Port 2)
                      /dev/fcd1
    从上面命令的输出可以看 ,/dev/fcd0 和 /dev/fcd1两块光纤卡。
    ② 查看光纤卡的WWN号
      # fcmsutil /dev/fcd0
      Vendor ID is = 0x001077
      Device ID is = 0x002312
      PCI Sub-system Vendor ID is = 0x00103c
      PCI Sub-system ID is = 0x0012ba
      PCI Mode = PCI-X 133 MHz
      ISP Code version = 3.3.18
      ISP Chip version = 3
      Topology = PTTOPT_FABRIC
      Link Speed = 2Gb
      Local N_Port_id is = 0xa10500
      Previous N_Port_id is = None
      N_Port Node World Wide Name = 0x50060b00001db241 
      N_Port Port World Wide Name = 0x50060b00001db240 
      Switch Port World Wide Name = 0x205e000dec0e2e00 
      Switch Node World Wide Name = 0x2001000dec0e2e01
      Driver state = ONLINE
      Hardware Path is = 0/3/1/0
      Maximum Frame Size = 2048
      Driver-Firmware Dump Available = NO
      Driver-Firmware Dump Timestamp = N/A
      Driver Version = @(#) libfcd.a HP Fibre Channel ISP 23xx & 24xx Driver B.11.23.04 /ux/core/isu/FCD/kern/src/common/wsio/fcd_init.c:Oct 18 2005,08:21:11
其中红色加粗部分显示了HBA卡的WWNN和WWPN号，另外还能看到该HBA卡连接的光纤交换机端口的WWN号。

