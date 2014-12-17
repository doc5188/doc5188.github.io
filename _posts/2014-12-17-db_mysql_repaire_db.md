---
layout: post
title: "[MySQL]快速解决\"is marked as crashed and should be repaired\"故障"
categories: 数据库
tags: [mysql, mysql恢复]
date: 2014-12-17 09:49:04
---

[MySQL]快速解决"is marked as crashed and should be repaired"故障


具体报错如下：<br><br>Table '.\Tablename\posts' is marked as crashed and should be repaired<br><br>提示说论坛的帖子表posts被标记有问题，需要修复。我记得以前也出现过类似的问题,但是只要点击Phpmyadmin上的repair按纽就自动修复了,但是这次很绝,什么都没有.于是赶快上网查找原因。最终将问题解决。解决方法如下：<br><br>找到mysql的安装目录的bin/myisamchk工具，在命令行中输入：<br><br>myisamchk -c -r ../data/tablename/posts.MYI<br><br>然后myisamchk 工具会帮助你恢复数据表的索引。好象也不用重新启动mysql，问题就解决了。<br><br>问题分析：<br><br>1、<br>错误产生原因，有网友说是频繁查询和更新dede_archives表造成的索引错误，因为我的页面没有静态生成，而是动态页面，因此比较同意这种说法。<br>还有说法为是MYSQL数据库因为某种原因而受到了损坏，如：数据库服务器突发性的断电、在提在数据库表提供服务时对表的原文件进行某种操作都有可能导致<br>MYSQL数据库表被损坏而无法读取数据。总之就是因为某些不可测的问题造成表的损坏。<br><br><br>2、问题解决办法。<br><br>当你试图修复一个被破坏的表的问题时，有三种修复类型。如果你得到一个错误信息指出一个临时文件不能建立，删除信息所指出的文件并再试一次--这通常是上一次修复操作遗留下来的。<br>这三种修复方法如下所示：<br>% myisamchk --recover --quick /path/to/tblName<br>% myisamchk --recover /path/to/tblName<br>% myisamchk --safe-recover /path/to/tblName<br><br>第一种是最快的，用来修复最普通的问题；而最后一种是最慢的，用来修复一些其它方法所不能修复的问题。<br><br>检查和修复MySQL数据文件<br>如果上面的方法无法修复一个被损坏的表，在你放弃之前，你还可以试试下面这两个技巧：<br>如<br>果你怀疑表的索引文件(*.MYI)发生了不可修复的错误，甚至是丢失了这个文件，你可以使用数据文件(*.MYD)和数据格式文件(*.frm)重新生<br>成它。首先制作一个数据文件(tblName.MYD)的拷贝。重启你的MySQL服务并连接到这个服务上，使用下面的命令删除表的内容：<br>mysql&gt; DELETE FROM tblName;<br>在<br>删除表的内容的同时，会建立一个新的索引文件。退出登录并重新关闭服务，然后用你刚才保存的数据文件(tblName.MYD)覆盖新的(空)数据文件。<br>最后，使用myisamchk执行标准的修复(上面的第二种方法)，根据表的数据的内容和表的格式文件重新生成索引数据。<br><br>如果你的表的<br>格式文件(tblName.frm)丢失了或者是发生了不可修复的错误，但是你清楚如何使用相应的CREATE<br>TABLE语句来重新生成这张表，你可以重新生成一个新的.frm文件并和你的数据文件和索引文件(如果索引文件有问题，使用上面的方法重建一个新的)一<br>起使用。首先制作一个数据和索引文件的拷贝，然后删除原来的文件(删除数据目录下有关这个表的所有记录)。<br><br>启动MySQL服务并使用当初的CREATE TABLE文件建立一个新的表。新的.frm文件应该可以正常工作了，但是最好你还是执行一下标准的修复(上面的第二种方法)。</div><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;为了不冒失修复，故采取保守做法，我们知道 MySQL 一个高效的管理工具便是 PhpMyAdmin，而在该管理软件中就包含了对表的检查、分析、修复、优化功能，比起网上提供的含糊命令行来说更安全更简便。</p><p><a href="http://goxia.maytide.net/ftpupfiles/MySQLismarkedascrashedandshouldberepaire_DDC6/image.png"><img style="display: inline; border: 0px none;" src="/upload/images/image_thumb.png" alt="image" title="image" height="400" border="0" width="604"></a> </p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过实践，在使用检查表功能后确实发现了问题，之后使用修复功能进行了修复，反馈结果每个表都已经 ok，再执行一次优化，重新测试访问网站终于恢复了正常。一场灾难就此避免……</p>
