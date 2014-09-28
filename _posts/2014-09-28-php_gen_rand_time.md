---
layout: post
title: "php生成某个范围内的随机时间"
date: 2014-09-28 14:36:43
categories: php
tags: [php, randtime]
---

{% highlight php %}
    /** 
     *   生成某个范围内的随机时间 
     * @param <type> $begintime  起始时间 格式为 Y-m-d H:i:s 
     * @param <type> $endtime    结束时间 格式为 Y-m-d H:i:s   
     */  
    function randomDate($begintime, $endtime="") {  
        $begin = strtotime($begintime);  
        $end = $endtime == "" ? mktime() : strtotime($endtime);  
        $timestamp = rand($begin, $end);  
        return date("Y-m-d H:i:s", $timestamp);  
    }  
{% endhighlight %}
