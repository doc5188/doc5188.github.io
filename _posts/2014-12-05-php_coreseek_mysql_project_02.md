---
layout: post
title: "Coreseek + PHP + MySQL实战随记（二）"
categories: php 
tags: [coreseek, php, 项目实战]
date: 2014-12-05 17:37:14
---
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">8.关于增量索引</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">#源定义</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">source main_novel_src</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">{</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; type &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = mysql</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_host &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = localhost</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_user &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = root</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_pass &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = develop</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_db &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = novel</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_port &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; = 3306</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_query_pre &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= SET NAMES utf8</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; #下面的语句是更新sph_counter表中的 max_doc_id。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_query_pre = REPLACE INTO sph_counter SELECT 1, MAX(id) FROM novel</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; <font color="#ff0000">sql_query = SELECT id, title,url &nbsp;FROM novel \</font></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; WHERE id&lt;=(SELECT max_doc_id FROM sph_counter WHERE counter_id=1)</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_query_info &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= SELECT * FROM novel WHERE id=$id &nbsp;#命令行查询时，从数据库读取原始数据信息</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">}</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">#</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3"><b>#请注意，上例中我们显示设置了数据源increment_novel_src的sql_query_pre选项，覆盖了全局设置。必须显示地覆盖这个选项，</b></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3"><b>#否则对increment_novel_src做索引的时候也会运行那条REPLACE查询，那样会导致increment_novel_src源中选出的数据为空。</b></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3"><b>#可是简单地将increment_novel_src的sql_query_pre设置成空也不行，因为在继承来的数据源上第一次运行这个指令的时候，</b></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3"><b>#继承来的所有值都会被清空，这样编码设置的部分也会丢失。因此需要再次显式调用编码设置查询。</b></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><font size="3"><span style="line-height: 18px;">#Via:&nbsp;</span><span style="line-height: 18px;"><a href="http://www.chunliumang.com/articles/info-14.htm" target="_blank">http://www.chunliumang.com/articles/info-14.htm</a></span></font></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">#</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">source increment_novel_src: main_novel_src</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">{</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_query_pre &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= SET NAMES utf8</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; #下面的语句是更新sph_counter表中的 max_doc_id。 &nbsp; &nbsp;</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; <font color="#ff0000">sql_query = SELECT id, title,url &nbsp;FROM novel \</font></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; WHERE id&gt;(SELECT max_doc_id FROM sph_counter WHERE counter_id=1)</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; sql_query_info &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= SELECT * FROM novel WHERE id=$id &nbsp;#命令行查询时，从数据库读取原始数据信息</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">}</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3">经测试，执行增量索引时，不会执行父配置(main_novel_src)中的replace into....语句, 因为手动往表novel中插入了一条记录后，表novel中的最大id为1640，sph_counter中的max_doc_id的值仍然是1639。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/coreseek/bin# ./indexer -c ../etc/csft.conf increment_novel_index --rotate</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">9.关于SetLimits的用法</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">$cl-&gt;SetLimits(0, 20, 30);</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">将SetLimits的第三个参数设为30，索引中总共有43条匹配的记录时的返回值</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">php csft.php 大 main_novel_index</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">...</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp;[total] =&gt; 30</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; [total_found] =&gt; 43</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">...</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">10.sphinxapi搜索后返回数组的结构</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">keyword: 海, index: main_novel_index</font></span></div>
<div><font color="#ff0000" size="3"><span style="line-height: 25px;"><b>为了节省篇幅，返回数组的结构同12</b></span></font></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">11.sphinx api返回结果只有1000条的问题</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">[total] =&gt; 1000</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; [total_found] =&gt; 1639</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3">这是因为sphinxapi.php里面maxmatches的默认值是1000导致的</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3">$this-&gt;_maxmatches<span style="white-space: pre;"> </span>= 1000; ///&lt; max matches to retrieve，最大获取的匹配记录数，比如搜索到了1500条记录，但是如果此值是1000，则只返回1000条记录。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font color="#ff0000" size="3">$this-&gt;_cutoff<span style="white-space: pre;"> </span>= 0; ///&lt; cutoff to stop searching at (default is 0), 搜索到多少条记录后停止搜索</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">SetLimits(offset, limit, max, cutoff)</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">int offset, int limit, int max (default: 0), int cutoff (default: 0)</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">Much like LIMIT in a SQL query, SetLimits() returns a section of the total results. offset allows one to view records starting from the offset. limit returns n results per query. max limits the maximum results returned overall, and cutoff shears all but the last n results from your query. For example, if you return 50 results sorted by newest first with a cutoff of 5, the 5 oldest documents will be returned.</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">&nbsp;More clarification on max and cutoff could be used, especially the purpose of cutoff.</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">$cl-&gt;SetLimits(0, 5); // Returns the first 5 results. "page 1"</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">$cl-&gt;SetLimits(5, 5); // Returns the next 5 results. "page 2"</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">$cl-&gt;SetLimits(50, 25, 60); // Returns the last 10 documents. This configuration limits the search to a maximum of 60 results.</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">$cl-&gt;SetLimits(0, 25, 60, 5); // Returns the last 5 results of all 60 results. Setting the offset here to greater than 4 will return a blank result set.</font></span></div>




<pre>
referer:http://iamcaihuafeng.blog.sohu.com/183219655.html
</pre>
