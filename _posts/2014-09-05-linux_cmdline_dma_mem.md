---
layout: post
date: 2014-09-05 17:44:38
categories: linux
tags: [linux]
title: "如何从linux内核--ubuntu系统cmdline上预留DDR物理内存DMA--mem=750M"
---

<div style="word-wrap: break-word;" class="Blog_wz1">
			
																<span style="font-weight: bold;">luther@gliethttp:~$</span> vim /proc/iomem<br>00100000-5bf0ffff : System RAM<br>00100000-00575553 : Kernel code<br>00575554-0078d307 : Kernel data<br>0081a000-008a809f : Kernel bss<br>可以看到kernel code和data,bss使用的ram就是我们的系统内存,<br><span style="font-weight: bold;">luther@gliethttp:~$</span> dmesg也可以看到物理内存的情况<br>BIOS-provided physical RAM map:<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 0000000000000000 - 000000000009dc00 (usable)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 000000000009dc00 - 00000000000a0000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 00000000000d2000 - 0000000000100000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: <span style="font-weight: bold;">0000000000100000 - 000000005bf10000 (usable)</span><br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 000000005bf10000 - 000000005bf19000 (ACPI data)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 000000005bf19000 - 000000005bf80000 (ACPI NVS)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 000000005bf80000 - 0000000060000000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 00000000e0000000 - 00000000f0000000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 00000000fec00000 - 00000000fec10000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 00000000fee00000 - 00000000fee01000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; BIOS-e820: 00000000fff80000 - 0000000100000000 (reserved)<br><span style="font-weight: bold;">luther@gliethttp:~$</span> vim /proc/meminfo<br>MemTotal:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1478540 kB<br>MemFree:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 868544 kB<br>Buffers:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 31084 kB<br>Cached:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 321672 kB<br>SwapCached:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0 kB<br><br>luther@gliethttp:~$ sudo vim /boot/grub/grub.cfg<br>原来的<br>linux&nbsp;&nbsp;&nbsp; /boot/vmlinuz-2.6.31-14-generic root=UUID=9a04b75d-22f4-4100-a8b0-a07ef00ead04 ro&nbsp;&nbsp; quiet splash<br>新改的<br>linux&nbsp;&nbsp;&nbsp; /boot/vmlinuz-2.6.31-14-generic root=UUID=9a04b75d-22f4-4100-a8b0-a07ef00ead04 ro&nbsp;&nbsp; quiet splash&nbsp;<span style="font-weight: bold;"> mem=1442M</span><br><br>修改之后dmesg将多出如下一行提示:<br>[&nbsp;&nbsp;&nbsp; 0.000000] user-defined physical RAM map:<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 0000000000000000 - 000000000009dc00 (usable)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 000000000009dc00 - 00000000000a0000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 00000000000d2000 - 0000000000100000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 0000000000100000 - <span style="font-weight: bold;">000000005a200000</span> (usable)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: <span style="font-weight: bold;">000000005bf10000</span> - 000000005bf19000 (ACPI data)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 000000005bf19000 - 000000005bf80000 (ACPI NVS)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 000000005bf80000 - 0000000060000000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 00000000e0000000 - 00000000f0000000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 00000000fec00000 - 00000000fec10000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 00000000fee00000 - 00000000fee01000 (reserved)<br>[&nbsp;&nbsp;&nbsp; 0.000000]&nbsp; user: 00000000fff80000 - 0000000100000000 (reserved)<br><br>之前<br><span style="font-weight: bold;">[&nbsp;&nbsp;&nbsp; 0.000000] 583MB HIGHMEM available.</span><br>之后<br><span style="font-weight: bold;">[&nbsp;&nbsp;&nbsp; 0.000000] 554MB HIGHMEM available.</span><br><br>这样<span style="font-weight: bold;">000000005a200000 － </span><span style="font-weight: bold;">000000005bf10000之间的29M物理内存就被预留出来供我们的DMA使用了[luther.gliethttp]</span><br><br><br>==================================================<br>=====第1步=============================================================================<br>[root@localhost ~]# cat /proc/meminfo <br>MemTotal:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1026124 kB<br><br>[root@localhost ~]# cat /proc/iomem <br>00000000-0009efff : System RAM<br>&nbsp; 00000000-00000000 : Crash kernel<br>0009f000-0009ffff : reserved<br>000a0000-000bffff : Video RAM area<br>000c0000-000c7fff : Video ROM<br>000d4000-000d4fff : Adapter ROM<br>000f0000-000fffff : System ROM<br>00100000-3f6effff : System RAM // 内存首尾地址,我们将从0x3f6effff结尾开始往前保留300M空间<br>&nbsp; 00400000-006081dd : Kernel code<br>&nbsp; 006081de-006e19bb : Kernel data<br>3f6f0000-3f6f2fff : ACPI Non-volatile Storage<br>3f6f3000-3f6fffff : ACPI Tables<br>40000000-400003ff : 0000:00:1f.1<br>f0000000-f7ffffff : 0000:00:02.0<br>f8000000-f8ffffff : PCI Bus #01<br>&nbsp; f8000000-f87fffff : 0000:01:04.0<br>&nbsp;&nbsp;&nbsp; f8000000-f87fffff : ceopen_dmp<br>&nbsp; f8800000-f880ffff : 0000:01:04.0<br>&nbsp;&nbsp;&nbsp; f8800000-f880ffff : ceopen_dmp<br>&nbsp; f8810000-f88100ff : 0000:01:03.0<br>&nbsp;&nbsp;&nbsp; f8810000-f88100ff : 8139too<br>&nbsp; f8811000-f88111ff : 0000:01:04.0<br>&nbsp;&nbsp;&nbsp; f8811000-f88111ff : ceopen_dmp<br>f9000000-f93fffff : 0000:00:00.0<br>f9400000-f947ffff : 0000:00:02.0<br>f9480000-f94803ff : 0000:00:1d.7<br>&nbsp; f9480000-f94803ff : ehci_hcd<br>f9481000-f94811ff : 0000:00:1f.5<br>&nbsp; f9481000-f94811ff : Intel ICH5<br>f9482000-f94820ff : 0000:00:1f.5<br>&nbsp; f9482000-f94820ff : Intel ICH5<br>fec00000-ffffffff : reserved<br>=====第2步=============================================================================<br>向cmdline加入mem和reserved启动参数<br><br>hex(0x3f6f0000-300*1024*1024)等于0x2caf0000,这里表示从0x3f6effff结尾开始往前保留300M空间<br>hex(300*1024*1024)等于0x12c00000<br><br>[root@localhost ~]# vim /boot/grub/menu.lst<br>kernel /boot/vmlinuz-2.6.18-53.el5 ro root=LABEL=/ rhgb quiet mem=0x2caf0000 reserve=0x2caf0000,0x12c00000<br>即保留0x2caf0000开始的300*1024*1024字节内存<br><br><span style="font-weight: bold;">kernel/resource.c|820| 
__setup("reserve=", reserve_setup);</span><br><a target="_blank" href="http://blog.chinaunix.net/u1/38994/showart_2019500.html">2.6.30.4内核cmdline常用命令行参数与相应处理函数</a><br><br>[root@localhost ~]# cat /proc/meminfo <br>MemTotal:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 721324 kB<br><br>[root@localhost ~]# cat /proc/iomem <br>00000000-0009efff : System RAM<br>&nbsp; 00000000-00000000 : Crash kernel<br>0009f000-0009ffff : reserved<br>000a0000-000bffff : Video RAM area<br>000c0000-000c7fff : Video ROM<br>000d4000-000d4fff : Adapter ROM<br>000f0000-000fffff : System ROM<br>00100000-2caeffff : System RAM<br>&nbsp; 00400000-006081dd : Kernel code<br>&nbsp; 006081de-006e19bb : Kernel data<br>2caf0000-3f6effff : reserved // 这就是我们保留出来的内存了,和上面的内存结构一致[luther.gliethttp]<br>3f6f0000-3f6f03ff : 0000:00:1f.1<br>f0000000-f7ffffff : 0000:00:02.0<br>f8000000-f8ffffff : PCI Bus #01<br>&nbsp; f8000000-f87fffff : 0000:01:04.0<br>&nbsp; f8800000-f880ffff : 0000:01:04.0<br>&nbsp; f8810000-f88100ff : 0000:01:03.0<br>&nbsp;&nbsp;&nbsp; f8810000-f88100ff : 8139too<br>&nbsp; f8811000-f88111ff : 0000:01:04.0<br>f9000000-f93fffff : 0000:00:00.0<br>f9400000-f947ffff : 0000:00:02.0<br>f9480000-f94803ff : 0000:00:1d.7<br>&nbsp; f9480000-f94803ff : ehci_hcd<br>f9481000-f94811ff : 0000:00:1f.5<br>&nbsp; f9481000-f94811ff : Intel ICH5<br>f9482000-f94820ff : 0000:00:1f.5<br>&nbsp; f9482000-f94820ff : Intel ICH5<br><br>=====第3步=============================================================================<br><span style="font-weight: bold;">虽然预留了300M空间,但是ioremap_nocache不能映射全部的300M空间,不知道为什么,可能和</span><br style="font-weight: bold;"><span style="font-weight: bold;">系统自身有关系,下面是具体的映射代码,因为已经将region做了reserved申请命名,所以</span><br style="font-weight: bold;"><span style="font-weight: bold;">我们也就不需要再使用request_mem_region(pdma, dma_size, "gliethttp_dma_area")来获得region了.</span><br style="font-weight: bold;"><br style="font-weight: bold;"><span style="font-weight: bold;">const dma_addr_t pdma = 0x2caf0000;</span><br style="font-weight: bold;"><span style="font-weight: bold;">const size_t dma_size = (280*1024*1024);</span><br style="font-weight: bold;"><br style="font-weight: bold;"><span style="font-weight: bold;">kdma = ioremap_nocache(pdma, dma_size);</span><br style="font-weight: bold;"><span style="font-weight: bold;">if (kdma == NULL)</span><br style="font-weight: bold;"><span style="font-weight: bold;">&nbsp;&nbsp;&nbsp; return -ENOMEM;</span><br style="font-weight: bold;"><span style="font-weight: bold;">其实2G内存也没有问题,mem=1.6G,然后ko驱动使用mmap将1.6G-2G之间的内存物理地址直接映射给user空间,这样user空间就可以直接向1.6G-2G物理内存写入数据了,然后PCI直接通过寄存器配置,向1.6G-2G的物理地址读取数据,这样透过ko驱动将user和pci建立了直连,当然了,因为内核线性地址为3G-4G只有1G的内存可以被映射,所以2G内存的另外1G内存就属于高端内存了,所以内核ko驱动不能映射1.6G-2G的内存到内核线性地址空间,但是可以通过kmap短暂的映射来使用[luther.gliethttp]</span><br><br><br>/*<br>&nbsp;* Pick out the memory size.&nbsp; We look for mem=size@start,<br>&nbsp;* where start and size are "size[KkMm]"<br>&nbsp;*/<br>static void __init early_mem(char **p)<br>{<br>&nbsp;&nbsp;&nbsp; static int usermem __initdata = 0;<br>&nbsp;&nbsp;&nbsp; unsigned long size, start;<br><br>&nbsp;&nbsp;&nbsp; /*<br>&nbsp;&nbsp;&nbsp; &nbsp;* If the user specifies memory size, we<br>&nbsp;&nbsp;&nbsp; &nbsp;* blow away any automatically generated<br>&nbsp;&nbsp;&nbsp; &nbsp;* size.<br>&nbsp;&nbsp;&nbsp; &nbsp;*/<br>&nbsp;&nbsp;&nbsp; if (usermem == 0) {<br>&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; usermem = 1;<br>&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; meminfo.nr_banks = 0;<br>&nbsp;&nbsp;&nbsp; }<br><br>&nbsp;&nbsp;&nbsp; start = PHYS_OFFSET;<br>&nbsp;&nbsp;&nbsp; size&nbsp; = memparse(*p, p);<br>&nbsp;&nbsp;&nbsp; if (**p == '@')<br>&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; start = memparse(*p + 1, p);<br><br>&nbsp;&nbsp;&nbsp; arm_add_memory(start, size);<br>}<br><span style="font-weight: bold;">__early_param("mem=", early_mem);</span><br><br>以下转自：http://hi.baidu.com/linuxbestbest/blog/item/9bc8dbdb72127763d0164e9c.html<br><div class="cnt" id="blog_text"><p>有时，内核不能识别你的全部内存（RAM）。你可以用 <tt class="COMMAND"><font face="NSimsun">cat /proc/meminfo</font></tt> 命令来校验。</p>
<p>查看一下所显示的数量是否与你所知的系统内存相同。如果不同，在 <tt class="FILENAME"><font face="NSimsun">/boot/grub/grub.conf</font></tt> 文件中添加以下一行：</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="USERINPUT"><strong>mem=<tt class="REPLACEABLE"><em>xx</em></tt>M</strong></tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>把 <tt class="REPLACEABLE"><em><font face="NSimsun">xx</font></em></tt> 替换成你拥有的内存数量（以 MB 为单位）。</p>
<p>在 <tt class="FILENAME"><font face="NSimsun">/boot/grub/grub.conf</font></tt> 文件中，以上的例子与下面相似：,</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="COMPUTEROUTPUT">#NOTICE: You have a /boot partition. This means that<br>#        all kernel paths are relative to /boot/<br>default=0<br>timeout=30<br>splashimage=(hd0,0)/grub/splash.xpm.gz<br>title Red Hat Linux (2.4.20-2.47.1)<br>        root (hd0,0)<br>        kernel /vmlinuz-2.4.20-2.47.1 ro root=/dev/hda3 mem=128M</tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>当你重新引导后，<tt class="FILENAME"><font face="NSimsun">grub.conf</font></tt> 文件中的改变将会反映在你的系统中。</p>
<p>或者，你可以在 <tt class="FILENAME"><font face="NSimsun">/etc/lilo.conf</font></tt> 文件中添加以下一行：</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="USERINPUT"><strong>append="mem=<tt class="REPLACEABLE"><em>xx</em></tt>M"</strong></tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>注意，<tt class="COMMAND"><font face="NSimsun">append</font></tt> 命令在 GRUB 和 LILO 中都可用。</p>
<p>把 <tt class="REPLACEABLE"><em><font face="NSimsun">xx</font></em></tt> 替换成你拥有的内存数量（以 MB 为单位）。切记，每映像后补的行会完全覆写全局后补的行。把这行添加到每映像描述中可能值得一试。</p>
<p>在 <tt class="FILENAME"><font face="NSimsun">/etc/lilo.conf</font></tt> 文件中，以上的例子与下面相似：</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="COMPUTEROUTPUT">boot=/dev/sda<br>      map=/boot/map<br>      install=/boot/boot.b<br>      prompt<br>      timeout=50<br><br>      image=/boot/vmlinuz-2.4.20-2.47.1<br>              label=linux<br>              root=/dev/sda1<br>              initrd=/boot/initrd-2.4.20-2.47.1.img<br>              read-only<br>              append="mem=128M"</tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>记住在改变了 <tt class="FILENAME"><font face="NSimsun">/etc/lilo.conf</font></tt> 文件后运行 <tt class="COMMAND"><font face="NSimsun">/sbin/lilo -v</font></tt> 命令。</p>
<p>请注意，在 GRUB 或 LILO 中指定所用标签（映像）时传递这一选项可以获得同样的效果。</p>
<p>当你已载入 GRUB 引导屏幕后，键入 <tt class="COMMAND"><font face="NSimsun">e</font></tt> 来编辑。你所选定的引导标签的配置文件中的项目列表就会在你面前出现。</p>
<p>选择开头为 <tt class="COMPUTEROUTPUT"><font face="NSimsun">kernel</font></tt> 的行，然后键入 <tt class="COMMAND"><font face="NSimsun">e</font></tt> 来编辑这一引导项目。</p>
<p>在 <tt class="COMPUTEROUTPUT"><font face="NSimsun">kernel</font></tt> 行的末尾，添加：</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="USERINPUT"><strong>mem=<tt class="REPLACEABLE"><em>xx</em></tt>M</strong></tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>或</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="USERINPUT"><strong>append=<tt class="REPLACEABLE"><em>xx</em></tt>M</strong></tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>这里的 <tt class="REPLACEABLE"><em><font face="NSimsun">xx</font></em></tt> 与你系统的内存数量相同。</p>
<p>按 <span class="KEYCAP"><keycap></keycap>[Enter]</span> 键来退出编辑模式。</p>
<p>回到 GRUB 屏幕后，键入 <tt class="COMMAND"><font face="NSimsun">b</font></tt> 来用你的新内存指数引导。</p>
<p>在图形化的 LILO 屏幕上，按 <span class="KEYCAP"><keycap></keycap>[Ctrl]</span>-<span class="KEYCAP"><keycap></keycap>[x]</span> 退回到 <tt class="PROMPT"><font face="NSimsun">boot:</font></tt> 提示。接下来，在 <tt class="PROMPT"><font face="NSimsun">boot:</font></tt> 提示下输入：</p>
<table width="100%" bgcolor="#dcdcdc" class="SCREEN">
    <tbody>
        <tr>
            <td>
            <pre class="SCREEN"><tt class="USERINPUT"><strong>linux mem=<tt class="REPLACEABLE"><em>xx</em></tt>M</strong></tt></pre>
            </td>
        </tr>
    </tbody>
</table>
<p>请记住将 <tt class="REPLACEABLE"><em><font face="NSimsun">xx</font></em></tt> 替换成你系统的内存数量。按 <span class="KEYCAP"><keycap></keycap>[Enter]</span> 键来引导。</p></div><br>
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		           </div>

<pre>
原文:
http://blog.chinaunix.net/uid-20564848-id-74177.html
</pre>
