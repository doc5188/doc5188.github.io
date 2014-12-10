---
layout: post
title: "用coreseek快速搭建sphinx中文分词搜索引擎"
categories: linux
tags: [linux, sphinx, coreseek, sphinx, 搜索引擎]
date: 2014-12-10 14:06:13
---

<p>以下内容基于linux 系统。</p>
<pre class="brush: bash; title: ; notranslate" title="">
yum -y install glibc-common libtool autoconf automake mysql-devel expat-devel

#如果不安装这个 可能下面 sh buildconf.sh会报错！！！
cd /data/src
tar -xjf ../software/autoconf-2.64.tar.bz2
cd autoconf-2.64/
./configure
make &amp;&amp; make install
cd ../

cd /data/software
wget http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz
cd /data/src
tar zxf ../software/coreseek-4.1-beta.tar.gz
cd coreseek-4.1-beta/mmseg-3.2.14
./bootstrap
./configure --prefix=/usr/local/mmseg3
make &amp;&amp; make install
cd ../

cd /data/src/coreseek-4.1-beta/csft-4.1/
sh buildconf.sh
./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --without-mysql
make &amp;&amp; make install
cd ../

##测试mmseg分词，coreseek搜索（需要预先设置好字符集为zh_CN.UTF-8，确保正确显示中文）
cd testpack
cat var/test/test.xml    #此时应该正确显示中文
/usr/local/mmseg3/bin/mmseg -d /usr/local/mmseg3/etc var/test/test.xml
/usr/local/coreseek/bin/indexer -c etc/csft.conf --all
/usr/local/coreseek/bin/search -c etc/csft.conf 网络搜索

#创建sphinx创建索引的脚本：
mkdir -p /data/sh/other
</pre>
<p>vi /data/sh/other/sphinx_update_index.sh</p>
<pre class="brush: bash; title: ; notranslate" title="">
#!/bin/bash
CONFFILE=/usr/local/coreseek/etc/sphinx_index.conf
/bin/sed s#var\/data\/#var\/data2\/#g ${CONFFILE} &gt; ${CONFFILE}.2

mkdir -p /usr/local/coreseek/var/data2
#/usr/local/coreseek/bin/indexer --config ${CONFFILE}.2 --all --rotate
/usr/local/coreseek/bin/indexer --config ${CONFFILE}.2 --all
pkill -9 searchd

sleep 4

/bin/rm -rf /usr/local/coreseek/var/data/
/bin/mv /usr/local/coreseek/var/data2/ /usr/local/coreseek/var/data/

sleep 2

/usr/local/coreseek/bin/searchd --config ${CONFFILE}
</pre>
<p>chmod 755 /data/sh/other/sphinx_update_index.sh</p>
<p>#配置sphinx索引参数配置</p>
<p>vi /usr/local/coreseek/etc/sphinx_index.conf</p>
<pre class="brush: bash; title: ; notranslate" title="">
################################### PHPCMS ############################################
source cc_phpcms
{
	type = mysql
	sql_host = 172.26.11.75  #此处请改成您的真实配置
	sql_user = phpcms  #此处请改成您的真实配置
	sql_pass = 123456   #此处请改成您的真实配置
	sql_db = phpcms   #此处请改成您的真实配置
	sql_port= 3306  #此处请改成您的真实配置
	sql_query_pre = SET SESSION query_cache_type=OFF
	sql_query_pre = SET character_set_client = 'gbk'
	sql_query_pre = SET character_set_connection ='gbk'
	sql_query_pre = SET character_set_results ='utf8'

	sql_query = SELECT `id`,`catid`,`typeid`,`title`,`status`,`updatetime` from `i_news` #此处请改成您的真实配置

	sql_range_step          = 1000
	sql_attr_timestamp      = updatetime
	sql_attr_uint           = catid
	sql_attr_uint           = typeid
	sql_attr_uint           = status

	sql_query_post  =
	sql_ranged_throttle= 0
}
index cc_phpcms
{
	source   = cc_phpcms
	path   = /dev/shm/cc_phpcms   #放这里比较好，因为这里是linux的内存区！
	docinfo   = extern
	mlock   = 0
	enable_star            = 1
	morphology   = none
	stopwords   =
	min_word_len  = 1
	charset_dictpath = /usr/local/mmseg3/etc/   #注意此处
	charset_type        = zh_cn.utf-8           #注意此处
	html_strip = 1
	html_remove_elements = style, script
	html_index_attrs = img=alt,title; a=title;
}

#################################### SETTING ############################################
indexer
{
	mem_limit   = 300M
}
searchd
{
	# address    = 0.0.0.0
	#listen                  = 3312
	#listen                  = 9312
	#listen                  = 9306:mysql41
	port    = 3312
	log     = /usr/local/coreseek/var/log/searchd.log
	query_log   = /usr/local/coreseek/var/log/query.log
	read_timeout  = 5
	max_children  = 30
	pid_file   = /usr/local/coreseek/var/log/searchd.pid
	max_matches   = 1000
	seamless_rotate  = 1
}

</pre>
<p>#接下来实现数据源支持：让sphinx支持MySQL数据源</p>
<pre class="brush: bash; title: ; notranslate" title="">
yum -y install mysql-devel libxml2-devel expat-devel
cd /data/src/coreseek-4.1-beta/csft-4.1/
make clean
sh buildconf.sh
 ./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql
make &amp;&amp; make install
cd ../

</pre>
<p><span style="color: #ff0000;">##如果出现错误提示：“ERROR: cannot find MySQL include files&#8230;&#8230;.To disable MySQL support, use &#8211;without-mysql option.“，可按照如下方法处理：</span><br />
<span style="color: #ff0000;"> ##请找到头文件mysql.h所在的目录，一般是/usr/local/mysql/include，请替换为实际的</span><br />
<span style="color: #ff0000;"> ##请找到库文件libmysqlclient.a所在的目录，一般是/usr/local/mysql/lib，请替换为实际的</span><br />
<span style="color: #ff0000;"> ##configure参数加上：&#8211;with-mysql-includes=/usr/local/mysql/include &#8211;with-mysql-libs=/usr/local/mysql/lib，执行后，重新编译安装</span><br />
#跑sphinx服务脚本<br />
/data/sh/other/sphinx_update_index.sh</p>
<p>好了，如果一切正常，将会顺利看到创建索引的信息如下：<br />
<a href="http://blog.zhuyin.org/wp-content/uploads/2013/04/112.jpg" rel="lightbox[789]" title="【原创】用coreseek快速搭建sphinx中文分词搜索引擎"><img src="http://blog.zhuyin.org/wp-content/uploads/2013/04/112.jpg" alt="112 【原创】用coreseek快速搭建sphinx中文分词搜索引擎" width="600" height="280" class="alignnone size-full wp-image-800" title="【原创】用coreseek快速搭建sphinx中文分词搜索引擎" /></a></p>
<p>下面写一段php代码进行测试（基于sphinx php 的api方式）：</p>
<pre class="brush: php; title: ; notranslate" title="">
		$page = (int)$_GET['page'];
		$page = ($page==0)?1:$page;
		$perpage = 200;
		$start = ($page -1) * $perpage;

		$keyword = urldecode($_GET['key']);

		require_once (S_ROOT . './api/sphinxapi.php');//请改成您的真实路径

 		$groupby = &quot;&quot;;
		$groupsort = &quot;@group desc&quot;;
		$filter = &quot;fieldid&quot;;
		$filtervals = array ();
		$distinct = &quot;&quot;;
		$sortby = &quot;&quot;;
		$cl = new SphinxClient();
		$cl-&gt;SetServer(&quot;localhost&quot;, 3312);
		$cl-&gt;SetWeights(array (
				100,
				1
		));
		$cl-&gt;SetMatchMode(SPH_MATCH_ANY);

		if (count($filtervals)) {
				$cl-&gt;SetFilter($filter, $filtervals);
		}
		if ($groupby) {
				$cl-&gt;SetGroupBy($groupby, SPH_GROUPBY_ATTR, $groupsort);
		}
		$order = 1;
		if ($order == 0) { //按时间倒序
				$cl-&gt;SetSortMode(SPH_SORT_ATTR_DESC, &quot;inputtime&quot;);
		}
		elseif ($order == 1) { //按相关度排序
				$cl-&gt;SetSortMode(SPH_SORT_RELEVANCE);
		}

		if ($distinct) {
				$cl-&gt;SetGroupDistinct($distinct);
		}

		$cl-&gt;SetLimits($start, $perpage, ($limit &gt; 1000) ? $limit : 1000);

		$cl-&gt;SetRankingMode(SPH_RANK_PROXIMITY_BM25);
		$cl-&gt;SetArrayResult(true);
		$res = $cl-&gt;Query($keyword, 'cc_phpcms');
		print_r($res);die;

</pre>
<p>上面的php代码没有做输入的字符过滤，这个请按自己的需要加上。<br />
另外，<br />
/data/sh/other/sphinx_update_index.sh 跑了一次后，<br />
请<br />
vi /data/sh/other/sphinx_update_index.sh<br />
将</p>
<pre class="brush: bash; title: ; notranslate" title="">
#/usr/local/coreseek/bin/indexer --config ${CONFFILE}.2 --all --rotate
/usr/local/coreseek/bin/indexer --config ${CONFFILE}.2 --all
</pre>
<p>变成</p>
<pre class="brush: bash; title: ; notranslate" title="">
/usr/local/coreseek/bin/indexer --config ${CONFFILE}.2 --all --rotate
#/usr/local/coreseek/bin/indexer --config ${CONFFILE}.2 --all
</pre>
<p>也就是将注释调换，这样以后就可以设定个定时计划跑/data/sh/other/sphinx_update_index.sh 脚本了，<br />
跑了/sphinx_update_index.sh 脚本后，自动会用&#8211;rotate的方式重建索引，也就是说新增加的内容也将会被索引到了。</p>
<p>当然，最好的方法还是做个实时索引的配置，下一篇将会重点介绍sphinx的实时索引功能！</p>



<pre>
referer:http://blog.zhuyin.org/789.html
</pre>
