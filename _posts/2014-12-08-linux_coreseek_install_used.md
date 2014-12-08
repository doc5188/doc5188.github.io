---
layout: post
title: "coreseek 安装、使用（实时索引+分布式）"
categories: linux
tags: [coreseek, 搜索引擎]
date: 2014-12-08 15:23:26
---

Coreseek 是一款中文全文检索/搜索软件，基于Sphinx研发并独立发布，专攻中文搜索和信息处理领域，它基本兼容sphinx一些特性，很多方面还是传承于sphinx。

1、Coreseek安装

下载：http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz

<pre>
$ tar -zxvf coreseek-4.1-beta
</pre>

**前提：需提前安装操作系统基础开发库及mysql依赖库以支持mysql数据源和xml数据源

##安装mmseg

<pre>
    $ cd mmseg-3.2.14  
    $ ./bootstrap    #输出的warning信息可以忽略，如果出现error则需要解决  
    $ ./configure --prefix=/usr/local/mmseg3  
    $ make && make install  
    $ cd ..  

    $ cd csft-4.1  

    $ sh buildconf.sh  

    $ ./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-$mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql  

    $ make && make install  
</pre>



PS：在安装过程中可能会出现一些常见错误：

（1）问题：undefined reference to `libiconv'

解决：
<pre>
	$ vi csft-4.1/src/Makefile
    注释掉：#LIBS = -ldl -lm -lz -lexpat  -L/usr/local/lib -lrt  -lpthread
    替换为：LIBS = -lm -lexpat -liconv -L/usr/local/lib
</pre>

（2）如下错误：

    undefined reference to `dlclose'  （-ldl）

    undefined reference to `clock_gettime'(-lrt)

    解决：

<pre>
	$ vi csft-4.1/src/Makefile

    修改：LDFLAGS = -lrt  -ldl
</pre>

2、使用


<pre>
    $ cd /usr/local/coreseek/etc  

    $ cp sphinx.conf.dist sphinx.conf  

    $ vi sphinx.conf  
</pre>



在示例配置文件中，将试图对MySQL数据库test中的 documents 表建立索引；因此在这里还提供了 example.sql 用于给测试表增加少量数据用于测试:

<pre>
$ mysql -u test < /usr/local/sphinx/etc/example.sql
</pre>

运行indexer 为你的数据创建全文索引:

<pre>
$ cd /usr/local/coreseek/etc
$ /usr/local/coreseek/bin/indexer --all
</pre>

你可以使用search（注意，是search而不是searchd）实用程序从命令行对索引进行检索:
<pre>
$ cd /usr/local/coreseek/etc
$ /usr/local/coreseek/bin/search test
</pre>

如果要从PHP脚本检索索引，你需要:

运行守护进程searchd，PHP脚本需要连接到searchd上进行检索:
<pre>
$ cd /usr/local/coreseek/etc
$ /usr/local/coreseek/bin/searchd
</pre>

运行PHP API 附带的test 脚本（运行之前请确认searchd守护进程已启动）:
<pre>
$ cd coreseek-4.1-beta/csft-4.1/api
$ php test.php test
</pre>

将API文件(位于api/sphinxapi.php) 包含进你自己的脚本，开始编程.

PS：

<pre>
(1)索引重新生成，需要重启searchd或者建索引时使用--rotate;
(2)目前支持数据源类型只能是UTF-8，MySQL4.1起可以通过SET NAMES UTF8设定输出字符集为UTF-8，即使原始数据为GBK也可（Latin1不能直接使用，需先转换为UTF-8或者GBK字符   集）；
</pre>

3、中文分词核心配置


<pre>
    $ vi sphinx.conf  

    index test1  

    {  

        .......  

        #加入以下设置  

        charset_dictpath       = /usr/local/mmseg3/etc/  

        charset_type       = zh_cn.utf-8  

        #charset_table             = .................... #需将原有注释掉  

        ngram_len                  = 0  

    }  
</pre>



4、分布式

加入如下配置：


<pre>
    index dist1  

    {   

           type                  = distributed  

           local                 = test1  

           agent                 = 172.xx.xx.xx:3312:test1//另一台机器上安装的sphinx     

           agent_connect_timeout = 1000  

           agent_query_timeout   = 3000  

    }  
</pre>



5、实时索引

添加统计表：


<pre>
    # in MySQL  

    CREATE TABLE sph_counter  

    (  

       counter_id INTEGER PRIMARY KEY NOT NULL,  

       max_doc_id INTEGER NOT NULL  

    );  
</pre>


添加增量索引：
<pre>
$ vi sphinx.conf
#修改test1索引数据源

    source test1  

    {  

       # ...  

       sql_query_pre = SET NAMES utf8  

       sql_query_pre = REPLACE INTO sph_counter SELECT 1, MAX(id) FROM documents  

       sql_query = SELECT id, title, body FROM documents \  

           WHERE id<=( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )  

    }  

    source delta : test1  

    {  

       sql_query_pre = SET NAMES utf8  

       sql_query = SELECT id, title, body FROM documents \  

           WHERE id>( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )  

    }  

     

    # 加在所以test1后  

    index delta : test1  

    {  

       source = delta  

       path = /path/to/delta  

    }  
</pre>


添加自动运行脚本：


<pre>
    $ cd /usr/local/coreseek/etc/  

    $ vi delta.sh  

    $ /usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/sphinx.conf delta --rotate >> /usr/local/coreseek/var/log/delta.log  

     

    $ vi test1.sh  

    /usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/sphinx.conf --merge test1 delta --rotate >> /usr/local/coreseek/var/log/test1.log  

     

    $ crontab -e  

    */1 * * * * /usr/local/coreseek/etc/delta.sh #每隔一分钟运行一次  

    30 2 * * * /usr/local/coreseek/etc/test1.sh #每天半夜2:30运行  
</pre>



保存并对delta.sh/test1.sh设权限 chmod 755;


重启crond服务
<pre>
    $ service crond stop  

    $ service crond start  
</pre>
