---
layout: post
date: 2014-09-01 17:24:21
title: "ceph运维常用指令"
categories: 文件系统
tags: [ceph, 文件系统, dfs, 运维]
---

<pre>
原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://zhanguo1110.blog.51cto.com/5750817/1543032

一、集群

1、启动一个ceph 进程

启动mon进程

service ceph start  mon.node1

启动msd进程

service ceph start mds.node1

启动osd进程

 service ceph start osd.0

2、查看机器的监控状态

[root@client ~]# ceph health

HEALTH_OK

3、查看ceph的实时运行状态

[root@client ~]# ceph -w

    cluster be1756f2-54f7-4d8f-8790-820c82721f17

     health HEALTH_OK

     monmap e2: 3 mons at {node1=10.240.240.211:6789/0,node2=10.240.240.212:6789/0,node3=10.240.240.213:6789/0}, election epoch 294, quorum 0,1,2 node1,node2,node3

     mdsmap e95: 1/1/1 up {0=node2=up:active}, 1 up:standby

     osdmap e88: 3 osds: 3 up, 3 in

      pgmap v1164: 448 pgs, 4 pools, 10003 MB data, 2520 objects

            23617 MB used, 37792 MB / 61410 MB avail

                 448 active+clean

2014-06-30 00:48:28.756948 mon.0 [INF] pgmap v1163: 448 pgs: 448 active+clean; 10003 MB data, 23617 MB used, 37792 MB / 61410 MB avail


4、检查信息状态信息

[root@client ~]# ceph -s

    cluster be1756f2-54f7-4d8f-8790-820c82721f17

     health HEALTH_OK

     monmap e2: 3 mons at {node1=10.240.240.211:6789/0,node2=10.240.240.212:6789/0,node3=10.240.240.213:6789/0}, election epoch 294, quorum 0,1,2 node1,node2,node3

     mdsmap e95: 1/1/1 up {0=node2=up:active}, 1 up:standby

     osdmap e88: 3 osds: 3 up, 3 in

      pgmap v1164: 448 pgs, 4 pools, 10003 MB data, 2520 objects

            23617 MB used, 37792 MB / 61410 MB avail

                 448 active+clean

[root@client ~]# 


5、查看ceph存储空间

[root@client ~]# ceph df

GLOBAL:

    SIZE       AVAIL      RAW USED     %RAW USED 

    61410M     37792M     23617M       38.46     

POOLS:

    NAME         ID     USED       %USED     OBJECTS 

    data         0      10000M     16.28     2500    

    metadata     1      3354k      0         20      

    rbd          2      0          0         0       

    jiayuan      3      0          0         0       

[root@client ~]# 

6、删除一个节点的所有的ceph数据包

[root@node1 ~]# ceph-deploy purge node1

[root@node1 ~]# ceph-deploy purgedata node1

7、为ceph创建一个admin用户并为admin用户创建一个密钥，把密钥保存到/etc/ceph目录下：

ceph auth get-or-create client.admin mds 'allow' osd 'allow *' mon 'allow *' > /etc/ceph/ceph.client.admin.keyring

或

ceph auth get-or-create client.admin mds 'allow' osd 'allow *' mon 'allow *' -o /etc/ceph/ceph.client.admin.keyring

8、为osd.0创建一个用户并创建一个key

ceph auth get-or-create osd.0 mon 'allow rwx' osd 'allow *' -o /var/lib/ceph/osd/ceph-0/keyring

9、为mds.node1创建一个用户并创建一个key

ceph auth get-or-create mds.node1 mon 'allow rwx' osd 'allow *' mds 'allow *' -o /var/lib/ceph/mds/ceph-node1/keyring

10、查看ceph集群中的认证用户及相关的key

ceph auth list

11、删除集群中的一个认证用户

ceph auth del osd.0

12、查看集群的详细配置

[root@node1 ~]# ceph daemon mon.node1 config show | more

13、查看集群健康状态细节

[root@admin ~]# ceph health detail

HEALTH_WARN 12 pgs down; 12 pgs peering; 12 pgs stuck inactive; 12 pgs stuck unclean

pg 3.3b is stuck inactive since forever, current state down+peering, last acting [1,2]

pg 3.36 is stuck inactive since forever, current state down+peering, last acting [1,2]

pg 3.79 is stuck inactive since forever, current state down+peering, last acting [1,0]

pg 3.5 is stuck inactive since forever, current state down+peering, last acting [1,2]

pg 3.30 is stuck inactive since forever, current state down+peering, last acting [1,2]

pg 3.1a is stuck inactive since forever, current state down+peering, last acting [1,0]

pg 3.2d is stuck inactive since forever, current state down+peering, last acting [1,0]

pg 3.16 is stuck inactive since forever, current state down+peering, last acting [1,2]


14、查看ceph log日志所在的目录

[root@node1 ~]# ceph-conf --name mon.node1 --show-config-value log_file

/var/log/ceph/ceph-mon.node1.log



二、mon

1、查看mon的状态信息

[root@client ~]# ceph mon stat

e2: 3 mons at {node1=10.240.240.211:6789/0,node2=10.240.240.212:6789/0,node3=10.240.240.213:6789/0}, election epoch 294, quorum 0,1,2 node1,node2,node3

2、查看mon的选举状态

[root@client ~]# ceph quorum_status

{"election_epoch":294,"quorum":[0,1,2],"quorum_names":["node1","node2","node3"],"quorum_leader_name":"node1","monmap":{"epoch":2,"fsid":"be1756f2-54f7-4d8f-8790-820c82721f17","modified":"2014-06-26 18:43:51.671106","created":"0.000000","mons":[{"rank":0,"name":"node1","addr":"10.240.240.211:6789\/0"},{"rank":1,"name":"node2","addr":"10.240.240.212:6789\/0"},{"rank":2,"name":"node3","addr":"10.240.240.213:6789\/0"}]}}

3、查看mon的映射信息

[root@client ~]# ceph mon dump

dumped monmap epoch 2

epoch 2

fsid be1756f2-54f7-4d8f-8790-820c82721f17

last_changed 2014-06-26 18:43:51.671106

created 0.000000

0: 10.240.240.211:6789/0 mon.node1

1: 10.240.240.212:6789/0 mon.node2

2: 10.240.240.213:6789/0 mon.node3

4、删除一个mon节点

[root@node1 ~]# ceph mon remove node1

removed mon.node1 at 10.39.101.1:6789/0, there are now 3 monitors

2014-07-07 18:11:04.974188 7f4d16bfd700  0 monclient: hunting for new mon

5、获得一个正在运行的mon map，并保存在1.txt文件中

[root@node3 ~]# ceph mon getmap -o 1.txt

got monmap epoch 6

6、查看上面获得的map

[root@node3 ~]#  monmaptool --print 1.txt 

monmaptool: monmap file 1.txt

epoch 6

fsid 92552333-a0a8-41b8-8b45-c93a8730525e

last_changed 2014-07-07 18:22:51.927205

created 0.000000

0: 10.39.101.1:6789/0 mon.node1

1: 10.39.101.2:6789/0 mon.node2

2: 10.39.101.3:6789/0 mon.node3

[root@node3 ~]#

7、把上面的mon map注入新加入的节点

ceph-mon -i node4 --inject-monmap 1.txt

8、查看mon的amin socket

root@node1 ~]# ceph-conf --name mon.node1 --show-config-value admin_socket

/var/run/ceph/ceph-mon.node1.asok 

9、查看mon的详细状态

[root@node1 ~]# ceph daemon mon.node1  mon_status 

{ "name": "node1",

  "rank": 0,

  "state": "leader",

  "election_epoch": 96,

  "quorum": [

        0,

        1,

        2],

  "outside_quorum": [],

  "extra_probe_peers": [

        "10.39.101.4:6789\/0"],

  "sync_provider": [],

  "monmap": { "epoch": 6,

      "fsid": "92552333-a0a8-41b8-8b45-c93a8730525e",

      "modified": "2014-07-07 18:22:51.927205",

      "created": "0.000000",

      "mons": [

            { "rank": 0,

              "name": "node1",

              "addr": "10.39.101.1:6789\/0"},

            { "rank": 1,

              "name": "node2",

              "addr": "10.39.101.2:6789\/0"},

            { "rank": 2,

              "name": "node3",

              "addr": "10.39.101.3:6789\/0"}]}

10、删除一个mon节点

[root@os-node1 ~]# ceph mon remove os-node1

removed mon.os-node1 at 10.40.10.64:6789/0, there are now 3 monitors


三、msd

1、查看msd状态

[root@client ~]# ceph mds stat

e95: 1/1/1 up {0=node2=up:active}, 1 up:standby

2、查看msd的映射信息

[root@client ~]# ceph mds dump

dumped mdsmap epoch 95

epoch   95

flags   0

created 2014-06-26 18:41:57.686801

modified        2014-06-30 00:24:11.749967

tableserver     0

root    0

session_timeout 60

session_autoclose       300

max_file_size   1099511627776

last_failure    84

last_failure_osd_epoch  81

compat  compat={},rocompat={},incompat={1=base v0.20,2=client writeable ranges,3=default file layouts on dirs,4=dir inode in separate object,5=mds uses versioned encoding,6=dirfrag is stored in omap}

max_mds 1

in      0

up      {0=5015}

failed

stopped

data_pools      0

metadata_pool   1

inline_data     disabled

5015:   10.240.240.212:6808/3032 'node2' mds.0.12 up:active seq 30

5012:   10.240.240.211:6807/3459 'node1' mds.-1.0 up:standby seq 38

3、删除一个mds节点

[root@node1 ~]# ceph  mds rm 0 mds.node1

 mds gid 0 dne


四、osd

1、查看ceph osd运行状态

[root@client ~]# ceph osd stat

     osdmap e88: 3 osds: 3 up, 3 in


2、查看osd映射信息

[root@client ~]# ceph osd dump

epoch 88

fsid be1756f2-54f7-4d8f-8790-820c82721f17

created 2014-06-26 18:41:57.687442

modified 2014-06-30 00:46:27.179793

flags 

pool 0 'data' replicated size 2 min_size 1 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0 flags hashpspool crash_replay_interval 45 stripe_width 0

pool 1 'metadata' replicated size 2 min_size 1 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0 flags hashpspool stripe_width 0

pool 2 'rbd' replicated size 2 min_size 1 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0 flags hashpspool stripe_width 0

pool 3 'jiayuan' replicated size 2 min_size 1 crush_ruleset 0 object_hash rjenkins pg_num 256 pgp_num 256 last_change 73 owner 0 flags hashpspool stripe_width 0

max_osd 3

osd.0 up   in  weight 1 up_from 65 up_thru 75 down_at 64 last_clean_interval [53,55) 10.240.240.211:6800/3089 10.240.240.211:6801/3089 10.240.240.211:6802/3089 10.240.240.211:6803/3089 exists,up 8a24ad16-a483-4bac-a56a-6ed44ab74ff0

osd.1 up   in  weight 1 up_from 59 up_thru 74 down_at 58 last_clean_interval [31,55) 10.240.240.212:6800/2696 10.240.240.212:6801/2696 10.240.240.212:6802/2696 10.240.240.212:6803/2696 exists,up 8619c083-0273-4203-ba57-4b1dabb89339

osd.2 up   in  weight 1 up_from 62 up_thru 74 down_at 61 last_clean_interval [39,55) 10.240.240.213:6800/2662 10.240.240.213:6801/2662 10.240.240.213:6802/2662 10.240.240.213:6803/2662 exists,up f8107c04-35d7-4fb8-8c82-09eb885f0e58

[root@client ~]# 


3、查看osd的目录树

[root@client ~]# ceph osd tree

# id    weight  type name       up/down reweight

-1      3       root default

-2      1               host node1

0       1                       osd.0   up      1

-3      1               host node2

1       1                       osd.1   up      1

-4      1               host node3

2       1                       osd.2   up      1


4、down掉一个osd硬盘

[root@node1 ~]# ceph osd down 0   #down掉osd.0节点

5、在集群中删除一个osd硬盘

[root@node4 ~]# ceph osd rm 0

removed osd.0

6、在集群中删除一个osd 硬盘 crush map

[root@node1 ~]# ceph osd crush rm osd.0

7、在集群中删除一个osd的host节点

[root@node1 ~]# ceph osd crush rm node1

removed item id -2 name 'node1' from crush map


查看最大osd的个数 

[root@node1 ~]# ceph osd getmaxosd

max_osd = 4 in epoch 514           #默认最大是4个osd节点

8、设置最大的osd的个数（当扩大osd节点的时候必须扩大这个值）

[root@node1 ~]# ceph osd setmaxosd 10

9、设置osd crush的权重为1.0

ceph osd crush set {id} {weight} [{loc1} [{loc2} ...]]

例如：

[root@admin ~]# ceph osd crush set 3 3.0 host=node4

set item id 3 name 'osd.3' weight 3 at location {host=node4} to crush map

[root@admin ~]# ceph osd tree

# id    weight  type name       up/down reweight

-1      6       root default

-2      1               host node1

0       1                       osd.0   up      1

-3      1               host node2

1       1                       osd.1   up      1

-4      1               host node3

2       1                       osd.2   up      1

-5      3               host node4

3       3                       osd.3   up      0.5


或者用下面的方式

[root@admin ~]# ceph osd crush reweight osd.3 1.0

reweighted item id 3 name 'osd.3' to 1 in crush map

[root@admin ~]# ceph osd tree

# id    weight  type name       up/down reweight

-1      4       root default

-2      1               host node1

0       1                       osd.0   up      1

-3      1               host node2

1       1                       osd.1   up      1

-4      1               host node3

2       1                       osd.2   up      1

-5      1               host node4

3       1                       osd.3   up      0.5

10、设置osd的权重

[root@admin ~]# ceph osd reweight 3 0.5

reweighted osd.3 to 0.5 (8327682)

[root@admin ~]# ceph osd tree

# id    weight  type name       up/down reweight

-1      4       root default

-2      1               host node1

0       1                       osd.0   up      1

-3      1               host node2

1       1                       osd.1   up      1

-4      1               host node3

2       1                       osd.2   up      1

-5      1               host node4

3       1                       osd.3   up      0.5

11、把一个osd节点逐出集群

[root@admin ~]# ceph osd out osd.3

marked out osd.3.  

[root@admin ~]# ceph osd tree

# id    weight  type name       up/down reweight

-1      4       root default

-2      1               host node1

0       1                       osd.0   up      1

-3      1               host node2

1       1                       osd.1   up      1

-4      1               host node3

2       1                       osd.2   up      1

-5      1               host node4

3       1                       osd.3   up      0      # osd.3的reweight变为0了就不再分配数据，但是设备还是存活的

12、把逐出的osd加入集群

[root@admin ~]# ceph osd in osd.3

marked in osd.3. 

[root@admin ~]# ceph osd tree

# id    weight  type name       up/down reweight

-1      4       root default

-2      1               host node1

0       1                       osd.0   up      1

-3      1               host node2

1       1                       osd.1   up      1

-4      1               host node3

2       1                       osd.2   up      1

-5      1               host node4

3       1                       osd.3   up      1

13、暂停osd （暂停后整个集群不再接收数据）

[root@admin ~]# ceph osd pause

set pauserd,pausewr      

14、再次开启osd （开启后再次接收数据） 

[root@admin ~]# ceph osd unpause

unset pauserd,pausewr


15、查看一个集群osd.2参数的配置

ceph --admin-daemon /var/run/ceph/ceph-osd.2.asok config show | less




五、PG组

1、1、查看pg组的映射信息

[root@client ~]# ceph pg dump

dumped all in format plain

version 1164

stamp 2014-06-30 00:48:29.754714

last_osdmap_epoch 88

last_pg_scan 73

full_ratio 0.95

nearfull_ratio 0.85

pg_stat objects mip     degr    unf     bytes   log     disklog state   state_stamp     v       reported       up      up_primary      acting  acting_primary  last_scrub      scrub_stamp     last_deep_scrudeep_scrub_stamp

0.3f    39      0       0       0       163577856       128     128     active+clean    2014-06-30 00:30:59.193479     52'128  88:242  [0,2]   0       [0,2]   0       44'25   2014-06-29 22:25:25.282347    0'0      2014-06-26 19:52:08.521434

3.3c    0       0       0       0       0       0       0       active+clean    2014-06-30 00:15:38.675465     0'0     88:21   [2,1]   2       [2,1]   2       0'0     2014-06-30 00:15:04.295637      0'0   2014-06-30 00:15:04.295637

2.3c    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:48.583702     0'0     88:46   [2,1]   2       [2,1]   2       0'0     2014-06-29 22:29:13.701625      0'0   2014-06-26 19:52:08.845944

1.3f    2       0       0       0       452     2       2       active+clean    2014-06-30 00:10:48.596050     16'2    88:66   [2,1]   2       [2,1]   2       16'2    2014-06-29 22:28:03.570074      0'0   2014-06-26 19:52:08.655292

0.3e    31      0       0       0       130023424       130     130     active+clean    2014-06-30 00:26:22.803186     52'130  88:304  [2,0]   2       [2,0]   2       44'59   2014-06-29 22:26:41.317403    0'0      2014-06-26 19:52:08.518978

3.3d    0       0       0       0       0       0       0       active+clean    2014-06-30 00:16:57.548803     0'0     88:20   [0,2]   0       [0,2]   0       0'0     2014-06-30 00:15:19.101314      0'0   2014-06-30 00:15:19.101314

2.3f    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:58.750476     0'0     88:106  [0,2]   0       [0,2]   0       0'0     2014-06-29 22:27:44.604084      0'0   2014-06-26 19:52:08.864240

1.3c    1       0       0       0       0       1       1       active+clean    2014-06-30 00:10:48.939358     16'1    88:66   [1,2]   1       [1,2]   1       16'1    2014-06-29 22:27:35.991845      0'0   2014-06-26 19:52:08.646470

0.3d    34      0       0       0       142606336       149     149     active+clean    2014-06-30 00:23:57.348657     52'149  88:300  [0,2]   0       [0,2]   0       44'57   2014-06-29 22:25:24.279912    0'0      2014-06-26 19:52:08.514526

3.3e    0       0       0       0       0       0       0       active+clean    2014-06-30 00:15:39.554742     0'0     88:21   [2,1]   2       [2,1]   2       0'0     2014-06-30 00:15:04.296812      0'0   2014-06-30 00:15:04.296812

2.3e    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:48.592171     0'0     88:46   [2,1]   2       [2,1]   2       0'0     2014-06-29 22:29:14.702209      0'0   2014-06-26 19:52:08.855382

1.3d    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:48.938971     0'0     88:58   [1,2]   1       [1,2]   1       0'0     2014-06-29 22:27:36.971820      0'0   2014-06-26 19:52:08.650070

0.3c    41      0       0       0       171966464       157     157     active+clean    2014-06-30 00:24:55.751252     52'157  88:385  [1,0]   1       [1,0]   1       44'41   2014-06-29 22:26:34.829858    0'0      2014-06-26 19:52:08.513798

3.3f    0       0       0       0       0       0       0       active+clean    2014-06-30 00:17:08.416756     0'0     88:20   [0,1]   0       [0,1]   0       0'0     2014-06-30 00:15:19.406120      0'0   2014-06-30 00:15:19.406120

2.39    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:58.784789     0'0     88:71   [2,0]   2       [2,0]   2       0'0     2014-06-29 22:29:10.673549      0'0   2014-06-26 19:52:08.834644

1.3a    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:58.738782     0'0     88:106  [0,2]   0       [0,2]   0       0'0     2014-06-29 22:26:29.457318      0'0   2014-06-26 19:52:08.642018

0.3b    37      0       0       0       155189248       137     137     active+clean    2014-06-30 00:28:45.021993     52'137  88:278  [0,2]   0       [0,2]   0       44'40   2014-06-29 22:25:22.275783    0'0      2014-06-26 19:52:08.510502

3.38    0       0       0       0       0       0       0       active+clean    2014-06-30 00:16:13.222339     0'0     88:21   [1,0]   1       [1,0]   1       0'0     2014-06-30 00:15:05.446639      0'0   2014-06-30 00:15:05.446639

2.38    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:58.783103     0'0     88:71   [2,0]   2       [2,0]   2       0'0     2014-06-29 22:29:06.688363      0'0   2014-06-26 19:52:08.827342

1.3b    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:58.857283     0'0     88:78   [1,0]   1       [1,0]   1       0'0     2014-06-29 22:27:30.017050      0'0   2014-06-26 19:52:08.644820

0.3a    40      0       0       0       167772160       149     149     active+clean    2014-06-30 00:28:47.002342     52'149  88:288  [0,2]   0       [0,2]   0       44'46   2014-06-29 22:25:21.273679    0'0      2014-06-26 19:52:08.508654

3.39    0       0       0       0       0       0       0       active+clean    2014-06-30 00:16:13.255056     0'0     88:21   [1,0]   1       [1,0]   1       0'0     2014-06-30 00:15:05.447461      0'0   2014-06-30 00:15:05.447461

2.3b    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:48.935872     0'0     88:57   [1,2]   1       [1,2]   1       0'0     2014-06-29 22:28:35.095977      0'0   2014-06-26 19:52:08.844571

1.38    0       0       0       0       0       0       0       active+clean    2014-06-30 00:10:48.597540     0'0     88:46   [2,1]   2       [2,1]   2       0'0     2014-06-29 22:28:01.519137      0'0   2014-06-26 19:52:08.633781

0.39    48      0       0       0       201326592       164     164     active+clean    2014-06-30 00:25:30.757843     52'164  88:432  [1,0]   1       [1,0]   1       44'32   2014-06-29 22:26:33.823947    0'0      2014-06-26 19:52:08.504628

下面部分省略


2、查看一个PG的map

[root@client ~]# ceph pg map 0.3f

osdmap e88 pg 0.3f (0.3f) -> up [0,2] acting [0,2]   #其中的[0,2]代表存储在osd.0、osd.2节点，osd.0代表主副本的存储位置

3、查看PG状态

[root@client ~]# ceph pg stat

v1164: 448 pgs: 448 active+clean; 10003 MB data, 23617 MB used, 37792 MB / 61410 MB avail

4、查询一个pg的详细信息

[root@client ~]# ceph pg  0.26 query

5、查看pg中stuck的状态

[root@client ~]# ceph pg dump_stuck unclean

ok

[root@client ~]# ceph pg dump_stuck inactive

ok

[root@client ~]# ceph pg dump_stuck stale

ok

6、显示一个集群中的所有的pg统计

ceph pg dump --format plain

7、恢复一个丢失的pg

ceph pg {pg-id} mark_unfound_lost revert

8、显示非正常状态的pg

ceph pg dump_stuck inactive|unclean|stale

六、pool

1、查看ceph集群中的pool数量

[root@admin ~]# ceph osd lspools

0 data,1 metadata,2 rbd,

2、在ceph集群中创建一个pool

ceph osd pool create jiayuan 100            #这里的100指的是PG组

3、为一个ceph pool配置配额

ceph osd pool set-quota data max_objects 10000

4、在集群中删除一个pool

ceph osd pool delete jiayuan  jiayuan  --yes-i-really-really-mean-it  #集群名字需要重复两次

5、显示集群中pool的详细信息

[root@admin ~]# rados df

pool name       category                 KB      objects       clones     degraded      unfound           rd        rd KB           wr        wr KB

data            -                  475764704       116155            0            0           0            0            0       116379    475764704

metadata        -                       5606           21            0            0           0            0            0          314         5833

rbd             -                          0            0            0            0           0            0            0            0            0

  total used       955852448       116176

  total avail      639497596

  total space     1595350044

[root@admin ~]# 

6、给一个pool创建一个快照

[root@admin ~]# ceph osd pool mksnap data   date-snap 

created pool data snap date-snap

7、删除pool的快照

[root@admin ~]# ceph osd pool rmsnap data date-snap

removed pool data snap date-snap

8、查看data池的pg数量

[root@admin ~]# ceph osd pool get data pg_num

pg_num: 64

9、设置data池的最大存储空间为100T（默认是1T)

[root@admin ~]# ceph osd pool set data target_max_bytes 100000000000000

set pool 0 target_max_bytes to 100000000000000

10、设置data池的副本数是3

[root@admin ~]# ceph osd pool set data size 3

set pool 0 size to 3

11、设置data池能接受写操作的最小副本为2

[root@admin ~]# ceph osd pool set data min_size 2

set pool 0 min_size to 2

12、查看集群中所有pool的副本尺寸

[root@admin mycephfs]# ceph osd dump | grep 'replicated size'

pool 0 'data' replicated size 3 min_size 2 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 26 owner 0 flags hashpspool crash_replay_interval 45 target_bytes 100000000000000 stripe_width 0

pool 1 'metadata' replicated size 2 min_size 1 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0 flags hashpspool stripe_width 0

pool 2 'rbd' replicated size 2 min_size 1 crush_ruleset 0 object_hash rjenkins pg_num 64 pgp_num 64 last_change 1 owner 0 flags hashpspool stripe_width 0

13、设置一个pool的pg数量

[root@admin ~]# ceph osd pool set data pg_num 100

set pool 0 pg_num to 100

14、设置一个pool的pgp数量

[root@admin ~]# ceph osd pool set data pgp_num 100

set pool 0 pgp_num to 100


七、rados和rbd指令

1、rados命令使用方法

（1）、查看ceph集群中有多少个pool （只是查看pool)

[root@node-44 ~]# rados lspools

data

metadata

rbd

images

volumes

.rgw.root

compute

.rgw.control

.rgw

.rgw.gc

.users.uid

（2）、查看ceph集群中有多少个pool,并且每个pool容量及利用情况

[root@node-44 ~]# rados df 

pool name       category                 KB      objects       clones     degraded      unfound           rd        rd KB           wr        wr KB

.rgw            -                          0            0            0            0           0            0            0            0            0

.rgw.control    -                          0            8            0            0           0            0            0            0            0

.rgw.gc         -                          0           32            0            0           0        57172        57172        38136            0

.rgw.root       -                          1            4            0            0           0           75           46           10           10

.users.uid      -                          1            1            0            0           0            0            0            2            1

compute         -                   67430708        16506            0            0           0       398128     75927848      1174683    222082706

data            -                          0            0            0            0           0            0            0            0            0

images          -                  250069744        30683            0            0           0        50881    195328724        65025    388375482

metadata        -                          0            0            0            0           0            0            0            0            0

rbd             -                          0            0            0            0           0            0            0            0            0

volumes         -                   79123929        19707            0            0           0      2575693     63437000      1592456    163812172

  total used       799318844        66941

  total avail    11306053720

  total space    12105372564

[root@node-44 ~]# 

（3）、创建一个pool

[root@node-44 ~]#rados mkpool test

(4)、查看ceph pool中的ceph object （这里的object是以块形式存储的）

[root@node-44 ~]# rados ls -p volumes | more

rbd_data.348f21ba7021.0000000000000866

rbd_data.32562ae8944a.0000000000000c79

rbd_data.589c2ae8944a.00000000000031ba

rbd_data.58c9151ff76b.00000000000029af

rbd_data.58c9151ff76b.0000000000002c19

rbd_data.58c9151ff76b.0000000000000a5a

rbd_data.58c9151ff76b.0000000000001c69

rbd_data.58c9151ff76b.000000000000281d

rbd_data.58c9151ff76b.0000000000002de1

rbd_data.58c9151ff76b.0000000000002dae

（5）、创建一个对象object 

[root@admin-node ~]# rados create test-object -p test


[root@admin-node ~]# rados -p test ls

test-object

（6）、删除一个对象

[root@admin-node ~]# rados rm test-object-1 -p test



2、rbd命令的用法 


（1）、查看ceph中一个pool里的所有镜像

[root@node-44 ~]# rbd ls images

2014-05-24 17:17:37.043659 7f14caa6e700  0 -- :/1025604 >> 10.49.101.9:6789/0 pipe(0x6c5400 sd=3 :0 s=1 pgs=0 cs=0 l=1 c=0x6c5660).fault

2182d9ac-52f4-4f5d-99a1-ab3ceacbf0b9

34e1a475-5b11-410c-b4c4-69b5f780f03c

476a9f3b-4608-4ffd-90ea-8750e804f46e

60eae8bf-dd23-40c5-ba02-266d5b942767

72e16e93-1fa5-4e11-8497-15bd904eeffe

74cb427c-cee9-47d0-b467-af217a67e60a

8f181a53-520b-4e22-af7c-de59e8ccca78

9867a580-22fe-4ed0-a1a8-120b8e8d18f4

ac6f4dae-4b81-476d-9e83-ad92ff25fb13

d20206d7-ff31-4dce-b59a-a622b0ea3af6


[root@node-44 ~]# rbd ls volumes

2014-05-24 17:22:18.649929 7f9e98733700  0 -- :/1010725 >> 10.49.101.9:6789/0 pipe(0x96a400 sd=3 :0 s=1 pgs=0 cs=0 l=1 c=0x96a660).fault

volume-0788fc6c-0dd4-4339-bad4-e9d78bd5365c

volume-0898c5b4-4072-4cae-affc-ec59c2375c51

volume-2a1fb287-5666-4095-8f0b-6481695824e2

volume-35c6aad4-8ea4-4b8d-95c7-7c3a8e8758c5

volume-814494cc-5ae6-4094-9d06-d844fdf485c4

volume-8a6fb0db-35a9-4b3b-9ace-fb647c2918ea

volume-8c108991-9b03-4308-b979-51378bba2ed1

volume-8cf3d206-2cce-4579-91c5-77bcb4a8a3f8

volume-91fc075c-8bd1-41dc-b5ef-844f23df177d

volume-b1263d8b-0a12-4b51-84e5-74434c0e73aa

volume-b84fad5d-16ee-4343-8630-88f265409feb

volume-c03a2eb1-06a3-4d79-98e5-7c62210751c3

volume-c17bf6c0-80ba-47d9-862d-1b9e9a48231e

volume-c32bca55-7ec0-47ce-a87e-a883da4b4ccd

volume-df8961ef-11d6-4dae-96ee-f2df8eb4a08c

volume-f1c38695-81f8-44fd-9af0-458cddf103a3


（2）、查看ceph pool中一个镜像的信息

[root@node-44 ~]# rbd info -p images --image 74cb427c-cee9-47d0-b467-af217a67e60a

rbd image '74cb427c-cee9-47d0-b467-af217a67e60a':

        size 1048 MB in 131 objects

        order 23 (8192 KB objects)

        block_name_prefix: rbd_data.95c7783fc0d0

        format: 2

        features: layering

（3）、在test池中创建一个命名为zhanguo的10000M的镜像

[root@node-44 ~]# rbd create -p test --size 10000 zhanguo

[root@node-44 ~]# rbd -p test info zhanguo    #查看新建的镜像的信息

rbd image 'zhanguo':

        size 10000 MB in 2500 objects

        order 22 (4096 KB objects)

        block_name_prefix: rb.0.127d2.2ae8944a

        format: 1

[root@node-44 ~]# 

（4）、删除一个镜像

[root@node-44 ~]# rbd rm  -p test  lizhanguo

Removing image: 100% complete...done.

（5）、调整一个镜像的尺寸

[root@node-44 ~]# rbd resize -p test --size 20000 zhanguo

Resizing image: 100% complete...done.

[root@node-44 ~]# rbd -p test info zhanguo   #调整后的镜像大小

rbd image 'zhanguo':

        size 20000 MB in 5000 objects

        order 22 (4096 KB objects)

        block_name_prefix: rb.0.127d2.2ae8944a

        format: 1

[root@node-44 ~]# 

（6）、给一个镜像创建一个快照

[root@node-44 ~]# rbd  snap create  test/zhanguo@zhanguo123  #池/镜像@快照

[root@node-44 ~]# rbd   snap ls  -p test zhanguo

SNAPID NAME           SIZE 

     2 zhanguo123 20000 MB 

[root@node-44 ~]# 

[root@node-44 ~]# rbd info test/zhanguo@zhanguo123

rbd image 'zhanguo':

        size 20000 MB in 5000 objects

        order 22 (4096 KB objects)

        block_name_prefix: rb.0.127d2.2ae8944a

        format: 1

        protected: False

[root@node-44 ~]# 

（7）、查看一个镜像文件的快照

[root@os-node101 ~]# rbd snap ls  -p volumes volume-7687988d-16ef-4814-8a2c-3fbd85e928e4

SNAPID NAME                                               SIZE 

     5 snapshot-ee7862aa-825e-4004-9587-879d60430a12 102400 MB 

（8）、删除一个镜像文件的一个快照快照

                                 快照所在的池/        快照所在的镜像文件           @ 快照

[root@os-node101 ~]# rbd snap rm volumes/volume-7687988d-16ef-4814-8a2c-3fbd85e928e4@snapshot-ee7862aa-825e-4004-9587-879d60430a12

rbd: snapshot 'snapshot-60586eba-b0be-4885-81ab-010757e50efb' is protected from removal.

2014-08-18 19:23:42.099301 7fd0245ef760 -1 librbd: removing snapshot from header failed: (16) Device or resource busy

上面不能删除显示的报错信息是此快照备写保护了，下面命令是删除写保护后再进行删除。

[root@os-node101 ~]# rbd snap unprotect volumes/volume-7687988d-16ef-4814-8a2c-3fbd85e928e4@snapshot-ee7862aa-825e-4004-9587-879d60430a12

[root@os-node101 ~]# rbd snap rm volumes/volume-7687988d-16ef-4814-8a2c-3fbd85e928e4@snapshot-ee7862aa-825e-4004-9587-879d60430a12

（9）删除一个镜像文件的所有快照

[root@os-node101 ~]# rbd snap purge  -p volumes volume-7687988d-16ef-4814-8a2c-3fbd85e928e4

Removing all snapshots: 100% complete...done.



（10）、把ceph pool中的一个镜像导出

导出镜像

[root@node-44 ~]# rbd export -p images --image 74cb427c-cee9-47d0-b467-af217a67e60a /root/aaa.img

2014-05-24 17:16:15.197695 7ffb47a9a700  0 -- :/1020493 >> 10.49.101.9:6789/0 pipe(0x1368400 sd=3 :0 s=1 pgs=0 cs=0 l=1 c=0x1368660).fault

Exporting image: 100% complete...done.


导出云硬盘

[root@node-44 ~]# rbd export -p volumes --image volume-470fee37-b950-4eef-a595-d7def334a5d6 /var/lib/glance/ceph-pool/volumes/Message-JiaoBenJi-10.40.212.24

2014-05-24 17:28:18.940402 7f14ad39f700  0 -- :/1032237 >> 10.49.101.9:6789/0 pipe(0x260a400 sd=3 :0 s=1 pgs=0 cs=0 l=1 c=0x260a660).fault

Exporting image: 100% complete...done.


（11）、把一个镜像导入ceph中 （但是直接导入是不能用的，因为没有经过openstack,openstack是看不到的）

[root@node-44 ~]# rbd import /root/aaa.img -p images --image 74cb427c-cee9-47d0-b467-af217a67e60a  

Importing image: 100% complete...done.
</pre>
