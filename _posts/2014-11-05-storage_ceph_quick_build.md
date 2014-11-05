---
layout: post
title: "ceph 快速部署"
categories: 存储
tags: [ceph, ceph部署]
date: 2014-11-05 16:21:42
---

ceph 统一存储现在火的不得了了，大家都在调研它，最近大脑发热，也尝试体验一把。下面简单记录下ceph ceph-deploy 部署步骤。

* 一、规划

* 1. 虚拟机5台，其功能如下:

        
<pre>
名称	pulic network	cluster network	 功能
admin-node	192.168.0.254/24	10.0.1.254/24	管理机器
mon01	192.168.0.2/24	10.0.1.2/24	集群状态监控机器
osd01	192.168.0.3/24	10.0.1.3/24	集群数据存放机器
osd02	192.168.0.4/24	10.0.1.4/24	集群数据存放机器
osd03	192.168.0.5/24	10.0.1.5/24	集群数据存放机器
</pre>

* 2. os:

ubuntu 12.04 x86_64

* 二、准备

* 1. 版本验证key
	
<pre>
wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
</pre>

* 2. ceph源库
	
<pre>
echo deb http://ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
</pre>

* 3. 更新系统安装ceph-deploy工具

<pre>
apt-get update && apt-get install ceph-deploy
</pre>

* 4.修改各个节点的主机名和hosts文件

(请自行修改好主机名和hosts文件)
<pre>
.....................
.....................
10.0.1.254 admin-node
10.0.1.2 mon01
10.0.1.3 osd01
10.0.1.4 osd02
10.0.1.5 osd03
</pre>

* 5. admin-node 免密码登录其它节点
	
<pre>
# ssh-keygen
Generating public/private key pair.
Enter file in which to save the key (/ceph-client/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /ceph-client/.ssh/id_rsa.
Your public key has been saved in /ceph-client/.ssh/id_rsa.pub.
 
# for h in mon01 osd01 osd02 osd03;do ssh-copy-id $i;done
</pre>

* 6. 创建ceph-deploy需要的配置
	
<pre>
vim /root/.ssh/config
 
Host mon01
   Hostname mon01
   User root
Host osd01
   Hostname osd01
   User root
Host osd02
   Hostname osd02
   User root
Host osd03
   Hostname osd03
   User root
</pre>

* 三、安装

* 1. 创建工作目录
	
<pre>
mkdir my-cluster
cd my-cluster
</pre>

* 2. 创建集群
	
<pre>
ceph-deploy new mon01
</pre>

* 3. 安装ceph
	
<pre>
ceph-deploy install admin-node mon01 osd01 osd02 osd03
</pre>

* 4. 初始化集群监控节点和访问key
	
<pre>
ceph-deploy mon create-initial
</pre>

注意:经过上步执行，我们会看到当前工作目录下有如下文件(若没有，请反复执行上面命令)
	
<pre>
ceph.client.admin.keyring
ceph.bootstrap-osd.keyring
ceph.bootstrap-mds.keyring
</pre>

* 四、添加OSD存储盘

* 1. 列出磁盘
	
<pre>
ceph-deploy disk list osd01 osd02 osd03
</pre>

* 2. 清理磁盘分区（我的虚拟机第二块磁盘是vdb）
<pre>
ceph-deploy disk zap osd01:/vdb
ceph-deploy disk zap osd02:/vdb
ceph-deploy disk zap osd03:/vdb
</pre>

* 3. 准备OSD磁盘

<pre>
ceph-deploy osd prepare osd01:vdb
ceph-deploy osd prepare osd02:vdb
ceph-deploy osd prepare osd03:vdb
</pre>

* 4.激活OSD磁盘

<pre>	
ceph-deploy osd activate osd01:/dev/vdb1
ceph-deploy osd activate osd02:/dev/vdb1
ceph-deploy osd activate osd03:/dev/vdb1
</pre>

* 五、查看集群状态
	
ceph health

显示ok就表示集群OK！



<pre>
referfer:http://ggbond.blog.51cto.com/8886865/1535684

</pre>
