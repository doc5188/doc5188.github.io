---
layout: post
title: "Coreseek + PHP + MySQL实战随记（五）"
categories: php 
tags: [coreseek, php, 项目实战]
date: 2014-12-05 17:43:12
---


<div><span style="line-height: 18px;"><b><br><font size="3"></font></b></span></div>
<div><span style="line-height: 18px;"><b><font size="3">5.测试</font></b></span></div>
<div><span style="line-height: 18px;"><font size="3">表documents中的数据</font></span></div>
<div><span style="line-height: 18px;"><font size="3">id | title | content</font></span></div>
<div><span style="line-height: 18px;"><font size="3">1 | <font color="#ff0000"><b>腾讯</b>,test</font> | QQ空间,新浪微博QQ团购，百度</font></span></div>
<div><span style="line-height: 18px;"><font size="3">2 | 阿里巴巴 | <font color="#ff0000"><b>腾讯</b>，全球最大的采购批发市场。阿里巴巴集团，阿里巴巴网络有限公司。</font></font></span></div>
<div><span style="line-height: 18px;"><font size="3">3 | 淘宝 | 淘江湖淘宝商城淘宝天下淘宝电器城</font></span></div>
<div><span style="line-height: 18px;"><font size="3">4 | 百度 | 百度说吧百度贴吧百度mp3有啊百度百科</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">a,b是关于字段权重的测试</font></b></span></div>
<div><span style="line-height: 18px;"><b><font size="3">a.测试一</font></b></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">将字段content的权重设为30, title的权重设为5, 则设置的权重高(content)且含有被搜索关键词的字段被搜索出来的结果权重值较高，结果会排在前面。</font></span></div>
<div><span style="line-height: 18px;"><font size="3">$cl-&gt;setFieldWeights(array('title' =&gt; 5, 'content' =&gt; 30));</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">php csft.php 腾讯 main_document_index</font></span></div>
<div><span style="line-height: 18px;"><font size="3">[matches] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [0] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <font color="#ff0000"><b>[id] =&gt; 2</b></font></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 60</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [1] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 10</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">b.测试二</font></b></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">将字段content的权重设为5, title的权重设为30, 则设置的权重高(title)且含有被搜索关键词的字段被搜索出来的结果权重值较高，结果会排在前面。</font></span></div>
<div><span style="line-height: 18px;"><font size="3">$cl-&gt;setFieldWeights(array('title' =&gt; 30, 'content' =&gt; 5));</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">php csft.php 腾讯 main_document_index</font></span></div>
<div><span style="line-height: 18px;"><font size="3">[matches] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [0] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <font color="#ff0000"><b>[id] =&gt; 1</b></font></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 60</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [1] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 2</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 10</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">c,d是测试搜索时的匹配模式</font></b></span></div>
<div><span style="line-height: 18px;"><b><font size="3">c.测试三</font></b></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">不设置任何匹配模式时, 默认的搜索匹配模式是SPH_MATCH_ALL，即搜索结果中必须同时含有输入的多个关键词中的每个关键词。</font></span></div>
<div><span style="line-height: 18px;"><font size="3">SPH_MATCH_ALL<span style="white-space: pre;"> </span>Match all query words (default mode).</font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">debian:/home/php# php csft.php "腾讯 百度" main_document_index</font></b></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">[matches] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [0] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 70</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">d.测试四</font></b></span></div>
<div><span style="line-height: 18px;"><font color="#ff0000" size="3">设置匹配模式为SPH_MATCH_ANY，意思是匹配输入的多个关键词中的任何一个关键词即可(Match any of query words.)，因此搜索出来的结果可能会更多一些，见下面的输出所示。</font></span></div>
<div><span style="line-height: 18px;"><font size="3">$cl-&gt;SetMatchMode(SPH_MATCH_ANY);</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">debian:/home/php# php csft.php "腾讯 百度" main_document_index</font></b></span></div>
<div><span style="line-height: 18px;"><font size="3">[matches] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [0] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 4970</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [1] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 4</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 4970</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [2] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [id] =&gt; 2</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [weight] =&gt; 710</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [attrs] =&gt; Array</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; )</font></span></div>



<pre>
referer:http://iamcaihuafeng.blog.sohu.com/183684826.html
</pre>
