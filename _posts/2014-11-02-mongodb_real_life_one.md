---
layout: post
title: "MongoDB实战系列之一：MongoDB安装部署"
categories: 数据库
tags: [mongodb实战系列, mongodb安装部署]
date: 2014-11-02 21:31:58
---

<p>简述：MongoDB是一个基于分布式文件存储的数据库。由C++语言编写。旨在为WEB应用提供可扩展的高性能数据存储解决方案。</p>
<p>环境：CentOS 5.5 x64</p>
<p>安装：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw3">cd</span> <span class="sy0">/</span>root<span class="sy0">/</span>tools<br>
<span class="kw2">wget</span> http:<span class="sy0">//</span>fastdl.mongodb.org<span class="sy0">/</span>linux<span class="sy0">/</span>mongodb-linux-x86_64-2.0.0.tgz<br>
<span class="kw2">tar</span> zxvf mongodb-linux-x86_64-2.0.0.tgz<br>
<span class="kw2">mv</span> mongodb-linux-x86_64-2.0.0 <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb-linux-x86_64-2.0.0<br>
<span class="kw2">ln</span> <span class="re5">-s</span> <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb-linux-x86_64-2.0.0 <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<br>
<span class="kw2">ln</span> <span class="re5">-s</span> <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/*</span> &nbsp;<span class="sy0">/</span>bin<span class="sy0">/</span></div></div>
<p>#添加用户组</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>usr<span class="sy0">/</span>sbin<span class="sy0">/</span>groupadd <span class="re5">-g</span> <span class="nu0">690</span> mongodb<br>
<span class="sy0">/</span>usr<span class="sy0">/</span>sbin<span class="sy0">/</span>useradd <span class="re5">-g</span> mongodb mongodb <span class="re5">-u</span> <span class="nu0">690</span> <span class="re5">-s</span> <span class="sy0">/</span>sbin<span class="sy0">/</span>nologin</div></div>
<p>#创建存储目录</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span><br>
<span class="kw2">chown</span> <span class="re5">-R</span> mongodb.mongodb <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span></div></div>
<p>#启动运行</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">nohup</span> mongod <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db <span class="sy0">&amp;</span></div></div>
<p><span id="more-602"></span>#开机自启动</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw3">echo</span> <span class="st0">"mongod --dbpath /elain/data/db"</span> <span class="sy0">&gt;&gt;/</span>etc<span class="sy0">/</span>rc.local</div></div>
<p>#以服务方式启动<span class="wp_keywordlink_affiliate"><a href="http://www.elain.org/?tag=mongodb" title="查看 mongodb 中的全部文章" target="_blank">mongodb</a></span>，要求验证</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27001</span> <span class="re5">--auth</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>#注：参数中用到的目录需创建</p>
<p>#停止</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">kill</span> <span class="re5">-2</span> <span class="sy0">`</span><span class="kw2">ps</span> <span class="re5">-ef</span><span class="sy0">|</span><span class="kw2">grep</span> mongod<span class="sy0">|</span><span class="kw2">grep</span> <span class="re5">-v</span> <span class="kw2">grep</span><span class="sy0">|</span><span class="kw2">awk</span> <span class="st_h">''</span><span class="br0">{</span>print <span class="re4">$2</span><span class="br0">}</span><span class="st_h">''</span><span class="sy0">`</span></div></div>
<p>#验证启动</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="br0">[</span>root<span class="sy0">@</span>md01 ~<span class="br0">]</span><span class="co0"># netstat -ln</span><br>
Active Internet connections <span class="br0">(</span>only servers<span class="br0">)</span><br>
Proto Recv-Q Send-Q Local Address &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Foreign Address &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; State<br>
tcp &nbsp; &nbsp; &nbsp; &nbsp;<span class="nu0">0</span> &nbsp; &nbsp; &nbsp;<span class="nu0">0</span> 0.0.0.0:<span class="nu0">28001</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 0.0.0.0:<span class="sy0">*</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; LISTEN<br>
tcp &nbsp; &nbsp; &nbsp; &nbsp;<span class="nu0">0</span> &nbsp; &nbsp; &nbsp;<span class="nu0">0</span> 0.0.0.0:<span class="nu0">27001</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 0.0.0.0:<span class="sy0">*</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; LISTEN</div></div>
<p>还可以通过访问：http://ip:28001/  浏览</p>
<p>#登录：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongo <span class="re5">--host</span> serverip:<span class="nu0">27001</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="br0">[</span>root<span class="sy0">@</span>md01 ~<span class="br0">]</span><span class="co0"># mongo --host localhost:27001</span><br>
MongoDB shell version: 2.0.0<br>
connecting to: localhost:<span class="nu0">27001</span><span class="sy0">/</span><span class="kw3">test</span><br>
<span class="sy0">&gt;</span></div></div>
<p>#测试</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="br0">[</span>root<span class="sy0">@</span>md02 mongodb<span class="br0">]</span><span class="co0"># mongo</span><br>
MongoDB shell version: 1.8.3<br>
connecting to: <span class="kw3">test</span><br>
Thu Sep &nbsp;<span class="nu0">8</span> <span class="nu0">22</span>:<span class="nu0">16</span>:<span class="nu0">13</span> <span class="br0">[</span>initandlisten<span class="br0">]</span> connection accepted from 127.0.0.1:<span class="nu0">43643</span> <span class="co0">#2</span><br>
<span class="sy0">&gt;</span>db.foo.save<span class="br0">(</span> <span class="br0">{</span> a : <span class="nu0">1</span> <span class="br0">}</span> <span class="br0">)</span><br>
<span class="sy0">&gt;</span>db.foo.find<span class="br0">(</span><span class="br0">)</span><br>
<span class="br0">{</span> <span class="st0">"_id"</span> : ObjectId<span class="br0">(</span><span class="st0">"4e68ce01f4be44b5812e7f9a"</span><span class="br0">)</span>, <span class="st0">"a"</span> : <span class="nu0">1</span> <span class="br0">}</span></div></div>
<p>附录一：<br>
<span class="wp_keywordlink_affiliate"><a href="http://www.elain.org/?tag=mongodb" title="查看 mongodb 中的全部文章" target="_blank">mongodb</a></span>的bin下各工具的用途：</p>
<p>mongod：数据库服务端，类似mysqld，每个实例启动一个进程，可以fork为Daemon运行<br>
mongo：客户端命令行工具，类似sqlplus/mysql，其实也是一个js解释器，支持js语法<br>
mongodump/mongorestore：将数据导入为bson格式的文件/将bson文件恢复为数据库，类似xtracbackup<br>
mongoexport/mongoimport：将collection导出为json/csv格式数据/将数据导入数据库，类似mysqldump/mysqlimport<br>
bsondump：将bson格式的文件转储为json格式的数据<br>
mongos：分片路由，如果使用了sharding功能，则应用程序连接的是mongos而不是mongod<br>
mongofiles：GridFS管理工具<br>
mongostat：实时监控工具</p>
<p>附录二：<br>
mongod的主要参数有：</p>
<p>dbpath: 数据文件存放路径，每个数据库会在其中创建一个子目录。<br>
logpath：错误日志文件<br>
logappend： 错误日志采用追加模式（默认是覆写模式）<br>
bind_ip： 对外服务的绑定ip，一般设置为空，及绑定在本机所有可用ip上，如有需要可以单独指定<br>
port： 对外服务端口。Web管理端口在这个port的基础上+1000<br>
fork： 以后台Daemon形式运行服务<br>
journal：开启日志功能，通过保存操作日志来降低单机故障的恢复时间，在1.8版本后正式加入，取代在1.7.5版本中的dur参数。<br>
syncdelay： 执行sync的间隔，单位为秒。<br>
directoryperdb： 每个db存放在单独的目录中，建议设置该参数。<br>
maxConns： 最大连接数<br>
repairpath： 执行repair时的临时目录。在如果没有开启journal，异常宕机后重启，必须执行repair操作。</p>
