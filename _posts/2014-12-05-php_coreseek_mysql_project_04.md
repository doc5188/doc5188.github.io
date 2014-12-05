---
layout: post
title: "Coreseek + PHP + MySQL实战随记（四）"
categories: php 
tags: [coreseek, php, 项目实战]
date: 2014-12-05 17:42:16
---
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">1.SphinxClient::setFieldWeights</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">通过字段的名称绑定每个字段的权重。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">搜索结果的排名会受到每个字段的权重的影响。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 25px; font-size: medium;"><font size="3">原型: function SetFieldWeights ( $weights )</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">按字段名称设置字段的权值。参数必须是一个hash（关联数组），该hash将代表字段名字</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">的字符串映射到一个整型的权值上。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">字段权重影响匹配项的评级。节 &nbsp; &nbsp; &nbsp; 4.4, “ &nbsp; &nbsp;权值计算 &nbsp; &nbsp;” &nbsp; 解释了词组相似度如何影响评级。这个调</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">用用于给不同的全文数据字段指定不同于默认值的权值。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">给定的权重必须是正的32位整数。最终的权重也是个32位的整数。默认权重为1。未知的</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">属性名会被忽略。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">目前对权重没有强制的最大限制。但您要清楚，设定过高的权值可能会导致出现32位整数</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">的溢出问题。例如，如果设定权值为10000000并在扩展模式中进行搜索，那么最大可能的</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">权值为10M（您设的值）乘以1000（BM25的内部比例系数，参见节 &nbsp; &nbsp; &nbsp; 4.4, “ &nbsp; &nbsp;权值计算” &nbsp; &nbsp;）再</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">乘以1或更多（词组相似度评级）。上述结果最少是100亿，这在32位整数里面没法存储，</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">将导致意想不到的结果。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">//字段title的权重设为10，content的权重设为30</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">$sphinxObj-&gt;setFieldWeights(array('title' =&gt; 10, 'content' =&gt; 30));</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 25px;"><a href="http://www.php.net/manual/en/sphinxclient.setfieldweights.php" target="_blank"><font size="3">http://www.php.net/manual/en/sphinxclient.setfieldweights.php</font></a></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">2.SphinxClient::setIndexWeights</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">设置每个索引的权重，也就是同时搜索多个索引的时候，权重高的索引优先搜出来，大概是这个意思。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">Sets per-index weights and enables weighted summing of match weights across different indexes.</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">原型: function SetIndexWeights ( $weights )</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">设置索引的权重，并启用不同索引中匹配结果权重的加权和。参数必须为在代表索引名的字</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">符串与整型权值之间建立映射关系的hash（关联数组）。默认值是空数组，意思是关闭带权加和。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">当在不同的本地索引中都匹配到相同的文档ID时，Sphinx默认选择查询中指定的最后一个</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">索引。这是为了支持部分重叠的分区索引。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">然而在某些情况下索引并不仅仅是被分区了，您可能想将不同索引中的权值加在一起，而不</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">是简单地选择其中的一个。SetIndexWeights()允许您这么做。当开启了加和功能后，最后的</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">匹配权值是各个索引中的权值的加权合，各索引的权由本调用指定。也就是说，如果文档</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">123在索引A被找到，权值是2，在B中也可找到，权值是3，而且您调用了</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">SetIndexWeights ( array ( "A"=&gt;100, "B"=&gt;10 ) )，那么文档123最终返回</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">给客户端的权值为2*100+3*10 = 230。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 25px;"><a href="http://www.php.net/manual/en/sphinxclient.setindexweights.php" target="_blank"><font size="3">http://www.php.net/manual/en/sphinxclient.setindexweights.php</font></a></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">3.SphinxClient::setMatchMode</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">设置搜索时的匹配模式</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">有如下可选的匹配模式：</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_MATCH_ALL, 匹配所有查询词（默认模式）</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_MATCH_ANY, 匹配查询词中的任意一个</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_MATCH_PHRASE, 将整个查询看作一个词组，要求按顺序完整匹配</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_MATCH_BOOLEAN, 将查询看作一个布尔表达式 （参见 节 &nbsp; &nbsp; &nbsp; 4.2, “ &nbsp; &nbsp;布尔查询语 &nbsp; &nbsp;</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">法 &nbsp; ” &nbsp;&nbsp;</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_MATCH_EXTENDED, 将查询看作一个Sphinx内部查询语言的表达式（参见</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">节 &nbsp; &nbsp; &nbsp; 4.3, “ &nbsp; &nbsp;扩展的查询语法 &nbsp; &nbsp;” &nbsp; ）</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">还有一个特殊的“完整扫描”模式，当如下条件满足时，该模式被自动激活：</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">1. 查询串是空的（即长度为零）</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">2. docinfo &nbsp; &nbsp; 存储方式为extern</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">在完整扫描模式中，全部已索引的文档都被看作是匹配的。这类匹配仍然会被过滤、排序或</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">分组，但是并不会做任何真正的全文检索。这种模式可以用来统一全文检索和非全文检索的</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">代码，或者减轻SQL服务器的负担（有些时候Sphinx扫描的速度要优于类似的MySQL查</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">询）&nbsp;</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><a href="http://php.net/manual/en/sphinxclient.setmatchmode.php" target="_blank"><font size="3">http://php.net/manual/en/sphinxclient.setmatchmode.php</font></a></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><b><font size="3">4.SphinxClient::setRankingMode</font></b></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">设置排序模式, 仅适用于SPH_MATCH_EXTENDED2匹配模式(对应于方法setMatchMode中的设置)</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 25px;"><a href="http://www.php.net/manual/en/sphinxclient.setrankingmode.php" target="_blank"><font size="3">http://www.php.net/manual/en/sphinxclient.setrankingmode.php</font></a></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">原型: function SetRankingMode ( $ranker )</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">设置评分模式。目前只在SPH_MATCH_EXTENDED2这个匹配模式中提供。参数必须是与某个已知模式对应的常数。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">Sphinx默认计算两个对最终匹配权重有用的因子。主要是查询词组与文档文本的相似度。其次是称之为BM25的统计函数，该函数值根据关键字文档中的频率（高频导致高权重）和在整个索引中的频率（低频导致高权重）在0和1之间取值。然而，有时可能需要换一种计算权重的方法——或者可能为了提高性能而根本不计算权值，结果集用其他办法排序。这个目的可以通过设置合适的相关度计算模式来达到。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3">已经实现的模式包括：&nbsp;</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_RANK_PROXIMITY_BM25， 默认模式，同时使用词组评分和BM25评分，并且将二者结合。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_RANK_BM25，统计相关度计算模式，仅使用BM25评分计算（与大多数全文检索引擎相同）。这个模式比较快，但是可能使包含多个词的查询的结果质量下降。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><font size="3"> SPH_RANK_NONE，禁用评分的模式，这是最快的模式。实际上这种模式与布尔搜索相同。所有的匹配项都被赋予权重1。</font></span></div>
<div style="line-height: 160%; font-size: 14px;"><span style="line-height: 18px;"><br><font size="3"></font></span></div>





<pre>
referer:http://iamcaihuafeng.blog.sohu.com/183683487.html
</pre>
