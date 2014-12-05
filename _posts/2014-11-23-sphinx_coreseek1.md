---
layout: post
title: "Coreseek"
categories:技术文章
tags: [coreseek]
date: 2014-11-23 23:28:26
---

(Windows下调试运行)

启动守护进程

bin\searchd -c etc\csft_mysql.conf --console

更新索引

bin\indexer --all --config etc\csft_mysql.conf --rotate

更新增量索引

bin\indexer post_delta --config etc\csft_mysql.conf --rotate

合并索引

bin\indexer --merge post_main post_delta --rotat --config etc\csft.conf

重建增量索引

bin\indexer post_delta --config etc\csft.conf --rotate

Coreseek安装成Windows服务

d:\xampp\htdocs\coreseek\bin\searchd.exe --install --config D:/xampp/htdocs/coreseek/etc/csft_mysql.conf

安装Coreseek后启动时出现错误1067进程意外终止

将配置文件csft.conf中的路径,修改为绝对路径 如:D:/xampp/htdocs/coreseek/etc/csft_mysql.conf.路径不得包含中文,也不得包含空格,路径分隔符用"/",而不是"\"

Coreseek多表索引(主要配置原文件)

<pre>
source mysql
{
    type                    = mysql

    sql_host                = localhost
    sql_user                = root
    sql_pass                =
    sql_db                    = test
    sql_port                = 3306
    sql_query_pre            = SET NAMES utf8
    sql_query_pre = REPLACE INTO sph_counter SELECT 1, MAX(id) FROM documents
    sql_query = SELECT id, group_id, UNIX_TIMESTAMP(date_added) AS date_added, title, content FROM documents WHERE id<=( SELECT max_doc_id FROM sph_counter WHERE counter_id=1)
                                                              #sql_query第一列id需为整数
                                                              #title、content作为字符串/文本字段，被全文索引
    sql_attr_uint            = group_id           #从SQL读取到的值必须为整数
    sql_attr_timestamp        = date_added #从SQL读取到的值必须为整数，作为时间属性

    sql_query_info_pre      = SET NAMES utf8                                        #命令行查询时，设置正确的字符集
    sql_query_info            = SELECT * FROM documents WHERE id=$id #命令行查询时，从数据库读取原始数据信息
    sql_query_post_index = REPLACE INTO sph_counter (counter_id,max_doc_id) VALUES (1,$maxid)
}
source delta : mysql
{
    sql_query_pre = SET NAMES utf8
    sql_query = SELECT id, group_id, UNIX_TIMESTAMP(date_added) AS date_added, title, content FROM documents WHERE id>( SELECT max_doc_id FROM sph_counter WHERE counter_id=1)
}
source text
{
    type                    = mysql
    sql_host                = localhost
    sql_user                = root
    sql_pass                =
    sql_db                    = test
    sql_port                = 3306
    sql_query_pre            = SET NAMES utf8
    sql_query                = SELECT id,  UNIX_TIMESTAMP(time) AS date_added, title, content FROM text
    sql_attr_timestamp        = time #从SQL读取到的值必须为整数，作为时间属性
    sql_query_info_pre      = SET NAMES utf8                                        #命令行查询时，设置正确的字符集
    sql_query_info            = SELECT * FROM text WHERE id=$id #命令行查询时，从数据库读取原始数据信息
}
#index定义
index mysql
{
    source            = mysql             #对应的source名称
    path            = D:/xampp/htdocs/coreseek/var/data/mysql #请修改为实际使用的绝对路径，例如：/usr/local/coreseek/var/...
    docinfo            = extern
    mlock            = 0
    morphology        = none
    min_word_len        = 1
    html_strip                = 0

    #中文分词配置，详情请查看：http://www.coreseek.cn/products-install/coreseek_mmseg/
    #charset_dictpath = /usr/local/mmseg3/etc/ #BSD、Linux环境下设置，/符号结尾
    charset_dictpath = D:/xampp/htdocs/coreseek/etc/                             #Windows环境下设置，/符号结尾，最好给出绝对路径，例如：C:/usr/local/coreseek/etc/...
    charset_type        = zh_cn.utf-8
}
index delta : mysql
{
    source = delta
    path = D:/xampp/htdocs/coreseek/var/data/delta
}
index text
{
    source            = text             #对应的source名称
    path            = D:/xampp/htdocs/coreseek/var/data/text #请修改为实际使用的绝对路径，例如：/usr/local/coreseek/var/...
    docinfo            = extern
    mlock            = 0
    morphology        = none
    min_word_len        = 1
    html_strip                = 0

    #中文分词配置，详情请查看：http://www.coreseek.cn/products-install/coreseek_mmseg/
    #charset_dictpath = /usr/local/mmseg3/etc/ #BSD、Linux环境下设置，/符号结尾
    charset_dictpath = D:/xampp/htdocs/coreseek/etc/                             #Windows环境下设置，/符号结尾，最好给出绝对路径，例如：C:/usr/local/coreseek/etc/...
    charset_type        = zh_cn.utf-8
}

</pre>
