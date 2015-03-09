---
layout: post
title: "sphinx下BuildExcerpts的使用"
categories: linux 
tags: [sphinx, 搜索引擎]
date: 2015-03-03 12:37:43
---

使用sphinx:

<pre>
$this->load->library("Sphinxclient",'',"sphinx");
$this->sphinx->SetServer ('127.0.0.1', 9312);
$this->sphinx->SetConnectTimeout(1);
$this->sphinx->SetArrayResult(true);

$this->sphinx->SetMatchMode(SPH_MATCH_EXTENDED2);
$this->sphinx->SetLimits($page,$perpage);
$res = $this->sphinx->Query("\"{$tag}\"/2", "sell");

//具体步骤省略

//假如我只想让tags_name相关部分高亮

$opts = array(
 'before_match' => '<b style="color:red">',
 'after_match'  => '</b>',
 'chunk_separator' => '...',
 'limit'    => 60,
 'around'   => 3,
);

//......

$result = mysql_query($sql);
 
 $tags = array();
 $tags_name = array();//需要变色的那一列
 while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) 
 {
  $tags[] = $row;

  $tags_name[] = $row['tags_name'];
 }
 $tags_name = $s->BuildExcerpts($tags_name, 'index名字', '搜索的词', $opts);//执行高亮，这里索引名字千万不能用*

 foreach($tags as $k=>$v)
 {
  $tags[$k]['tags_name'] = $tags_name[$k];//高亮后覆盖

 }
 foreach($tags as $k=>$v)
 {
  echo $v['tags_id'].':'.$v['tags_name'].'<br/>';
 }

</pre>
 

总结，估计是sphinx2中对BuildExcerpts进行了优化，第一个参数变成了数组，一直报错1293行，查看sphinxapi.php才发现下边这行代码：

<pre>
assert ( is_array($docs) );
</pre>

 

其实我还是觉得这个高亮的部分自己写一个function代替也差不多。

<pre>
 function searchResult($search,$productName)//搜索的词，产品名字
 {
  $arr_p1 = explode(" ",$productName);
 
  $arr_s2 = explode(" ",strtolower($search));
  $arr_p2 = explode(" ",strtolower($productName));
  $len_p2 = count($arr_p2);
  for($i=0;$i<$len_p2;$i++)
  {
   if(in_array($arr_p2[$i],$arr_s2))
    $arr_p1[$i] = '<font color="#ff0000">'.$arr_p1[$i].'</font>';
  }
  return implode(" ",$arr_p1);
 }

</pre>
