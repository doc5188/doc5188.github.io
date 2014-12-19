---
layout: post
title: "MySQL 中frm、MYI、MYD 分别代表什么文件"
categories: 数据库
tags: [mysql, mysql数据文件]
date: 2014-12-19 10:25:09
---

frm、MYI、MYD   分别是   MyISAM   表的表结构\索引\数据文件  
   
  一个库在一个目录下  

  不过在   MySQL   4.0   以上版本中,  

  你可以在   CREATE   TABLE   语句中通过使用   DATA   DIRECTORY="directory"   或   INDEX   DIRECTORY="directory"，你可以指定存储引擎在什么地方存放它的表和索引文件。注意，目录必须以一个完整路径指定(不是相对路径)。   这仅仅工作于   MySQL   4.0   中的   MyISAM   表，并且你没有使用   --skip-symlink   选项。查看章节   5.6.1.2   对表使用符号链接。      
    
    
  日志文件可以是一个文件,  
   
  也可以是多个文件,在每次系统启动时产生一个,扩展名是   .000   ,依次递增  
   
  使用一个文件,还是多个日志文件,在系统配置文件   my.cnf   或   my.ini   中的配置项确定
