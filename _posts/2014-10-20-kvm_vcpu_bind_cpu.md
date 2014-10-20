---
layout: post
title: "为虚拟机vCPU绑定物理CPU"
categories: 虚拟化
tags: [vcpu绑定]
date: 2014-10-20 16:45:34
---

为了提高缓存命中率，提高虚拟机性能，可以将vCPU绑定到指定的物理CPU去执行。具体设置步骤如下：

在宿主机操作系统启动时将用于虚拟机的CPU独立出来，使其上只运行vCPU线程，QEMU进程和少数的管理进程。设置方法即是在内核启动参数中加入：
isolcpus=0,1

例如在grub.cfg下面的配置如下：
<pre>
menuentry 'Fedora (3.13.6-200.fc20.x86_64) 20 (Heisenbug)' --class fedora --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-3.13.4-200.fc20.x86_64-advanced-5bcef32f-430b-4d74-beaa-4fcfccc438f9' {
        ......
    linux   /vmlinuz-3.13.6-200.fc20.x86_64 root=UUID=5bcef32f-430b-4d74-beaa-4fcfccc438f9 ro vconsole.font=latarcyrheb-sun16  rhgb quiet LANG=zh_CN.UTF-8 isolcpus=0,1
    initrd /initramfs-3.13.6-200.fc20.x86_64.img
}
</pre>

使用taskset命令将vCPU线程绑定到指定的物理CPU。例如，某虚拟机的qemu进程及两个vCPU线程如下：
<pre>
[root@kelvin ~]# ps -eLo ruser,pid,ppid,lwp,psr,args | grep qemu | grep -v grep
root      4706  3629  4706   1 qemu-system-x86_64 -m 2G -smp 2 /var/lib/libvirt/images/fedora.img -enable-kvm
root      4706  3629  4708   1 qemu-system-x86_64 -m 2G -smp 2 /var/lib/libvirt/images/fedora.img -enable-kvm
root      4706  3629  4709   0 qemu-system-x86_64 -m 2G -smp 2 /var/lib/libvirt/images/fedora.img -enable-kvm
</pre>

若要将线程ID为4709的vCPU从CPU0绑定到CPU2上执行，可使用如下命令：
	
{% highlight bash %}
# taskset -p 0x4 4709
{% endhighlight %}

-p后面接的是物理CPU的掩码，其二进制表示从最低位到最高位分别表示第0个物理CPU到最后一个物理CPU，若二进制表示为1，则表示某线程可以在该物理CPU上运行，若为0，则不能。上面的命令的含义就是，线程ID为4709的线程(vCPU)只能在第2个(从0开始编号)物理CPU上运行。执行上述命令的结果如下：
	
{% highlight bash %}
[root@kelvin ~]# taskset -p 0x4 4709
pid 4709's current affinity mask: f
pid 4709's new affinity mask: 4
[root@kelvin ~]# ps -eLo ruser,pid,ppid,lwp,psr,args | grep qemu | grep -v grep
root      4706  3629  4706   3 qemu-system-x86_64 -m 2G -smp 2 /var/lib/libvirt/images/fedora.img -enable-kvm
root      4706  3629  4708   0 qemu-system-x86_64 -m 2G -smp 2 /var/lib/libvirt/images/fedora.img -enable-kvm
root      4706  3629  4709   2 qemu-system-x86_64 -m 2G -smp 2 /var/lib/libvirt/images/fedora.img -enable-kvm
{% endhighlight %}

线程ID为4709的vCPU已经在编号为2的物理CPU上运行了。

<pre>
referer: http://my.oschina.net/kelvinxupt/blog/211826
</pre>
