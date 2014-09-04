---
layout: post
title: "Linux下查看FC HBA信息"
categories: linux
tags: [linux, fc-san, hba]
date: 2014-09-04 14:31:23
---

一 如果没有加载正确的驱动，则有些信息，比如HBA的Link Speed可能无法获得，比如：

{% highlight bash %}
localhost:~ # lspci
00:00.0 Host bridge: Intel Corporation 5000X Chipset Memory Controller Hub (rev 12)
00:02.0 PCI bridge: Intel Corporation 5000 Series Chipset PCI Express x4 Port 2 (rev 12)
00:03.0 PCI bridge: Intel Corporation 5000 Series Chipset PCI Express x4 Port 3 (rev 12)
00:04.0 PCI bridge: Intel Corporation 5000 Series Chipset PCI Express x8 Port 4-5 (rev 12)
00:05.0 PCI bridge: Intel Corporation 5000 Series Chipset PCI Express x4 Port 5 (rev 12)
00:06.0 PCI bridge: Intel Corporation 5000 Series Chipset PCI Express x8 Port 6-7 (rev 12)
00:07.0 PCI bridge: Intel Corporation 5000 Series Chipset PCI Express x4 Port 7 (rev 12)
00:10.0 Host bridge: Intel Corporation 5000 Series Chipset FSB Registers (rev 12)
00:10.1 Host bridge: Intel Corporation 5000 Series Chipset FSB Registers (rev 12)
00:10.2 Host bridge: Intel Corporation 5000 Series Chipset FSB Registers (rev 12)
00:11.0 Host bridge: Intel Corporation 5000 Series Chipset Reserved Registers (rev 12)
00:13.0 Host bridge: Intel Corporation 5000 Series Chipset Reserved Registers (rev 12)
00:15.0 Host bridge: Intel Corporation 5000 Series Chipset FBD Registers (rev 12)
00:16.0 Host bridge: Intel Corporation 5000 Series Chipset FBD Registers (rev 12)
00:1c.0 PCI bridge: Intel Corporation 631xESB/632xESB/3100 Chipset PCI Express Root Port 1 (rev 09)
00:1d.0 USB Controller: Intel Corporation 631xESB/632xESB/3100 Chipset UHCI USB Controller #1 (rev 09)
00:1d.1 USB Controller: Intel Corporation 631xESB/632xESB/3100 Chipset UHCI USB Controller #2 (rev 09)
00:1d.2 USB Controller: Intel Corporation 631xESB/632xESB/3100 Chipset UHCI USB Controller #3 (rev 09)
00:1d.7 USB Controller: Intel Corporation 631xESB/632xESB/3100 Chipset EHCI USB2 Controller (rev 09)
00:1e.0 PCI bridge: Intel Corporation 82801 PCI Bridge (rev d9)
00:1f.0 ISA bridge: Intel Corporation 631xESB/632xESB/3100 Chipset LPC Interface Controller (rev 09)
00:1f.1 IDE interface: Intel Corporation 631xESB/632xESB IDE Controller (rev 09)
00:1f.2 IDE interface: Intel Corporation 631xESB/632xESB/3100 Chipset SATA IDE Controller (rev 09)
01:00.0 SCSI storage controller: LSI Logic / Symbios Logic SAS1068E PCI-Express Fusion-MPT SAS (rev 08)
02:00.0 PCI bridge: Broadcom EPB PCI-Express to PCI-X Bridge (rev c3)
03:00.0 Ethernet controller: Broadcom Corporation NetXtreme II BCM5708 Gigabit Ethernet (rev 12)
04:00.0 PCI bridge: Intel Corporation 6311ESB/6321ESB PCI Express Upstream Port (rev 01)
04:00.3 PCI bridge: Intel Corporation 6311ESB/6321ESB PCI Express to PCI-X Bridge (rev 01)
05:00.0 PCI bridge: Intel Corporation 6311ESB/6321ESB PCI Express Downstream Port E1 (rev 01)
05:01.0 PCI bridge: Intel Corporation 6311ESB/6321ESB PCI Express Downstream Port E2 (rev 01)
06:00.0 PCI bridge: Broadcom EPB PCI-Express to PCI-X Bridge (rev c3)
07:00.0 Ethernet controller: Broadcom Corporation NetXtreme II BCM5708 Gigabit Ethernet (rev 12)
08:00.0 Fibre Channel: Emulex Corporation Saturn-X: LightPulse Fibre Channel Host Adapter (rev 03)
08:00.1 Fibre Channel: Emulex Corporation Saturn-X: LightPulse Fibre Channel Host Adapter (rev 03)
0a:00.0 Ethernet controller: Broadcom Corporation NetXtreme II BCM57711 10Gigabit PCIe
0a:00.1 Ethernet controller: Broadcom Corporation NetXtreme II BCM57711 10Gigabit PCIe
0e:0d.0 VGA compatible controller: ATI Technologies Inc ES1000 (rev 02)
{% endhighlight %}
 
<pre>
08:00.0 Fibre Channel: Emulex Corporation Saturn-X: LightPulse Fibre Channel Host Adapter (rev 03)
08:00.1 Fibre Channel: Emulex Corporation Saturn-X: LightPulse Fibre Channel Host Adapter (rev 03)
</pre>
从蓝色字体只能知道该卡是emulex的FC HBA，但是不知道是什么型号的；进一步：

这个时候可以通过lspci命令直接查看芯片组信息，比如：

{% highlight bash %}
localhost:~ # lspci -n
00:00.0 0600: 8086:25c0 (rev 12)
00:02.0 0604: 8086:25e2 (rev 12)
00:03.0 0604: 8086:25e3 (rev 12)
00:04.0 0604: 8086:25f8 (rev 12)
00:05.0 0604: 8086:25e5 (rev 12)
00:06.0 0604: 8086:25f9 (rev 12)
00:07.0 0604: 8086:25e7 (rev 12)
00:10.0 0600: 8086:25f0 (rev 12)
00:10.1 0600: 8086:25f0 (rev 12)
00:10.2 0600: 8086:25f0 (rev 12)
00:11.0 0600: 8086:25f1 (rev 12)
00:13.0 0600: 8086:25f3 (rev 12)
00:15.0 0600: 8086:25f5 (rev 12)
00:16.0 0600: 8086:25f6 (rev 12)
00:1c.0 0604: 8086:2690 (rev 09)
00:1d.0 0c03: 8086:2688 (rev 09)
00:1d.1 0c03: 8086:2689 (rev 09)
00:1d.2 0c03: 8086:268a (rev 09)
00:1d.7 0c03: 8086:268c (rev 09)
00:1e.0 0604: 8086:244e (rev d9)
00:1f.0 0601: 8086:2670 (rev 09)
00:1f.1 0101: 8086:269e (rev 09)
00:1f.2 0101: 8086:2680 (rev 09)
01:00.0 0100: 1000:0058 (rev 08)
02:00.0 0604: 1166:0103 (rev c3)
03:00.0 0200: 14e4:164c (rev 12)
04:00.0 0604: 8086:3500 (rev 01)
04:00.3 0604: 8086:350c (rev 01)
05:00.0 0604: 8086:3510 (rev 01)
05:01.0 0604: 8086:3514 (rev 01)
06:00.0 0604: 1166:0103 (rev c3)
07:00.0 0200: 14e4:164c (rev 12)
08:00.0 0c04: 10df:f100 (rev 03)
08:00.1 0c04: 10df:f100 (rev 03)
0a:00.0 0200: 14e4:164f
0a:00.1 0200: 14e4:164f
0e:0d.0 0300: 1002:515e (rev 02)
{% endhighlight bash %}
通过查找10df：f100，可以知道该卡是emulex的8Gb FC HBA LPe12000:
http://www.vm-help.com/esx/esx3i/Hardware_support.php
 
 
另外，还可以通过-vvv参数获得更详细的信息：
 
<pre>
08:00.1 Fibre Channel: Emulex Corporation Saturn-X: LightPulse Fibre Channel Host Adapter (rev 03)
        Subsystem: Emulex Corporation Saturn-X: LightPulse Fibre Channel Host Adapter
        Control: I/O+ Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr+ Stepping- SERR+ FastB2B- DisINTx-
        Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
        Latency: 0, Cache Line Size: 64 bytes
        Interrupt: pin B routed to IRQ 18
        Region 0: Memory at d5efe000 (64-bit, non-prefetchable) [size=4K]
        Region 2: Memory at d5ef4000 (64-bit, non-prefetchable) [size=16K]
        Region 4: I/O ports at d800 [size=256]
        Capabilities: [58] Power Management version 3
                Flags: PMEClk- DSI- D1- D2- AuxCurrent=0mA PME(D0-,D1-,D2-,D3hot-,D3cold-)
                Status: D0 PME-Enable- DSel=0 DScale=0 PME-
        Capabilities: [60] Message Signalled Interrupts: Mask+ 64bit+ Count=1/16 Enable-
                Address: 0000000000000000  Data: 0000
                Masking: 00000000  Pending: 00000000
        Capabilities: [78] MSI-X: Enable- Mask- TabSize=32
                Vector table: BAR=2 offset=00002000
                PBA: BAR=2 offset=00003000
        Capabilities: [84] Vital Product Data <?>
        Capabilities: [94] Express (v2) Endpoint, MSI 00
                DevCap: MaxPayload 2048 bytes, PhantFunc 0, Latency L0s <1us, L1 unlimited
                        ExtTag+ AttnBtn- AttnInd- PwrInd- RBE+ FLReset-
                DevCtl: Report errors: Correctable- Non-Fatal- Fatal+ Unsupported-
                        RlxdOrd+ ExtTag- PhantFunc- AuxPwr- NoSnoop+
                        MaxPayload 128 bytes, MaxReadReq 512 bytes
                DevSta: CorrErr+ UncorrErr- FatalErr- UnsuppReq+ AuxPwr- TransPend-
                LnkCap: Port #0, Speed 5GT/s, Width x8, ASPM L0s, Latency L0 <1us, L1 <64us
                        ClockPM- Suprise- LLActRep- BwNot-
                LnkCtl: ASPM Disabled; RCB 64 bytes Disabled- Retrain- CommClk-
                        ExtSynch- ClockPM- AutWidDis- BWInt- AutBWInt-
                LnkSta: Speed 2.5GT/s, Width x4, TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
                DevCap2: Completion Timeout: Range ABCD, TimeoutDis+
                DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis-
                LnkCtl2: Target Link Speed: 2.5GT/s, EnterCompliance- SpeedDis-, Selectable De-emphasis: -6dB
                         Transmit Margin: Normal Operating Range, EnterModifiedCompliance- ComplianceSOS-
                         Compliance De-emphasis: -6dB
                LnkSta2: Current De-emphasis Level: -6dB
        Capabilities: [100] Advanced Error Reporting
                UESta:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq+ ACSVoil-
                UEMsk:  DLP- SDES- TLP- FCP- CmpltTO+ CmpltAbrt+ UnxCmplt+ RxOF- MalfTLP- ECRC- UnsupReq+ ACSVoil-
                UESvrt: DLP+ SDES- TLP+ FCP+ CmpltTO- CmpltAbrt- UnxCmplt- RxOF+ MalfTLP+ ECRC+ UnsupReq- ACSVoil-
                CESta:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- NonFatalErr+
                CESta:  RxErr+ BadTLP+ BadDLLP+ Rollover+ Timeout+ NonFatalErr-
                AERCap: First Error Pointer: 00, GenCap+ CGenEn- ChkCap+ ChkEn-
        Capabilities: [12c] Power Budgeting <?>
        Kernel driver in use: lpfc
        Kernel modules: lpfc
</pre>
 

 
二 如果FC HBA加载了正确的驱动，则在/sys/class/fc_host/hostx下有大量的HBA的信息，比如
wwpn等：
 
{% highlight bash %}
localhost:~ # cd /sys/class/fc_host/host1/
localhost:/sys/class/fc_host/host1 # ls
active_fc4s  fabric_name  maxframe_size  port_id    port_state  power  statistics  supported_classes  supported_speeds  tgtid_bind_type
device       issue_lip    node_name      port_name  port_type   speed  subsystem   supported_fc4s     symbolic_name     uevent
localhost:/sys/class/fc_host/host1 # cat node_name
0x20000000c988bece
localhost:/sys/class/fc_host/host1 # cat port_name
0x10000000c988bece
{% endhighlight %}

<pre>
原文: 
http://blog.chinaunix.net/uid-1829236-id-3179986.html
</pre>
