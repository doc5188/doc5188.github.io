---
layout: post
title: "Python 之ConfigParser"
categories: python
tags: [python模块, ConfigParser]
date: 2014-12-08 14:33:23
---

* 一、ConfigParser简介

ConfigParser 是用来读取配置文件的包。配置文件的格式如下：中括号“[ ]”内包含的为section。section 下面为类似于key-value 的配置内容。

<pre>
[db]
db_host = 127.0.0.1
db_port = 22
db_user = root
db_pass = rootroot

[concurrent]
thread = 10
processor = 20
</pre>
 
中括号“[ ]”内包含的为section。紧接着section 为类似于key-value 的options 的配置内容。

 
* 二、ConfigParser 初始工作

使用ConfigParser 首选需要初始化实例，并读取配置文件：

<pre>

cf = ConfigParser.ConfigParser()

cf.read("配置文件名")
</pre>

 

 
* 三、ConfigParser 常用方法

1. 获取所有sections。也就是将配置文件中所有“[ ]”读取到列表中：

<pre>
s = cf.sections()


print 'section:', s
</pre>

 

将输出（以下将均以简介中配置文件为例）：

<pre>
section: ['db', 'concurrent']
</pre>

 

2. 获取指定section 的options。即将配置文件某个section 内key 读取到列表中：

<pre>
o = cf.options("db")


print 'options:', o
</pre>

 

将输出：

<pre>
options: ['db_host', 'db_port', 'db_user', 'db_pass']
</pre>

 

3. 获取指定section 的配置信息。

<pre>
v = cf.items("db")


print 'db:', v
</pre>

 

将输出：
<pre>
db: [('db_host', '127.0.0.1'), ('db_port', '22'), ('db_user', 'root'), ('db_pass', 'rootroot')]
</pre>

 

4. 按照类型读取指定section 的option 信息。

同样的还有getfloat、getboolean。


 
<pre>
#可以按照类型读取出来
db_host = cf.get("db", "db_host")

db_port = cf.getint("db", "db_port")

db_user = cf.get("db", "db_user")

db_pass = cf.get("db", "db_pass")

# 返回的是整型的

threads = cf.getint("concurrent", "thread")

processors = cf.getint("concurrent", "processor")


print "db_host:", db_host


print "db_port:", db_port


print "db_user:", db_user


print "db_pass:", db_pass


print "thread:", threads


print "processor:", processors
</pre>

 

将输出：

<pre>
db_host: 127.0.0.1

db_port: 22

db_user: root

db_pass: rootroot

thread: 10

processor: 20

</pre>

5. 设置某个option 的值。（记得最后要写回）
<pre>
cf.set("db", "db_pass", "zhaowei")

cf.write(open("test.conf", "w"))
</pre>

 

6.添加一个section。（同样要写回）

<pre>
cf.add_section('liuqing')

cf.set('liuqing', 'int', '15')

cf.set('liuqing', 'bool', 'true')

cf.set('liuqing', 'float', '3.1415')

cf.set('liuqing', 'baz', 'fun')

cf.set('liuqing', 'bar', 'Python')

cf.set('liuqing', 'foo', '%(bar)s is %(baz)s!')

cf.write(open("test.conf", "w"))
</pre>

 

7. 移除section 或者option 。（只要进行了修改就要写回的哦）

<pre>
cf.remove_option('liuqing','int')

cf.remove_section('liuqing')

cf.write(open("test.conf", "w"))
</pre>


实例:

<pre>
    #!/usr/bin/env python
    from ConfigParser import ConfigParser
    CONFIGFILE="f.txt"
    config=ConfigParser()
    config.read(CONFIGFILE)
    print config.get('messages','greeting')
    radius=input(config.get('messages','questions')+' ')
    print config.get('messages','result')
    print config.getfloat('numbers','pi')*radius**2

    s=config.sections()
    print'section: ',s
    o=config.options('messages')
    print'messages option: ',o
    v=config.items("messages")
    print'message de xinxi: ',v

    config.add_section('liuyang1')
    config.set('liuyang1','int','15')
    config.set('liuyang'1,'hhhh','hello world')
    config.write(open("f.txt","w"))
    print config.get('liuyang1','int')
    print config.get('liuyang1','hhhh')





    #!/usr/bin/env python
    import ConfigParser
    import sys
    config=ConfigParser.ConfigParser()
    config.add_section("book1")
    config.set("book1","title","hello world")
    config.set("book1","aut","log")
    config.write(open("f.txt","w"))

</pre>

