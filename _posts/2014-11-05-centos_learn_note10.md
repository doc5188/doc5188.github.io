---
layout: post
title: "第四天:centos6.5的软件安装，用户管理等"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:28
---

<p>1.软件的安装命令：</P>
<p>&nbsp;<wbr> 第一种:以 软件名.rpm&nbsp;<wbr>
为结尾的二进制文件，这样的文件的安装</P>
<p>&nbsp;<wbr> rpm -ivh
软件名.rpm&nbsp;<wbr>&nbsp;<wbr> i 是
install&nbsp;<wbr> v 是校验&nbsp;<wbr> h 进度</P>
<p>&nbsp;<wbr> 卸载软件 是&nbsp;<wbr> rpm -e 软件报名， 不需要 打出
.rpm这样的格式，只需要软件包名就可以了</P>
<p>&nbsp;<wbr>卸载软件需要首先知道要卸载的软件名称，使用 rpm -qa
就可以查询出所有安装的软件包名。</P>
<p>&nbsp;<wbr>有些软件包的卸载需要依赖其他软件包，这种情况就不允许卸载了，使用 rpm -e
--nodeps packagename</P>
<p>强力卸载，但是 有可能其他的软件包就不好用了，因为也可能依赖于这个软件包的依赖.</P>
<p>&nbsp;<wbr>第二种：以源代码的方式安装的软件包:以 src.rpm结尾的软件包：</P>
<p>&nbsp;<wbr> 先编译: rpm -rebuild
xx.scr.rpm&nbsp;<wbr> 然后会在centos的/usr/src下会生成一个 xx.rpm
然后就可以用 rpm -ivh安装了。</P>
<p>第三种：常见的tar.gz .bz2
结尾的二进制软件包,：gz是用gzip压缩的,bz是用bzip压缩的，所以需要的解压软件不相同.</P>
<p>&nbsp;<wbr> 上回说到 tar -zxvf xx.gz&nbsp;<wbr> tar
-jxvf xx.bz2</P>
<p>&nbsp;<wbr>&nbsp;<wbr>
z是调用gzip解压,j是调用bzip解压,x是解压,v是校验
f&nbsp;<wbr>是指定的文件名.这样的文件几乎是通用格式。</P>
<p>&nbsp;<wbr> 如果要卸载，我觉得需要手动一点一点搜索卸载。</P>
<p>第四种:以 tar.gz xx.bz2结尾的源代码软件包：先用 tar -zxvf xx.gz 解压，解压后进目录:</P>
<p>&nbsp;<wbr> ./configure 配置&nbsp;<wbr> make
编译&nbsp;<wbr> make install 全通用的三步，。通过 我 这几次安装vncserver
来看，如果不是通过yum 来安装的软件呢，你需要多观察下 解压后的文件目录：看看有没有 readme，install
这样的说明文件，看看安装的命令参数格式等，或者都需要那些依赖的软件。很重要，centos下 我觉得
先观察多用眼，少动手，对于我这样的新手。还有后缀是.bin的执行文件，安装的时候都看下文件权限，没有执行权限需要先给与权限，再安装。安装后使用垃圾清理命令：make
clean 或者 make distclean 清理临时文件。</P>
<p>注意问题:</P>
<p>有的软件说明里 标注 make uninstall 卸载，没有的话
只有手动删除，所以尽量看说明安装的时候就直接填写安装的目录名称，以后删除也好删除，直接用 rm -rf 就可以删除目录.</P>
<p>如果需要编译安装的软件，在编译的时候 ，直接带上编译的参数。./configure --prefix =
目录名，这样安装的时候就是安装到这个目录，方便，不需要编译的安装看下，时候可自定义安装目录，很重要，我装vncserver都装的很乱，都没法删除了。</P>
<p>2.用户管理，群组</P>
<p>&nbsp;<wbr>&nbsp;<wbr> 1.&nbsp;<wbr>
用户名：uid,每个用户属于某个组内，用户群组：gid 一个用户可以加入多个群组。</P>
<p>useradd -g -d -s -p 密码
username01&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
增加一个用户名为 username01 所属群组,-d 建立目录,-s 运行shell。</P>
<p>usermod 用户名 更改用户名 主目录 登录的shell.</P>
<p>passwd 用户名&nbsp;<wbr> 修改用户密码</P>
<p>userdel -r 用户名&nbsp;<wbr> -r 将用户目录下的文件都删除。</P>
<p>注意:1.删除用户前 ，看下是否该用户还在线，是否有进程在运行，有的话 不能删除，查看进程ps -aux |gerp
"我的用户名"</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
2.还要查看定时器中是否有要删除用户的执行计划， 使用 crontab -u 用户名 -r 来删除定时器任务。</P>
<p>&nbsp;<wbr>&nbsp;<wbr> 2./etc/group 群组文件,</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
groupadd 组名&nbsp;<wbr>&nbsp;<wbr> groupmod -g 102
group01 将群组group01的序号改为102号组。</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
groupdel 组名, 注意：如果有这个组内的用户正在线上，不能删除，关闭才能删除组名</P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
