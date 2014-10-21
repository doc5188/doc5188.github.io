---
layout: post
title: "（原创）Linux下nginx支持.htaccess文件实现伪静态的方法！"
categories: linux
tags: [nginx rewrite]
date: 2014-10-21 09:22:03
---

在Google上搜索的资料很多人都说nginx目前不支持.htaccess文件，我按照nginx的规则试验了一下，结果发现nginx是完全支持.htaccess文件的！</strong></p>
<p>方法如下：</p>
<p><span id="more-942"></span></p>
<p>1. 在需要使用.htaccess文件的目录下新建一个.htaccess文件，<br>
如本人的一个Discuz论坛目录：</p>
<blockquote><p>vim /var/www/html/168pc/bbs/.htaccess</p></blockquote>
<p>2. 在里面输入规则，我这里输入Discuz的伪静态规则：</p>
<blockquote><p># nginx rewrite rule<br>
rewrite ^(.*)/archiver/((fid|tid)-[w-]+.html)$ $1/archiver/index.php?$2 last;<br>
rewrite ^(.*)/forum-([0-9]+)-([0-9]+).html$ $1/forumdisplay.php?fid=$2&amp;page=$3 last;<br>
rewrite ^(.*)/thread-([0-9]+)-([0-9]+)-([0-9]+).html$ $1/viewthread.php?tid=$2&amp;extra=page%3D$4&amp;page=$3 last;<br>
rewrite ^(.*)/profile-(username|uid)-(.+).html$ $1/viewpro.php?$2=$3 last;<br>
rewrite ^(.*)/space-(username|uid)-(.+).html$ $1/space.php?$2=$3 last;<br>
rewrite ^(.*)/tag-(.+).html$ $1/tag.php?name=$2 last;<br>
# end nginx rewrite rule</p></blockquote>
<p>wq保存退出。</p>
<p>3. 修改nginx配置文件：</p>
<blockquote><p>vim /etc/nginx/nginx.conf</p></blockquote>
<p>4. 在需要添加伪静态的虚拟主机的server{}中引入.htaccess文件，如图所示：<br>
<a href="/upload/images/htaccess.jpg"><img class="alignnone size-full wp-image-943" title="htaccess" src="/upload/images/htaccess.jpg" alt="" height="322" width="439"></a></p>
<p>include /var/www/html/168pc/bbs/.htaccess;（把这个改成你.htaccess文件的具体位置）</p>
<p>wq保存退出。</p>
<p>5. 重新加载nginx配置文件：</p>
<blockquote><p>/etc/init.d/nginx reload</p></blockquote>
<p>重新打开网页看看，如果伪静态正常就证明你的rewrite rule语法是正确的。<br>
<a href="/upload/images/htaccess2.jpg"><img class="alignnone size-full wp-image-944" title="htaccess2" src="/upload/images/htaccess2.jpg" alt="" height="412" width="562"></a><br>
正常，完毕！</p>
<p>补充：偶在网上发现了个可以在线将Apache Rewrite伪静态规则自动转换为Nginx Rewrite网页。大家可以试试看。</p>
<p><a rel="nofollow" target="_blank" href="http://www.anilcetin.com/convert-apache-htaccess-to-nginx/" onclick="javascript:_gaq.push(['_trackPageview','/yoast-ga/outbound-article/http://www.anilcetin.com/convert-apache-htaccess-to-nginx/']);">http://www.anilcetin.com/convert-apache-htaccess-to-nginx/</a></p>
<p>此地址里面的内容包含可以完成上面说的略做修改的功能。就是把.htaccess中的规则自动转换成nginx下面可用的规则。</p>
<p><span style="color: rgb(255, 0, 0);">总结：.htaccess文件本来是apache专用的分布式配置文件，提供了针对每个目录改变配置的方法，即在一个特定的目录中放置一个包含指令的文件，其中的指令作用于此目录及其所有子目录。其实修改一下，nginx也可使用.htaccess文件实现多种功能。实现伪静态只是.htaccess的其中一个用途，.htaccess还可以做很多的用途，如过滤访问IP，设置web目录访问权限、密码等。</span>







<pre>
referer: http://www.ha97.com/942.html
</pre>
