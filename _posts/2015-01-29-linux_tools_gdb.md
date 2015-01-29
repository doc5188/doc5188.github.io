---
layout: post
title: "gdb运行时调试-关于死循环"
categories: linux 
tags: [gdb, 调试]
date: 2015-01-29 14:20:12
---

对于正在运行的程序，使用gdb attach功能进行运行时调试（启动gdb后使用attach <PID>命令或在启动gdb时使用-p <PID>参数）。

以下是一段故意构造的简单死循环程序：

<pre>
#include <stdio.h>
#include <unistd.h>
int main()
{
    int i;
    for (i = 0; ; ++i) {
        printf("%d\n", i);
        sleep(1);
    }
}
</pre>

使用gcc -O2编译程序后运行，并在另一个虚拟终端里使用gdb attach进程：
	
<pre>
root@bt:～# gdb -q -p 2569
Attaching to process 2569
Reading symbols from /root/test3...(no debugging symbols found)...done.
Reading symbols from /lib/libc.so.6...(no debugging symbols found)...done.
Loaded symbols for /lib/libc.so.6
Reading symbols from /lib64/ld-linux-x86-64.so.2...(no debugging symbols found)...done.
Loaded symbols for /lib64/ld-linux-x86-64.so.2
0x00007fbf605ac380 in nanosleep () from /lib/libc.so.6
(gdb) bt
#0 0x00007fbf605ac380 in nanosleep () from /lib/libc.so.6
#1 0x00007fbf605ac210 in sleep () from /lib/libc.so.6
#2 0x00000000004005c8 in main ()
(gdb) finish
Run till exit from #0 0x00007fbf605ac380 in nanosleep () from /lib/libc.so.6
0x00007fbf605ac210 in sleep () from /lib/libc.so.6
(gdb) finish
Run till exit from #0 0x00007fbf605ac210 in sleep () from /lib/libc.so.6
0x00000000004005c8 in main ()
(gdb) ni
0x00000000004005a8 in main ()
(gdb)
0x00000000004005aa in main ()
(gdb)
0x00000000004005af in main ()
(gdb)
0x00000000004005b4 in main ()
(gdb)
0x00000000004005b6 in main ()
(gdb)
0x00000000004005b9 in main ()
(gdb)
0x00000000004005be in main ()
(gdb)
0x00000000004005c3 in main ()
(gdb)
0x00000000004005c8 in main ()
(gdb)
0x00000000004005a8 in main ()
(gdb)
0x00000000004005aa in main ()
...

</pre>
attach会使进程挂起，现象类似于插入了一个临时断点。上面的操作中使用了两次finish命令使程序运行至返回到main()函数中。

对于使用-O2选项编译的程序，无法简单的进行源代码级别的调试，next/step命令不可用。对于此类程序，可以使用nexti/stepi命令，它们大体与next/step相同，分别表示步过与步入，不同之处在于前者针对单条汇编指令。上述示例中连续使用ni(nexti)命令，从指令地址（rip寄存器值）可以比较容易的发现死循环，指令地址始终徘徊在0x00000000004005a8-0x00000000004005c8。

这一招数对于后台daemon程序相当有效。我曾经维护过一个带有守护进程的deamon程序，对于出现问题的运行中子进程，守护进程会将其杀死重启，但并不会记录详细原因。一日，某版本频繁重启，领导下了死命令：必须在XXX之前解决！于是动用重量级上古神器gdb挂上守护进程，让运行中子进程自生自灭。。。天可怜见，终于在一周后重现了问题，并使用上述方法确认了死循环问题及其位置。。。

那晚我梦见了花团锦簇。。。 


<pre>
referer:my.oschina.net/u/180497/blog/141645
</pre>
