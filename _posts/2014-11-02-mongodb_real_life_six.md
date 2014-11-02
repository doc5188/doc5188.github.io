---
layout: post
title: "MongoDB实战系列之六：mongodb的高可用集群设计实战"
categories: 数据库
tags: [mongodb实战系列, mongodb高可用集群]
date: 2014-11-02 21:55:58
---

<p>环境：<br>
CentOS 6.0 x64</p>
<p>md01: 10.0.0.11<br>
md02: 10.0.0.12<br>
md03: 10.0.0.14<br>
md04: 10.0.0.15<br>
md05: 10.0.0.16<br>
md06: 10.0.0.17</p>
<p>设计思路：</p>
<p>md01、md02、md03 做一组复制集<br>
md04、md05、md06 做一组复制集<br>
再把这两组复制集用分片做成 shard1、shard2 用LVS 调用</p>
<p>下载安装<span class="wp_keywordlink_affiliate"><a href="http://www.elain.org/?tag=mongodb" title="查看 mongodb 中的全部文章" target="_blank">mongodb</a></span></p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw3">cd</span> <span class="sy0">/</span>root<span class="sy0">/</span>tools<br>
<span class="kw2">wget</span> http:<span class="sy0">//</span>fastdl.mongodb.org<span class="sy0">/</span>linux<span class="sy0">/</span>mongodb-linux-x86_64-2.0.0.tgz<br>
<span class="kw2">tar</span> zxvf mongodb-linux-x86_64-2.0.0.tgz<br>
<span class="kw2">mv</span> mongodb-linux-x86_64-2.0.0 <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb-linux-x86_64-2.0.0<br>
<span class="kw2">ln</span> <span class="re5">-s</span> <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb-linux-x86_64-2.0.0 <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<br>
<span class="kw2">ln</span> <span class="re5">-s</span> <span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/*</span> <span class="sy0">/</span>bin<span class="sy0">/</span></div></div>
<p>#添加用户组</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>usr<span class="sy0">/</span>sbin<span class="sy0">/</span>groupadd <span class="re5">-g</span> <span class="nu0">690</span> mongodb<br>
<span class="sy0">/</span>usr<span class="sy0">/</span>sbin<span class="sy0">/</span>useradd <span class="re5">-g</span> mongodb mongodb <span class="re5">-u</span> <span class="nu0">690</span> <span class="re5">-s</span> <span class="sy0">/</span>sbin<span class="sy0">/</span>nologin</div></div>
<p>各节点hosts文件 添加：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">true</span> <span class="sy0">&gt;</span> <span class="sy0">/</span>etc<span class="sy0">/</span>hosts<br>
<span class="kw3">echo</span> <span class="re5">-ne</span> <span class="st0">"<br>
10.0.0.11 md01<br>
10.0.0.12 md02<br>
10.0.0.14 md03<br>
10.0.0.15 md04<br>
10.0.0.16 md05<br>
10.0.0.17 md06<br>
"</span> <span class="sy0">&gt;&gt;/</span>etc<span class="sy0">/</span>hosts</div></div>
<p><span id="more-676"></span><br>
———————————————<br>
副本集配置：<br>
启动各节点：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">md01<br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span><br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md01:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log<br>
md02<br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span><br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md02:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log<br>
md03<br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span><br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md03:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>#启动仲裁节点<br>
在md02上</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>arb<br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--fork</span> <span class="re5">--rest</span> <span class="re5">--replSet</span> elain <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>arb <span class="re5">--port</span> <span class="nu0">27015</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>初始化节点:<br>
md01:(登录其中任何一个节点操作皆可)</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> rs.initiate<span class="br0">(</span><span class="br0">{</span><br>
_id : <span class="st0">"elain"</span>,<br>
members : <span class="br0">[</span><br>
<span class="br0">{</span>_id : <span class="nu0">1</span>, host : <span class="st0">"md01:27017"</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id : <span class="nu0">2</span>, host : <span class="st0">"md02:27017"</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id : <span class="nu0">3</span>, host : <span class="st0">"md03:27017"</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id : <span class="nu0">4</span>, host : <span class="st0">"md02:27015"</span>, <span class="st0">"arbiterOnly"</span>: <span class="kw2">true</span><span class="br0">}</span>,<br>
<span class="br0">]</span><br>
<span class="br0">}</span><span class="br0">)</span>;</div></div>
<p>#验证</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">PRIMARY<span class="sy0">&gt;</span> rs.status<span class="br0">(</span><span class="br0">)</span></div></div>
<p>也可浏览：http://10.0.0.11:28017/_replSet 查看状态</p>
<p>查看副本集状态</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>rs.status<span class="br0">(</span><span class="br0">)</span><br>
<span class="sy0">&gt;</span>user <span class="kw3">local</span>;<br>
<span class="sy0">&gt;</span>rs.isMaster<span class="br0">(</span><span class="br0">)</span><br>
<span class="sy0">&gt;</span>db.system.replset.find<span class="br0">(</span><span class="br0">)</span></div></div>
<p>查看当前主库：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>db.<span class="re1">$cmd</span>.findOne<span class="br0">(</span><span class="br0">{</span>ismaster:<span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span>;</div></div>
<p>另一组副本集同理操作即可;这里为省篇幅就不再写出,但切记两复制集名称不可以重复</p>
<p>—————————————————</p>
<p>启动并配置三台Config Server</p>
<p>#md01,03,05上执行</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>config<span class="sy0">/</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--configsvr</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>config<span class="sy0">/</span> <span class="re5">--port</span> <span class="nu0">20000</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>config.log <span class="re5">--logappend</span> <span class="re5">--fork</span></div></div>
<p>5、部署并配置三台Routing Server</p>
<p>指定所有的config sever地址参数，chunkSize是分割数据时每块(Chunk)的单位大小</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="co0">#md02,md04,md06</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongos <span class="re5">--configdb</span> md01:<span class="nu0">20000</span>,md03:<span class="nu0">20000</span>,md05:<span class="nu0">20000</span> <span class="re5">--port</span> <span class="nu0">30000</span> <span class="re5">--chunkSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongos.log <span class="re5">--logappend</span> <span class="re5">--fork</span></div></div>
<p>6、命令行添加分片</p>
<p>连接到mongs服务器，并切换到admin</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongo 10.0.0.11:<span class="nu0">30000</span><span class="sy0">/</span>admin<br>
<br>
db.runCommand<span class="br0">(</span> <span class="br0">{</span><br>
addshard : <span class="st0">"elain/md01:27017"</span>,<br>
name:<span class="st0">"shard1"</span>,<br>
maxsize:<span class="nu0">2048</span>,<br>
allowLocal:true <span class="br0">}</span> <span class="br0">)</span>;<br>
<br>
db.runCommand<span class="br0">(</span> <span class="br0">{</span><br>
addshard : <span class="st0">"chujq/md04:27017"</span>,<br>
name:<span class="st0">"shard2"</span>,<br>
maxsize:<span class="nu0">2048</span>,<br>
allowLocal:true <span class="br0">}</span> <span class="br0">)</span>;</div></div>
<p>注：添加复制集elain，其中包含一个服务器md01:27017(还饿别的服务器，如md02、md03)，如果md01挂了，mongos会知道它所连接的是一个复制集，并会使用新的主节点（md02或md03）</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">db.runCommand<span class="br0">(</span> <span class="br0">{</span> listshards : <span class="nu0">1</span> <span class="br0">}</span> <span class="br0">)</span>;</div></div>
<p>如果列出(sharding)了以上二个你加的shards，表示shards已经配置成功</p>
<p>导入数据：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongoimport <span class="re5">-d</span> elain <span class="re5">-c</span> elain <span class="re5">--type</span> csv <span class="re5">--headerline</span> <span class="re5">--file</span> <span class="sy0">/</span>root<span class="sy0">/</span>bak<span class="sy0">/</span>test.csv <span class="re5">--host</span> md02:<span class="nu0">30000</span></div></div>
<p>注：数据自备，我这里是从生产环境下MYSQL里导出的一些真实数据来做测试</p>
<p>#激活数据库分片</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">db.runCommand<span class="br0">(</span> <span class="br0">{</span> enablesharding : <span class="st0">"elain"</span> <span class="br0">}</span> <span class="br0">)</span>;<br>
mongos<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span> <span class="br0">{</span> enablesharding : <span class="st0">"elain"</span> <span class="br0">}</span> <span class="br0">)</span>;<br>
<span class="br0">{</span> <span class="st0">"ok"</span> : <span class="nu0">1</span> <span class="br0">}</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> show dbs<br>
config 0.1875GB<br>
elain 0.453125GB<br>
<span class="kw3">test</span> <span class="br0">(</span>empty<span class="br0">)</span></div></div>
<p>#进入数据库，建立索引，为分片做准备</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongo 10.0.0.12:<span class="nu0">30000</span><span class="sy0">/</span>admin</div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">use elain;<br>
db.elain.ensureIndex<span class="br0">(</span><span class="br0">{</span><span class="st0">"client_userid"</span>:<span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span>;</div></div>
<p>查看索引：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.elain.find<span class="br0">(</span><span class="br0">{</span><span class="st0">"client_userid"</span> : <span class="nu0">151512</span><span class="br0">}</span><span class="br0">)</span>.explain<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"cursor"</span> : <span class="st0">"BtreeCursor client_userid_1"</span>,<br>
<span class="st0">"nscanned"</span> : <span class="nu0">3</span>,<br>
<span class="st0">"nscannedObjects"</span> : <span class="nu0">3</span>,<br>
<span class="st0">"n"</span> : <span class="nu0">3</span>,<br>
<span class="st0">"millis"</span> : <span class="nu0">0</span>,<br>
<span class="st0">"nYields"</span> : <span class="nu0">0</span>,<br>
<span class="st0">"nChunkSkips"</span> : <span class="nu0">0</span>,<br>
<span class="st0">"isMultiKey"</span> : <span class="kw2">false</span>,<br>
<span class="st0">"indexOnly"</span> : <span class="kw2">false</span>,<br>
<span class="st0">"indexBounds"</span> : <span class="br0">{</span><br>
<span class="st0">"client_userid"</span> : <span class="br0">[</span><br>
<span class="br0">[</span><br>
<span class="nu0">151512</span>,<br>
<span class="nu0">151512</span><br>
<span class="br0">]</span><br>
<span class="br0">]</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span></div></div>
<p>#添加分片：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">use admin;<br>
db.runCommand<span class="br0">(</span> <span class="br0">{</span> shardcollection : <span class="st0">"elain.elain"</span>,key : <span class="br0">{</span>client_userid: <span class="nu0">1</span><span class="br0">}</span> <span class="br0">}</span> <span class="br0">)</span><br>
<br>
mongos<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span> <span class="br0">{</span> shardcollection : <span class="st0">"elain.elain"</span>,key : <span class="br0">{</span>client_userid: <span class="nu0">1</span><span class="br0">}</span> <span class="br0">}</span> <span class="br0">)</span><br>
<span class="br0">{</span> <span class="st0">"collectionsharded"</span> : <span class="st0">"elain.elain"</span>, <span class="st0">"ok"</span> : <span class="nu0">1</span> <span class="br0">}</span></div></div>
<p>#查看分片状态</p>
<div class="codecolorer-container bash blackboard" style="width:99%;height:100%;"><div class="bash codecolorer">use elain;<br>
db.elain.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<br>
mongos<span class="sy0">&gt;</span> db.elain.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"sharded"</span> : <span class="kw2">true</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">507372</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">10</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">84375328</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">97849344</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">29253728</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">16474640</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">12779088</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.29874727024747</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"nchunks"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"shards"</span> : <span class="br0">{</span><br>
<span class="st0">"shard2"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">507372</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">84375328</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.29874727024747</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">97849344</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">10</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">26099712</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">29253728</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">16474640</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">12779088</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>在分片后新写数据第一次：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;height:100%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.elain.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"sharded"</span> : <span class="kw2">true</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">676496</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">12</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">112500436</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">129179648</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">47551616</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">21968912</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">25582704</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.29874529930703</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"nchunks"</span> : <span class="nu0">8</span>,<br>
<span class="st0">"shards"</span> : <span class="br0">{</span><br>
<span class="st0">"shard1"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">0</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">0</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">8192</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">8192</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">16352</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">8176</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">8176</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"shard2"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">676496</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">112500436</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.29874529930703</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">129171456</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">11</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">31322112</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">47535264</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">21960736</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">25574528</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>分片后新写数据第二次：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;height:100%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.elain.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"sharded"</span> : <span class="kw2">true</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">1189194</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">23</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">194533928</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">252874752</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">87262448</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">43692544</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">43569904</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">163.58468677103988</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"nchunks"</span> : <span class="nu0">8</span>,<br>
<span class="st0">"shards"</span> : <span class="br0">{</span><br>
<span class="st0">"shard1"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">396370</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">62195348</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">156.91234957236924</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">86114304</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">11</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">20881408</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">35949872</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">17954496</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">17995376</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"shard2"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">792824</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">132338580</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.9205019020615</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">166760448</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">12</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">37588992</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">51312576</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">25738048</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">25574528</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>分片后新写数据第三次：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;height:100%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.elain.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"sharded"</span> : <span class="kw2">true</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">1376876</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">23</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">225576604</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">252874752</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">100826432</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">50249696</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">50576736</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">163.83218532387812</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"nchunks"</span> : <span class="nu0">10</span>,<br>
<span class="st0">"shards"</span> : <span class="br0">{</span><br>
<span class="st0">"shard1"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">494202</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">77551984</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">156.92365469990003</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">86114304</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">11</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">20881408</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">42057344</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">21600992</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">20456352</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"shard2"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">882674</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">148024620</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">167.70021548159343</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">166760448</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">12</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">37588992</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">58769088</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">28648704</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">30120384</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>分片后新写数据第四次（DOWN 掉md04的mongo服务）</p>
<div class="codecolorer-container bash blackboard" style="width:99%;height:100%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.elain.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"sharded"</span> : <span class="kw2">true</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">1686310</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">26</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">275761376</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">353116160</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">129033632</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">63265888</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">65767744</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">163.52946729842083</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"nchunks"</span> : <span class="nu0">10</span>,<br>
<span class="st0">"shards"</span> : <span class="br0">{</span><br>
<span class="st0">"shard1"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">740264</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">116213588</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">156.98938216636228</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">141246464</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">13</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">30072832</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">61810560</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">32556832</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">29253728</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"shard2"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.elain"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">946046</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">159547788</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">168.64696642657967</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">211869696</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">13</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">2</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">45109248</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">67223072</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">30709056</span>,<br>
<span class="st0">"client_userid_1"</span> : <span class="nu0">36514016</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>总结：通过以上四次的写数据测试，我们可以看到分片是成功的，每次写数据,shard1、shard2都有数据写入，且，在下面的复制集中DOWN 掉任意一台，不影响整个架构的正常服务。</p>
<p>删除片操作</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span><span class="br0">{</span><span class="st0">"removeshard"</span> : <span class="st0">"10.0.0.11:27011"</span><span class="br0">}</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"msg"</span> : <span class="st0">"draining started successfully"</span>,<br>
<span class="st0">"state"</span> : <span class="st0">"started"</span>,<br>
<span class="st0">"shard"</span> : <span class="st0">"shard2"</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>再执行，可看到removeshard的挪动进度</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span><span class="br0">{</span><span class="st0">"removeshard"</span> : <span class="st0">"10.0.0.11:27011"</span><span class="br0">}</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"msg"</span> : <span class="st0">"draining ongoing"</span>,<br>
<span class="st0">"state"</span> : <span class="st0">"ongoing"</span>,<br>
<span class="st0">"remaining"</span> : <span class="br0">{</span><br>
<span class="st0">"chunks"</span> : NumberLong<span class="br0">(</span><span class="nu0">3</span><span class="br0">)</span>,<br>
<span class="st0">"dbs"</span> : NumberLong<span class="br0">(</span><span class="nu0">0</span><span class="br0">)</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>到此结束</p>





<pre>
referer: http://www.elain.org/?p=676
</pre>
