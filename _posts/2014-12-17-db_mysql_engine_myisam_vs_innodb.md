---
layout: post
title: "MySQL: InnoDB 还是 MyISAM?"
categories: 数据库
tags: [mysql, mysql引擎]
date: 2014-12-17 13:10:46
---

<h2>MyISAM存储引擎</h2>
<h2> </h2>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     MyISAM是 默认存储引擎。它基于更老的ISAM代码，但有很多有用的扩展。MyISAM存储引擎的一些特征：<br>
 ·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         所有数据值先存储低字节。这使得数据机和操作系统分离。二进制轻便性的唯一要求是机器使用补码（如最近20年的机器有的一样）和IEEE浮点格式（在主流机器中也完全是主导的）。唯一不支持二进制兼容性的机器是嵌入式系统。这些系统有时使用特殊的处理器。
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         先存储数据低字节并不严重地影响速度；数据行中的字节一般是未联合的，从一个方向读未联合的字节并不比从反向读更占用更多的资源。服务器上的获取列值的代码与其它代码相比并不显得时间紧。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;大文件（达63位文件长度）在支持大文件的文件系统和操作系统上被支持。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         当把删除和更新及插入混合的时候，动态尺寸的行更少碎片。这要通过合并相邻被删除的块，以及若下一个块被删除，就扩展到下一块来自动完成。</p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         每个MyISAM表最大索引数是64。             这可以通过重新编译来改变。每个索引最大的列数是16个。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         最大的键长度是1000字节。这也可以通过编译来改变。对于键长度超过250字节的情况，一个超过1024字节的的键块被用上。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         BLOB和TEXT列可以被索引。</p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         NULL值被允许在索引的列中。这个占每个键的0-1个字节。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         所有数字键值以高字节为先被存储以允许一个更高地索引压缩。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;当记录以排好序的顺序插入（就像你使用一个AUTO_INCREMENT列之时），索引树被劈开以便高节点仅包含一个键。这改善了索引树的空间利用率。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         每表一个AUTO_INCREMEN列的内部处理。MyISAM为INSERT和UPDATE操作自动更新这一 列。这使得AUTO_INCREMENT列更快（至少10%）。在序列顶的值被删除之后就不能再利用。（当AUTO_INCREMENT列被定义为多列索 引的最后一列，可以出现重使用从序列顶部删除的值的情况 ）。AUTO_INCREMENT值可用ALTER TABLE或<strong>myisamch</strong>来重置。</p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         如果数据文件中间的表没有自由块了，在其它线程从表读的同时，你可以INSERT新行到表中。（这被认识为并发操作 ）。自由块的出现是作为删除行的结果，或者是用比当前内容多的数据对动态长度行更新的结果。当所有自由块被用完（填满），未来的插入又变成并发。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         你可以把数据文件和索引文件放在不同目录，用DATA DIRECTORY和INDEX DIRECTORY选项CREATE TABLE以获得更高的速度，请参阅<a title="13.1.5.&nbsp;CREATE TABLE Syntax" href="http://dev.mysql.com/doc/refman/5.1/zh/sql-syntax.html#create-table">13.1.5节，“CREATE      TABLE语法”</a>。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         每个字符列可以又不同的字符集。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  在MyISAM索引文件里又一个标志，它表明表是否被正确关闭。如果用--myisam-recover选项启动<strong>mysqld</strong>，MyISAM表在打开得时候被自动检查，如果被表被不恰当地关闭，就修复表。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         如果你用--update-state选项运行<strong>myisamchk</strong>，它标注表为已检查。<strong>myisamchk --fast</strong>只检查那些没有这个标志的表。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         <strong>myisamchk --analyze</strong>为部分键存储统计信息，也为整个键存储统计信息。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         <strong>myisampack</strong>可以打包BLOB和VARCHAR列。 </p>
<p>MyISAM也支持下列特征：</p>
<div>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         支持true VARCHAR类型；VARCHAR列以存储在2个字节中的长度来开始。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         有VARCHAR的表可以有固定或动态记录长度。</p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         VARCHAR和CHAR列可以多达64KB。 </p>
<p>·&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;           一个被搞乱的已计算索引对可对UNIQUE来使用。这允许你在表内任何列的合并上有UNIQUE。（尽管如此，你不能在一个UNIQUE已计算索引上搜索）。</p>
<h2>InnoDB存储引擎</h2>
InnoDB给MySQL提供 了具有提交，回滚和崩溃恢复能力的事务安全（ACID兼容）存储引擎。InnoDB锁定在行级并且也在SELECT语句提供一个Oracle风格一致的非 锁定读。这些特色增加 了多用户部署和性能。没有在InnoDB中扩大锁定的需要，因为在InnoDB中行级锁定适合非常小的空间。InnoDB也支持FOREIGN KEY强制。在SQL查询中，你可以自由地将InnoDB类型的表与其它MySQL的表的类型混合起来，甚至在同一个查询中也可以混合。
<p>InnoDB是为处理巨大数据量时的最大性能设计。它的CPU效率可能是任何其它基于磁盘的关系数据库引擎所不能匹敌的。 </p>
<p>InnoDB存储引擎被完全与MySQL服务器整合，InnoDB存储引擎为在主内存中缓存数据和索引而维持它自己的缓冲池。 InnoDB存储它的表＆索引在一个表空间中，表空间可以包含数个文件（或原始磁盘分区）。这与MyISAM表不同，比如在MyISAM表中每个表被存在 分离的文件中。InnoDB 表可以是任何尺寸，即使在文件尺寸被限制为2GB的操作系统上。 </p>
<p>InnoDB默认地被包含在MySQL二进制分发中。Windows Essentials installer使InnoDB成为Windows上MySQL的 默认表。 </p>
InnoDB被用来在众多需要高性能的大型数据库站点上产生。著名的Internet新闻站点Slashdot.org运行在 InnoDB上。Mytrix, Inc.在InnoDB上存储超过1TB的数据，还有一些其它站点在InnoDB上处理平均每秒800次插入/更新的负荷。<br>
<br>
<h2>InnoDB和MyISAM的区别</h2>
<h2>区别概述：</h2>
<p>MyISAM 是MySQL中默认的存储引擎，一般来说不是有太多人关心这个东西。决定使用什么样的存储引擎是一个很tricky的事情，但是还是值我们去研究一下，这里的文章只考虑 MyISAM 和InnoDB这两个，因为这两个是最常见的。</p>
<p>下面先让我们回答一些问题：</p>
<ul>
<li>你的数据库有外键吗？</li>
<li>你需要事务支持吗？</li>
<li>你需要全文索引吗？</li>
<li>你经常使用什么样的查询模式？</li>
<li>你的数据有多大？</li>
</ul>
<p>&nbsp;</p>
<p>思考上面这些问题可以让你找到合适的方向，但那并不是绝对的。如果你需要事务处理或是外键，那么InnoDB 可能是比较好的方式。如果你需要全文索引，那么通常来说 MyISAM是好的选择，因为这是系统内建的，然而，我们其实并不会经常地去测试两百万行记录。所以，就算是慢一点，我们可以通过使用Sphinx从 InnoDB中获得全文索引。</p>
<p>数据的大小，是一个影响你选择什么样存储引擎的重要因素，大尺寸的数据集趋向于选择InnoDB方式，因为其支持事务处理和故障恢复。数据库的在小 决定了故障恢复的时间长短，InnoDB可以利用事务日志进行数据恢复，这会比较快。而MyISAM可能会需要几个小时甚至几天来干这些事，InnoDB 只需要几分钟。</p>
<p>您操作数据库表的习惯可能也会是一个对性能影响很大的因素。比如： COUNT() 在 MyISAM 表中会非常快，而在InnoDB 表下可能会很痛苦。而主键查询则在InnoDB下会相当相当的快，但需要小心的是如果我们的主键太长了也会导致性能问题。大批的inserts 语句在MyISAM下会快一些，但是updates 在InnoDB 下会更快一些——尤其在并发量大的时候。</p>
<p>所以，到底你检使用哪一个呢？根据经验来看，如果是一些小型的应用或项目，那么MyISAM 也许会更适合。当然，在大型的环境下使用MyISAM 也会有很大成功的时候，但却不总是这样的。如果你正在计划使用一个超大数据量的项目，而且需要事务处理或外键支持，那么你真的应该直接使用InnoDB方 式。但需要记住InnoDB 的表需要更多的内存和存储，转换100GB 的MyISAM 表到InnoDB 表可能会让你有非常坏的体验。</p>
<h2>区别总结：</h2>
<p>1.InnoDB不支持FULLTEXT类型的索引。<br>
2.InnoDB 中不保存表的具体行数，也就是说，执行select count(*) from table时，InnoDB要扫描一遍整个表来计算有多少行，但是MyISAM只要简单的读出保存好的行数即可。注意的是，当count(*)语句包含 where条件时，两种表的操作是一样的。<br>
3.对于AUTO_INCREMENT类型的字段，InnoDB中必须包含只有该字段的索引，但是在MyISAM表中，可以和其他字段一起建立联合索引。<br>
4.DELETE FROM table时，InnoDB不会重新建立表，而是一行一行的删除。<br>
5.LOAD TABLE FROM MASTER操作对InnoDB是不起作用的，解决方法是首先把InnoDB表改成MyISAM表，导入数据后再改成InnoDB表，但是对于使用的额外的InnoDB特性（例如外键）的表不适用。</p>
<p>另外，InnoDB表的行锁也不是绝对的，如果在执行一个SQL语句时MySQL不能确定要扫描的范围，InnoDB表同样会锁全表，例如update table set num=1 where name like “%aaa%”</p>
<p>&nbsp;</p>
<h2>提升InnoDB性能的方法：</h2>
MyISAM和InnoDB存储引擎性能差别并不是很大，针对InnoDB来说，影响性能的主要是 innodb_flush_log_at_trx_commit 这个选项，如果设置为1的话，那么每次插入数据的时候都会自动提交，导致性能急剧下降，应该是跟刷新日志有关系，设置为0效率能够看到明显提升，当然，同 样你可以SQL中提交“SET AUTOCOMMIT = 0”来设置达到好的性能。另外，还听说通过设置innodb_buffer_pool_size能够提升InnoDB的性能，但是我测试发现没有特别明显 的提升。<br>
<br>
基本上我们可以考虑使用InnoDB来替代我们的MyISAM引擎了，因为InnoDB自身很多良好的特点，比如事务支持、存储 过程、视图、行级锁定等等，在并发很多的情况下，相信InnoDB的表现肯定要比MyISAM强很多，当然，相应的在my.cnf中的配置也是比较关键 的，良好的配置，能够有效的加速你的应用。<br>
任何一种表都不是万能的，只用恰当的针对业务类型来选择合适的表类型，才能最大的发挥MySQL的性能优势。<br>
