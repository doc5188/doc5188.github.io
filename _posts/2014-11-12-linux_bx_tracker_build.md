---
layout: post
title: "局域网bt tracker服务器配置"
categories: linux
tags: [bt tracker]
date: 2014-11-12 17:27:42
---

因为facebook使用bt分发应用包提高部署的速度，所以大家都在想能不能只用用现有开发成熟的软件做一个类似的方案出来。<br>
自己简单地测试了一下，凑合可以用。不过bt的客户端很难找到一个合适的，transmission本来还不错的，但是细节的使用还是需要多搞一下。<br>
昨天简单地用opentracker和ctorrent来测试了一下，基本能跑起来。</p>
<p>1.先设置单个的tracker服务器<br>
直接找了一个开源的tracker服务器 http://erdgeist.org/arts/software/opentracker/。对照里面的readme就可以完成安装,</p>
<p>cvs -d :pserver:cvs@cvs.fefe.de:/cvs -z9 co libowfat<br>
cd libowfat<br>
make<br>
cd ..<br>
cvs -d:pserver:anoncvs@cvs.erdgeist.org:/home/cvsroot co opentracker<br>
cd opentracker<br>
make<br>
我是把opentracker安装到了/opt目录下面。然后直接用命令启动 就行了</p>
<p>/opt/opentracker/bin/opentracker -p 6969 -P 6969 -d /opt/opentracker/run/ -u nobody &amp;</p>
<p>2.使用mktorrent创建torrent(ctorrent其实也能建立种子但是测试了一下不支持目录)</p>
<p>根据单个文件制作种子的时候最好写绝对路径，简单测试一下把centos的一个镜像(CentOS-6.3-x86_64-LiveCD.iso )添加到种子里面。<br>
$ mktorrent -a http://xxx.test1.net:6969/announce -o centos.torrent /home/admin/CentOS-6.3-x86_64-LiveCD.iso<br>
mktorrent 1.0 (c) 2007, 2009 Emil Renner Berthing</p>
<p>Hashed 2768 of 2768 pieces.<br>
Writing metainfo file… done.<br>
类似根据目录添加到种子文件就是<br>
mktorrent -a http://xxx.test1.net:6969/announce -o test2.torrent /home/admin/path_to_dir</p>
<p>在做种的服务器上直接提交种子<br>
ctorrent centos.torrent<br>
文件校验完成后就开始做种。</p>
<p>3.把种子文件拷贝到需要传输的几个机器上，然后在每台服务器上运行<br>
ctorrent centos.torrent -s p2p/centos.iso<br>
就会把文件下载到p2p目录下，并把文件存为centos.iso<br>
简单测试了一下，把一个服务器上的文件删除后，可以看到另外一个服务器的在做种了，第一次上传了349M，第二次430M，还可以。局域网这样传输的速度非常的快。<br>
Listening on 0.0.0.0:2705<br>
\ 2/0/3 [2751/2768/2768] 688MB,0MB | 88078,0K/s | 81920,0K E:0,1<br>
Download complete.<br>
Total time used: 0 minutes.<br>
Seed for other 72 hours.</p>
<p>\ 0/0/3 [2768/2768/2768] 692MB,349MB | 0,0K/s | 0,0K E:0,2<br>
/ 0/0/3 [2768/2768/2768] 692MB,779MB | 0,0K/s | 0,0K E:0,2 </p>
<p>后续： 这个只是简单测试了部署局域网内BT P2P分发的可行性，实际上很多细节的地方需要考虑。比如tracker服务器的精细化、集群化配置，opentracker感觉还是非常粗糙的一个东西，可以设置的地方很少，而且也没有后台页面查看。另外ctorrent虽然简单用用还行，但是几千台服务器还是要客户端能后台执行，命令行远程进行种子的添加(或者自动添加某个目录下的种子)、删除、任务完成后进行通知。transmission目前看来还可以，但是在N个版本的OS上安装就比较麻烦。</p>
