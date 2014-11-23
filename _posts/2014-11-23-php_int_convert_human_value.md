---
layout: post
title: "PHP字节单位转换"
categories: php
tags: [php]
date: 2014-11-23 14:32:14
---

PHP将字节大小或文件尺寸转换为以G/M/K/B字符表示的大小.

精确计算所有单位,请使用下面第一个函数.转换结果如2M 545K 352B如果只需要最大的单位.请使用第二个函数.转换结果如5002.33 PB

因为函数同名,所以不要两个同时都写到一个PHP文件里面.

{% highlight bash %}

<?php


function calc($size){
$units = array(3=>'G',2=>'M',1=>'K',0=>'B');//单位字符,可类推添加更多字符.
foreach($units as $i => $unit){
        if($i>0){
                $n = $size /pow(1024,$i)%pow(1024,$i);
        }else{
                $n = $size24;
        }
                
        if($n!=0){
                @$str.=" $n{$unit} ";
        }
}
return  $str;
}
echo calc(2655584);
?>

{% endhighlight %}
