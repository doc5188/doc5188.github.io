---
layout: post
title: "第三天：centos6.5的yum安装软件设置。安装webmin软件包"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:29
---

<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
软件的安装是首要的问题，我想安装个webmin这个图形化的管理配置服务器的软</P>
<p>件包，首先面临着从哪来，怎么装的问题。<br />
如果你是用的cengos桌面方式启动，你可以上网直接下载最新版本的webmin,如</P>
<p>果你的局域网内有ftp服务器，你也可以，你有u盘也可以。<br />
但是呢，centos提供了yum更新方式。所以就用yum更新，省去了软件的关联等问</P>
<p>题。<br />
&nbsp;<wbr>&nbsp;<wbr> 1.先说下rpm软件包安装命令：rpm<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
一个rpm包的结构是这样子的， webmin-1.510-1.noarch(x86).rpm<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> 是有 - 和 .
连接而成， 包名称-版本号-发布版本号.适用的平台.rpm</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> 安装软件 rpm
-ivh 软件全名， 就是带进度显示信息的安装,常用的</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
更新一个软件包，用新的版本替换旧版本 rpm -Uvh rpm文件</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> 删除一个软件包，
rpm -e 软件名称</P>
<p>&nbsp;<wbr> a.查询已经安装过的软件包rpm包</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查询一个已经安装的软件包都安装到那个位置了：rpm -ql 软件名称</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查询所有安装过的rpm软件包 rpm -qa</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查询一个已经安装软件的软件包的信息 rpm -qi 软件名称</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查询一个已经安装软件的配置文件信息 rpm -qc 软件名称</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查询一个已经安装软件所依赖的软件包及文件 rpm -qR 软件名称</P>
<p>&nbsp;<wbr> b.对于未安装的rpm包的查询：</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查看一个软件包的作用，版本等 rpm -qpi rpm全名，如果麻烦，建议选中后，rpm名就出来了.</P>
<p>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
查看一个软件包包含的文件 rpm -qpl rpm全名</P>
<p>2.yum安装方法：</P>
<p>&nbsp;<wbr> yum 就是 yellow dog
updater,就是添加，删除，&nbsp;<wbr>更新rpm包，自动解决包的依赖性问题。&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr></P>
<p>&nbsp;<wbr>可以使用 yum-downloadonly
插件，字面意思就是只从yum仓库中下载而不安装rpm包。</P>
<p>看下 /etc/yum/pluginconf.d/目录下是否有downloadonly.conf没有的话，就需要 yum -y
install yum-download 先安装插件。</P>
<p>&nbsp;<wbr>在安装的过程中,如果存在yum进程，无法安装的话，就需要先杀死yum进程，方法很多,kill
pid,或者进程文件存放在/var/run下，会发现一个yum.pid文件，删除就可以了,rm -f yum.hpid</P>
<p>&nbsp;<wbr>安装成功后，如果我要安装webmin这个图形化的管理rpm包呢？</P>
<p>&nbsp;<wbr>yum install --downloadonly webmin</P>
<p>默认的，包会被报存在/var/cache/yum/updates/packages/目录中。<br />
如果指定yum的参数--downloaddir和--downloadonly一并使用，则可以指定另外</P>
<p>的目录来存放下载的包。像我这样yum install --downloadonly
--downloaddir=/home/fuwei3006 webmin就可以自己指定下载的目录</P>
<p>我装的这个系统就没有webmin的源泉，这中情况要想下载安装webmin等，需要手动建立一个文件</P>
<p>比如我下载的webmin 那么</P>
<p>vi /etc/yum.repos.d/webmin.repo 内容是</P>
<p>&nbsp;<wbr>[Webmin]</P>
<p>name=Webmin Distribution Neutral<br />
baseurl=http://download.webmin.com/download/yum<br />
enabled=1</P>
<p>还需要导入这个webmin的key,否则不会安装</P>
<p>rpm --import <a HREF="http://www.webmin.com/jcameron-key.asc">http://www.webmin.com/jcameron-key.asc</A>
不运行这个asc key 是不会安装的，老提示</P>
<p>然后就可以用 yum install webmin了， 和webmin比，好像听群里的人说
kloxo更家强大，以后在练习吧。</P>
<p>yum用法:</P>
<p>检查可以更新的软件包<br />
yum check-update<br />
更新所有的软件包<br />
yum update</P>
<p>rpm包的安装</P>
<p>yum install 软件名称</P>
<p>rpm包的删除</P>
<p>yum remove 软件名称</P>
<p>清除缓存中rpm包文件<br />
&nbsp;<wbr>yum clean packages<br />
清除缓存中rpm的头文件<br />
yum clean&nbsp;<wbr> headers<br />
清除缓存中旧的头文件<br />
yum clean old headers<br />
清除缓存中旧的rpm头文件和包文件</P>
<p>yum clean all<br />
还要说下软件包信息的查询：</P>
<p>列出资源库中所有可以安装或更新的rpm包 yum list</P>
<p>列出资源库中特定的可</P>
<p>以安装或更新以及已经安装的rpm包 yum list&nbsp;<wbr>webmin</P>
<p>列出资源库中所有可以更新的rpm包 yum list updates</P>
<p>列出已经安装的所有的rpm包 yum list installed</P>
<p>列出已经安装的</P>
<p>但是不包含在资源库中的rpm包 yum list extras 通过如网站下载安装的rpm包</P>
<p>rpm包信息显示(info参数同list)，列出资源库中所有可以安装或更新的rpm包的信息 yum inf</P>
<p>列出资源库中特定的可以安装或更新以及已经安装的rpm包的信息 yum info webmin</P>
<p>列出资源库中所有可以更新的rpm包的信息yum info updates</P>
<p>如果要结束webmin进程，可以查看进程号： netstat -nap | grep 10000 看是否占用了</P>
<p>然后 kill 进程号</P>
<p>重新启动 webmin服务&nbsp;<wbr> service webmin start
是否安安装了webmin使用 rpm -q webmin查看</P>
<p>====今天的操作用到了查找命令。使用了 locate命令：</P>
<p>&nbsp;<wbr>
工作原理:通过生成文件名相关的数据文件（一般会存放在/var/lib/mlocate/mlocate.db），当然会导致刚刚安装的软件找不到，这时候大家需要使用（updatedb）来更新locate数据文件。远离是先保存到mlocate.db数据库内，然后在查找.注意更新locate数据库</P>
<p>=webmin的深入学习，等以后了。东西太多了.</P>
<p>今天的学习结束了.明天回老家,大连-东港.</P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
<p>&nbsp;<wbr></P>
