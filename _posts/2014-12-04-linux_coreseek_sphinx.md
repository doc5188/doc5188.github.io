---
layout: post
title: "coreseek(sphinx)中文分词之前缀索引，中缀索引和同义词及分词配置"
categories: linux
tags: [coreseek, sphinx, 搜索引擎, 中文分词]
date: 2014-12-04 16:47:38
---

<p>coreseek(sphinx)中文分词之前缀索引，中缀索引和同义词及分词配置<br></p>
<p><strong>平台</strong>：linux (centos5.5)</p>
<p><strong>使用环境</strong>：php+mysql(sphinxSE)</p>
<p>&nbsp;<wbr></p>
<p>下载CORESEEK4.1源码安装包，里面自带了中文分词软件包mmseg-3.2.14。在mmseg-3.2.14目录下执行
./configure &amp;&amp; make
&amp;&amp; make
install完成安装。默认安装目录在/usr/local/mmseg3。在/usr/local/mmseg/bin下可以之执行mmseg命令，有相应的参数查看分词效果。<br>

&nbsp;<wbr><br>
Sphinx搜索一个比较有特点的地方就是按最大匹配度搜索的。比如分词中有南京，南京市，我搜索南京市，是搜索不出南京的，同样如果搜索南京，也搜索不出南京市。&nbsp;<wbr><br>

&nbsp;<wbr><br>
Mmseg的分词库文档是unigam.txt,在/usr/local/mmseg/etc/下，按照格式修改相应的分词。<br>
&nbsp;<wbr><br>
最后/usr/local/mmseg3/bin/mmseg –u unigram.txt<br>
&nbsp;<wbr><br>
生成unigram.uni文件，重命名为uni.lib复制到sphinx安装目录下的dict文件下，并重建索引。记住需要重启sphinx。<br>
</p>
<p>如果相要搜索南京时南京市也能被匹配到，那需要做以下的配置：<br>
详细的看了coreseek的文档才知道需要建立同义词库。同义词库不需要自己填写，可以根据分词库生成。<br></p>
<p>1. 处理unigram.txt生成同义词库文件<br>
&nbsp;<wbr><br>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
mmseg-3.2.14源代码/script/build_thesaurus.py unigram.txt
&gt; thesaurus.txt<br>
&nbsp;<wbr><br>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
thesaurus.txt文件的格式如下：<br>
&nbsp;<wbr><br>
南京西路<br>
&nbsp;<wbr><br>
-南京,西路,<br>
&nbsp;<wbr><br>
张三丰<br>
&nbsp;<wbr><br>
-太极宗师,武当祖师,<br>
&nbsp;<wbr><br>
2. 生成同义词词典<br>
&nbsp;<wbr><br>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> mmseg -t
thesaurus.txt<br>
&nbsp;<wbr><br>
3. 将thesaurus.lib放到uni.lib同一目录，重启sphinx。<br>
&nbsp;<wbr><br>
4. coreseek索引和搜索时，会自动进行复合分词处理<br>
&nbsp;<wbr><br>
Ok，最后成功解决问题。不过我还是觉得sphinx分词还是不成熟。</p>
<p>&nbsp;<wbr></p>
<p>如果用同义词方式解决的话，同义词库就会很大。还有另外一种方法，就是配置中缀索引。<br></p>
<p>(本文出自php_sir的新浪博客，用户名php_sir，首页链接：<a href="http://blog.sina.com.cn/phpsir">http://blog.sina.com.cn/phpsir</a>，未经本人（php_sir）同意禁止转载)</p>
<p><br>
在配置文件sphinx.conf中配置min_infix_len = 1。中缀索引是实现“start*”, “*end”, and
“*middle*”等形式的通配符成为可能（通配符语法的细节请参考 enable_star
选项）。当最小中缀长度设置为正值，indexer除了对关键字本身还会对所有可能的中缀（即子字符串）做索引。太短的中缀（短于允许的最小长度）不会被索引。例如，在min_infix_len=2设置下索引关键字“test”会导致产生6个索引项
"te", "es", "st", "tes",
"est"等中缀和词本身。对此索引搜索“es”会得到包含“test”的文档，即使它并不包含“es”本身。然而，中缀索引会使索引体积急剧增大（因为待索引关键字增多了很多），而且索引和搜索的时间皆会恶化。在中缀索引中没有自动的办法可以提高精确匹配（整个词完全匹配）的评分，但可以使用与
prefix indexes 选项中相同的技巧。<br>
<br>
这样配置好后，输入南京是能搜到南京市的，反之却不能。</p>
<p>
如果想用“南路”能搜到“南京西路”，则需要在以上配置的前题下sphinx的匹配模式为extended2（mode=extended2）。</p>
<p>&nbsp;<wbr></p>
<p>
要用“南京市”能搜到“南京”，查看了文档以及coreseek社区的讨论帖，发现要对搜索词进行预处理，也就是搜索词输入后在PHP程序中对搜索词进行相应的切分处理。比如搜索南京市，PHP程序中，@name
(南京)|(南京市)。为了使搜索结果更加有用，按分词的最大匹配出结果是合理的，加之可以用部分关键字搜索能搜出含其并在分词库中有更大的词组的结果，也就差不多完美了。如果有其它的法则，那就不应再考虑用搜索引擎来处理了。</p>
<p>&nbsp;<wbr></p>
<p>本文关键词：coreseek sphinx 分词 小配大 同义词 中缀索引 前缀索引</p>
