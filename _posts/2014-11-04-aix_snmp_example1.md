---
layout: post
title: "通过SNMP监控AIX系统的简单案例"
categories: 网络
tags: [netsnmp, aix snmp]
date: 2014-11-04 11:11:52
---

<p>
	SNMP即简单网络管理协议（Simple Network Management Protocol），通过该协议可以管理各种不同厂家的软硬件产品，常常用于对设备状态的监控，可以说是网管软件中最常用的服务之一。<br />
本文主要向大家简单介绍SNMP服务在AIX6.1中的配置，以及如何使用它为我们的日常监控服务。不会涉及太多关于SNMP协议的理论知识，一则我肯定不及Google和百度说得清楚明白，二则我个人也完全没兴趣研究太深入，因此我会用一些不太专业的词汇来达到描述清楚的目的，希望谅解。<br />
假设我们要监控的AIX系统其IP地址为192.0.246.23，而监控机使用Linux系统，其IP地址为192.0.243.113。<b><br />
一、</b><b style="text-indent:-25.5pt;line-height:1.5;">配置</b><b style="text-indent:-25.5pt;line-height:1.5;">AIX</b><b style="text-indent:-25.5pt;line-height:1.5;">下</b><b style="text-indent:-25.5pt;line-height:1.5;">SNMP</b><b style="text-indent:-25.5pt;line-height:1.5;">代理程序</b> 
</p>
<p style="margin-left:25.5pt;text-indent:-25.5pt;">
	<b></b> 
</p>
<p>
	1、查看当前运行的snmp版本<br />
<img src="/attachment/201304/24/316679_1366764334RRzS.png" width="556" height="77" alt="" /><br />
<span style="line-height:150%;">可以看到当前snmpd使用的是snmpdv3ne，表示支持的是SNMPv3非加密版本，ne=no encryption（非加密），只要对/etc/snmpdv3.conf进行相关配置，就能够以SNMPv1的方式使用，因此一般默认使用这个版本都能满足要求，如果有特殊需要也可用snmpv3_ssw命令来更改版本：</span> 
</p>
<p class="MsoNormal" style="line-height:150%;">
	
</p>
<p class="MsoNormal" style="line-height:150%;">
	snmpv3_ssw -1&nbsp; 切换至SNMPv1
</p>
<p class="MsoNormal" style="line-height:150%;">
	snmpv3_ssw -n&nbsp; 切换至SNMPv3非加密版本
</p>
<p class="MsoNormal" style="line-height:150%;">
	snmpv3_ssw -e&nbsp; 切换至SNMPv3的加密版本（该版本默认并未安装）
</p>
<p class="MsoNormal" style="line-height:150%;">
	2、创建一个叫hmsnmp的community
</p>
<p class="MsoNormal" style="line-height:150%;">
	修改/etc/snmpdv3.conf文件如下所示，请特别注意用红线标注部分的内容。
</p>
<p class="MsoNormal" style="line-height:150%;">
	其中192.0.243.113是监控机的地址，就是安装监控软件的那台设备地址，根据需要进行修改，表示只对该IP开放本机的snmp服务，这是出于安全性的考虑。<br />
<img src="/attachment/201304/24/316679_1366765535rJ1f.png" width="558" height="482" alt="" /> 
</p>
<p>
	3、停止并启动相关服务，使得对/etc/snmpdv3.conf的修改生效
</p>
<p>
	stopsrc -s aixmibd
</p>
<p>
	stopsrc -s snmpmibd
</p>
<p>
	stopsrc -s hostmibd
</p>
<p>
	stopsrc -s snmpd
</p>
<p>
	startsrc -s snmpd
</p>
<p>
	startsrc -s hostmibd -a "-c hmsnmp"
</p>
<p>
	startsrc -s snmpmibd -a "-c hmsnmp"
</p>
<p>
	startsrc -s aixmibd -a "-c hmsnmp"
</p>
<p>
	这里需要注意的是，当操作系统重启后，由于默认情况下是按照public的community去启动的，因此为了使得重启后hmsnmp的community能正常工作，建议修改/etc/rc.tcpip文件，修改默认的启动参数，如下所示：
</p>
<p>
	# Start up the hostmibd daemon
</p>
<p>
	start /usr/sbin/hostmibd "$src_running"
"-c hmsnmp "
</p>
<p>
	# Start up the snmpmibd daemon
</p>
<p>
	start /usr/sbin/snmpmibd "$src_running"
"-c hmsnmp "
</p>
<p>
	# Start up the aixmibd daemon
</p>
<p>
	start /usr/sbin/aixmibd "$src_running"
"-c hmsnmp "
</p>
<p>
	4、测试snmp服务是否正常
</p>
<p>
	在本机可执行命令如下：
</p>
<p>
	# snmpinfo -md -c hmsnmp sysDescr
</p>
<p>
	1.3.6.1.2.1.1.1.0 = "IBM PowerPC CHRP Computer
</p>
<p>
	Machine Type: 0x0800004c Processor id: 00F7TEST4C00
</p>
<p>
	Base Operating System Runtime AIX version:
06.01.0007.0015
</p>
<p>
	TCP/IP Client Support version: 06.01.0007.0016"
</p>
<p>
	在监控机可执行命令如下：
</p>
<p>
	# snmpwalk -v 1 -c hmsnmp &nbsp;192.0.246.23 &nbsp;1.3.6.1.2.1.1.1.0
</p>
<p>
	SNMPv2-MIB::sysDescr.0 = STRING: IBM PowerPC CHRP
Computer
</p>
<p>
	Machine Type: 0x0800004c Processor id: 00F7TEST4C00
</p>
<p>
	Base Operating System Runtime AIX version:
06.01.0007.0015
</p>
<p>
	TCP/IP Client Support version: 06.01.0007.0016
</p>
<p>
	<b>二、</b><b>AIX</b><b>常用的</b><b>MIB OID<br />
</b><span style="text-indent:21pt;line-height:1.5;">上面我们主要完成的工作是配置了一个community叫hmsnmp，可用于监控机调用snmp相关服务，接下去给大家一些常用的MIB库信息，特别是OID，供参考。<br />
</span><span style="text-indent:21pt;line-height:1.5;">AIX系统的常见基本信息的MIB为“AIX”打头，如果需要查找对于对象的OID，可以先到/etc/mib.defs中找到相应的对象，然后通过snmpinfo -md ObjectName，获取对应的OID，用于远程调用。</span> 
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	1、显示CPU使用率
</p>
<p>
	# snmpinfo -md -v -c hmsnmp aixSeCPUUtilization
</p>
<p>
	aixSeCPUUtilization.0 = 5
</p>
<p>
	去掉-v参数看到的就是OID值
</p>
<p>
	# snmpinfo -md -c hmsnmp aixSeCPUUtilization&nbsp;
</p>
<p>
	1.3.6.1.4.1.2.6.191.1.2.1.0 = 5
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	2、显示Paging Space
</p>
<p>
	# snmpinfo -md -v -c hmsnmp aixPagingSpace
</p>
<p>
	aixPageThreshold.0 = 95
</p>
<p>
	aixPageName.1 = "hd6"
</p>
<p>
	aixPageNameVG.1 = "rootvg"
</p>
<p>
	aixPageNamePV.1 = "hdisk0"
</p>
<p>
	aixPageSize.1 = 14336
</p>
<p>
	aixPagePercentUsed.1 = 1
</p>
<p>
	aixPageStatus.1 = 1
</p>
<p>
	aixPageType.1 = 1
</p>
<p>
	aixPageIndex.1 = 1
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	3、查看机器的序列号
</p>
<p>
	# snmpinfo -md -v -c hmsnmp aixSeMachineType
</p>
<p>
	aixSeMachineType.0 = "IBM,8205-E6C"
</p>
<p>
	# snmpinfo -md -v -c hmsnmp aixSeSerialNumber
</p>
<p>
	aixSeSerialNumber.0 = "IBM,0210TESTR"
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	4、查看CPU数量
</p>
<p>
	# snmpinfo -md -v -c hmsnmp aixSeNumCPUs
</p>
<p>
	aixSeNumCPUs.0 = 4
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	5、查看VG相关信息aixVolumeGroup
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	6、查看LV相关信息aixLogicalVolume
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	7、查看PV相关信息aixPhysicalVolume
</p>
<p style="margin-left:18.0pt;text-indent:-18.0pt;">
	8、查看FS相关信息aixFileSystem
</p>
<p style="margin-left:25.5pt;text-indent:-25.5pt;">
	<b>三、</b><b>通过</b><b>SNMP</b><b>进行系统监控的简单案例</b><b></b> 
</p>
<p>
	配置好需要使用的snmp agent的community名称，了解清楚需要监控对象的OID值，接下去就只要在监控机上部署对应的监控软件来调用snmp就可以了，常用的开源监控软件如cacti，nagios，zabbix都支持snmp。如果只是做一个简单监控，那自己写shell脚本也不失为一种方法。
</p>
<p>
	下面我们就以监控文件系统的使用率为例，来自己编写一个shell脚本AIX_FS_CHECK.sh，该脚本部署到监控机上。<br />
<img src="/attachment/201304/24/316679_13667656074E5z.png" width="558" height="532" alt="" /> 
</p>
<p>
	为了观察实际输出效果，在脚本中我们将阀值设置的比较低，如果你有兴趣也可以把阀值作为一个参数带入到脚本中，我们来执行以下脚本看看效果：
</p>
<p>
	# ./AIX_FS_CHECK.sh -h 192.0.246.23 -c hmsnmp
</p>
<p>
	WARNING!!/usr used 74%
</p>
<p>
	WARNING!!/usr Inodes used 18%
</p>
<p>
	WARNING!!/patch used 97%
</p>
<p>
	监控机通过snmp顺利的获取到了被监控设备的信息，并根据我们的要求发出相关报警信息。
</p>
<p style="margin-left:25.5pt;text-indent:-25.5pt;">
	<b>四、</b><b>小结</b><b></b> 
</p>
<p>
	本文展示了使用SNMP对AIX系统进行监控的简单案例，虽然距离实现多种指标监控仍有着较大的距离，灵活性和易用性也有待提高，但为实现操作系统无代理方式的监控提供了一种思路，希望能给有需要的朋友带来一些帮助。
</p>
<p>
	<br />
</p>

<p>
	<br />
</p>
<p>
	<br />
</p>
<p>
	<b></b> 
</p>


<pre>
referer: http://blog.chinaunix.net/uid-316679-id-3615725.html
</pre>
           
