---
layout: post
title: "virtio驱动分析之libvirt层的参数配置"
categories: 虚拟化
tags: [virtio驱动分析, libvirt层配置]
date: 2014-10-28 17:01:11
---


一直在研究kvm的para-virtualization driver - virtio，可能是太熟的原因吧，今天突然发现不知道咋在libvirt层配置kvm采用virtio驱动了，问题在于，看到下面这个配置文件，我竟不能确定此配置是否是采用了virtio驱动，先来看下配置文件的virtio相关的部分：
{% highlight bash %}
<disk type='file' device='disk'>
    <source file='/data0/0/21/disk.0'/>
    <target dev='vda'/>
    <driver name='qemu' type='qcow2' cache='default'/>
</disk>
{% endhighlight %}
于是，我就google一个网上的采用virtio驱动的配置文件：
{% highlight bash %}
<disk type='file' device='disk'>
            <driver name='qemu' cache='none'/>
            <source file='/opt/images/win7.img'/>
            <target dev='vda' bus='virtio'/>
          </disk>
{% endhighlight %}

然后，问题就更多了：

<pre>
   （1）是不是在target item中增加bus='virtio'就说明采用了virtio驱动
   （2）google的这个例子的image文件win7.img是什么格式的，我的例子可以从driver item的type参数看出是qcow2，google的例子怎么看出来？(可能有人会说，可以通过file命令来查看)，但是这并不符合我的风格，写个配置文件必须能解决所有疑问才行，要file下才知道啥意思，那只能说这个配置文件写的太失败了。
</pre>

带着以上问题，我阅读了下libvirt documents，下了如下总结。

1. <disk/>配置项说明
<pre>
    disk常用的配置参数：type，device，snapshot等
（1）type属性可以设置为：file，block，dir，network等值，这主要取决于底层的实现
（2）device属性用来表示Guest OS看来，disk表现为什么类型的设备，其值为：floppy，disk，cdrom，lun等，默认值为disk
（3）snapshot属性用来描述与磁盘快照相关的功能时的一些默认的行为：
snapshot='internal',表示snapshot与data存储在同一个文件中，比如一个qcow2文件，即镜像和数据是一体的，没有单独的snapshot文件
snapshot='external',表示镜像文件和data分离存储，即有单独的snapshot文件
snapshot='no',表示禁止disk的snapshot的功能
      read-only的disk不支持快照的功能，另外，这些属性是否生效还要取决于hypervisor。
</pre>

2. <source/> 说明

source常用的配置参数：dev，file，dir，protocol等，如果disk的type='file',那么source的file属性指向image文件的完整路径；如果disk的type='block',那么source的dev属性指向host上的某个设备，如/dev/sdb；如果disk的type='dir'，那么source的dir指向host上的某一个目录，此目录用来做vm的镜像；如果disk的type='network'，那么source的protocol参数，该参数用来指定访问remote image的协议，其值可以为：nbd，rbd，sheepdog或gluster，此时，另外一个mandatory属性必须设置为remote端的哪一个volume/image将被使用

（1）file attribute
{% highlight bash %}
<disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='/data2/vms/ubuntu.qcow2'/>
            <target dev='vda' bus='virtio'/>
        </disk>
{% endhighlight %}

（2）dev attribute

{% highlight bash %}
<disk type='block' device='lun'>
      <driver name='qemu' type='raw'/>
      <source dev='/dev/sda'/>
      <target dev='sda' bus='scsi'/>
      <address type='drive' controller='0' bus='0' target='3' unit='0'/>
    </disk>
{% endhighlight %}

（3）dir attribute （use a directory as floppy）
{% highlight bash %}
<disk type='dir' device='floppy'>
          <source dir='/tmp/test'/>
          <target dev='fda' bus='fdc'/>
          <readonly/>
        </disk>
{% endhighlight %}
（4）protocol attribute
{% highlight bash %}
<disk type='network'>
      <driver name="qemu" type="raw" io="threads" ioeventfd="on" event_idx="off"/>
      <source protocol="sheepdog" name="image_name">
        <host name="hostname" port="7000"/>
      </source>
      <target dev="hdb" bus="ide"/>
      <boot order='1'/>
      <transient/>
      <address type='drive' controller='0' bus='1' unit='0'/>
    </disk>
{% endhighlight %}
3. <target/> 说明

target item用来说明disk所挂载的总线的类型，此总线是guest os中看到的总线类型，比如从guest os中看到的硬盘是ide还是scsi的，这取决于设备挂载的总线。 target常用的attribute有：dev和bus.

(1) dev attribute

  disk设备的logical name，比方说：hdx，sdx，vdx等

(2) bus attribute

  此用来描述仿真的设备的类型，其值可以为:ide,scsi,virtio,xen,usb,sata等，此attribute value可以通过dev的value来推断 出来，如果dev='hdb',那么bus='ide'；如果dev='vda',那么bus='virtio'

4. <driver/>说明

  this item更详细的描述了hypervisor为disk提供的driver，其common used attribute包括：name，type，cache等

（1）name attribute

    对于kvm来说，name has an unique value - 'qemu'，xen可以支持很多值，不错详细介绍。

（2）type attribute

   kvm支持raw，qcow2，qed，bochs等多种镜像格式，不同的镜像格式对应着不同的驱动类型。另外，kvm是目前支持的镜像格式最全的一种hypervisor。

（3）cache attribute

   cache控制着guest os对disk的cache机制，cache的方式有：default，none，writethrough，writeback，directsync，unsafe等，cache的类型影响着guest os的性能，所以需要根据实际应用场景来选择，比较常用的类型为：none，writethrough，writeback.

   至于三种cache的区别和原理，请参见《kvm 存储栈分析 》一文！

   至此，virtio的问题已经解决！感觉以后必须随时做好笔记，加深对某些问题的理解，要不然时间已久就全忘了。
