---
layout: post
title: "PHP数字格式化"
categories: php
tags: [php]
date: 2014-11-23 14:45:58
---

例如，echo number_format(285266237); 

可以输出 285,266,237 

另外如果需要格式化文件字节大小，下面的方法可以借鉴： 

<pre>
function byte_format($input, $dec=0) 
{  
 $prefix_arr = array(' B', 'K', 'M', 'G', 'T'); 
 $value = round($input, $dec); 
 $i=0; 
 while ($value>1024) 
 {  
  $value /= 1024; 
  $i++; 
  } 
  $return_str = round($value, $dec).$prefix_arr[$i]; 
  return $return_str; 
} 

</pre>

echo byte_format(285266237); 

显示结果为 272M 

例如，echo number_format(285266237); 

可以输出 285,266,237 
