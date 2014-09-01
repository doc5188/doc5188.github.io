---
layout: post
date: 2014-09-01 15:24:21
title: "Ceph monitor故障恢复探讨"
categories: 文件系统
tags: [linux, ceph, 文件系统, dfs]
---

1 问题

一般来说，在实际运行中，ceph monitor的个数是2n+1(n>=0)个，在线上至少3个，只要正常的节点数>=n+1，ceph的paxos算法能保证系统的正常运行。所以，对于3个节点，同时只能挂掉一个。一般来说，同时挂掉2个节点的概率比较小，但是万一挂掉2个呢？

如果ceph的monitor节点超过半数挂掉，paxos算法就无法正常进行仲裁(quorum)，此时，ceph集群会阻塞对集群的操作，直到超过半数的monitor节点恢复。

If there are not enough monitors to form a quorum, the ceph command will block trying to reach the cluster. In this situation, you need to get enough ceph-mon daemons running to form a quorum before doing anything else with the cluster.

 

所以，

（1）如果挂掉的2个节点至少有一个可以恢复，也就是monitor的元数据还是OK的，那么只需要重启ceph-mon进程即可。所以，对于monitor，最好运行在RAID的机器上。这样，即使机器出现故障，恢复也比较容易。

（2）如果挂掉的2个节点的元数据都损坏了呢？出现这种情况，说明人品不行，2台机器的RAID磁盘同时损坏，这得多背？肯定是管理员嫌工资太低，把机器砸了。如何恢复呢？
2 恢复

其实，也没有其它办法，只能想办法将故障的节点恢复，但元数据已经损坏。幸好还有一个元数据正常的节点，通过它可以恢复。

 

添加monitor的步骤：

{% highlight bash %}
$ ceph mon getmap -o /tmp/monmap           # provides fsid and existing monitor addrs
$ ceph auth export mon. -o /tmp/monkey     # mon. auth key
$ ceph-mon -i newname --mkfs --monmap /tmp/monmap --keyring /tmp/monkey
{% endhighlight %}

所以，只要得到monmap，就可以恢复monitor了。

为了模拟，考虑2个monitor节点，挂掉一个，此时通过网络访问ceph的所有操作都会被阻塞，但monitor的本地socket还是可以通信的。

<img src="/upload/images/202345249879286.png" >

 

但是，让人蛋疼的是通过socket不能进行monmap的导出。不过，幸好有monmaptool工具，通过它，我们可以手动生成(注意fsid)：

{% highlight bash %}
# monmaptool  --create  --add vm2 172.16.213.134:6789 --add vm3 172.16.213.135:6789 --fsid eb295a51-ec22-4971-86ef-58f6d2bea3bf --clobber monmap

monmaptool: monmap file monmap
monmaptool: set fsid to eb295a51-ec22-4971-86ef-58f6d2bea3bf
monmaptool: writing epoch 0 to monmap (2 monitors)
{% endhighlight %}

将正常monitor节点的mon key拷贝过来：

{% highlight bash %}
# cat /var/lib/ceph/mon/cluster1-vm2/keyring

[mon.]

        key = AQDZQ8VTAAAAABAAX9HqE0NITrUt7j1w0YadvA==

        caps mon = "allow *"
{% endhighlight %}

 

然后初始化：

{% highlight bash %}
# ceph-mon --cluster cluster1 -i vm3 --mkfs --monmap /root/monmap --keyring /tmp/keyring

ceph-mon: set fsid to eb295a51-ec22-4971-86ef-58f6d2bea3bf

ceph-mon: created monfs at /var/lib/ceph/mon/cluster1-vm3 for mon.vm3
{% endhighlight %}

最后，启动故障节点：

{% highlight bash %}
# ceph-mon --cluster cluster1 -i vm3 --public-addr 172.16.213.135:6789
{% endhighlight %}

 

<img src="/upload/images/202346092533176.png" >

一切OK!

 

主要参考

［1］RECOVERING FROM CEPH-MON FAILURE: http://ceph.com/docs/argonaut/ops/manage/failures/mon/

<pre>
引用：
http://www.cnblogs.com/hustcat/p/3925971.html
</pre>
