---
layout: post
title: "linux redis python-redis 安装详细步骤"
categories: python 
tags: [linux, python, redis, python-redis]
date: 2015-01-04 13:06:44
---


为了平衡solr索引的生产消费效率，使用redis作为消息队列：rpush 生产，lpop消费，效果很好
安装redis

把redis安装到 /opt/redis-2.8目录中

<pre>
    wget http://download.redis.io/releases/redis-2.8.1.tar.gz
    tar -zxfx redis-2.8.1.tar.gz
    cd redis-2.8.1
    make && make PREFIX=/opt/redis-2.8 install
    cp redis.conf /opt/redis-2.8/
<pre>

只是把redis当做队列用，不需要存储，所以编辑 /opt/redis-2.8/redis.conf

<pre>
    设置 daemonize yes
    把3条 save .. 都注释掉，这样就关闭了硬盘存储
</pre>

启动redis 非常简单: /opt/redis-2.8/bin/redis-server /opt/redis-2.8/redis.conf

$REIDS_INSTALL_DIR/utils/redis_init_script 这个脚本稍做修改就可以放到/etc/init.d 作为redis启动脚本用
安装python

CentOS 自带的python2.4，太旧了，升级到2.7

<pre>
    wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
    tar -zvxf Python-2.7.6.tgz
    cd Python-2.7.6
    ./configure
    make && make install
    替换系统默认的python: sudo ln -s /usr/local/bin/python2.7 /usr/bin/python
</pre>

安装python的redis模块

<pre>
    wget --no-check-certificate https://pypi.python.org/packages/source/r/redis/redis-2.8.0.tar.gz
    tar -zvxf redis-2.8.0.tar.gz
    mv redis-2.8.0 python-redis-2.8.0
    cd python-redis-2.8.0
    python setup.py install
</pre>

部署成功，写段代码验证一下

<pre>
import redis
client =  redis.StrictRedis(host='localhost', port=6379)
print client.ping()
</pre>

True

执行成功




<pre>
referer:http://lutaf.com/205.htm
</pre>
