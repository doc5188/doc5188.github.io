---
layout: post
title: "CentOS安装配置MongoDB及PHP MongoDB 扩展安装配置"
categories: linux
tags: [mongodb安装]
date: 2014-10-17 23:12:38
---

<p>一，登录vps，使用wget下载mongodb官网上的安装文件。</p>
<table>
<tbody>
<tr>
<td class="number"><code>1</code></td>
<td class="content"><code class="plain">wget&nbsp;<a href="http://fastdl.mongodb.org/linux/mongodb-linux-i686-2.0.3.tgz">http://fastdl.mongodb.org/linux/mongodb-linux-i686-2.0.3.tgz</a></code></td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<p>好吧，我承认我秒杀它了。见图，37.3M/s，神速啊！<br><a href="/upload/images/download-mongodb.jpg"><img class="alignnone  wp-image-290" title="download-mongodb" src="/upload/images/download-mongodb.jpg" alt="" height="246" width="575"></a></p>
<p>二、解压、安装、运行</p>
<div id="highlighter_687423" class="syntaxhighlighter notranslate ">
<div class="bar        show">
<div class="toolbar"><a class="item viewSource" title="view source" href="http://gevin.me/289.html#viewSource"><br></a>
<div class="item copyToClipboard">&nbsp;</div>








</div>
</div>
<div class="lines">
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>1</code></td>
<td class="content"><code class="functions">tar</code>&nbsp;<code class="plain">-xvf mongodb-linux-i686-2.0.3.tgz&nbsp;&nbsp;</code><code class="comments">#解压</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt2">
<table>
<tbody>
<tr>
<td class="number"><code>2</code></td>
<td class="content"><code class="functions">mv</code>&nbsp;<code class="plain">mongodb-linux-i686-2.0.3.tgz /usr/</code><code class="functions">local</code><code class="plain">/mongodb</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>3</code></td>
<td class="content"><code class="functions">mkdir</code>&nbsp;<code class="plain">-p /data/db&nbsp;&nbsp;</code><code class="comments">#新建mongodb数据文件存放目录</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt2">
<table>
<tbody>
<tr>
<td class="number"><code>4</code></td>
<td class="content"><code class="functions">mkdir</code>&nbsp;<code class="plain">-p /data/logs&nbsp;</code><code class="comments">#新建log文件存放目录</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>5</code></td>
<td class="content"><code class="functions">cd</code>&nbsp;<code class="plain">/usr/</code><code class="functions">local</code><code class="plain">/mongodb/bin</code></td>








</tr>








</tbody>








</table>








</div>








</div>








</div>
<p>新建配置文件，mongodb支持把参数写进配置文件，然后以配置文件的配置来启动，我们此处也使用此方式。</p>
<div id="highlighter_614693" class="syntaxhighlighter notranslate ">
<div class="lines">
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>1</code></td>
<td class="content"><code class="functions">vi</code>&nbsp;<code class="plain">mongodb.conf</code></td>








</tr>








</tbody>








</table>








</div>








</div>








</div>
<p>内容如下：</p>
<div id="highlighter_343808" class="syntaxhighlighter notranslate ">
<div class="lines">
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>1</code></td>
<td class="content"><code class="plain">dbpath = /data/db&nbsp;</code><code class="comments">#数据文件存放目录</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt2">
<table>
<tbody>
<tr>
<td class="number"><code>2</code></td>
<td class="content"><code class="plain">logpath = /data/logs/mongodb.log&nbsp;</code><code class="comments">#日志文件存放目录</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>3</code></td>
<td class="content"><code class="plain">port = 27017&nbsp;&nbsp;</code><code class="comments">#端口</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt2">
<table>
<tbody>
<tr>
<td class="number"><code>4</code></td>
<td class="content"><code class="plain">fork =&nbsp;</code><code class="functions">true</code>&nbsp;&nbsp;<code class="comments">#以守护程序的方式启用，即在后台运行</code></td>








</tr>








</tbody>








</table>








</div>








</div>








</div>
<p>启动Mongo程序，使用配置文件mongodb.conf定义的参数启动</p>
<div id="highlighter_31959" class="syntaxhighlighter notranslate ">
<div class="lines">
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>1</code></td>
<td class="content"><code class="plain">./mongod --config mongodb.conf</code></td>








</tr>








</tbody>








</table>








</div>








</div>








</div>
<p>三、测试，OK，安装成功！</p>
<p><a href="/upload/images/mongo-run.jpg"><img class="alignnone  wp-image-291" title="mongo-run" src="/upload/images/mongo-run.jpg" alt="" height="203" width="581"></a></p>
<p>四、关闭Http访问端口，mongodb安装完之后，默认是启用了Http的访问端口，比mongodb监听的端口大1000，即28017。</p>
<p>通过访问http://gevin.me:28017/可以查看到mongodb启动的一些信息，同时也对mongodb运行的统计情况进行监控。在使用mongodb过程中，我们可以使用参数将该功能禁用掉。</p>
<p>修改配置文件mongodb.conf，增加参数选项：nohttpinterface = true 即可。</p>
<p>完整mongodb.conf 如下：</p>
<div id="highlighter_907466" class="syntaxhighlighter notranslate ">
<div class="lines">
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>1</code></td>
<td class="content"><code class="plain">dbpath = /data/db&nbsp;</code><code class="comments">#数据文件存放目录</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt2">
<table>
<tbody>
<tr>
<td class="number"><code>2</code></td>
<td class="content"><code class="plain">logpath = /data/logs/mongodb.log&nbsp;</code><code class="comments">#日志文件存放目录</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt1">
<table>
<tbody>
<tr>
<td class="number"><code>3</code></td>
<td class="content"><code class="plain">port = 27017&nbsp;&nbsp;</code><code class="comments">#端口</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt2">
<table>
<tbody>
<tr>
<td class="number"><code>4</code></td>
<td class="content"><code class="plain">fork =&nbsp;</code><code class="functions">true</code>&nbsp;&nbsp;<code class="comments">#以守护程序的方式启用，即在后台运行</code></td>








</tr>








</tbody>








</table>








</div>
<div class="line alt1 highlighted">
<table>
<tbody>
<tr>
<td class="number"><code>5</code></td>
<td class="content"><code class="plain">nohttpinterface =&nbsp;</code><code class="functions">true</code></td>








</tr>








</tbody>








</table>








</div>








</div>








</div>







</div>
<div class="postTitle">&nbsp;</div>
<div class="postTitle">&nbsp;</div>
<div class="postTitle">&nbsp;</div>
<div class="postTitle">&nbsp;</div>
<div class="postTitle"><a id="cb_post_title_url" class="postTitle2" href="http://www.cnblogs.com/liupeizhi/archive/2012/10/05/MongoDB_PHP.html">PHP MongoDB 扩展安装配置</a></div>
<div id="cnblogs_post_body">
<p>近日对MongoDB比较感兴趣，在linux下部署了一套LAMP,想把MongoDB加进来，下面进入正题：</p>
<p>1.确保安装好LAMP环境，假设php安装目录：/usr/local/php5</p>
<p>2.下载<a href="https://github.com/mongodb/mongo-php-driver/downloads%C3%AF%C2%BC%C2%8C">https://github.com/mongodb/mongo-php-driver/downloads，</a>我下载的是mongodb-mongo-php-driver-1.3.0beta2-112-g0878db0.tar.gz 传到服务器上</p>
<p>3.到服务器上，解压mongodb-mongo-php-driver-1.3.0beta2-112-g0878db0.tar.gz，进入目录，执行命令：/usr/local/php5/bin/phpize,会输出如下内容</p>
<div class="cnblogs_code">
<pre>Configuring for:
PHP Api Version:         20090626
Zend Module Api No:      20090626
Zend Extension Api No:   220090626</pre>
</div>
<p>说明命令正常，如果出错，应该是缺包，yum install XXX</p>
<p>4.执行configure：./configure --with-php-config=/usr/local/php5/bin/php-config</p>
<p>5.make =&gt;make test=&gt;make install最后输出：</p>
<p>Installing shared extensions:&nbsp;&nbsp;&nbsp;&nbsp; /usr/local/php5/lib/php/extensions/no-debug-non-zts-20090626/</p>
<p>进入这个目录看一下是否生成一个mongo.so的文件。</p>
<p>&nbsp;</p>
<p>安装完毕，下面需要设置一下php配置文件，在php.ini文件的最后加上这两句：</p>
<div class="cnblogs_code">
<pre>extension_dir = "/usr/local/php5/lib/php/extensions/no-debug-non-zts-20090626/"

extension=mongo.so</pre>
</div>
<p>访问 phpinfo()页面，如看到下面内容，大功告成！</p>
<p><img src="/upload/images/2012100522190614.png" alt=""></p>
<p>&nbsp;</p>
<p>写一个测试的页面，testMongo.jsp:</p>
<pre>&lt;?php

$mongo = new Mongo();
$dbs = $mongo-&gt;listDBs();
print_r($dbs);

?&gt;</pre>
<p>访问页面输出类似如下内容：</p>
<p>Array ( [databases] =&gt; Array ( [0] =&gt; Array ( [name] =&gt; local [sizeOnDisk] =&gt; 1090519040 [empty] =&gt; ) ) [totalSize] =&gt; 1090519040 [ok] =&gt; 1 )</p>
