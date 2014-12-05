---
layout: post
title: "coreseek 增量索引模拟实时索引"
categories: linux 
tags: [coreseek, sphinx, 搜索引擎]
date: 2014-12-05 17:20:30
---

<p style="font-family:Simsun; font-size:14px">有这么一种常见的情况：整个数据集非常大，以至于难于经常性的重建索引，但是每次新增的记录却相当地少。一个典型的例子是：一个论坛有1000000个已经归档的帖子，但每天只有1000个新帖子。</p>
<p style="font-family:Simsun; font-size:14px">在这种情况下可以用所谓的“主索引＋增量索引”（main&#43;delta）模式来实现“近实时”的索引更新。</p>
<p style="font-family:Simsun; font-size:14px">这种方法的基本思路是设置两个数据源和两个索引，对很少更新或根本不更新的数据建立主索引，而对新增文档建立增量索引。在上述例子中，那1000000个已经归档的帖子放在主索引中，而每天新增的1000个帖子则放在增量索引中。增量索引更新的频率可以非常快，而文档可以在出现几分种内就可以被检索到。</p>
<p style="font-family:Simsun; font-size:14px">确定具体某一文档的分属那个索引的分类工作可以自动完成。一个可选的方案是，建立一个计数表，记录将文档集分成两部分的那个文档ID，而每次重新构建主索引时，这个表都会被更新。</p>
<p style="font-family:Simsun; font-size:14px">第一步要先创建增量索引表sph_counter</p>
<p style="font-family:Simsun; font-size:14px"></p>
<pre class="programlisting" style="padding:0.5em; margin-left:2em; margin-right:2em">CREATE TABLE sph_counter
(
    counter_id INTEGER PRIMARY KEY NOT NULL,
    max_doc_id INTEGER NOT NULL
);</pre>
第二步：修改原来的索引配置
<p></p>
<p style="font-family:Simsun; font-size:14px"><pre name="code" class="plain">source mysql
{
    type                = mysql

    sql_host                = localhost
    sql_user                = root
    sql_pass                = mfy
    sql_db                = zlk
    sql_port                = 3306
    sql_query_pre            = SET NAMES utf8
    # 下面2行是新增的内容 
    sql_query_pre = REPLACE INTO sph_counter SELECT 1,MAX(id) FROM picture_info
    sql_query = SELECT * FROM picture_info \
                WHERE id&lt;=( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )
    
#这还是以前sql_query现在已经不用了sql_query                = SELECT id,pic_id,city,captionwriter,countryname,title,description,contenttype,generator,author,keyword,language,datecreatedline  FROM picture_info
                                                              #sql_query第一列id需为整数
                                                              #title、content作为字符串/文本字段，被全文索引
   # sql_attr_uint            = id           #从SQL读取到的值必须为整数
   sql_attr_uint            = pic_id           #从SQL读取到的值必须为整数
   sql_attr_timestamp        = datecreatedline #从SQL读取到的值必须为整数，作为时间属性
   # sql_attr_str2ordinal	= title

}
source delta:mysql
{#这里是新增的增量索引源
        sql_query_pre = SET NAMES utf8
        sql_query = SELECT * FROM picture_info \
                WHERE id&gt;( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )
        #sql_query_post_index    = replace into sph_counter select 1,max(id) from picture_info
}
#index定义
index mysql
{
    source            = mysql             #对应的source名称
    path            = /usr/local/coreseek/var/data/mysql

    docinfo            = extern
    mlock            = 0
    morphology        = none
    min_word_len        = 1
    min_infix_len =1
    html_strip                = 0
    charset_dictpath = /usr/local/mmseg3/etc/    #BSD、Linux环境下设置，/符号结尾
    #charset_dictpath = etc/                        #Windows环境下设置，/符号结尾
    charset_type        = zh_cn.utf-8
}
index delta:mysql
{#这是新增的增量索引
        source          = delta
        path            =       /usr/local/coreseek/var/data/delta
}
  
#全局index定义  
indexer  
{  
    mem_limit           = 2G    
}   
   
searchd  
{  
       listen                                   = 9312  
       max_matches                         	= 10000  
       pid_file                                 = /usr/local/coreseek/var/log/searchd_mysql.pid  
       log                                      = /usr/local/coreseek/var/log/searchd_mysql.log  
       query_log                                = /usr/local/coreseek/var/log/query_mysql.log  
}  </pre><br>
<br>
</p>
<br>
<br>
<p></p>
<p></p>
<p style="font-family:Simsun; font-size:14px"><span style="font-family:Simsun; font-size:14px">执行索引：<span style="color:#ff0000">/usr/local/coreseek/bin/indexer -c /var/htdocs/zlk/sphinx/mysql.conf --all --rotate</span></span><br>
</p>
<p style="font-family:Simsun; font-size:14px">执行增量索引：<span style="color:#ff0000">/usr/local/coreseek/bin/indexer -c /var/htdocs/zlk/sphinx/mysql.conf delta --rotate&nbsp;</span></p>
<p style="font-family:Simsun; font-size:14px"><br>
合并索引：<span style="color:#ff0000">/usr/local/coreseek/bin/indexer -c /var/htdocs/zlk/sphinx/mysql.conf --merge mysql delta --rotate --merge-dst-range deleted 0 0</span><br>
<br>
</p>
<p style="font-family:Simsun; font-size:14px">写两个脚本一个是执行增量索引并合并索引的另一个是重建索引的。</p>
<p style="font-family:Simsun; font-size:14px">delta.sh:执行增量索引</p>
<p style="font-family:Simsun; font-size:14px"></p>
<pre name="code" class="plain">#!/bin/sh 
/usr/local/coreseek/bin/indexer -c /var/htdocs/zlk/sphinx/mysql.conf delta --rotate 
</pre>
<p>merge.sh ：合并索引</p>
<p><pre name="code" class="plain">#!/bin/sh
/usr/local/coreseek/bin/indexer -c /var/htdocs/zlk/sphinx/mysql.conf --merge mysql delta --rotate --merge-dst-range deleted 0 0</pre><br>
</p>
<p>main.sh：重建索引</p>
<p></p>
<p style="font-family:Simsun; font-size:14px"></p>
<pre name="code" class="plain">#!/bin/sh 
/usr/local/coreseek/bin/indexer -c /var/htdocs/zlk/sphinx/mysql.conf --all --rotate</pre><br>
最后写个计划任务每隔一分钟执行一遍delta.sh每五分钟执行一遍merge.sh每天1:30执行main.sh
<p></p>
<p style="font-family:Simsun; font-size:14px">执行命令：crontab -e&nbsp;</p>
<p style="font-family:Simsun; font-size:14px">写入下面两行</p>
<p style="font-family:Simsun; font-size:14px">*/1 * * * * /bin/sh /var/htdocs/zlk/sphinx/delta.sh</p>
<p style="font-family:Simsun; font-size:14px"><span style="font-family:Simsun; font-size:14px">*/5 * * * * /bin/sh /var/htdocs/zlk/sphinx/merge.sh</span><br>
30 1 * * * /bin/sh /var/htdocs/zlk/sphinx/main.sh<br>
<br>
</p>
<p style="font-family:Simsun; font-size:14px"><br>
</p>
<p style="font-family:Simsun; font-size:14px"><br>
</p>
<p style="font-family:Simsun; font-size:14px"><br>
</p>



<pre>
referere:http://blog.csdn.net/liushuai_andy/article/details/9138455
</pre>
