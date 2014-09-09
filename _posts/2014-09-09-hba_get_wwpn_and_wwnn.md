---
layout: post
title: "WWNN和WWPN的相关概念以及AIX、HPUX上的查询(原创)"
categories: 存储
tags: [HBA, 存储, linux]
date: 2014-09-09 15:41:21
---


<div class="blog_content" id="blog_content">
    <p>WWN是HBA卡用的编号，每一个光纤通道设备都有一个唯一的标识，称为WWN（world wide name），由IEEE负责分配。在有多台主机使用磁盘阵列时，通过WWN号来确定哪台主机正在使用指定的LUN（或者说是逻辑驱动器），被使用的LUN其他主机将无法使用。<br>
WWN概念包含WWPN、WWNN。<br>
一个不可拆分的独立的设备有WWNN，一个端口有WWPN。<br>
比如一台SAN交换机，不可拆分，有一个WWNN，它有一堆端口，每个端口有一个WWPN。一块多口光纤HBA，卡本身有一个WWNN，每个端口有一个WWPN，单口的HBA也是，不过只有一个WWNN和一个WWPN。但主机就没有WWNN，因为卡和主机是可以分离的，单纯一个主机本身并不一定是SAN环境中的设备。<br>
有WWNN的好处是：即使不去看连线，也可以清楚地知道，哪些端口是在一个物理设备上<br>
wwn：有两种表示方法：&nbsp; wwpn&nbsp; wwnn<br>
对于主机来说：<br>
单个hba卡（单口）的情况下： wwnn只有一个&nbsp;&nbsp;&nbsp;&nbsp; wwpn和wwnn一样<br>
单个hba卡（双口）的情况下： wwnn只有一个&nbsp;&nbsp;&nbsp;&nbsp; wwpn有两个<br>
两个hba卡（单口）的情况下： wwnn有两个&nbsp;&nbsp;&nbsp; &nbsp; &nbsp; wwpn有两个<br>
两个hba卡（双口）的情况下： wwnn有两个&nbsp;&nbsp; &nbsp;&nbsp; &nbsp; wwpn有四个</p>
<p>AIX上WWPN的查询</p>
<p>查看HBA卡具体在哪个插槽上<span style="color: #008000;"><br>
#lsslot -c pci|grep fc<br>
U787B.001.DNW7603-P1-C4 PCI-X capable, 64 bit, 133MHz slot fcs0<br>
U787B.001.DNW7603-P1-C5 PCI-X capable, 64 bit, 133MHz slot fcs1 </span>
</p>
<p>HBA卡的物理位置 U787B.001.DNW7603-P1-C4 可以看机器盖板上的图,也可以去查阅 IBM 系统硬件信息中心.</p>
<p>通过lsdev获取系统中识别有几块HBA卡；<span style="color: #008000;"><br>
# lsdev -C | grep fcs<br>
fcs0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Available 00-08&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; FC Adapter<br>
fcs1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Available 05-08&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; FC Adapter</span>
<br>
即有两块HBA卡，对应的AIX系统中为fcs0，fcs1；<br>
再使用lscfg命令获取各个HBA卡属性；<br><span style="color: #008000;"># lscfg -vl fcs0<br>
&nbsp; fcs0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; U787B.001.DNWGXVH-P1-C3-T1&nbsp; FC Adapter<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Part Number.................46K6838<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Serial Number...............1B83504003<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Manufacturer................001B<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; EC Level....................A<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Customer Card ID Number.....280D<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; FRU Number.................. 46K6838<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(ZM)........3<br><span style="color: #0000ff;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Network Address.............10000000C97E5FFA&nbsp; WWPN</span>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ROS Level and ID............02C82774<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z0)........1036406D<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z1)........00000000<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z2)........00000000<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z3)........03000909<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z4)........FFC01231<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z5)........02C82774<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z6)........06C32715<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z7)........07C32774<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z8)........20000000C97E5FFA<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(Z9)........BS2.71X4<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(ZA)........B1D2.70A5<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(ZB)........B2D2.71X4<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device Specific.(ZC)........00000000<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Hardware Location Code......U787B.001.DNWGXVH-P1-C3-T1</span>
</p>
<p>HPUX上的WWNN和WWPN查询</p>
<p><span style="color: #008000;">#ioscan -fnC fc<br>
Class&nbsp;&nbsp;&nbsp;&nbsp; I&nbsp; H/W Path&nbsp;&nbsp;&nbsp; Driver S/W State&nbsp;&nbsp; H/W Type&nbsp;&nbsp;&nbsp;&nbsp; Description<br>
===================================================================<br>
fc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2&nbsp; 0/0/2/1/0&nbsp;&nbsp; fcd&nbsp; CLAIMED&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;&nbsp; HP AB378-60101 4Gb Single Port PCI/PCI-X Fibre Channel Adapter (FC Port 1)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; /dev/fcd2<br>
fc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3&nbsp; 0/0/4/1/0&nbsp;&nbsp; fcd&nbsp; CLAIMED&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;&nbsp; HP AB378-60101 4Gb Single Port PCI/PCI-X Fibre Channel Adapter (FC Port 1)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; /dev/fcd3<br>
fc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0/0/12/1/0&nbsp; td&nbsp;&nbsp; CLAIMED&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;&nbsp; HP Tachyon XL2 Fibre Channel Mass Storage Adapter<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; /dev/td0</span>
<br>
用fcmsutil显示WWN号码<br><span style="color: #008000;">#fcmsutil /dev/fcd2<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Vendor ID is = 0x001077<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Device ID is = 0x002422<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PCI Sub-system Vendor ID is = 0x00103c<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PCI Sub-system ID is = 0x0012d6<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PCI Mode = PCI-X 133 MHz<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ISP Code version = 4.0.22<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ISP Chip version = 3<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Topology = PTTOPT_FABRIC<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Link Speed = 2Gb<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Local N_Port_id is = 0x621213<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Previous N_Port_id is = None</span>
<span style="color: #008000;"><span style="color: #0000ff;"><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; N_Port Node World Wide Name = 0x500143800131155b&nbsp; #本机HAB卡的WWNN<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; N_Port Port World Wide Name = 0x500143800131155a&nbsp;&nbsp;&nbsp; #本机HBA卡的WWPN<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Switch Port World Wide Name = 0x2012080088a0ae1a&nbsp;&nbsp; #HBA卡连接光纤交换机的WWPN<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Switch Node World Wide Name = 0x1000080088a0ae1a #HBA卡连接光纤交换机的WWNN</span>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Driver state = ONLINE<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Hardware Path is = 0/0/2/1/0<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Maximum Frame. Size = 2048<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Driver-Firmware Dump Available = NO<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Driver-Firmware Dump Timestamp = N/A<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Driver Version = @(#) libfcd.a HP Fibre Channel ISP 23xx &amp; 24xx Driver B.11.23.06 /ux/core/isu/FCD/kern/src/common/wsio/fcd_init.c:Jun 23 2006,14:05:23</span>
</p>
<p>&nbsp;</p>
<p>参考至:http://blog.itpub.net/post/3232/504272</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; http://space.itpub.net/14136300/viewspace-659626</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; http://blog.csdn.net/xiaolantian/article/details/4934906</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; http://publib.boulder.ibm.com/infocenter/svc/ic/index.jsp?topic=/com.ibm.storage.svc.console.doc/svc_aixlocwwpn_1dcvtx.html</p>
<p>本文原创，转载请注明出处、作者</p>
<p>如有错误，欢迎指正</p>
<p>邮箱:czmcj@163.com</p>
  </div>

<pre>
源：http://czmmiao.iteye.com/blog/1139393
</pre>
