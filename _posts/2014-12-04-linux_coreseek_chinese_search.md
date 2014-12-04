---
layout: post
title: "windows下coreseek,sphnix支持中文搜索"
categories: linux
tags: [coreseek, sphinx, 中文搜索]
date: 2014-12-04 14:34:59
---

windows下coreseek,sphnix支持中文搜索，这个是十分有意思的。我们可以通过对coreseek,sphnix的设置来对ecshop商品信息以及文章进行检索。那么如何设置coreseek的csft.conf文件才能让coreseek,sphnix在windows下支持中文搜索。

我们按照以下配置，就可以让coreseek,sphinx很方便的支持中文搜索。

csft.conf的index里面增加以下代码

<pre>
charset_dictpath=d:\coreseek\etc/
charset_type=zh_cn.utf-8
</pre>


<pre>
require ( "sphinxapi.php" );

$cl = new SphinxClient ();
$cl->SetServer ( '127.0.0.1', 9312);
$cl->SetConnectTimeout ( 3 );

//设置过滤条件
//$cl->SetFilter('cat_id',array(3));
$keyword=  '*诺基亚N85*';
//设置偏移量
//$cl->SetLimits(0,2);
$cl->SetArrayResult ( true );
$cl->SetMatchMode ( SPH_MATCH_ANY);
//$cl->SetSortMode ( SPH_SORT_ATTR_DESC,"reg_time" );
$keyword = $cl->EscapeString($keyword);
//$k = $cl->BuildKeywords($keyword,'mysql',false);
//print_r($k);
$res = $cl->Query ( $keyword, "mysql" );
//print_r($cl);
print_r($res);
//print_r($cl->Status());

</pre>

   看，我们通过coreseek的设置搜索出来ecshop中文名称的商品信息。


