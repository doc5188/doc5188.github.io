---
layout: post
categories: linux
tags: [linux, dpkg, rpm]
date: 2014-09-10 15:48:11
title: "rpm 与 dpkg 用法比较"
---

<div class="blog_content" id="blog_content">
    <div style="font-size: 14px;" class="iteye-blog-content-contain">
<p><strong><span class="notranslate"><span class="text_h2">Linux界的两大主流: RPM与DPKG</span></span> </strong></p>
<p>&nbsp;</p>
<div class="block2">
<p><span class="notranslate">由于自由软体的蓬勃发展，加上大型Unix-Like 主机的强大效能，让很多软体开发者将他们的软体使用Tarball 来释出。</span> <span class="notranslate">后来Linux 发展起来后，由一些企业或社群将这些软体收集起来制作成为distributions 以发布这好用的Linux 作业系统。</span> <span class="notranslate">但后来发现到，这些distribution 的软体管理实在伤脑筋， 如果软体有漏洞时，又该如何修补呢？</span> <span class="notranslate">使用tarball 的方式来管理吗？</span> <span class="notranslate">又常常不晓得到底我们安装过了哪些程式？</span> <span class="notranslate">因此，一些社群与企业就开始思考Linux 的软体管理方式。</span></p>
<p>&nbsp;</p>
<p><span class="notranslate">如同刚刚谈过的方式，Linux 开发商先在固定的硬体平台与作业系统平台上面将需要安装或升级的软体编译好， 然后将这个软体的所有相关档案打包成为一个特殊格式的档案，在这个软体档案内还包含了预先侦测系统与相依软体的脚本， 并提供记载该软体提供的所有档案资讯等。</span> <span class="notranslate">最终将这个软体档案释出。</span> <span class="notranslate"> <span class="text_import2">用户端取得这个档案后，只要透过特定的指令来安装，那么该软体档案就会依照内部的脚本来侦测相依的前驱软体是否存在，若安装的环境符合需求，那就会开始安装</span> ，安装完成后还会将该软体的资讯写入软体管理机制中，以达成未来可以进行升级、移除等动作呢。</span></p>
<p>&nbsp;</p>
<p><span class="notranslate">目前在Linux 界软体安装方式最常见的有两种，分别是：</span></p>
<ul>
<li>
<span class="notranslate"> <span class="text_import1">dpkg</span> ：</span> <br><span class="notranslate">这个机制最早是由Debian Linux 社群所开发出来的，透过dpkg 的机制， Debian 提供的软体就能够简单的安装起来，同时还能提供安装后的软体资讯，实在非常不错。</span> <span class="notranslate">只要是衍生于Debian 的其他Linux distributions 大多使用dpkg 这个机制来管理软体的， 包括B2D, Ubuntu 等等。</span> <br><br>
</li>
<li>
<span class="notranslate"> <span class="text_import1">RPM</span> ：</span> <br><span class="notranslate">这个机制最早是由Red Hat 这家公司开发出来的，后来实在很好用，因此很多distributions 就使用这个机制来作为软体安装的管理方式。</span> <span class="notranslate">包括Fedora, CentOS, SuSE 等等知名的开发商都是用这咚咚。</span>
</li>
</ul>
<p><span class="notranslate">如前所述，不论dpkg/rpm 这些机制或多或少都会有软体属性相依的问题，那该如何解决呢？</span> <span class="notranslate">其实前面不是谈到过每个软体档案都有提供相依属性的检查吗？</span> <span class="notranslate">那 么如果我们将相依属性的资料做成列表， 等到实际软体安装时，若发生有相依属性的软体状况时，例&#8203;&#8203;如安装A 需要先安装B 与C ，而安装B 则需要安装D 与E 时，那么当妳要安装A ，透过相依属性列表，管理机制自动去取得B, C, D, E 来同时安装， 不就解决了属性相依的问题吗？</span></p>
<p>&nbsp;</p>
<p><span class="notranslate">没错！</span> <span class="notranslate">您真聪明！</span> <span class="notranslate">目前新的Linux 开发商都有提供这样的『线上升级』机制，透过这个机制， 原版光碟就只有第一次安装时需要用到而已，其他时候只要有网路，妳就能够取得原本开发商所提供的任何软体了呢！</span> <span class="notranslate">在dpkg 管理机制上就开发出APT 的线上升级机制，RPM 则依开发商的不同，有Red Hat 系统的yum ， SuSE 系统的Yast Online Update (YOU)， Mandriva 的urpmi 软体等。</span></p>
<table cellspacing="0" cellpadding="3" border="1" style="width: 95%;">
<tbody><tr>
<td><span class="notranslate"> distribution 代表</span></td>
<td><span class="notranslate">软体管理机制</span></td>
<td><span class="notranslate">使用指令</span></td>
<td><span class="notranslate">线上升级机制(指令)</span></td>
</tr>
<tr>
<td><span class="notranslate"> Red Hat/Fedora</span></td>
<td><span class="notranslate"> RPM</span></td>
<td><span class="notranslate"> rpm, rpmbuild</span></td>
<td><span class="notranslate"> YUM (yum)</span></td>
</tr>
<tr>
<td><span class="notranslate"> Debian/Ubuntu</span></td>
<td><span class="notranslate"> DPKG</span></td>
<td><span class="notranslate"> dpkg</span></td>
<td><span class="notranslate"> APT (apt-get)</span></td>
</tr>
</tbody></table>
<p><span class="notranslate">我们这里使用的是CentOS 系统嘛！</span> <span class="notranslate">所以说： <span class="text_import2">使用的软体管理机制为RPM机制，而用来作为线上升级的方式则为yum</span> ！</span> <span class="notranslate">底下就让我们来谈谈RPM 与YUM 的相关说明吧！</span></p>
</div>
<p>&nbsp;</p>
<p><span style="font-size: 14px;" class="notranslate"><strong>RPM与DPKG</strong></span></p>
<p><span class="notranslate">目前市面上大部分的Linux distro都是根基于Red Hat及Debian这两大厂牌的改装（SuSE是一个异类）&#8203;&#8203;。</span> <span class="notranslate">因此在套件管理上，Red Hat的RPM与Debian的DPKG就成为Linux套件管理上的两大标准。</span></p>
<p>&nbsp;</p>
<p><span class="notranslate">这边也不讨论类Unix作业系统在套件管理（软体的安装，移除，查询）上所持的哲学与一般人常用的MS Windows系列有很大的不同而衍生出的困难了，直接就这两个套件管理工具列出比较以利查询。</span></p>
<p>&nbsp;<a name="more"></a></p>
<div class="main">
<p><span class="notranslate">以下整理列表来自<a href="http://cha.homeip.net/blog/archives/2005/08/rpm_vs_dpkg.html">Jamyy's Weblog</a> ：</span></p>
<p>&nbsp;</p>
<p><span class="notranslate"> <span style="color: #0000ff;">安装</span></span></p>
<blockquote>
<table cellspacing="0" cellpadding="3" border="1" style="border-collapse: collapse;">
<tbody><tr>
<td><span class="notranslate">目的</span></td>
<td><span class="notranslate"> rpm 用法</span></td>
<td><span class="notranslate"> dpkg 用法</span></td>
</tr>
<tr>
<td><span class="notranslate">安装指定套件</span></td>
<td><span class="notranslate"> rpm -i <span style="color: #333333;">pkgfile.rpm</span></span></td>
<td><span class="notranslate"> dpkg -i <span style="color: #333333;">pkgfile.deb</span></span></td>
</tr>
</tbody></table>
</blockquote>
<p><span class="notranslate"> <span style="color: #0000ff;">查询</span></span></p>
<blockquote>
<table cellspacing="0" cellpadding="3" border="1" style="border-collapse: collapse;">
<tbody><tr>
<td><span class="notranslate">目的</span></td>
<td><span class="notranslate"> rpm 用法</span></td>
<td><span class="notranslate"> dpkg 用法</span></td>
</tr>
<tr>
<td><span class="notranslate">显示所有已安装的套件名称</span></td>
<td><span class="notranslate"> rpm -qa</span></td>
<td><span class="notranslate"> dpkg -l (小写L)</span></td>
</tr>
<tr>
<td><span class="notranslate">显示套件包含的所有档案</span></td>
<td><span class="notranslate"> rpm -ql <span style="color: #333333;">softwarename</span> (小写L)</span></td>
<td><span class="notranslate"> dpkg -L <span style="color: #333333;">softwarename</span></span></td>
</tr>
<tr>
<td><span class="notranslate">显示特定档案所属套件名称</span></td>
<td><span class="notranslate"> rpm -qf <span style="color: #333333;">/path/to/file</span></span></td>
<td><span class="notranslate"> dpkg -S <span style="color: #333333;">/path/to/file</span></span></td>
</tr>
<tr>
<td><span class="notranslate">查询套件档案资讯</span></td>
<td>
<span class="notranslate"> rpm -qip <span style="color: #333333;">pkgfile.rpm</span> (显示套件资讯)</span> <span style="color: #333333;"><br></span> <span class="notranslate"> rpm -qlp <span style="color: #333333;">pkgfile.rpm</span> (小写L,显示套件内所有档案)</span>
</td>
<td>
<span class="notranslate"> dpkg -I <span style="color: #333333;">pkgfile.deb</span> (大写I )</span> <span style="color: #333333;"><br></span> <span class="notranslate"> dpkg -c <span style="color: #333333;">pkgfile.deb</span></span>
</td>
</tr>
<tr>
<td><span class="notranslate">显示指定套件是否安装</span></td>
<td>
<span class="notranslate"> rpm -q <span style="color: #333333;">softwarename</span> (只显示套件名称)</span> <br><span class="notranslate"> rpm -qi <span style="color: #333333;">softwarename</span> (显示套件资讯)</span>
</td>
<td>
<span class="notranslate"> dpkg -l <span style="color: #333333;">softwarename</span> (小写L,只列出简洁资讯)</span> <br><span class="notranslate"> dpkg -s <span style="color: #333333;">softwarename</span> (显示详细资讯)</span> <br><span class="notranslate"> dpkg -p <span style="color: #333333;">softwarename</span> (显示详细资讯)</span>
</td>
</tr>
</tbody></table>
</blockquote>
<p><span class="notranslate"> <span style="color: #0000ff;">移除</span></span></p>
<blockquote>
<table cellspacing="0" cellpadding="3" border="1" style="border-collapse: collapse;">
<tbody><tr>
<td><span class="notranslate">目的</span></td>
<td><span class="notranslate"> rpm 用法</span></td>
<td><span class="notranslate"> dpkg 用法</span></td>
</tr>
<tr>
<td><span class="notranslate">移除指定套件</span></td>
<td><span class="notranslate"> rpm -e <span style="color: #333333;">softwarename</span></span></td>
<td>
<span class="notranslate"> dpkg -r <span style="color: #333333;">softwarename</span> (会留下套件设定档)</span> <br><span class="notranslate"> dpkg -P <span style="color: #333333;">softwarename</span> (完全移除)</span>
</td>
</tr>
</tbody></table>
</blockquote>
<p><span class="notranslate"> <span style="color: #0000ff;">在Debian使用alien处理RPM套件</span></span></p>
<blockquote>
<p><span class="notranslate"> alien 可处理.deb、.rpm、.slp、.tgz 等档案格式, 进行转档或安装.</span> <br><span class="notranslate">于Debian安装非Debian套件时,可使用<span style="color: #000000;"><strong>alien</strong></span>进行安装.</span> <br><span class="notranslate">安装alien套件: <span style="color: #0000ff;">apt-get install alien</span></span></p>
</blockquote>
<ul>
<li><span class="notranslate">在Debian安装RPM套件: <span style="color: #0000ff;">alien -i quota-3.12-7.i386.rpm</span></span></li>
<li><span class="notranslate">制作成deb的套件格式: <span style="color: #0000ff;">alien -d quota-3.12-7.i386.rpm</span></span></li>
<li><span class="notranslate">制作成rpm的套件格式: <span style="color: #0000ff;">alien -r quota_3.12-6_i386.deb</span></span></li>
</ul>
<p>&nbsp; </p>
<p><span style="font-size: 14px;" class="notranslate"><strong>APT与YUM</strong></span></p>
<p><span class="notranslate">虽然RPM与DPKG有效的解决的软体的安装，移除与查询的需求，但是在Linux上的套件管理还有一个很大的问题必须解决，就是各软体间的相依性(dependency)。</span> <span class="notranslate"> RPM与DPKG只能做到检查相依性，在安装或移除时告知相依性的不满足，皆下来就需要使用者自行去找出所需的套件来安装。</span> <span class="notranslate">这样的确是有点不方便，因此产生了前端工具软体- APT及YUM。</span></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p><strong><span class="notranslate">APT</span> </strong></p>
<blockquote>
<p><span class="notranslate"> Debian开发，目前也有porting到其他版本，要在Red Hat系的Fedora或CentOS使用也是可以的。</span></p>
<p><span class="notranslate">使用方法：</span></p>
<ul>
<li>
<span class="notranslate">编辑<strong>/etc/apt/sources.list</strong> ，设定所选用的版本，如stable，testing，unstable及套件来源站台或装置。</span> <span class="notranslate">档案详细设定请参考： <a href="http://docs.huihoo.com/gnu_linux/debian/tutorial/Debian-Install-Guide-5.html">了解Debian系统的哲学</a></span>
</li>
<li><span class="notranslate">基本指令：</span></li>
</ul>
<table border="1" style="width: 600px;">
<tbody><tr>
<td width="328"><span class="notranslate"> apt-setup</span></td>
<td width="306"><span class="notranslate">设定/etc/apt/souces.list</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-get update</span></td>
<td><span class="notranslate">软体资料库同步</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-get install <span style="color: #333333;">softwarename1 [softwarename2.....]</span></span></td>
<td><span class="notranslate">安装软体</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-get remove <span style="color: #333333;">softwarename</span> 1 [ <span style="color: #333333;">softwarename</span> 2...]</span></td>
<td><span class="notranslate">移除软体(保留设定档）</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-get --purge remove <span style="color: #333333;">softwarename</span> 1 [ <span style="color: #333333;">softwarename</span> 2...]</span></td>
<td><span class="notranslate">移除软体(不保留设定档）</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-cache search <span style="color: #333333;">softwarename</span></span></td>
<td><span class="notranslate">列出所有sofrwarename的套件</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-upgrade <span style="color: #333333;">[softwarename</span> 1 <span style="color: #333333;">softwarename</span> 2...]</span></td>
<td><span class="notranslate">更新套件，不指定套件名则更新所有可更新的套件</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-get clean(autoclean)</span></td>
<td><span class="notranslate">删除系统暂存的deb(autoclean只会将比目前系统旧版的套件删除)</span></td>
</tr>
<tr>
<td><span class="notranslate"> apt-get dist-upgrade</span></td>
<td><span class="notranslate">转换系统的版本（需在/etc/apt/sources.list指定stable，testing或unstable）</span></td>
</tr>
</tbody></table>
</blockquote>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p><strong><span class="notranslate">YUM</span> </strong></p>
<blockquote>
<p><span class="notranslate"> YUM（Yellow dog Updater, Modified ）是Yellow Dog Linux开发的。</span> <span class="notranslate"> Yellow Dog Linux原本是一套完全源于Red Hat但运作于先前使用IBM PPC平台的MAC机器，原本以为这个版本已经消失，没想到最新消息是他们推出了在Sony PS3上面运作的版本。</span> <span class="notranslate"> CentOS及Fedora的基本预设安装中即将YUM列入其内。</span> <span class="notranslate">如果没记错，要在Debian上使用YUM也是可以的。</span></p>
<p><span class="notranslate">使用方法：</span></p>
<ul>
<li><span class="notranslate">编辑/etc/yum.conf档案详细设定请参考： <a href="http://linux.vbird.org/linux_server/0450apt.php">简易APT/YUM伺服器设定</a>注1</span></li>
<li><span class="notranslate">基本指令： （如果yum在工作过程中需要使用者回应，可加上<strong>-y</strong>参数直接回答yes ）</span></li>
</ul>
<table border="1" style="width: 600px;">
<tbody><tr>
<td width="306"><span class="notranslate"> yum install <span style="color: #333333;">softwarename1 [softwarename2.....]</span></span></td>
<td width="328"><span class="notranslate">安装套件</span></td>
</tr>
<tr>
<td><span class="notranslate"> yum update <span style="color: #333333;">[softwarename</span> 1 <span style="color: #333333;">softwarename</span> 2...]</span></td>
<td><span class="notranslate">更新套件，不指定套件名则更新所有可更新的套件</span></td>
</tr>
<tr>
<td><span class="notranslate"> yum list</span></td>
<td><span class="notranslate">列出目前在yum server 上面有的套件</span></td>
</tr>
<tr>
<td><span class="notranslate"> yum info</span></td>
<td><span class="notranslate">类似rpm -qi</span></td>
</tr>
<tr>
<td><span class="notranslate"> yum clean</span></td>
<td><span class="notranslate">移除下载到本机的packages 或headers</span></td>
</tr>
<tr>
<td><span class="notranslate"> yum remove <span style="color: #333333;">softwarename1 [softwarename2.....]</span></span></td>
<td><span class="notranslate">移除已经安装的套件</span></td>
</tr>
</tbody></table>
</blockquote>
<p><span class="notranslate">注1：Red Hat近年来致力于将一个设定档切割成很多小设定档。</span> <span class="notranslate">以yum.conf为例，Red Hat将其分割成xxx.repo档放置在/etc/yum.repos.d这个目录下。</span> <span class="notranslate">并在yum.conf档里增加一行注解： PUT YOUR REPOS HERE OR IN separate files named file.repo in /etc/yum.repos.d。</span> <span class="notranslate">个人可视喜好决定。</span></p>
<p>&nbsp;</p>
<p><span class="notranslate">参考文件：</span></p>
<ol>
<li><span class="notranslate">鸟哥的Linux与ADSL私房菜： <a href="http://linux.vbird.org/linux_server/0450apt.php">简易APT/YUM伺服器设定</a></span></li>
<li><span class="notranslate"> Debian无痛起步法： <a href="http://docs.huihoo.com/gnu_linux/debian/tutorial/Debian-Install-Guide-5.html">了解Debian系统的哲学</a></span></li>
<li><span class="notranslate"> Jamyy's Weblog： <a href="http://cha.homeip.net/blog/archives/2005/08/rpm_vs_dpkg.html">rpm vs. dpkg常用参数对照</a></span></li>
</ol>
<p><span class="notranslate">来源： http://blog.roodo.com/schonrosemary/archives/4362693.html</span></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
</div>
</div>
  </div>
