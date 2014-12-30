---
layout: post
title: "Linux 下强制中断其他用户的登陆连接"
categories: linux
tags: [linux]
date: 2014-12-30 09:31:50
---

Linux 下查看我们的不速之客

我们通过下面这个命令，可以查看 VPS 上还有谁在登陆：

w

输出类似下列信息：

<pre>
23:20:00 up 960 days, 4:29, 2 user, load average: 0.05, 0.02, 0.00

USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT

root pts/0 183.16.xxx.x 22:59 0.00s 0.04s 0.00s w

root pts/3 70.82.xxx.xx 22:59 0.00s 0.04s 0.00s w
</pre>

踢掉那些不速之客

<pre>
skill -9 -t pts/3
</pre

其中，pts/3 就是第二行里面，70.82.xxx.xx 所对应的 TTY 。执行上述命令后,连接用户被断开
