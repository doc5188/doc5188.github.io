---
layout: post
title: "coreseek实时索引更新之增量索引"
categories: linux
tags: [coreseek, coreseek增量索引, 搜索引擎, sphinx]
date: 2014-12-05 17:32:10
---

<p>coreseek实时索引更新有两种选择:</p>
<p>1.使用基于磁盘的索引，手动分区，然后定期重建较小的分区（被称为“增量”）。通过尽可能的减小重建部分的大小，可以将平均索引滞后时间降低到30~60秒.在0.9.x版本中，这是唯一可用的方法。在一个巨大的文档集上，这可能是最有效的一种方法</p>
<p>2.版本1.x（从版本1.10-beta开始）增加了实时索引（简写为Rt索引）的支持，用于及时更新全文数据。在RT索引上的更新，可以在1~2毫秒（0.001-0.002秒）内出现在搜索结果中。然而，RT实时索引在处理较大数据量的批量索引上效率并不高。</p>
<p>这篇我们只要是增量索引</p>
<p>基本思路是设置两个数据源和两个索引，对很少更新或根本不更新的数据建立主索引，而对新增文档建立增量索引</p>
<p>在配置文件中定义了主索引和增量索引之后,不能直接用indexer –config d:\coreseek\csft.conf –all,再添加数据到数据库中,再用indexer –config d:\coreseek\csft.confg main delta –rotate来弄(我居然这样弄了两次)。正确的步骤为:</p>
<p>1.<span style="color:black">创建主索引</span><span style="color:black">:</span><span style="color:#ff0000">indexer –cd:\coreseek\csft.conf --all</span></p>
<p>2.<span style="color:black">添加数据</span></p>
<p>3.<span style="color:black">再创建增量索引</span><span style="color:black">:</span><span style="color:#ff0000">indexer –cd:\coreseek\csft.conf delta --rotate</span></p>
<p>4.<span style="color:black">合并索引</span><span style="color:black">:<span style="color:#ff0000">indexer –cd:\coreseek\csft.conf --merge main delta –rotate</span>(<span style="color:black">为了防止多个关键字指向同一个文档加上</span><span style="color:#ff0000">--merge-dst-range
 deleted 0 0</span>)</span></p>
<p><span style="color:black">增量配置文件如下</span>:</p>
<pre class="plain" name="code">#增量索引
source main
{
    type                    = mysql
    sql_host                = localhost
    sql_user                = root
    sql_pass                = 123456
    sql_db                  = hottopic
    sql_port                = 3306
    sql_query_pre           = SET NAMES utf8
    sql_query_pre	    = replace into sph_counter select 1,max(id) from st_info
    sql_query_range	    = select 1,max(id) from st_info
    sql_range_step          = 1000

    sql_query               = SELECT id, pubDate, title, description,nav_id,rss_id FROM st_info where id&gt;=$start and id &lt;=$end and \
				id &lt;=(select max_doc_id from sph_counter where counter_id=1)
    sql_attr_uint           = nav_id          
    sql_attr_uint	    = rss_id
    sql_attr_timestamp      = pubDate 
}

source delta : main
{
    sql_query_pre           = SET NAMES utf8
    sql_query		    = SELECT id, pubDate, title, description,nav_id,rss_id FROM st_info where id&gt;=$start and id &lt;=$end and \
				id &gt;(select max_doc_id from sph_counter where counter_id=1)
    sql_query_post_index    = replace into sph_counter select 1,max(id) from st_info
}

#index定义
index main
{
    source              = main            
    path                = D:/coreseek/coreseek-4.1-win32/var/data/mysqlInfoSPHMain 
    docinfo             = extern
    mlock               = 0
    morphology          = none
    min_word_len        = 1
    html_strip          = 0
    stopwords		=

    charset_dictpath    =  D:/coreseek/coreseek-4.1-win32/etc    
    charset_type        = zh_cn.utf-8
}

index delta : main
{
    source		= delta
    path                = D:/coreseek/coreseek-4.1-win32/var/data/mysqlInfoSPHDelta
   
}

#全局index定义
indexer
{
    mem_limit            = 128M
}

#searchd服务定义
searchd
{
    listen			= 127.0.0.1:9312
    read_timeout		= 5
    max_children		= 30
    max_matches			= 1000
    seamless_rotate		= 0
    preopen_indexes		= 0
    unlink_old			= 1
    pid_file			= D:/coreseek/coreseek-4.1-win32/var/log/searchd_mysqlInfoSph.pid
    log				= D:/coreseek/coreseek-4.1-win32/var/log/searchd_mysqlInfoSph.log
    query_log			= D:/coreseek/coreseek-4.1-win32/var/log/query_mysqlInfoSph.log
    binlog_path			=          
    compat_sphinxql_magics	= 0
}</pre>
<p><br>
<span style="color:#ff0000">注意问题</span><span style="color:black">:</span><span style="color:black">如果我的主索引为</span><span style="color:black">50W</span><span style="color:black">条我前天建立的</span><span style="color:black">,</span><span style="color:black">我昨天增加了</span><span style="color:black">10W</span><span style="color:black">条的数据</span><span style="color:black">,</span><span style="color:black">并且建立了增量索引还和主索引合并了</span><span style="color:black">,</span><span style="color:black">我今天增加了</span><span style="color:black">10W</span><span style="color:black">的数据并且建立增量索引而且也和主索引合并了</span><span style="color:black">,</span><span style="color:black">在这两天内我是没有重新建立主索引的</span><span style="color:black">,</span><span style="color:black">问题来了：昨天是对</span><span style="color:black">10W</span><span style="color:black">数据进行建立</span><span style="color:black">,</span><span style="color:black">今天就是</span><span style="color:black">20W</span><span style="color:black">的数据建立</span><span style="color:black">,</span><span style="color:black">并且这</span><span style="color:black">20W</span><span style="color:black">数据中有</span><span style="color:black">10W</span><span style="color:black">数据其实在主索引中了</span><span style="color:black">,</span><span style="color:black">这个是非常可怕的</span><span style="color:black">?</span><span style="color:black">解决方案:</span></p>
<p>1.一天建立一次主索引</p>
<p>2.在不考虑重新建立主索引的时候,在添加增量索引的时候用<span style="color:#ff0000">sql_query_post_index</span>来改变maxid&#20540;我是windows下面手动输入代码成功(不知道用脚本的时候会怎么样)</p>
<p>3.在不考虑重新建立主索引的时候,在合并索引的时候,用脚本链接数据库直接去修改(可以查看:http://banu.blog.163.com/blog/static/2314648201092911412539)</p>
<p>&nbsp;</p>
<p>&nbsp;</p>


<pre>
referer:http://blog.csdn.net/ms_x0828/article/details/7679229
</pre>
