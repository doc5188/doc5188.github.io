---
layout: post
title: "Coreseek 增量索引"
categories: linux
tags: [coreseek, 搜索引擎]
date: 2014-12-05 17:25:24
---

如果在第一次建立索引的时候数据量较大比如：100W，而每天新增的仅仅在1W左右，那么要重新进行索引需要花费的代价就太大了，所以只需要对新添加的数据进行操作建立索引即可。


* 1.建立索引：

<pre>
   /usr/local/coreseek/bin/indexer --config /usr/local/coreseek/etc/zl_sphinx.conf  --all
</pre>

添加数据之后执行：

* 2.更新增量索引：
<pre>
    /usr/local/coreseek/bin/indexer --config /usr/local/coreseek/etc/zl_sphinx.conf  delta --rotate
</pre>

* 3.合并索引：加上 --merge-dst-range deleted 0 0 防止多个关键字指向同一个文档

<pre>
/usr/local/coreseek/bin/indexer --merge zhl delta --config /usr/local/coreseek/etc/zl_sphinx.conf --rotate --merge-dst-range deleted 0 0
</pre>


* 4.配置文件：

{% highlight bash %}
source zhl
{
        type                    = mysql
        sql_host                = localhost
        sql_user                = test
        sql_pass                =
        sql_db                  = test
        sql_port                = 3306  # optional, default is 3306
         #定义连接数据库后取数据之前执行的SQL语句
        sql_query_pre           = SET NAMES utf8
        #sql_query_pre          = SET SESSION query_cache_type=OFF
         #创建一个sph_counter用于增量索引
        sql_query_pre           = CREATE TABLE IF NOT EXISTS sph_counter (counter_id integer primary key not null, max_doc_id integer not null)
        #取数据之前将表的最大id记录到sph_counter表中
        sql_query_pre           = REPLACE INTO sph_counter SELECT 1, MAX(id) FROM documents
        sql_query_range         = select 1,max(id) from documents
        # main document fetch query
        # mandatory, integer document ID field MUST be the first selected column
        #定义取数据的SQL，第一列ID列必须为唯一的正整数值
        sql_query               = \
                SELECT id, group_id, score, UNIX_TIMESTAMP(date_added) AS created_time, title, content, author\
                FROM documents where id >= $start and id<=$end and id <=(select max_doc_id from sph_counter where counter_id=1)
        sql_attr_uint           = group_id
        sql_attr_timestamp      = created_time
        sql_attr_string         = author
        sql_attr_string         = title
        sql_attr_float          = score
        #设置分区查询的时间间隔
        ####sql_ranged_throttle = 0
        # document info query, ONLY for CLI search (ie. testing and debugging)
        # optional, default is empty
        # must contain $id macro and must fetch the document by that id
         #用于CLI的调试
        ####sql_query_info              = SELECT * FROM documents WHERE id=$id
}
#定义一个增量的源
source delta:zhl
{
        sql_query_pre   = set names utf8
         #增量源只查询上次主索引生成后新增加的数据
         #
        ##如果新增加的searchid比主索引建立时的searchid还小那么会漏掉
        sql_query       = SELECT id,group_id, score, UNIX_TIMESTAMP(date_added) as created_time,title,content,author FROM documents where \
                                 id>=$start and id <= $end and id > (SELECT max_doc_id FROM sph_counter WHERE counter_id=1)
        sql_query_post_index  =replace into sph_counter select 1, max(id)  from documents
}
index zhl
{
         #设置索引的源
        source                  = zhl
         #设置生成的索引存放路径
        path                    = /usr/local/coreseek/var/data/zhl
}

index delta : zhl
{
         #设置索引的源
        source                  = zhl
         #设置生成的索引存放路径
        path                    = /usr/local/coreseek/var/data/delta
}
#全局index
indexer
{
        #定义生成索引过程使用索引的限制
        mem_limit               = 128M
}
##########i###################################################################
## searchd settings
#############################################################################
searchd
{
        #定义监听的IP和端口
        listen                  = 127.0.0.1:9312
        #定义log的位置
        log                     = /usr/local/coreseek/var/log/zhl_sphinx_searchd.log
        #定义查询log的位置
        query_log               = /usr/local/coreseek/var/log/zhl_sphinx_query.log
        #定义网络客户端请求的读超时时间
        read_timeout            = 5
        #客户端请求时间限制
        ##client_timeout                = 300
        # 义子进程的最大数量
        max_children            = 30
        #设置searchd进程pid文件名
        pid_file                = /usr/local/coreseek/var/log/zhl_sphinx_searchd.pid
        #定义守护进程在内存中为每个索引所保持并返回给客户端的匹配数目的最大值
        max_matches             = 1000
         #启用无缝seamless轮转，防止searchd轮转在需要预取大量数据的索引时停止响应
         #    #也就是说在任何时刻查询都可用，或者使用旧索引，或者使用新索引
        seamless_rotate         = 1
        #  #配置在启动时强制重新打开所有索引文件
        preopen_indexes         = 0
        # #设置索引轮转成功以后删除以.old为扩展名的索引拷贝
        unlink_old              = 1
                                                                   
        # #最大允许的包大小
        max_packet_size         = 8M
        # #最大允许的过滤器数
        max_filters             = 256
                                                              
        max_filter_values       = 4096
                                                                   
        max_batch_queries       = 32
                                                              
        workers                 = threads # for RT to work
                                                                   
        # SphinxQL compatibility mode (legacy columns and their names)
        # optional, default is 0 (SQL compliant syntax and result sets)
        #
         compat_sphinxql_magics = 1
}

{% endhighlight %}
