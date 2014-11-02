---
layout: post
title: "MongoDB实战系列之二：MongoDB的常用操作"
categories: 数据库
tags: [mongodb实战系列, mongodb常用操作]
date: 2014-11-02 21:36:58
---

<p>恭祝大家元旦快乐！</p>
<p>#以服务方式启动mongodb，要求验证</p>
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
<p>#远程登录：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongo <span class="re5">--host</span> serverip:<span class="nu0">27001</span></div></div>
<p>#本机登录：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongo <span class="re5">--port</span> <span class="nu0">27001</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="br0">[</span>root<span class="sy0">@</span>md01 ~<span class="br0">]</span><span class="co0"># mongo --host localhost:27001</span><br>
MongoDB shell version: 2.0.0<br>
connecting to: localhost:<span class="nu0">27001</span><span class="sy0">/</span><span class="kw3">test</span><br>
<span class="sy0">&gt;</span></div></div>
<p><span id="more-614"></span></p>
<p>#获取MongoDB服务器统计信息</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span><span class="br0">{</span><span class="st0">"serverStatus"</span> : <span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span></div></div>
<p>#使用实时监控工具</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongostat <span class="re5">-h</span> localhost:<span class="nu0">27001</span></div></div>
<p>#查看版本</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> db.version<span class="br0">(</span><span class="br0">)</span><br>
2.0.0</div></div>
<p>用户管理：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> db.addUser<span class="br0">(</span><span class="st0">"root"</span>,<span class="st0">"123456"</span><span class="br0">)</span>; &nbsp; &nbsp;<span class="co0">#添加管理员root</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> use <span class="kw3">test</span><br>
switched to db <span class="kw3">test</span><br>
<span class="sy0">&gt;</span> db.addUser<span class="br0">(</span><span class="st0">"test_w"</span>,<span class="st0">"123456"</span><span class="br0">)</span>; &nbsp;<span class="co0">#为TEST库添加普通用户test_w</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> use <span class="kw3">test</span><br>
switched to db <span class="kw3">test</span><br>
<span class="sy0">&gt;</span> db.addUser<span class="br0">(</span><span class="st0">"test_r"</span>, <span class="st0">"123456"</span>, <span class="kw2">true</span><span class="br0">)</span>; &nbsp; <span class="co0">#为TEST库添加只读用户test_r</span><br>
<span class="sy0">&gt;</span> db.system.users.remove<span class="br0">(</span><span class="br0">{</span><span class="st0">"user"</span>: <span class="st0">"test_w"</span><span class="br0">}</span><span class="br0">)</span>; &nbsp; &nbsp;<span class="co0">#删除名为test_w的用户</span><br>
<span class="sy0">&gt;</span> db.auth<span class="br0">(</span><span class="st0">"test_w"</span>, <span class="st0">"123456"</span><span class="br0">)</span>; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="co0">#验证并切换用户身份</span><br>
<span class="sy0">&gt;</span> db.system.users.find<span class="br0">(</span><span class="br0">)</span>; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <span class="co0">#查看当前库的所有用户</span><br>
<span class="sy0">&gt;</span> show <span class="kw2">users</span>; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <span class="co0">#查看当前库的所有用户</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span> use admin<br>
<span class="sy0">&gt;</span> db.runCommand<span class="br0">(</span><span class="br0">{</span><span class="st0">"buildInfo"</span>:<span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="co0">#查看系统信息与mongodb版本</span></div></div>
<p>数据管理：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>use elain &nbsp; &nbsp; &nbsp; &nbsp; <span class="co0">#建库</span><br>
<span class="sy0">&gt;</span>db.elain.insert<span class="br0">(</span><span class="br0">{</span>name:<span class="st_h">''</span>elain<span class="st_h">''</span><span class="br0">}</span><span class="br0">)</span>; &nbsp; &nbsp;<span class="co0">#数据插入</span><br>
<span class="sy0">&gt;</span>db.elain.remove<span class="br0">(</span><span class="br0">{</span>name:<span class="st_h">''</span>elain<span class="st_h">''</span><span class="br0">}</span><span class="br0">)</span>; &nbsp; &nbsp;<span class="co0">#数据删除</span><br>
<span class="sy0">&gt;</span>db.elain.remove<span class="br0">(</span><span class="br0">{</span>name:<span class="st_h">''</span>elain<span class="st_h">''</span><span class="br0">}</span><span class="br0">)</span>; &nbsp; &nbsp;<span class="co0">#数据删除(永久删除)</span><br>
<span class="sy0">&gt;</span>show dbs; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <span class="co0">#显示数据库</span><br>
<span class="sy0">&gt;</span>show collections; &nbsp; <span class="co0">#显示表</span><br>
<span class="sy0">&gt;</span>db.elain.find<span class="br0">(</span><span class="br0">)</span>; &nbsp; &nbsp;<span class="co0">#数据查询</span><br>
<span class="sy0">&gt;</span>db.elain.findOne<span class="br0">(</span><span class="br0">)</span>; <span class="co0">#只查一行</span><br>
<span class="sy0">&gt;</span>db &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="co0">#查看当前所在库</span><br>
<span class="sy0">&gt;</span>db.collection.count<span class="br0">(</span><span class="br0">)</span>; &nbsp;<span class="co0">#统计colleciton的数量</span><br>
<span class="sy0">&gt;</span>db.collection.drop<span class="br0">(</span><span class="br0">)</span>; &nbsp; <span class="co0">#删除此colleciton</span><br>
<span class="sy0">&gt;</span>db.foo.find<span class="br0">(</span><span class="br0">)</span>.count &nbsp; &nbsp;<span class="co0">#某个数据的数量</span><br>
<span class="sy0">&gt;</span>db.deliver_status.dataSize<span class="br0">(</span><span class="br0">)</span>; &nbsp; &nbsp; &nbsp; &nbsp; <span class="co0">#查看collection数据的大小</span><br>
<span class="sy0">&gt;</span>db.deliver_status.stats<span class="br0">(</span><span class="br0">)</span>; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="co0">#查看colleciont状态</span><br>
<span class="sy0">&gt;</span>db.deliver_status.totalIndexSize<span class="br0">(</span><span class="br0">)</span>; &nbsp; <span class="co0">#查询所有索引的大小</span></div></div>
<p>#删除数据库</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">use elain;<br>
db.dropDatabase<span class="br0">(</span><span class="br0">)</span>;</div></div>
<p>#修复数据库</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">db.repairDatabase<span class="br0">(</span><span class="br0">)</span>;</div></div>
<p>#删除表</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">db.elain.drop<span class="br0">(</span><span class="br0">)</span>;</div></div>
<p>#查看profiling</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">show profile</div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">&gt;</span>db.test.find<span class="br0">(</span><span class="br0">{</span><span class="br0">}</span>,<span class="br0">{</span><span class="st0">"_id"</span>:<span class="nu0">0</span><span class="br0">}</span><span class="br0">)</span>; &nbsp;<span class="co0">#不显示id列</span><br>
<span class="sy0">&gt;</span>db.test.find<span class="br0">(</span><span class="br0">{</span><span class="st_h">''</span>name<span class="st_h">''</span>:<span class="sy0">/</span>mp<span class="sy0">/</span>i<span class="br0">}</span><span class="br0">)</span>; &nbsp;<span class="co0">#正则查找忽略大小写</span></div></div>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">db.elain.ensureIndex<span class="br0">(</span><span class="br0">{</span><span class="st0">"name"</span>:<span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span>; &nbsp; &nbsp; &nbsp; &nbsp;<span class="co0">#建立索引</span><br>
db.elain.dropIndex<span class="br0">(</span><span class="br0">{</span><span class="st0">"name"</span>:<span class="nu0">1</span><span class="br0">}</span><span class="br0">)</span>; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="co0">#删除索引</span><br>
db.elain.find<span class="br0">(</span><span class="br0">{</span><span class="st0">"name"</span>:<span class="st0">"elain"</span><span class="br0">}</span><span class="br0">)</span>.explain<span class="br0">(</span><span class="br0">)</span>; &nbsp;<span class="co0">#查看索引</span></div></div>
<p>—————————————</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="st0">"<span class="es2">$lt</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="sy0">&amp;</span>lt;<br>
<span class="st0">"<span class="es2">$lte</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; <span class="sy0">&amp;</span>lt;=<br>
<span class="st0">"<span class="es2">$gt</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="sy0">&gt;</span><br>
<span class="st0">"<span class="es2">$gte</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; <span class="sy0">&gt;</span>=<br>
<span class="st0">"<span class="es2">$ne</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span class="sy0">&amp;</span>lt;<span class="sy0">&gt;</span><br>
<span class="st0">"<span class="es2">$in</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;一个键匹配多个值<br>
<span class="st0">"<span class="es2">$nin</span>"</span> &nbsp; &nbsp; &nbsp; &nbsp; 一个键不匹配多个值<br>
<span class="re1">$not</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 不匹配<br>
<span class="re1">$all</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 匹配数组全值<br>
<span class="re1">$size</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;数组长度<br>
<span class="re1">$slice</span> &nbsp; &nbsp; &nbsp; &nbsp; 返子集合 <span class="br0">{</span><span class="st0">"<span class="es2">$slice</span>”:10} &nbsp;-10 &nbsp; [10,20]<br>
. &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;内嵌文档 {“name.first”：“xxx”}<br>
<span class="es2">$where</span> &nbsp; &nbsp; &nbsp; &nbsp; *通常情况下不建议使用</span></div></div>
<p>—————————————–</p>
<p>备份恢复：<br>
数据导出：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongoexport <span class="re5">-h</span> 127.0.0.1:<span class="nu0">27001</span> <span class="re5">-uroot</span> <span class="re5">-p</span> <span class="re5">-d</span> elain <span class="re5">-c</span> <span class="re5">-o</span> elain elain_con.csv</div></div>
<p>数据导入：</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer"><span class="sy0">/</span>elain<span class="sy0">/</span>apps<span class="sy0">/</span>mongodb<span class="sy0">/</span>bin<span class="sy0">/</span>mongoimport <span class="re5">-h</span> 127.0.0.1:<span class="nu0">27001</span> <span class="re5">-uroot</span> <span class="re5">-p</span> <span class="re5">-d</span> elain <span class="re5">-c</span> elain elain_con.csv</div></div>
<p>备份数据库:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongodump <span class="re5">-h</span> 127.0.0.1:<span class="nu0">27001</span> <span class="re5">-uroot</span> <span class="re5">-p</span> <span class="re5">-d</span> elain <span class="re5">-o</span> <span class="sy0">/</span>elain<span class="sy0">/</span>backup<span class="sy0">/</span>mongodb</div></div>
<p>恢复数据库:</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongorestore <span class="re5">-h</span> 127.0.0.1:<span class="nu0">27001</span> <span class="re5">-uroot</span> <span class="re5">-p</span> <span class="re5">-d</span> elain <span class="sy0">/</span>elain<span class="sy0">/</span>backup<span class="sy0">/</span>mongodb<span class="sy0">/</span>elain</div></div>
<p>恢复数据库(恢复前清除已有数据):</p>
<div class="codecolorer-container bash blackboard" style="width:99%;"><div class="bash codecolorer">mongorestore <span class="re5">-h</span> 127.0.0.1:<span class="nu0">27001</span> <span class="re5">-uroot</span> <span class="re5">-p</span> <span class="re5">-d</span> elain <span class="re5">--drop</span> <span class="sy0">/</span>elain<span class="sy0">/</span>backup<span class="sy0">/</span>mongodb<span class="sy0">/</span>elain</div></div>
<p>性能测试：<br>
备份方面：mongodump的速度和压缩率都最好，每秒125M的数据，压缩率达28%<br>
恢复方面：<br>
mongoimport速度较快，但不保证数据完整导入<br>
mongorestore，速度较慢，比mongoimport慢2.5倍左右，但是根据mongodump导出的数据，可以完整导入数据。</p>
<p>主从复制常用操作：<br>
见本人主从部署文档</p>

