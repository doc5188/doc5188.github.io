---
layout: post
title: "CentOS 6.3下PostgreSQL 的安装与配置"
categories: linux
tags: [postgresql]
date: 2014-10-15 16:18:50
---

<span style="color: rgb(128, 0, 0); font-family: verdana,geneva;">一、简介</span></strong></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">PostgreSQL 是一种非常复杂的对象-关系型数据库管理系统（ORDBMS），也是目前功能最强大，特性最丰富和最复杂的自由软件数据库系统。有些特性甚至连商业数据库都不具备。这个起源于伯克利（BSD）的数据库研究计划目前已经衍生成一项国际开发项目，并且有非常广泛的用户。</span></p>
<p><span style="font-size: 16px;"><strong><span style="color: rgb(128, 0, 0); font-family: verdana,geneva;">二、系统环境</span></strong></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><strong>系统平台：</strong>CentOS release 6.3 (Final)</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><strong>PostgreSQL 版本：</strong>PostgreSQL 9.2.4</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">防火墙已关闭/iptables: Firewall is not running.</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">SELINUX=disabled</span></p>
<p><span style="font-size: 16px;"><strong><span style="color: rgb(128, 0, 0); font-family: verdana,geneva;">三、安装方式</span></strong></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">A. RPM包安装</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">B. yum 安装</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">C. 源码包安装</span></p>
<p><span style="font-size: 16px;"><strong><span style="color: rgb(128, 0, 0); font-family: verdana,geneva;">四、安装过程</span></strong></span></p>
<p><strong><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">A. RPM包安装</span></strong></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">1. 检查PostgreSQL 是否已经安装</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -qa|grep postgres<br></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">若已经安装，则使用rpm -e 命令卸载。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">2. 下载RPM包</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">#wget http://yum.postgresql.org/9.2/redhat/rhel-6-i386/postgresql92-server-9.2.4-1PGDG.rhel6.i686.rpm
</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">#wget http://yum.postgresql.org/9.2/redhat/rhel-6-i386/postgresql92-contrib-9.2.4-1PGDG.rhel6.i686.rpm
</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">#wget http://yum.postgresql.org/9.2/redhat/rhel-6-i386/postgresql92-libs-9.2.4-1PGDG.rhel6.i686.rpm
</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">#wget http://yum.postgresql.org/9.2/redhat/rhel-6-i386/postgresql92-9.2.4-1PGDG.rhel6.i686.rpm</span></p>
<p><span style="line-height: 1.5; color: rgb(0, 0, 0); font-family: verdana,geneva;">3. 安装PostgreSQL，注意安装顺序</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -ivh postgresql92-libs-9.2.4-1PGDG.rhel6.i686.rpm </span><br><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -ivh postgresql92-9.2.4-1PGDG.rhel6.i686.rpm</span><br><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -ivh postgresql92-server-9.2.4-1PGDG.rhel6.i686.rpm&nbsp;</span><br><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -ivh postgresql92-contrib-9.2.4-1PGDG.rhel6.i686.rpm</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">4. 初始化PostgreSQL 数据库</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">PostgreSQL 服务初次启动的时候会提示初始化。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28145447-729ee8cef9b04c5a8d2681acd2e167c0.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">初始化数据库</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># service postgresql-<span style="font-weight: bold;">9.2</span> initdb</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28145804-780bf3a8fd6e4f1797ec6ef2bd78f13a.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">5. 启动服务</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># service postgresql-<span style="font-weight: bold;">9.2</span> start</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28145954-85d72b453ff24392adeda6f9780f932f.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">6. 把PostgreSQL 服务加入到启动列表</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># chkconfig postgresql-<span style="font-weight: bold;">9.2</span> on
</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># chkconfig --list|grep postgres</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28150245-32e737e65150441fa2ae41b9adacb5ff.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">7.&nbsp;修改PostgreSQL 数据库用户postgres的密码(注意不是linux系统帐号)</span></p>
<p><span style="line-height: 1.5; color: rgb(0, 0, 0); font-family: verdana,geneva;">PostgreSQL 数据库默认会创建一个postgres的数据库用户作为数据库的管理员，默认密码为空，我们需要修改为指定的密码，这里设定为’postgres’。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># su - postgres
</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">$ psql
</span></p>
<div class="cnblogs_code">
<pre># <span style="color: rgb(0, 0, 255);">ALTER</span> <span style="color: rgb(255, 0, 255);">USER</span> postgres <span style="color: rgb(0, 0, 255);">WITH</span> PASSWORD <span style="color: rgb(255, 0, 0);">'</span><span style="color: rgb(255, 0, 0);">postgres</span><span style="color: rgb(255, 0, 0);">'</span><span style="color: rgb(0, 0, 0);">;
# </span><span style="color: rgb(0, 0, 255);">select</span> <span style="color: rgb(128, 128, 128);">*</span> <span style="color: rgb(0, 0, 255);">from</span> pg_shadow ;</pre>
</div>
<p><img style="line-height: 1.5;" src="/upload/images/28153017-72ca9da38cb3401485e288e4d0b85f94.jpg" alt=""></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">8. 测试数据库</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">8.1 创建测试数据库</span></p>
<div class="cnblogs_code">
<pre># <span style="color: rgb(0, 0, 255);">create</span> <span style="color: rgb(0, 0, 255);">database</span> david;</pre>
</div>
<p><img style="font-family: verdana,geneva; line-height: 1.5;" src="/upload/images/28164359-83b6c400931d49eb8585e9f9fe8a0535.jpg" alt=""></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">8.2 切换到david 数据库</span></p>
<div class="cnblogs_code">
<pre># \c david</pre>
</div>
<p><img style="font-family: verdana,geneva; line-height: 1.5;" src="/upload/images/28164553-ba4ff1dcb0654db1a27f32fab28658a2.jpg" alt=""></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">8.3 创建测试表</span></p>
<div class="cnblogs_code">
<pre>david<span style="color: rgb(128, 128, 128);">=</span># <span style="color: rgb(0, 0, 255);">create</span> <span style="color: rgb(0, 0, 255);">table</span> test (id <span style="color: rgb(0, 0, 255);">integer</span>, name <span style="color: rgb(0, 0, 255);">text</span>);</pre>
</div>
<p><img style="line-height: 1.5;" src="/upload/images/28164856-c44167b494dd4ff58579a9ba411ca67d.jpg" alt=""></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">8.4 插入测试数据</span></p>
<div class="cnblogs_code">
<pre>david<span style="color: rgb(128, 128, 128);">=</span># <span style="color: rgb(0, 0, 255);">insert</span> <span style="color: rgb(0, 0, 255);">into</span> test <span style="color: rgb(0, 0, 255);">values</span> (<span style="color: rgb(128, 0, 0); font-weight: bold;">1</span>,<span style="color: rgb(255, 0, 0);">'</span><span style="color: rgb(255, 0, 0);">david</span><span style="color: rgb(255, 0, 0);">'</span><span style="color: rgb(0, 0, 0);">);
</span><span style="color: rgb(0, 0, 255);">INSERT</span> <span style="color: rgb(128, 0, 0); font-weight: bold;">0</span> <span style="color: rgb(128, 0, 0); font-weight: bold;">1</span><span style="color: rgb(0, 0, 0);">
david</span><span style="color: rgb(128, 128, 128);">=</span># </pre>
</div>
<p><span style="font-family: verdana,geneva; line-height: 1.5;">8.5 选择数据</span></p>
<div class="cnblogs_code"><div class="cnblogs_code_toolbar"><span class="cnblogs_code_copy"><a href="javascript:void(0);" onclick="copyCnblogsCode(this)" title="复制代码"><img src="/upload/images/copycode.gif" alt="复制代码"></a></span></div>
<pre>david<span style="color: rgb(128, 128, 128);">=</span># <span style="color: rgb(0, 0, 255);">select</span> <span style="color: rgb(128, 128, 128);">*</span> <span style="color: rgb(0, 0, 255);">from</span><span style="color: rgb(0, 0, 0);"> test ;
 id </span><span style="color: rgb(128, 128, 128);">|</span><span style="color: rgb(0, 0, 0);"> name  
</span><span style="color: rgb(0, 128, 128);">--</span><span style="color: rgb(0, 128, 128);">--+-------</span>
  <span style="color: rgb(128, 0, 0); font-weight: bold;">1</span> <span style="color: rgb(128, 128, 128);">|</span><span style="color: rgb(0, 0, 0);"> david
(</span><span style="color: rgb(128, 0, 0); font-weight: bold;">1</span><span style="color: rgb(0, 0, 0);"> row)

david</span><span style="color: rgb(128, 128, 128);">=</span># </pre>
<div class="cnblogs_code_toolbar"><span class="cnblogs_code_copy"><a href="javascript:void(0);" onclick="copyCnblogsCode(this)" title="复制代码"><img src="/upload/images/copycode.gif" alt="复制代码"></a></span></div></div>
<p><span style="font-family: verdana,geneva; line-height: 1.5;">测试完成，RPM包安装成功。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">9.&nbsp;修改linux 系统用户postgres 的密码</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">PostgreSQL 数据库默认会创建一个linux 系统用户postgres，通过passwd 命令设置系统用户的密码为post123。</span></p>
<p><span># passwd postgres</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img style="line-height: 1.5;" src="/upload/images/28153600-1e89e193f894451ca5e4cb4bc8a9c651.jpg" alt=""></span></p>
<p><span style="line-height: 1.5; color: rgb(0, 0, 0); font-family: verdana,geneva;">10.&nbsp;修改PostgresSQL 数据库配置实现远程访问</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10.1 修改postgresql.conf 文件</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># vi /var/lib/pgsql/9.2/data/postgresql.conf</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28154751-0fcfa706681f41409895b3d3eed87c64.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">如果想让PostgreSQL 监听整个网络的话，将listen_addresses 前的#去掉，并将 listen_addresses = 'localhost' 改成 listen_addresses = '*'</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10.2 修改客户端认证配置文件pg_hba.conf<br></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">将需要远程访问数据库的IP地址或地址段加入该文件。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># vi /var/lib/pgsql/9.2/data/pg_hba.conf</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28155810-63ed9663c45c4c9fab26b1809111d6b5.jpg" alt=""></span></p>
<p><span style="line-height: 1.5; color: rgb(0, 0, 0); font-family: verdana,geneva;">11. 重启服务以使设置生效</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># service postgresql-9.2 restart</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28160228-5de45a3aa5cb49d8a3c11ef76bdb8a0d.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">12. 远程测试连接</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28162924-6c74b8726a7f409e8e5e549ca697e270.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28162938-1eb15be15b104ad8922f2a04496e5950.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">连接成功。</span></p>
<p><strong><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">B. yum 安装</span></strong></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">1. 将刚才安装的PostgreSQL 卸载</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">//停止PostgreSQL服务</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># /etc/init.d/postgresql-9.2 stop</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28172108-7aa893e33494470c80ee1edbbe71cb0f.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">//查看已安装的包</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -qa|grep postgres</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/28172116-7cbcdc7574664d87a8f4ac0a7ca4ee09.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">//卸载</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -e postgresql92-server-9.2.4-1PGDG.rhel6.i686</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -e postgresql92-contrib-9.2.4-1PGDG.rhel6.i686</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -e postgresql92-9.2.4-1PGDG.rhel6.i686</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -e postgresql92-libs-9.2.4-1PGDG.rhel6.i686</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30113356-5d2109031fb74d9d99b749e8c845ca6c.jpg" alt="">&nbsp;</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">2. yum 安装</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">如果是默认yum 安装的话，会安装较低版本的PostgreSQL 8.4，这不符合我们的要求。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30113726-34a75a30c3c44a94a9669105b7e9a777.jpg" alt="" width="900"></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">我们使用PostgreSQL Yum Repository 来安装最新版本的PostgreSQL。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">2.1 安装PostgreSQL yum repository</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># rpm -i http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-redhat92-9.2-7.noarch.rpm</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30115806-22b5be55ec49420cbbe9fb629021a518.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">2.2 安装新版本PostgreSQL</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># yum install postgresql92-server postgresql92-contrib</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30130504-fc69c73a927d40f0a6df4f12b85fb085.jpg" alt="" width="900"></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">2.3 查看安装</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30130629-4fff0ce352f04afb9224db0246da0a59.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">3. 初始化并启动数据库</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30131048-bcd36fe7627d4592abb8cac844b88a5e.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30131100-ca2862d2a5a54044a4c88dfff306c08d.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">4. 测试</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/30131148-41948ad79d0f45d7ad3b2a297b09aa5c.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">其他步骤如A方式。</span></p>
<p><strong><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">C.&nbsp;源码包安装</span></strong></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">1. 下载PostgreSQL 源码包</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># wget http://ftp.postgresql.org/pub/source/v9.2.4/postgresql-9.2.4.tar.bz2</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">2. 解压源码包</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># tar xjf postgresql-9.2.4.tar.bz2</span></p>
<p><span style="font-family: verdana,geneva; line-height: 1.5;">3. 进入解压后的目录</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># cd postgresql-9.2.4</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/27141017-81ae02a505ae42f49b5f53fbee80f325.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">4. 查看INSTALL 文件</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">INSTALL 文件中Short Version 部分解释了如何安装PostgreSQL 的命令，Requirements 部分描述了安装PostgreSQL 所依赖的lib，比较长，先configure 试一下，如果出现error，那么需要检查是否满足了Requirements 的要求。</span></p>
<p><img src="/upload/images/06103238-ad7922632f284f7b844cd9d92aaa574e.jpg" alt=""></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">5. 开始编译安装PostgreSQL 数据库。</span></p>
<p>[root@TS-DEV postgresql-9.2.4]# ./configure&nbsp;</p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/06103540-77b96db647514c91a58682939ebd68a2.jpg" alt=""></span></p>
<p>configure 成功，无错误。</p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">6. 执行gmake</span></p>
<p>[root@TS-DEV postgresql-9.2.4]# gmake</p>
<p><img src="/upload/images/06104246-36c39a32a39e4569ab6ac191ae3008ec.jpg" alt=""></p>
<p>gmake 成功，Ready to install.</p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">7. 执行gmake install</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">[root@TS-DEV postgresql-9.2.4]# gmake install</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/06104540-a653646b91a949759a2a58cc7417bece.jpg" alt=""></span></p>
<p>gmake install 成功，到这一步，PostgreSQL 源码编译安装完成，下面开始配置PostgreSQL.</p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">8. 设置环境变量</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># vi .bash_profile</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">把&nbsp;PATH=$PATH:$HOME/bin</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">改成&nbsp;PATH=$PATH:$HOME/bin:/usr/local/pgsql/bin</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">保存退出。</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">让环境变量生效：</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># source .bash_profile&nbsp;</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">9. 添加用户postgres</span></p>
<p># adduser postgres</p>
<p><img src="/upload/images/06105232-e8119dd36cb640df852856d8d1d0b2d9.jpg" alt=""></p>
<p>* 更改用户目录（可选操作）</p>
<p># vi /etc/passwd</p>
<p>把&nbsp;postgres:x:528:528::/home/postgres:/bin/bash</p>
<p>改成&nbsp;postgres:x:528:528::/usr/local/pgsql:/bin/bash</p>
<p>将.bash_profile 移动到新的用户目录并修改权限</p>
<p># cp /home/postgres/.bash_profile /usr/local/pgsql/</p>
<p># chown postgres.postgres .bash_profile</p>
<p>删除用户目录：</p>
<p>[root@TS-DEV home]# rm -rf postgres/</p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10. 初始化数据库</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10.1 新建数据目录</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># mkdir /usr/local/pgsql/data</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10.2 更改权限</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># chown postgres /usr/local/pgsql/data</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10.3 切换到postgres 用户</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"># su - postgres</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/06110948-7104d06287244905ba41e05c3607326f.jpg" alt=""></span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">10.4 init db</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;">$ /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data/</span></p>
<p><span style="color: rgb(0, 0, 0); font-family: verdana,geneva;"><img src="/upload/images/06111316-0bfcc10f263e4a60a69c17ac3ab57284.jpg" alt=""></span></p>
<p><span>到这里数据的初始化就完成了。</span></p>
<p><span>11. 系统服务</span></p>
<p><span>11.1 回到root 用户</span></p>
<p><span>$ exit</span></p>
<p><span>11.2&nbsp;<span>复制安装目录下的linux文件到/etc/init.d/</span></span></p>
<p><span><span><span>进入postgresql 的安装目录（即刚刚使用tar命令解压的目录）</span></span></span></p>
<p><span># cd postgresql-9.2.4</span></p>
<p><span># cp contrib/start-scripts/linux /etc/init.d/postgresql</span></p>
<p><img src="/upload/images/06112032-a22b1ce77bdc46ff8f8389e4c95f954a.jpg" alt="" width="900"></p>
<p>11.3 添加执行权限</p>
<p># chmod +x /etc/init.d/postgresql</p>
<p>11.4 启动数据库</p>
<p><img src="/upload/images/06112316-96f4b32eb56a4154a8a7ccc601cdaba9.jpg" alt=""></p>
<p>11.5 让数据库开机启动</p>
<p># chkconfig --add postgresql&nbsp;</p>
<p># chkconfig postgresql on</p>
<p><img src="/upload/images/06112508-d40079956dbe4d4e8699c614395a0dee.jpg" alt=""></p>
<p>11.6 创建<span>数据库操作的历史记录文件</span></p>
<p><img src="/upload/images/06112719-203ce88b87b649aaa0012c10d5b6118e.jpg" alt=""></p>
<p>12. 测试使用</p>
<p># su - postgres</p>
<p>$ createdb test</p>
<p>$ psql test</p>
<div class="cnblogs_code">
<pre>test<span style="color: rgb(128, 128, 128);">=</span># <span style="color: rgb(0, 0, 255);">create</span> <span style="color: rgb(0, 0, 255);">table</span> test(id <span style="color: rgb(0, 0, 255);">int</span>);</pre>
</div>
<p><img style="line-height: 1.5;" src="/upload/images/06123949-37c86fd2d6304122b0fa38f0d0e59d36.jpg" alt=""><span style="line-height: 1.5;">&nbsp;</span></p>
<p>源码编译安装成功。</p>
<p>&nbsp;</p>
<hr>
<p><span style="color: rgb(128, 0, 0);"><strong>David Camp</strong></span></p>
<ul>
<li>技术交流，请加QQ群：</li>
</ul>
<p>　　　　系统运维技术分享：<span>296513821</span></p>
<ul>
<li>业务合作，请联系作者QQ：562866602</li>
<li>我的微信号：mchina_tang</li>
<li>给我写信：mchina_tang@qq.com</li>
<li>我的地址：江苏·苏州</li>
</ul>
<p><span style="color: rgb(128, 0, 0);"><strong><strong><strong>我们永远相信，分享是一种美德 |&nbsp;</strong></strong>We Believe, Great People Share Knowledge...</strong>
