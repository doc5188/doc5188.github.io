---
layout: post
title: "mysql 主从复制，读写分离"
categories: 数据库
tags: [mysql, 主从复制,　mysql集群, mysql读写分离]
date: 2014-12-26 16:49:03
---

一个简单完整的 Mysql 主从复制，读写分离的示意图。


<img src='/upload/images/5e8b503f-7e74-39ab-8c6c-5a1bd77a01f6.png' />


1. 首先搭建 Mysql 主从架构，实现 将 mater 数据自动复制到 slave

MySQL 复制的工作方式很简单，一台服务器作为主机，一台或多台服务器作为从机。主机会把数据库的变化记录到日志。一旦这些变化被记录到日志，就会立刻（或者以设定的时间间隔）被送到从机。


<img src='/upload/images/bc837715-8d0e-36b4-b659-4389e01f76d0.png' />

使用MySQL 复制提供扩展大型网站的能力，这些大型网站的数据库主要是读操作(SELECTs)。从机用於复制主机的銷秏是很少的（通常每个从机1%的开销），在大型网站中每个主机部署30 个从机也是常见的。

异步复制与同步复制

异步复制：MySQL本身支持单向的、异步的复制。异步复制意味着在把数据从一台机器拷贝到另一台机器时有一个延时 – 最重要的是这意味着当应用系统的事务提交已经确认时数据并不能在同一时刻拷贝/应用到从机。通常这个延时是由网络带宽、资源可用性和系统负载决定的。然而，使用正确的组件并且调优，复制能做到接近瞬时完成。

同步复制：同步复制可以定义为数据在同一时刻被提交到一台或多台机器，通常这是通过众所周知的“两阶段提交”做到的。虽然这确实给你在多系统中保持一致性，但也由于增加了额外的消息交换而造成性能下降。

 
使用MyISAM或者InnoDB存储引擎的MySQL本身并不支持同步复制，然而有些技术，例如分布式复制块设备（简称DRBD），可以在下层的文件系统提供同步复制，允许第二个MySQL服务器在主服务器丢失的情况下接管（使用第二服务器的复本）。要了解更多信息，请参见：http://www.drbd.org/

<img src='/upload/images/8abb03b3-5b7b-3986-b2fb-7269498ac6b3.png' />

 异步复制方案：

* 1. Mysql 数据库安装

 

安装过程省略： 详细参见：http://pengranxiang.iteye.com/admin/blogs/1138059

 

服务器 Master ：192.168.14.131

Mysql 安装目录： /home/mysql/mysql   （使用源码安装，独立目录）

 

服务器 Slave    ：192.168.14.132

Mysql 安装目录 ：/home/mysql/mysql

 

* 2. 修改配置

 

为了不影响原来的配置文件： /etc/my.cnf

 

创建新的配置文件，

 

cp /etc/my.cnf  /home/mysql/mysql/conf/master.cnf

cp /etc/my.cnf  /home/mysql/mysql/conf/slave.cnf

 
修改 master.cnf，  增加下面的设置 ，

（官方说明：为了使用事务的InnoDB在复制中最大的持久性和一致性，你应该指定innodb_flush_log_at_trx_commit=1,sync_binlog=1选项。）

 
<pre>
    log-bin=mysql-bin #slave会基于此log-bin来做replication  
    server-id=1           #master的标示  
      
    innodb_flush_log_at_trx_commit=1  
      
    sync_binlog=1  
</pre>

 

 

修改 slave.cnf

<pre>
    [mysqld]  
      
    server-id=2 #slave的标示  
</pre>

* 3. 启动服务


<pre>
    # Master  
      
    # 如果 Mysql 已启动，先关掉。  
      
    /home/mysql/mysql/bin/mysqladmin -u root -p shutdown   
      
    # 使用修改过的 master.cnf 启动 mysql  
      
    /home/mysql/mysql/bin/mysqld_safe --defaults-file=/home/mysql/mysql/conf/master.cnf &   
</pre>

<pre>
    # Slave  
      
    # 如果 Mysql 已启动，先关掉。  
      
    /home/mysql/mysql/bin/mysqladmin -u root -p shutdown   
      
    # 使用修改过的 slave.cnf 启动 mysql  
      
    /home/mysql/mysql/bin/mysqld_safe --defaults-file=/home/mysql/mysql/conf/slave.cnf &   
</pre>

* 4. 在 Master 上创建一个专门用于复制的账号 repl_user

<img src='/upload/images/ffcdebd9-7c6b-3419-be1c-3331f134fe52.png' />


* 5. 启动主从复制功能

 

需要查看 Master 中的  Master status

 

mysql> show master status;

 

然后再 Slave 中，启动复制

<img src='/upload/images/241acc94-075d-31c9-bfd6-6c466f54f09b.png' />
 


 

 

上面窗口是连接 Master ， 下面窗口连接 Slave

 

6. 测试复制

 

在 Master 中插入一条数据， 然后在 Slave 中查询。 可以验证。


<img src='/upload/images/f2f3ca62-d4fa-3945-9bf4-ebff988282b2.png' />



2 简单的读写分离实现

 

读写分离可以直接在 客户端 实现， 也可以通过 代理服务器 实现。

 

代理服务器一般可以选择：

 

官方的：mysql proxy  地址：http://dev.mysql.com/downloads/mysql-proxy/#downloads

 

国产开源项目：amoeba
Amoeba开发者博客: http://amoeba.meidusa.com

Amoeba开源项目地址: http://www.sourceforge.net/projects/amoeba
amoeba 中文文档下载地址：http://amoeba.meidusa.com/amoeba.pdf

 

这里只演示最简单的方案： JDBC 直接实现 读写分离。

<pre>
    package prx.dao;  
      
    import java.sql.Connection;  
    import java.sql.ResultSet;  
    import java.util.Properties;  
      
    import com.mysql.jdbc.ReplicationDriver;  
      
    public class Test {  
      
        public static void main(String[] args) throws Exception {  
            ReplicationDriver driver = new ReplicationDriver();  
      
            Properties props = new Properties();  
      
            // We want this for failover on the slaves  
            props.put("autoReconnect", "true");  
      
            // We want to load balance between the slaves  
            props.put("roundRobinLoadBalance", "true");  
      
            props.put("user", "foo");  
            props.put("password", "bar");  
      
            //    
            // Looks like a normal MySQL JDBC url, with a  
            // comma-separated list of hosts, the first  
            // being the 'master', the rest being any number  
            // of slaves that the driver will load balance against  
            //    
      
            Connection conn = driver.connect(  
                    "jdbc:mysql://master,slave1,slave2,slave3/test", props);  
      
            //    
            // Perform read/write work on the master  
            // by setting the read-only flag to "false"  
            //  
            // 通过 conn 的 readOnly 是否为 true 来判断，要取 connection 连接的数据库是 主数据库，还是从数据库  
            // false 为 主数据库的连接  
            // true 为 从数据库的连接  
              
            conn.setReadOnly(false);  
      
            conn.setAutoCommit(false);  
            conn.createStatement().executeUpdate("UPDATE some_table ....");  
            conn.commit();  
      
            //    
            // Now, do a query from a slave, the driver automatically picks one  
            // from the list  
            //    
      
            conn.setReadOnly(true);  
      
            ResultSet rs = conn.createStatement().executeQuery(  
                    "SELECT a,b FROM alt_table");  
      
        }  
    }  
</pre>
