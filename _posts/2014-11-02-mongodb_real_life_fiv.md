---
layout: post
title: "MongoDB实战系列之五：mongodb的分片配置"
categories: 数据库
tags: [mongodb实战系列, mongodb分片配置]
date: 2014-11-02 21:51:58
---

<p>md01 10.0.0.11<br>
md02 10.0.0.12<br>
md03 10.0.0.14</p>
<p>2、启动三台机器的mongod实例<br>
根据Replica Set、Sharding策略部署mongod。将两个sharding组部署到三台服务器上，每个sharding组有三个replica set成员。<br>
#Server1:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard11<br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard21<br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--shardsvr</span> <span class="re5">--replSet</span> shard1 <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard11 <span class="re5">--oplogSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard11.log <span class="re5">--logappend</span> <span class="re5">--fork</span> <span class="re5">--rest</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--shardsvr</span> <span class="re5">--replSet</span> shard2 <span class="re5">--port</span> <span class="nu0">27018</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard21 <span class="re5">--oplogSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard21.log <span class="re5">--logappend</span> <span class="re5">--fork</span> <span class="re5">--rest</span></div></div>
<p>#Server2:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard12<span class="sy0">/</span><br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard22<span class="sy0">/</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--shardsvr</span> <span class="re5">--replSet</span> shard1 <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard12 <span class="re5">--oplogSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard12.log <span class="re5">--logappend</span> <span class="re5">--fork</span> <span class="re5">--rest</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--shardsvr</span> <span class="re5">--replSet</span> shard2 <span class="re5">--port</span> <span class="nu0">27018</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard22 <span class="re5">--oplogSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard22.log <span class="re5">--logappend</span> <span class="re5">--fork</span> <span class="re5">--rest</span></div></div>
<p>#Server3:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard13<span class="sy0">/</span><br>
<span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard23<span class="sy0">/</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--shardsvr</span> <span class="re5">--replSet</span> shard1 <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard13 <span class="re5">--oplogSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard13.log <span class="re5">--logappend</span> <span class="re5">--fork</span> <span class="re5">--rest</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--shardsvr</span> <span class="re5">--replSet</span> shard2 <span class="re5">--port</span> <span class="nu0">27018</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard23 <span class="re5">--oplogSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard23.log <span class="re5">--logappend</span> <span class="re5">--fork</span> <span class="re5">--rest</span></div></div>
<p><span id="more-672"></span><br>
3、初始化Replica Set<br>
通过命令行初始化两组Replica Set，通过mongo连接到一个mongod</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongo 10.0.0.11:<span class="nu0">27017</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">config = <span class="br0">{</span>_id: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>shard1<span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>, members: <span class="br0">[</span><br>
<span class="br0">{</span>_id: <span class="nu0">0</span>, host: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>10.0.0.11:<span class="nu0">27017</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id: <span class="nu0">1</span>, host: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>10.0.0.12:<span class="nu0">27017</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id: <span class="nu0">2</span>, host: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>10.0.0.14:<span class="nu0">27017</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="br0">}</span><span class="br0">]</span><span class="br0">}</span>;<br>
<br>
rs.initiate<span class="br0">(</span>config<span class="br0">)</span>;<br>
<br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongo 10.0.0.11:<span class="nu0">27018</span><br>
<br>
config = <span class="br0">{</span>_id: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>shard2<span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>, members: <span class="br0">[</span><br>
<span class="br0">{</span>_id: <span class="nu0">0</span>, host: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>10.0.0.11:<span class="nu0">27018</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id: <span class="nu0">1</span>, host: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>10.0.0.12:<span class="nu0">27018</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id: <span class="nu0">2</span>, host: <span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span>10.0.0.14:<span class="nu0">27018</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="st_h">''</span><span class="br0">}</span><span class="br0">]</span><span class="br0">}</span>;<br>
<br>
rs.initiate<span class="br0">(</span>config<span class="br0">)</span>;</div></div>
<p>4、启动并配置三台Config Server</p>
<p>#Server1、2、3:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="kw2">mkdir</span> <span class="re5">-p</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>config<span class="sy0">/</span><br>
<span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--configsvr</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>config<span class="sy0">/</span> <span class="re5">--port</span> <span class="nu0">20000</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>config1.log <span class="re5">--logappend</span> <span class="re5">--fork</span></div></div>
<p>5、部署并配置三台Routing Server</p>
<p>指定所有的config sever地址参数，chunkSize是分割数据时每块(Chunk)的单位大小</p>
<p>#Server1、2、3:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongos <span class="re5">--configdb</span> 10.0.0.11:<span class="nu0">20000</span>,10.0.0.12:<span class="nu0">20000</span>,10.0.0.14:<span class="nu0">20000</span> <span class="re5">--port</span> <span class="nu0">30000</span> <span class="re5">--chunkSize</span> <span class="nu0">100</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongos.log <span class="re5">--logappend</span> <span class="re5">--fork</span></div></div>
<p>6、命令行添加分片<br>
连接到mongs服务器，并切换到admin</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongo 10.0.0.11:<span class="nu0">30000</span><span class="sy0">/</span>admin<br>
<br>
db.runCommand<span class="br0">(</span> <span class="br0">{</span><br>
addshard : <span class="st0">"shard1/10.0.0.11:27017,10.0.0.12:27017,10.0.0.14:27017"</span>,<br>
name:<span class="st0">"shard1"</span>,<br>
maxsize:<span class="nu0">2048</span>,<br>
allowLocal:true <span class="br0">}</span> <span class="br0">)</span>;<br>
<br>
db.runCommand<span class="br0">(</span> <span class="br0">{</span><br>
addshard : <span class="st0">"shard2/10.0.0.11:27018,10.0.0.12:27018,10.0.0.14:27018"</span>,<br>
name:<span class="st0">"shard2"</span>,<br>
maxsize:<span class="nu0">2048</span>,<br>
allowLocal:true <span class="br0">}</span> <span class="br0">)</span>;<br>
<br>
db.runCommand<span class="br0">(</span> <span class="br0">{</span> listshards : <span class="nu0">1</span> <span class="br0">}</span> <span class="br0">)</span>;</div></div>
<p>如果列出(sharding)了以上二个你加的shards，表示shards已经配置成功</p>
<p>#激活数据库分片</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">db.runCommand<span class="br0">(</span> <span class="br0">{</span> enablesharding : <span class="st0">"elain"</span> <span class="br0">}</span> <span class="br0">)</span>;</div></div>
<p>要使单个collection也分片存储，需要给collection指定一个分片key，通过以下命令操作：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;height:100%;"><div class="bash codecolorer">db.runCommand<span class="br0">(</span> <span class="br0">{</span> shardcollection : “”,key : db.chujq.t1.stats<span class="br0">(</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"sharded"</span> : <span class="kw2">true</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"ns"</span> : <span class="st0">"elain.test"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">4058977</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">34</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">675039816</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">818757632</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">131854352</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">131854352</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.30786919955446</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"nchunks"</span> : <span class="nu0">14</span>,<br>
<span class="st0">"shards"</span> : <span class="br0">{</span><br>
<span class="st0">"shard1"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.test"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">1860365</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">309376352</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.29873815084673</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">408920064</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">16</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">77955072</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">60371584</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">60371584</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"shard2"</span> : <span class="br0">{</span><br>
<span class="st0">"ns"</span> : <span class="st0">"elain.test"</span>,<br>
<span class="st0">"count"</span> : <span class="nu0">2198612</span>,<br>
<span class="st0">"size"</span> : <span class="nu0">365663464</span>,<br>
<span class="st0">"avgObjSize"</span> : <span class="nu0">166.31559547569103</span>,<br>
<span class="st0">"storageSize"</span> : <span class="nu0">409837568</span>,<br>
<span class="st0">"numExtents"</span> : <span class="nu0">18</span>,<br>
<span class="st0">"nindexes"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"lastExtentSize"</span> : <span class="nu0">74846208</span>,<br>
<span class="st0">"paddingFactor"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"flags"</span> : <span class="nu0">1</span>,<br>
<span class="st0">"totalIndexSize"</span> : <span class="nu0">71482768</span>,<br>
<span class="st0">"indexSizes"</span> : <span class="br0">{</span><br>
<span class="st0">"_id_"</span> : <span class="nu0">71482768</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>删除片操作</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span><span class="br0">{</span><span class="st0">"removeshard"</span> : <span class="st0">"10.0.0.11:27018"</span><span class="br0">}</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"msg"</span> : <span class="st0">"draining started successfully"</span>,<br>
<span class="st0">"state"</span> : <span class="st0">"started"</span>,<br>
<span class="st0">"shard"</span> : <span class="st0">"shard2"</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>再执行，可看到removeshard的挪动进度</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongos<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span><span class="br0">{</span><span class="st0">"removeshard"</span> : <span class="st0">"10.0.0.11:27018"</span><span class="br0">}</span><span class="br0">)</span>;<br>
<span class="br0">{</span><br>
<span class="st0">"msg"</span> : <span class="st0">"draining ongoing"</span>,<br>
<span class="st0">"state"</span> : <span class="st0">"ongoing"</span>,<br>
<span class="st0">"remaining"</span> : <span class="br0">{</span><br>
<span class="st0">"chunks"</span> : NumberLong<span class="br0">(</span><span class="nu0">3</span><span class="br0">)</span>,<br>
<span class="st0">"dbs"</span> : NumberLong<span class="br0">(</span><span class="nu0">0</span><span class="br0">)</span><br>
<span class="br0">}</span>,<br>
<span class="st0">"ok"</span> : <span class="nu0">1</span><br>
<span class="br0">}</span></div></div>
<p>例:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--config</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>shard1<span class="sy0">/</span>shard1.properties <span class="re5">--rest</span></div></div>


<pre>
referer: http://www.elain.org/?p=672

</pre>
