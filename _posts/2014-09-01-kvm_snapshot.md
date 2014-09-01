---
layout: post
title: "kvm环境快照（snapshot）的使用方法"
date: 2014-09-01 17:29:32
categories: 虚拟化
tags: [linux,kvm, qemu, snapshot]
---

实例一  使用qemu-img命令使用快照

kvm环境下qcow2的镜像支持快照

1 确认镜像的格式
{% highlight bash%}
  [root@nc1 boss]# qemu-img info test.qcow2 
  image: test.qcow2
  file format: qcow2
  virtual size: 10G (10737418240 bytes)
  disk size: 1.6G
  cluster_size: 65536
{% endhighlight %}

2 为镜像test.qcow2创建快照，创建快照并没有产生新的镜像，虚拟机镜像大小增加，快照应属于镜像。
{% highlight bash%}
  [root@nc1 boss]# qemu-img snapshot -c snapshot01 test.qcow2 
  [root@nc1 boss]# qemu-img snapshot -c snapshot02 test.qcow2
{% endhighlight %}
                                        快照名      镜像名

3 列出某个镜像的所有快照
{% highlight bash%}
  [root@nc1 boss]# qemu-img snapshot -l test.qcow2 
  Snapshot list:
  ID        TAG                 VM SIZE                DATE       VM CLOCK
  1         snapshot01                0 2011-09-07 15:39:25   00:00:00.000
  2         snapshot02                0 2011-09-07 15:39:29   00:00:00.000
{% endhighlight %}

4 使用快照
{% highlight bash%}
  [root@nc1 boss]# qemu-img snapshot -a snapshot01 test.qcow2 
{% endhighlight %}

5 删除快照
{% highlight bash%}
  [root@nc1 boss]# qemu-img snapshot -d snapshot01 test.qcow2
{% endhighlight %}

附：
<pre>
  'snapshot' is the name of the snapshot to create, apply or delete
  '-a' applies a snapshot (revert disk to saved state)
  '-c' creates a snapshot
  '-d' deletes a snapshot
  '-l' lists all snapshots in the given image
</pre>

实例二 利用libvirt使用快照

1 同样先确认镜像的格式为qcow2
{% highlight bash %}
  [root@nc1 boss]#qemu-img info test.qcow2
  image: test.qcow2
  file format: qcow2
  virtual size: 10G (10737418240 bytes)
  disk size: 1.1G
  cluster_size: 65536
{% endhighlight %}
 
2 创建并启动以test.qcow2作为镜像的虚拟机,假设虚拟机名称为testsnp，如果虚拟机没有启动，也可创建快照，但是意义不大，快照size为0
  开始使用配置文件来创建指定虚拟机的快照
{% highlight bash %}
  <domainsnapshot>
    <name>snapshot02</name> //快照名
    <description>Snapshot of OS install and updates</description>//描述
    <disks>
      <disk name='/home/guodd/boss/test.qcow2'>           //虚拟机镜像的绝对路径
      </disk>
      <disk name='vdb' snapshot='no'/>
    </disks>
  </domainsnapshot>
{% endhighlight %}

  保存为snp.xml,开始创建
{% highlight bash%}
  [root@nc1 boss]#virsh snapshot-create testsnp snp.xml  //即以snp.xml作为快照的配置文件为虚拟机testsnp创建快照
   Domain snapshot snapshot02 created from 'snp.xml'
{% endhighlight %}
  
3 查看虚拟机testsnp已有的快照
{% highlight bash%}
  [root@nc1 boss]# virsh snapshot-list testsnp
  Name                 Creation Time             State
  ---------------------------------------------------
  1315385065           2011-09-07 16:44:25 +0800 running        //1315385065创建时间比snapshot02早
  snapshot02           2011-09-07 17:32:38 +0800 running
{% endhighlight %}

  同样地，也可以通过qemu-img命令来查看快照
{% highlight bash%}
  [root@nc1 boss]# qemu-img info test.qcow2
   image: test.qcow2
   file format: qcow2
   virtual size: 10G (10737418240 bytes)
   disk size: 1.2G
   cluster_size: 65536
   Snapshot list:
   ID        TAG                 VM SIZE                DATE       VM CLOCK
   1         1315385065             149M 2011-09-07 16:44:25   00:00:48.575
   2         snapshot02             149M 2011-09-07 17:32:38   00:48:01.341
{% endhighlight %}

4 可以通过snapshot-dumpxml命令查询该虚拟机某个快照的详细配置
{% highlight bash%}
[root@nc1 boss]# virsh snapshot-dumpxml testsnp 1315385065
 <domainsnapshot>
  <name>1315385065</name>
  <description>Snapshot of OS install and updates</description>
  <state>running</state>     //虚拟机状态  虚拟机关机状态时创建的快照状态为shutoff（虚拟机运行时创建的快照，即使虚拟机状态为shutoff，快照状态依然为running）
  <creationTime>1315385065</creationTime>   //虚拟机的创建时间 Readonly 由此可以看出没有给快照指定名称的话，默认以时间值来命名快照
  <domain>
    <uuid>afbe5fb7-5533-d154-09b6-33c869a05adf</uuid> //此快照所属的虚拟机(uuid)
  </domain>
</domainsnapshot>
{% endhighlight %}

 查看第二个snapshot
{% highlight bash%}
 [root@nc1 boss]# virsh snapshot-dumpxml testsnp snapshot02
 <domainsnapshot>
   <name>snapshot02</name>
   <description>Snapshot of OS install and updates</description>
   <state>running</state>
   <parent>
     <name>1315385065</name>        //当前快照把前一个快照作为parent
   </parent>
   <creationTime>1315387958</creationTime>
   <domain>
     <uuid>afbe5fb7-5533-d154-09b6-33c869a05adf</uuid>
   </domain>
 </domainsnapshot>
{% endhighlight %}

5 查看最新的快照信息
{% highlight bash%}
  [root@nc1 boss]# virsh snapshot-current testsnp
  <domainsnapshot>
    <name>1315385065</name>
    <description>Snapshot of OS install and updates</description>
    <state>running</state>
    <creationTime>1315385065</creationTime>  
    <domain>
      <uuid>afbe5fb7-5533-d154-09b6-33c869a05adf</uuid>
    </domain>
   </domainsnapshot>
{% endhighlight %}

6 使用快照，指定使用哪一个快照恢复虚拟机
{% highlight bash%}
 [root@nc1 boss]# virsh snapshot-revert testsnp snapshot02
{% endhighlight %}

7 删除指定快照
{% highlight bash%}
  [root@nc1 boss]# virsh snapshot-delete testsnp snapshot02
  Domain snapshot snapshot02 deleted
{% endhighlight %}

附：
<pre>
Snapshot (help keyword 'snapshot')
    snapshot-create                Create a snapshot from XML
    snapshot-create-as             Create a snapshot from a set of args
    snapshot-current               Get the current snapshot
    snapshot-delete                Delete a domain snapshot
    snapshot-dumpxml               Dump XML for a domain snapshot
    snapshot-list                  List snapshots for a domain
    snapshot-revert                Revert a domain to a snapshot
</pre>
 
更多详细内容可查看 http://libvirt.org/formatsnapshot.html#SnapshotAttributes

<pre>
http://blog.csdn.net/gg296231363/article/details/6899533
</pre>
