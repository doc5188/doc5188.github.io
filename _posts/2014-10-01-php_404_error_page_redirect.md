---
layout: post
title: "php 404 错误 页面 重定向"
categories: php
tags: [php, apache,.htaccess]
date: 2014-10-01 11:45:35
---

<div id="zoomtext" class="textbox-content">
<p>这样做的<span style="color: #ff0000;">好处一个是很友好</span>
，另一个是对于你的网站会更安全些，如果没设置，别人在你的网址后随便输入一个路径，会显示404错误，并且会显示
你的服务器版本号，服务器配置一目了然，为了避免这种情况，可以设置错误页面。</p>
<p>当出现404错误，即找不到网页时，把访问者导入到一个事先
定义好的错误页面。</p>
<p>修改 <span style="color: #ff0000;">httpd.conf</span>
</p>
<p>找到：<br>
#ErrorDocument 500 "The 
server made a boo boo."<br>
<span style="color: #ff0000;">#ErrorDocument 404 /missing.html</span>
<br>
#ErrorDocument
 404 "/cgi-bin/missing_handler.pl"<br>
#ErrorDocument 402 xxxxxxx<br>
<br>
httpd.conf
中的这一部分,#ErrorDocument 404 /missing.html 是显示错误页信息的,去掉前面的#<br>
<br>
修改为 
ErrorDocument 404 /<span style="color: #ff0000;">error.htm</span>
</p>
<p>其中error.htm为站点根目录下和error目录下的一个错误文件，需
要你自己建立。当发生404错误时，进入error.htm页面，可以提示网页没有找到。这样就不可能看到你的服务器软件信息了。也可以设置其它的错误导
向的页面，具体http响应错误编号请查阅相关资料。</p>
<p><br>
<span style="color: #ff0000;">重新启动apache</span>
，如果没意外，此时已经安装成功，把静态页面放到站点根
目录和error目录下,看能不能成功解析。</p>
<p><br>
随便输入一个:http://localhost/abcd.htm，看是不是导向你
设置的404错误，即error.htm错误页面.!</p>
</div>

<pre>
来源: http://blog.csdn.net/q356309936/article/details/5912706
</pre>
