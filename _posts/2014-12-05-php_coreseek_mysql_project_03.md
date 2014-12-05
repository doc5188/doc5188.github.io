---
layout: post
title: "Coreseek + PHP + MySQL实战随记（三）"
categories: php
tags: [coreseek, php, 项目实战]
date: 2014-12-05 17:41:04
---


<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">12.同时在两个索引里面搜索数据时的返回值结构</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" color="#ff0000" size="3"><b style="line-height: 25px;">如果同时在两个索引里面搜索数据，当两个索引对应的表不同，且同时在两个索引中搜索到数据且id也相同的时候，则只返回一个id，此时无法区分此id是哪一个索引里面对应数据源的id。</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" color="#0000ff" size="3"><b style="line-height: 25px;">如下例所示，搜索test时，返回的id均是1，是无法区分的</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" color="#0000ff" size="3"><b style="line-height: 25px;">main_document_index对应"1 腾讯,test"</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" color="#0000ff" size="3"><b style="line-height: 25px;">main_novel_index对应"1 求败中国 - test"</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">debian:/home/php# php csft.php test main_novel_index,main_document_index</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">(</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [0] =&gt; csft.php</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [1] =&gt; test</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [2] =&gt; main_novel_index,main_document_index</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">)</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">keyword: test, index: main_novel_index,main_document_index</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">(</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [error] =&gt;&nbsp;</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [warning] =&gt;&nbsp;</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [status] =&gt; 0</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [fields] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [0] =&gt; title</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [1] =&gt; url</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [matches] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [0] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [1] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 1640</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [2] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 1641</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [total] =&gt; 3</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [total_found] =&gt; 3</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [time] =&gt; 0.022</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; [words] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [test] =&gt; Array</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [docs] =&gt; 3</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [hits] =&gt; 3</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">)</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">用命令行查询时会区分开来是哪一个索引里面的数据</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">debian:/usr/local/web/coreseek/bin# ./search.sh test</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">Copyright (c) 2007-2010,</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp;using config file '/usr/local/web/coreseek/etc/csft.conf'...</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">index 'main_novel_index': query 'test ': returned 3 matches of 3 total in 0.018 sec</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">displaying matches:</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">1. document=1, weight=1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; id=1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; ...</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">2. document=1640, weight=1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; id=1640</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; ...</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">3. document=1641, weight=1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; id=1641</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; ...</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">words:</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">1. 'test': 3 documents, 3 hits</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">index 'increment_novel_index': query 'test ': returned 0 matches of 0 total in 0.000 sec</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">words:</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">1. 'test': 0 documents, 0 hits</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">index 'main_document_index': query 'test ': returned 1 matches of 1 total in 0.000 sec</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">displaying matches:</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">1. document=1, weight=1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; d_id=1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; ...</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">words:</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">1. 'test': 1 documents, 1 hits</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">index 'increment_document_index': query 'test ': returned 0 matches of 0 total in 0.000 sec</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">words:</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">1. 'test': 0 documents, 0 hits</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">13.关于数据库中字段与返回结果字段匹配的问题</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" color="#ff0000" size="3"><b style="line-height: 25px;">即使数据库中主键的字段的名称不是id(是d_id)，通过sphinxapi.php搜索以后返回的结果里面matches里面仍然是id</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">CREATE TABLE `documents` (</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; `d_id` int(11) NOT NULL AUTO_INCREMENT,</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; `group_id` int(11) NOT NULL DEFAULT '0',</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; `group_id2` int(11) NOT NULL DEFAULT '0',</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; `date_added` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; `title` varchar(255) NOT NULL DEFAULT '',</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; `content` text NOT NULL,</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; PRIMARY KEY (`d_id`)</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">) ENGINE=MyISAM DEFAULT CHARSET=utf8;</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">csft.conf</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">source xxx</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">{</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">sql_query = SELECT d_id, title, content FROM documents \</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; WHERE d_id&lt;=(SELECT max_doc_id FROM search.sph_counter WHERE counter_id=2)</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">&nbsp; &nbsp; sql_query_info &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;= SELECT * FROM documents WHERE d_id=$id &nbsp;#命令行查询时，从数据库读取原始数据信息</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">}</font></span></div>
<div><span style="line-height: 25px;"><br><font size="3"></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"><b style="line-height: 25px;">14.sphinx相关配置的含义</b></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"># 编码</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">charset_type = utf-8</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"># 指定utf-8的编码表</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">charset_table = 0..9, A..Z-&gt;a..z, _, a..z, U+410..U+42F-&gt;U+430..U+44F, U+430..U+44F</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"># 简单分词，只支持0和1，如果要搜索中文，请指定为1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">ngram_len = 1</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;"><br><font size="3"></font></font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3"># 需要分词的字符，如果要搜索中文，去掉前面的注释</font></span></div>
<div style="line-height: 22px; font-size: 14px;"><span style="line-height: 18px;"><font style="line-height: 25px;" size="3">ngram_chars = U+3000..U+2FA1F</font></span></div>











<pre>
referer:http://iamcaihuafeng.blog.sohu.com/183219747.html
<pre>
