---
layout: post
title: "如何配置apache或httpd启用日志里的referer来源记录？"
categories: linux
tags: [apache, httpd, referer]
date: 2014-10-01 11:48:02
---
<br>
其实貌似httpd就是apache，apache也就是httpd，<br>
可能是其官方发布的不同版本吧，<br>
哈<br>
<br>
哪位知道它们的区别，请麻烦赐教，谢谢。<br>
<br>
言归正传，<br>
apache也好，httpd也好，<br>
<strong><font color="#ff0000">如何配置它的配置文件，才能让它的log日志里，记录请求的referer来源呢？</font></strong><br>
<br>
我的应用场景如下，<br>
lighttpd做前端server，做请求转发，<br>
httpd做后端server，处理php请求。<br>
<br>
有一天突然看到httpd的日志里，<br>
没有<strong>请求来源referer</strong>的信息，<br>
于是想知道到底是lighttpd转发没转发过来呢？<br>
还是httpd没有配置上，让它记录referer请求来源？<br>
<br>
因为之前有用过nginx做前端转发server，<br>
它是需要额外配置nginx的，<br>
nginx才会把referer信息转发到后端server，<br>
而且httpd还需要安装一个扩展，<br>
并配置上，<br>
才能拿到referer信息。<br>
<br>
lighttpd是不是也需要这样呢？<br>
仔细查阅lighttpd官方的资料，<br>
发现它的proxy设置，非常的简单，<br>
并没有可以设置referer的地方。<br>
<br>
难道它已经转发了这些信息，<br>
只是httpd没有正确地记录到日志吗？<br>
<br>
于是查找apache的日志格式，<br>
找到一个关键设置：<strong>LogFormat</strong><br>
打开httpd的配置文件：vim <strong>/etc/httpd/conf/httpd.conf</strong><br>
发现里面定义了好几个<strong>LogFormat日志格式</strong>，<br>
默认配置如下：<br>
<div class="blockcode"><div id="code_deG"><ol><li>LogFormat "%h %l %u %t \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined<br>
</li><li>LogFormat "%h %l %u %t \"%r\" %&gt;s %b" common<br>
</li><li>LogFormat "%{Referer}i -&gt; %U" referer<br>
</li><li>LogFormat "%{User-agent}i" agent</li></ol></div><em onclick="copycode($('code_deG'));"></em></div><br>

<br>
看到这里，明白了，<br>
八成是我的网站配置文件里，<br>
用的格式并不包含referer请求来源信息的记录，<br>
查看一下，果不其然，<br>
配置文件用的是<strong>common</strong>，而不是<strong>combined格式</strong>，<br>
于是修改网站的<strong>日志配置</strong>如下：<br>
<div class="blockcode"><div id="code_wie"><ol><li>CustomLog logs/oncecode.com-access_log combined</li></ol></div><em onclick="copycode($('code_wie'));"></em></div><br>

<br>
然后<strong>重启httpd服务</strong>，<br>
<div class="blockcode"><div id="code_oPN"><ol><li>/etc/init.d/httpd restart</li></ol></div><em onclick="copycode($('code_oPN'));"></em></div><br>

<br>
再看一下<strong>日志</strong>：<br>
<div class="blockcode"><div id="code_wj9"><ol><li>tail -f /var/log/httpd/mysite-access_log</li></ol></div><em onclick="copycode($('code_wj9'));"></em></div><br>

<br>
有<strong>Referer请求来源</strong>信息啦！！<br>
大功告成。<br>
<br>
