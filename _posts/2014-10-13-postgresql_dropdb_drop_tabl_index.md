---
layout: post
title: "postgresql 删除 数据库,表,索引"
categories: 数据库 
tags: [postgresql, postgresql删除表]
date: 2014-10-13 17:57:43
---

前面写了一些，关于postgresql，安装配置；创建数据库，表，导入导出等。可以在pgsql分类目录下查看。下面说一下删除。

1，删除数据库

<pre>
    -bash-3.2$ createdb abc -O playboy  
    CREATE DATABASE  
    -bash-3.2$ dropdb abc                   //dropdb删除数据库  
    DROP DATABASE  
    -bash-3.2$ createdb abc -O playboy  
    CREATE DATABASE  
    -bash-3.2$ psql -U playboy -d playboy  
    Welcome to psql 8.1.23, the PostgreSQL interactive terminal.  
      
    Type:  \copyright for distribution terms  
           \h for help with SQL commands  
           \? for help with psql commands  
           \g or terminate with semicolon to execute query  
           \q to quit  
      
    playboy=> drop database abc;           //登录后的删除数据库，注意，不能删除当前登录的数据库  
    DROP DATABASE  
</pre>

删除操作的前提是，你是超级用户，或者是该数据库的拥有者才行。表也一样，pgsql有一点很特别，就是库是你的，表不一定是你的。这个有点搞。

2，删除索引

<pre>
    playboy_test=# drop index unique_name,playboy_id_pk;   //主索引是删除不掉的，拥有者和超级用户都不行  
    ERROR:  cannot drop index playboy_id_pk because constraint playboy_id_pk on table test requires it  
    HINT:  You may drop constraint playboy_id_pk on table test instead.  
      
    playboy_test=# drop index unique_name;    //删除索引  
    DROP INDEX  
</pre>

3，删除表

<pre>
    playboy_test=# drop table test,test1;   //删除表  
    DROP TABLE  
</pre>

删除操作，根mysql很像，删除数据库有点不一样。pgsql还有一个dropdb命令。上面的删除操作都必须是owner才行。
