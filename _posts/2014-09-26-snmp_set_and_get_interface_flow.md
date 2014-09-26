---
layout: post
title: "SNMP配置和查看网卡流量"
date: 2014-09-26 14:39:21
categories: linux
tags: [linux, snmp]
---

<pre>
安装snmp
apt-get install snmp snmpd
编辑/etc/snmp/snmpd.conf配置文件，

1.将原有“agentAddress udp:127.0.0.1:161”改为：

agentAddress 192.168.1.9 /*192.168.1.9为本机IP，即监控服务器要监控的主机IP*/

2.加入一行如下：

access MyROSystem “” any noauth exact all none none

3.将原有“rocommunity public default -V systemonly” 的”-V systemonly” 参数去掉，变成：

rocommunity public default

4.将“#trap2sink localhost public”和“#informsink localhost public”前面的“#”去掉，改为：

trap2sink localhost public

informsink localhost public

5.重启SNMP服务：

/etc/init.d/snmpd restart

6.检验snmp获取数据：

snmpwalk -v 2c -c public 192.168.1.9

流量查询
snmpwalk -v 2c -c public 192.168.1.103 .1.3.6.1.2.1.2.2.1.16.2 send
snmpwalk -v 2c -c public 192.168.1.103 .1.3.6.1.2.1.2.2.1.10.2 receive

查到的结果是总流量，需要取差值计算。

发现一篇好文章，http://www.freeoa.net/osuport/netmanage/get-host-net-traffice-info-by-snmp_1979.html
取得所有网/端口的描述
snmpwalk -v 2c -c public ipaddr ifDescr

cisco交换机端口流量取值需要注意的问题：
If interfaces are in trunk mode, you won’t see them with that OID. CISCO-VLAN-MEMBERSHIP-MIB is only for non-trunking ports.

You can try vlanTrunkPortDynamicStatus from CISCO-VTP-MIB to check.

得到机器的网络接口：
snmpwalk -v 2c -c public 192.168.1.20 ifDescr
or
snmpwalk -v 2c -c public 192.168.1.20 .1.3.6.1.2.1.2.2.1.2

You should get a result like this:
IF-MIB::ifDescr.1 = STRING: lo
IF-MIB::ifDescr.2 = STRING: eth0
IF-MIB::ifDescr.3 = STRING: wifi0
IF-MIB::ifDescr.4 = STRING: ath0
IF-MIB::ifDescr.5 = STRING: br0

# snmpwalk -v1 -c public 192.168.1.20 ifDescr

取得网卡的进/出流量计数：
# snmpwalk -v1 -c public 192.168.1.20 ifinOctets
IF-MIB::ifInOctets.1 = Counter32: 0
IF-MIB::ifInOctets.2 = Counter32: 186740992
IF-MIB::ifInOctets.3 = Counter32: 4117381100
IF-MIB::ifInOctets.4 = Counter32: 3824919421
IF-MIB::ifInOctets.5 = Counter32: 569163

# snmpwalk -v1 -c public 192.168.1.20 ifoutOctets
IF-MIB::ifOutOctets.1 = Counter32: 0
IF-MIB::ifOutOctets.2 = Counter32: 3824764209
IF-MIB::ifOutOctets.3 = Counter32: 305295003
IF-MIB::ifOutOctets.4 = Counter32: 168468497
IF-MIB::ifOutOctets.5 = Counter32: 172865

它们分别代表的意义
ifHCOutOctets OID 1.3.6.1.2.1.31.1.1.1.10 – outgoing traffic (bytes)

ifHCInOctets OID 1.3.6.1.2.1.31.1.1.1.6 – incoming traffic (bytes)

取得交换机端口1的流量
statistic for port 1, then OID is: 1.3.6.1.2.1.31.1.1.1.10.1

使用SNMP RFC1213-mib定义进行流量分析

使用snmp管理网络设备，unix下常用net-snmp的snmpwalk，snmpget等，要得到网络的相关信息，可通过提取’RFC1213-mib’的定义值得到。例如：要取得远程主机的团体字为’public’，IP为’192.168.1.20′的网络端口流入(IN)的数据流量，可以使用如下命令：
snmpwalk -v 2c -c public 192.168.1.20 RFC1213-MIB::ifInOctets

返回各端口信息如下：
IF-MIB::ifInOctets.112 = counter32:165070862

IF-MIB::ifInOctets是 rfc1213的定义端口流入数据量
112是查询网络设备的1模块插槽12端口
counter32后的数值就是该端口的流量：165070862 bits，在终端下可以通过shell命令取得这两个值

# 首先取得 12 接口的 ifIndex
index=$(snmpwalk -v 2c -c public -IR 192.168.1.20 RFC1213-MIB::ifDescr |grep IF-MIB::ifInOctets.112 |cut -d ‘=’ -f 1|cut -d ‘.’ -f 2)

# 再通过 snmp 协议取得 ififInOctets 和 ifOutOctets 的值
# 也可在 /etc/snmp.conf 中配置好’defVersion’和’defCommunity’，这样 snmpget 命令不用指定这两个参数：
eth12_in=$(snmpget -v 2c -c public -IR -Os 192.168.1.20 ifInOctets.${index}|cut -d ‘:’ -f 2|tr -d ‘[:blank:]‘)

eth12_out=$(snmpget -v 2c -c public -IR -Os 192.168.1.20 ifOutOctets.${index}|cut -d ‘:’ -f 2 |tr -d ‘[:blank:]‘)

echo $eth12_in
echo $eth12_out

一般端口流量分析

针对普通网络设备的端口，MIB的相关定义是Interface组，主要管理如下信息：
ifIndex 端口索引号
ifDescr 端口描述
ifType 端口类型
ifMtu 最大传输包字节数
ifSpeed 端口速度
ifPhysAddress 物理地址
ifOperStatus 操作状态
ifLastChange 上次状态更新时间
*ifInOctets 输入字节数
*ifInUcastPkts 输入非广播包数
*ifInNUcastPkts 输入广播包数
*ifInDiscards 输入包丢弃数
*ifInErrors 输入包错误数
*ifInUnknownProtos 输入未知协议包数
*ifOutOctets 输出字节数
*ifOutUcastPkts 输出非广播包数
*ifOutNUcastPkts 输出广播包数
*ifOutDiscards 输出包丢弃数
*ifOutErrors 输出包错误数
ifOutQLen 输出队长
其中，*号标识的是与网络流量有关的信息。

例如看看网络接口：
#snmpwalk -v 1 222.90.47.169 -c public ifIndex
输出：
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifIndex.2 = INTEGER: 2
IF-MIB::ifIndex.3 = INTEGER: 3
表示有三个网络接口

网络接口明成：
[root@localhost snmp]# snmpwalk -v 1 222.90.47.169 -c public ifDescr
IF-MIB::ifDescr.1 = STRING: lo
IF-MIB::ifDescr.2 = STRING: eth0
IF-MIB::ifDescr.3 = STRING: ppp0

三个接口分别为
1 本地回路
2 以太网卡
3 ADSL连接

通过 snmp 协议取得 ififInOctets 和 ifOutOctets 的值
# snmpwalk -v1 -c public ipaddr ififInOctets/ifOutOctets

注意：端口的流量是一个累加值，即是从其加电工作开始到取数时，流经其的注意，因此这个数值是一直增加的。但受制于硬件的32位模式，处于32的系统下，这个值在超过4G后，会重新计数，64位系统没有这个限制。 
</pre>
