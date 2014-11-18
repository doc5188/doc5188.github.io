---
layout: post
title: "Linux下编译安装Sphinx、中文分词coreseek及PHP的sphinx扩展"
categories: linux 
tags: [shpinx, coreseek]
date: 2014-11-18 17:34:34
---

<p>Linux环境为：CentOS5.5、Ubuntu12.04</p>
<h3><strong>1、软件下载</strong></h3>
<p><a href="http://pan.baidu.com/s/1d5uwY" target="_blank">sphinx-2.1.3</a></p>
<p><a href="http://pan.baidu.com/s/17X1z0" target="_blank">coreseek-4.1</a></p>
<h3><strong>2、安装 sphinx</strong></h3>
<pre>tar zxvf sphinx-2.1.3.tar.gz //解压sphinx包
cd sphinx-2.1.3
./configure --prefix=/usr/local/sphinx --with-mysql=/usr/local/mysql/</pre>
<p>--prefix：指定 sphinx 的安装路径<br>
--with-mysql：指定 mysql 安装路径</p>
<pre>sudo make &amp;&amp; make install</pre>
<p>编译并安装</p>
<p>安装成功之后，sphinx 会形成三个命令：</p>
<pre>indexer 创建索引命令
searchd 启动进程命令
search 命令行搜索命令</pre>
<p>注：上述命令默认在/usr/local/sphinx/bin目录下</p>
<h3><strong>3、配置 sphinx及使用</strong></h3>
<pre>cd /usr/local/sphinx/etc</pre>
<p>进入 sphinx 的 etc 目录下</p>
<pre>sudo cp sphinx.conf.dist sphinx.conf</pre>
<p>拷贝一份配置文件，并且命名为 sphinx.conf。</p>
<p>将该目录下的example.sql文件导入本地数据库名为test的数据库中。</p>
<p>修改配置信息，将其中数据库连接信息修改为你的本地数据库信息。</p>
<p>然后使用如下命令导入数据并生成索引：</p>
<pre>$ cd /usr/local/sphinx/etc
$ sudo /usr/local/sphinx/bin/indexer --all</pre>
<p>如果执行indexer命令报错：</p>
<pre>ERROR: index 'test1stemmed': sql_connect: Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock'</pre>
<p>则可能是因为mysql.sock的位置问题，在本机中，改位置是/tmp/mysql.sock（与安装mysql时设置有关），在sphinx.conf中取消这一行的注释即可（去掉前面的#号）：</p>
<pre>#sql_sock &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= /tmp/mysql.sock</pre>
<p>再次执行上述indexer命令，一切正常。</p>
<p>执行查询的话可以使用如下指令：</p>
<pre>$ cd /usr/local/sphinx/etc
$ sudo /usr/local/sphinx/bin/search test</pre>
<p>在执行search搜索过程中可能报错：</p>
<pre>index 'test1': search error: query too complex, not enough stack (thread_stack=-2665032K or higher required).</pre>
<p>我试着在sphinx.conf中的searchd模块中修改thread_stack的值，但没有解决问题，后来注释掉source src1中的如下这行</p>
<pre>#sql_query_info &nbsp; &nbsp; &nbsp; &nbsp; = SELECT * FROM documents WHERE id=$id</pre>
<p>再执行search命令，就OK了。</p>
<p>后台启动sphinx使用如下指令：</p>
<pre>$ cd /usr/local/sphinx/etc
$ sudo /usr/local/sphinx/bin/searchd</pre>
<p>使用php脚本执行搜素命令，可使用如下指令：</p>
<pre>$ cd sphinx/api
$ php test.php test</pre>
<p>输入结果如下：</p>
<pre>Query 'test ' retrieved 3 of 3 matches in 0.022 sec.
Query stats:
'test' found 10 times in 6 documents

Matches:
1. doc_id=1, weight=101, group_id=1, date_added=2014-01-20 10:07:37
2. doc_id=2, weight=101, group_id=1, date_added=2014-01-20 10:07:37
3. doc_id=4, weight=1, group_id=2, date_added=2014-01-20 10:07:37</pre>
<h3><strong>4、安装 coreseek</strong></h3>
<pre>tar zxvf coreseek-4.1.tar.gz</pre>
<p>解压会出现两个目录：csft-4.1、mmseg-3.2.14</p>
<p><strong>先安装 mmseg</strong></p>
<pre>cd mmseg-3.2.14/
./configure --prefix=/usr/local/mmseg</pre>
<p>编译如果出现错误：“config.status: error: cannot find input file: src/Makefile.in”</p>
<p>解决方案：</p>
<pre>sudo apt-get install automake
aclocal
libtoolize --force 我运行后有一个错误，没管它。
automake --add-missing
autoconf
autoheader
make clean
./configure --prefix=/usr/local/mmseg
make
sudo make install</pre>
<p><strong>安装 csft(coreseek)</strong></p>
<pre>cd csft-4.1/
sh buildconf.sh
./configure --prefix=/usr/local/coreseek --with-mysql=/usr/local/mysql/ --with-mmseg=/usr/local/mmseg/ --with-mmseg-includes=/usr/local/mmseg/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg/lib/ 
sudo make &amp;&amp; make install</pre>
<p>安装完成之后和sphinx安装后一样，需要导入coreseek/etc/example.sql文件到本地数据库，然后拷贝sphinx.conf.dist到csft.conf，修改其中数据库用户名及密码,测试出错和sphinx中出错解决办法一样。</p>
<p><strong>使用 sphinx 需要做以下几件事</strong></p>
<p>1.有数据；</p>
<p>2.建立 sphinx 配置文件；</p>
<p>3.生成索引；</p>
<p>4.启动 searchd 服务进程，默认是9312</p>
<p>5.用 PHP 去连接 sphinx 服务</p>
<p><strong>启动 sphinx</strong></p>
<pre>cd /usr/local/coreseek/bin/
./searchd</pre>
<p>启动命令</p>
<p>searchd 命令参数介绍：</p>
<p>-c 指定配置文件</p>
<p>--stop 停止服务</p>
<p>--pidfile 用来显式指定一个 PID 文件</p>
<p>-p 指定端口</p>
<h3><strong>5、php 安装 sphinx</strong>&nbsp;扩展</h3>
<pre>sudo pecl install sphinx</pre>
<p>如果出现错误：“configure: error: Cannot find libsphinxclient headers”</p>
<p>解决方法：</p>
<pre>cd coreseek-4.1/csft-4.1/api/libsphinxclient/
./configure --prefix=/usr/local/libsphinxclient
sudo make &amp;&amp; make install</pre>
<p>解决完毕！</p>
<p>回去接着执行</p>
<pre>./configure --with-php-config=/usr/local/php/bin/php-config --with-sphinx=/usr/local/libsphinxclient</pre>
<pre>sudo make &amp;&amp; make install</pre>
<p>出现类似“Installing shared extensions: /usr/lib/php5/20090626/sphinx.so”，表示成功。</p>
<p>可以进入该目录下会发现生成了一个 sphinx.so 文件</p>
<p>在 php.ini 中加载该 so 文件</p>
<p>extension=/usr/lib/php5/20090626/sphinx.so</p>
<p>重启 apache ，phpinfo() 中出现这个表明成功。</p>
<p><img class="box" alt="sphinx" src="/upload/images/sphinx.png" data-pinit="registered" height="126" width="616"></p>
