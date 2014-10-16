---
layout: post
title: "Linux服务器开发环境搭建 Nginx+PHP+MongoDB"
categories: linux 
tags: [nginx, php, mongodb]
date: 2014-10-16 23:20:16
---


<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-size:14px; line-height:28px; font-family:宋体,'Arial Narrow',arial,serif">
</p>
<p style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px">
安装gcc编译器使用命令：</p>
<p style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px">
&nbsp;&nbsp;&nbsp;&nbsp;<strong>yum -y install gcc<br>
</strong></p>
<p style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px">
安装g++编译器使用命令：</p>
<p style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px">
&nbsp;&nbsp;&nbsp;&nbsp;<strong>yum -y install gcc-c++</strong></p>
<p><span style="font-family:'Trebuchet MS',Arial,Verdana; font-size:14px; line-height:25px; background-color:rgb(235,235,236)">yum -y install pcre-devel &nbsp;<span style="color:rgb(68,68,68); font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif; line-height:20px">zlib-devel</span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana">针对Ubuntu</span></span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana"><span style="font-family:'Courier New',Courier,monospace; font-size:14px; line-height:25.1875px; white-space:pre">apt-get
 install libpcre3 libpcre3-dev</span><br>
</span></span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana"><span style="font-family:'Courier New',Courier,monospace; font-size:14px; line-height:25.1875px; white-space:pre"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">$sudo
 apt-get install ruby <span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
&nbsp;zlib1g-dev</span></span><br>
</span></span></span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana"><span style="font-family:'Courier New',Courier,monospace; font-size:14px; line-height:25.1875px; white-space:pre"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px">sudo&nbsp;apt-get
 install libxml2-dev&nbsp;</span><br>
</span></span></span></span></span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana"><span style="font-family:'Courier New',Courier,monospace; font-size:14px; line-height:25.1875px; white-space:pre"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px">(对于在64位系统上使用32位Zendstudio,需要安装32位依赖库)</span></span></span></span></span></span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana"><span style="font-family:'Courier New',Courier,monospace; font-size:14px; line-height:25.1875px; white-space:pre"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px"><span style="color:rgb(46,139,87); font-family:Monaco,'Andale Mono','Courier New',Courier,mono; line-height:15.59375px">sudo
 apt-get install ia32-libs</span><br>
</span></span></span></span></span></span></span></p>
<p><span style="font-size:14px; background-color:rgb(235,235,236)"><span style="color:rgb(68,68,68); line-height:25px"><span style="font-family:Trebuchet MS,Arial,Verdana"><span style="font-family:'Courier New',Courier,monospace; font-size:14px; line-height:25.1875px; white-space:pre"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(85,85,85); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px"><span style="color:rgb(51,51,51); font-family:Arial; font-size:14px; line-height:26px"><span style="color:rgb(46,139,87); font-family:Monaco,'Andale Mono','Courier New',Courier,mono; line-height:15.59375px">sudo
 apt-get install openjdk-6-jre<br>
</span></span></span></span></span></span></span></span></p>
<hr style="padding:0px; margin:0px; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px">&nbsp;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px"><span style="padding:0px; margin:0px; font-size:24px">1. 安装Nginx</span></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cd /usr/soft</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">wget http://nginx.org/download/<a target="_blank" href="http://nginx.org/download/nginx-1.5.6.tar.gz">nginx-1.5.6.tar.gz</a><br>
tar zxvf&nbsp;</span><a target="_blank" href="http://nginx.org/download/nginx-1.5.6.tar.gz" style="font-size:16px">nginx-1.5.6.tar.gz</a><span style="background-color:rgb(240,240,240); font-size:16px"></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cd /usr/soft/nginx-1.5.6</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">./configure&nbsp;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">make</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">make install</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<br>
</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">配置nginx.conf使其支持.php文件的解析</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">cd /usr/local/nginx/conf</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">vim nginx.conf</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">将如下几行的注释去掉，并将scripts改成$document_root（如红色字体所示）</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px"><span style="color:#505050">&nbsp; &nbsp; &nbsp;location ~ \.php$ {</span><br>
<span style="color:#505050">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; root &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; html;</span><br>
<span style="color:#505050">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; fastcgi_pass &nbsp; 127.0.0.1:9000;</span><br>
<span style="color:#505050">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; fastcgi_index &nbsp;index.php;</span><br>
<span style="color:#505050">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; fastcgi_param &nbsp;SCRIPT_FILENAME </span><span style="color:#ff0000">&nbsp;$document_root</span><span style="color:#505050">$fastcgi_script_name;</span><br>
<span style="color:#505050">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; include &nbsp; &nbsp; &nbsp; &nbsp;fastcgi_params;</span><br>
<span style="color:#505050">&nbsp; &nbsp; &nbsp; &nbsp; }</span><br>
</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px"><span style="color:#505050">修改完后重启nginx（关于如何将nginx添加成系统服务，可参考<a target="_blank" href="http://blog.csdn.net/pang040328/article/details/12876263">http://blog.csdn.net/pang040328/article/details/12876263</a>）</span></span></p>
<hr style="padding:0px; margin:0px; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px">&nbsp;<span style="padding:0px; margin:0px; font-size:24px">&nbsp;2. 安装PHP</span></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
安装依赖库：</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="font-family:Consolas,'Liberation Mono',Courier,monospace; line-height:16px; white-space:pre">yum install libxml2<span style="color:rgb(102,102,102); font-family:宋体,Arial; line-height:26px">libxml2-devel -y</span></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cd /usr/soft</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">wget <a target="_blank" href="http://cn2.php.net/get/php-5.5.4.tar.gz/from/this/mirror">
http://cn2.php.net/get/php-5.5.4.tar.gz/from/this/mirror</a></span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">tar zxvf php-5.5.4.tar.gz</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cd php-5.5.4;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">./configure --enable-fpm --<span style="color:rgb(51,51,51); font-family:Verdana,Tahoma,'BitStream vera Sans',Arial,Helvetica,sans-serif; line-height:17px">with-libdir=lib64（如果是64位系统，需要加入该语句）</span></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">make</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">make install</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cd /usr/local/etc</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cp php-fpm.conf.default php-fpm.conf</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">vim php-fpm.conf, 修改pm.start_servers, pm.min_spare_servers, pm.max_spare_servers. 简单点取消注释即可</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">php: /usr/local/sbin/php-fpm 启动下php~</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">./php-fpm</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<br>
</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
测试php是否安装成功</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
cd /usr/local/nginx/html</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
vim test.php</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
添加如下内容</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
</p>
<div class="dp-highlighter bg_python"><div class="bar"><div class="tools"><b>[python]</b> <a href="#" class="ViewSource" title="view plain" onclick="dp.sh.Toolbar.Command('ViewSource',this);return false;">view plain</a><a href="#" class="CopyToClipboard" title="copy" onclick="dp.sh.Toolbar.Command('CopyToClipboard',this);return false;">copy</a><a href="#" class="PrintSource" title="print" onclick="dp.sh.Toolbar.Command('PrintSource',this);return false;">print</a><a href="#" class="About" title="?" onclick="dp.sh.Toolbar.Command('About',this);return false;">?</a><a href="https://code.csdn.net/snippets/96716" target="_blank" title="在CODE上查看代码片" style="text-indent:0;"><img src="https://code.csdn.net/assets/CODE_ico.png" width="12" height="12" alt="在CODE上查看代码片" style="position:relative;top:1px;left:2px;"></a><a href="https://code.csdn.net/snippets/96716/fork" target="_blank" title="派生到我的代码片" style="text-indent:0;"><img src="https://code.csdn.net/assets/ico_fork.svg" width="12" height="12" alt="派生到我的代码片" style="position:relative;top:2px;left:2px;"></a><div style="position: absolute; left: 635px; top: 2372px; width: 18px; height: 18px; z-index: 99;"><embed id="ZeroClipboardMovie_1" src="http://static.blog.csdn.net/scripts/ZeroClipboard/ZeroClipboard.swf" loop="false" menu="false" quality="best" bgcolor="#ffffff" width="18" height="18" name="ZeroClipboardMovie_1" align="middle" allowscriptaccess="always" allowfullscreen="false" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="id=1&amp;width=18&amp;height=18" wmode="transparent"></div></div></div><ol start="1" class="dp-py"><li class="alt"><span><span>&lt;?php&nbsp;&nbsp;</span></span></li><li class=""><span>&nbsp;echo&nbsp;phpinfo();&nbsp;&nbsp;</span></li><li class="alt"><span>?&gt;&nbsp;&nbsp;</span></li></ol></div><pre code_snippet_id="96716" snippet_file_name="blog_20131204_1_1220664" name="code" class="python" style="display: none;">&lt;?php
 echo phpinfo();
?&gt;</pre><br>
然后在浏览器访问即可。
<p></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<br>
</p>
<hr style="padding:0px; margin:0px; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px">&nbsp;<span style="padding:0px; margin:0px; font-size:24px">3. 安装PHP eaccelerator</span></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px"><span style="padding:0px; margin:0px; font-size:16px">eAccelerator 是一个开源并且免费的 PHP 加速器，优化器，编码器，同时也能够为 PHP提供动态内容缓存。它能够将 PHP 脚本缓存为已编译状态以达到提升 PHP 脚本运行性能的目的，因此传统的预编译几乎被消除。eAccelerator 也能够优化 PHP 脚本以提升 PHP脚本的执行速度。eAccelerator
 可有效降低服务器负载并且提高 PHP 程序速度达 1-10 倍。</span></span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cd /home/trlinux/download;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">wget http://bart.eaccelerator.net/source/0.9.6.1/eaccelerator-0.9.6.1.tar.bz2</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">tar jxvf eaccelerator-0.9.6.1.tar.bz2; cd eaccelerator-0.9.6.1;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">/home/server/php/bin/phpize</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">./configure --enable-eaccelerator=shared --with-php-config=/home/server/php/bin/php-config</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">make</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">make install</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">mkdir /tmp/eaccelerator</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">chmod 0777 /tmp/eaccelerator</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">cp /home/trlinux/download/php-5.3.6/php.inproduction /home/trlinux/server/php/lib/php.ini</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">vim /home/trlinux/server/php/lib/php.ini&nbsp;</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">添加：</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">extension="eaccelerator.so" #可加载的扩展(模块)的目录位置</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.shm_size="16" #</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.cache_dir="/tmp/eaccelerator"&nbsp;</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.enable="1"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.optimizer="1"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.check_mtime="1"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.debug="0"&nbsp;</span>&nbsp;</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.log_file = "/tmp/eaccelerator/eaccelerator.log"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.filter=""</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.shm_max="0"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.shm_ttl="0"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.shm_prune_period="0"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.shm_only="0"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">eaccelerator.compress="1"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
e<span style="padding:0px; margin:0px; font-size:16px">accelerator.compress_level="9"</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
&nbsp;<span style="padding:0px; margin:0px; font-size:16px">php -v&nbsp; 重启php查看eaccelerator是否安装成功</span></p>
<hr style="padding:0px; margin:0px; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px">&nbsp;&nbsp;<span style="padding:0px; margin:0px; font-size:24px">4. 安装mongodb</span>&nbsp;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">关于如何在CentOS系统下安装mongodb,官网已经给出了很详细的安装过程（<a target="_blank" href="http://docs.mongodb.org/manual/tutorial/install-mongodb-on-red-hat-centos-or-fedora-linux/">http://docs.mongodb.org/manual/tutorial/install-mongodb-on-red-hat-centos-or-fedora-linux/</a>），在这里不再赘述。</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; line-height:28px">
<span style="font-size:14px">需要注意的是，在执行如下命令的时候可能会提示连不上服务器</span></p>
<pre style="overflow-x:auto; overflow-y:hidden; padding:10px; background-color:rgb(245,245,245); color:rgb(34,34,34); line-height:1.2em; font-size:1.1em; margin-top:20px; margin-bottom:20px; font-family:Inconsolata,monospace; letter-spacing:0.30000001192092896px">yum install mongo-10gen mongo-10gen-server</pre>
<pre style="overflow-x:auto; overflow-y:hidden; padding:10px; background-color:rgb(245,245,245); color:rgb(34,34,34); line-height:1.2em; font-size:1.1em; margin-top:20px; margin-bottom:20px; font-family:Inconsolata,monospace; letter-spacing:0.30000001192092896px">这多半是网络问题，换个给力点的网络即可。如果把yum源换成国内的话，比如163，这可能会出现checksum不一致的问题（在更新源后，系统需要一定的时间去更新checksum），所以总的来还是换一个给力点的网络下载吧。</pre>
<p></p>
<hr style="padding:0px; margin:0px; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px"><span style="padding:0px; margin:0px; font-size:24px">5. 安装MongoDB的PHP</span></span><a target="_blank" href="http://driver.zol.com.cn/" style="padding:0px; margin:0px; color:rgb(80,80,80)"><span style="padding:0px; margin:0px"><span style="padding:0px; margin:0px; font-size:24px">驱动</span></span></a></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">sudo pecl install mongo&nbsp;</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">安装完之后会显示mongo.so的位置信息</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">Installing '/usr/local/lib/php/extensions/no-debug-non-zts-20121212/mongo.so'<br>
</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
此时查看php的extension目录是不是与上述目录相同，如果不同需要把mongo.so拷贝到相应目录</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
php -i | grep extension</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">vim /etc/php.ini</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">添加extension=mongo.so到最后一行</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px"><span style="color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:16px; line-height:28px">注意，一定要确保php.ini所在路径就是php配置文件所指定的路径：执行php --ini查看php配置文件路径，如果当前路径没有php.ini，则讲php.ini拷贝到指定路径</span><br>
</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">重启php-fpm</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<span style="padding:0px; margin:0px; font-size:16px">service php-fpm restart(关于如何添加php-fpm为系统服务，<span style="color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">可参考</span><a target="_blank" href="http://blog.csdn.net/pang040328/article/details/12876263" style="font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">http://blog.csdn.net/pang040328/article/details/12876263</a>)</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
检测php是否支持mongo</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
php -m | grep mongo</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
如果出现mongo，则说明已经成功安装mongo模块</p>
<hr style="padding:0px; margin:0px; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:0px; clear:both; height:auto; overflow:hidden; color:rgb(80,80,80); font-family:宋体,'Arial Narrow',arial,serif; font-size:14px; line-height:28px">
<br>
</p>

