---
layout: post
title: "MongoDB实战系列之四：mongodb副本集部署"
categories: 数据库
tags: [mongodb实战系列, mongodb副本集部署]
date: 2014-11-02 21:47:58
---


<p>简述：副本集合（Replica Sets)，是一个基于主/从复制机制的复制功能，但增加了自动故障转移和恢复特性。一个集群最多可以支持7个服务器，并且任意节点都可以是主节点。所有的写操作都被分发到主节点，而读操作可以在任何节点上进行。</p>
<p>环境：CentOS 5.5 x64</p>
<p>md01 10.0.0.11<br>
md02 10.0.0.12<br>
md03 10.0.0.14</p>
<p>把以上主机名对应IP 添加到hosts文件</p>
<p>方法一：设置优先级</p>
<p>启动各节点：<br>
md01</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md01:<span class="nu0">27017</span> <span class="re5">--master</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>md02</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md02:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>md03</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md03:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>初始化节点:<br>
md01:(登录其中任何一个节点操作皆可)</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongo <span class="re5">--port</span> <span class="nu0">27017</span><br>
<br>
<span class="sy0">&gt;</span>rs.initiate<span class="br0">(</span><span class="br0">{</span><br>
_id : <span class="st0">"elain"</span>,<br>
members : <span class="br0">[</span><br>
<span class="br0">{</span>_id : <span class="nu0">1</span>, host : <span class="st0">"md01:27017"</span>, priority:<span class="nu0">2</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id : <span class="nu0">2</span>, host : <span class="st0">"md02:27017"</span>, priority:<span class="nu0">3</span><span class="br0">}</span>,<br>
<span class="br0">{</span>_id : <span class="nu0">3</span>, host : <span class="st0">"md03:27017"</span>, priority:<span class="nu0">4</span><span class="br0">}</span>,<br>
<span class="br0">]</span><br>
<span class="br0">}</span><span class="br0">)</span>;</div></div>
<p><span id="more-654"></span><br>
#priority 是设置优先级的，默认优先级为1,可以是1-1000的数字<br>
注：通常在同一个交换机上，同一个网内，通常使用优先级来设置 副本集就已经足够使用了</p>
<p>方法二:添加仲裁节点(这里设置在md02)：</p>
<p>启动各节点：<br>
md01</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md01:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>md02</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md02:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
<p>md03</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongod <span class="re5">--rest</span> <span class="re5">--replSet</span> elain<span class="sy0">/</span>md03:<span class="nu0">27017</span> <span class="re5">--fork</span> <span class="re5">--port</span> <span class="nu0">27017</span> <span class="re5">--dbpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>data<span class="sy0">/</span>mongodb<span class="sy0">/</span>db<span class="sy0">/</span> <span class="re5">--logpath</span> <span class="sy0">/</span>elain<span class="sy0">/</span>logs<span class="sy0">/</span>mongodb<span class="sy0">/</span>mongodb.log</div></div>
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
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">PRIMARY<span class="sy0">&gt;</span>rs.status<span class="br0">(</span><span class="br0">)</span></div></div>
<p>也可浏览：http://10.0.0.11:28017/_replSet 查看状态</p>
<p>#设置从库可读(从库上执行)</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>rs.slaveOk<span class="br0">(</span><span class="br0">)</span>;</div></div>
<p>查看副本集状态</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>rs.status<span class="br0">(</span><span class="br0">)</span><br>
<span class="sy0">&gt;</span>user <span class="kw3">local</span>;<br>
<span class="sy0">&gt;</span>rs.isMaster<span class="br0">(</span><span class="br0">)</span><br>
<span class="sy0">&gt;</span>db.system.replset.find<span class="br0">(</span><span class="br0">)</span></div></div>
<p>查看当前主库：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>;db.<span class="re1">$cmd</span>.findOne<span class="br0">(</span><span class="br0">{</span>ismaster:<span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span>;</div></div>

<pre>

referer: http://www.elain.org/?p=654
</pre>
