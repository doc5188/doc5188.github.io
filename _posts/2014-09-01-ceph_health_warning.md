---
layout: post
date: 2014-09-01 17:15:13
title: "HEALTH_WARN 192 pgs degraded; 192 pgs stuck unclean"
categories: "文件系统"
tags: [ceph, dfs,　文件系统]
---

前几天尝试快速部署ceph，所用虚拟机环境为：

2台虚拟机，2个mon。每台2个OSD。。

采用ceph-deploy部署，部署后修改了ceph.conf文件如下：

{% highlight bash %}

[global]
osd_journal_size = 1024
filestore_xattr_use_omap = true
auth_cluster_required = none
auth_service_required = none
auth_client_required = none
osd_pool_default_size = 3
osd_pool_default_min_size = 2
osd_pool_default_pg_num = 700
osd_pool_default_pgp_num = 700

[osd]
osd_mount_options_xfs = rw,noatime,inode64,logbsize=256k,delaylog

{% endhighlight %}

隐掉了mon和fsid相关内容。。

 

安装之后遇见了如题所述的错误：

HEALTH_WARN 192 pgs degraded; 192 pgs stuck unclean

 

解决办法：

错误原因是replica数和当前osd数目之间有冲突，在本例中replica为3，而osd为4个，又仅有2个host，无法实现replica为3。

因此解决办法是增加host，osd或者修改replica。。。

增加host，osd比较简单，这里就略过了，这里讲一讲如何修改你replica。

1.修改ceph.conf文件

<pre>
osd_pool_default_size = 2
osd_pool_default_min_size = 1
</pre>

min size务必要小于size

2.修改已有的所有pool的replica

查看现有pool的复制数：

{% highlight bash %}

# ceph osd dump | grep ‘rep size’

pool 0 ‘data’ rep size 3 min_size 2 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0
pool 1 ‘metadata’ rep size 3 min_size 2 crush_ruleset 1 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0
pool 2 ‘rbd’ rep size 3 min_size 2 crush_ruleset 2 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0

# ceph osd pool set data size 3

# ceph osd pool set data min size 2

{% endhighlight %}

3.重启所有mon和osd服务


{% highlight bash %}
# service ceph-mon restart id=[hostname]
# service ceph-osd restart id=[osd num]

{% endhighlight %}

 

