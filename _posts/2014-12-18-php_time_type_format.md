---
layout: post
title: "PHP把时间转换成几分钟前、几小时前、几天前的几个函数、类分享"
categories: php
tags: [php, 时间转换]
date: 2014-12-18 11:12:55
---

这篇文章主要介绍了php计算时间几分钟前、几小时前、几天前的几个函数、类分享,需要的朋友可以参考下<br>
一、函数实现<br>
实例1：<br>
{% highlight bash %}
    <?php  
    header("Content-type: text/html; charset=utf8");  
    date_default_timezone_set("Asia/Shanghai");   //设置时区  
    function time_tran($the_time) {  
        $now_time = date("Y-m-d H:i:s", time());  
        //echo $now_time;  
        $now_time = strtotime($now_time);  
        $show_time = strtotime($the_time);  
        $dur = $now_time - $show_time;  
        if ($dur < 0) {  
            return $the_time;  
        } else {  
            if ($dur < 60) {  
                return $dur . '秒前';  
            } else {  
                if ($dur < 3600) {  
                    return floor($dur / 60) . '分钟前';  
                } else {  
                    if ($dur < 86400) {  
                        return floor($dur / 3600) . '小时前';  
                    } else {  
                        if ($dur < 259200) {//3天内  
                            return floor($dur / 86400) . '天前';  
                        } else {  
                            return $the_time;  
                        }  
                    }  
                }  
            }  
        }  
    }  
      
      
    echo time_tran("2014-7-8 19:22:01");  
    ?>  
{% endhighlight %}

实例2：<br>
{% highlight bash %}
    <?php  
    function time_tranx($the_time){  
       $now_time = date("Y-m-d H:i:s",time()+8*60*60);  
       $now_time = strtotime($now_time);  
       $show_time = strtotime($the_time);  
       $dur = $now_time - $show_time;  
       if($dur < 0){  
            return $the_time;  
       }else{  
            if($dur < 60){  
             return $dur.'秒前';  
            }else{  
                 if($dur < 3600){  
                  return floor($dur/60).'分钟前';  
                 }else{  
                      if($dur < 86400){  
                         return floor($dur/3600).'小时前';  
                      }else{  
                           if($dur < 259200){ //3天内  
                                return floor($dur/86400).'天前';  
                           }else{  
                                return $the_time;  
                           }  
                      }  
                }  
            }  
       }  
    }  
    echo time_tranx("2014-7-8 19:22:01");  
    ?>  
{% endhighlight %}

实例3：<br>

{% highlight bash %}
    <?php  
    function format_date($time){  
        $t=time()-$time;  
    <span style="white-space:pre">    </span>//echo time();  
        $f=array(  
            '31536000'=>'年',  
            '2592000'=>'个月',  
            '604800'=>'星期',  
            '86400'=>'天',  
            '3600'=>'小时',  
            '60'=>'分钟',  
            '1'=>'秒'  
        );  
        foreach ($f as $k=>$v)    {  
            if (0 !=$c=floor($t/(int)$k)) {  
                return $c.$v.'前';  
            }  
        }  
    }  
    echo format_date("1404600000");  
    ?>  
{% endhighlight %}

实例4：<br>
{% highlight bash %}
    <?php  
    function formatTime($date) {  
        $str = '';  
        $timer = strtotime($date);  
        $diff = $_SERVER['REQUEST_TIME'] - $timer;  
        $day = floor($diff / 86400);  
        $free = $diff % 86400;  
        if($day > 0) {  
            return $day."天前";  
        }else{  
            if($free>0){  
                $hour = floor($free / 3600);  
                $free = $free % 3600;  
                    if($hour>0){  
                        return $hour."小时前";  
                    }else{  
                        if($free>0){  
                            $min = floor($free / 60);  
                            $free = $free % 60;  
                            if($min>0){  
                                return $min."分钟前";  
                            }else{  
                                if($free>0){  
                                    return $free."秒前";  
                                }else{  
                                    return '刚刚';  
                                }  
                           }  
                        }else{  
                            return '刚刚';  
                        }  
                   }  
           }else{  
               return '刚刚';  
           }  
        }  
    }  
    echo formatTime("2014-7-8 19:22:01");  
    ?>  
{% endhighlight %}

二、类的实现<br>

{% highlight bash %}
    <?php  
    /* 
     * author: china_skag 
     * time: 2014-07-08 
     * 发博时间计算(年，月，日，时，分，秒) 
     * $createtime 可以是当前时间 
     * $gettime 你要传进来的时间 
     */  
    class Mygettime{  
            function  __construct($createtime,$gettime) {  
                $this->createtime = $createtime;  
                $this->gettime = $gettime;  
        }  
        function getSeconds()  
        {  
                return $this->createtime-$this->gettime;  
            }  
        function getMinutes()  
           {  
           return ($this->createtime-$this->gettime)/(60);  
           }  
          function getHours()  
           {  
           return ($this->createtime-$this->gettime)/(60*60);  
           }  
          function getDay()  
           {  
            return ($this->createtime-$this->gettime)/(60*60*24);  
           }  
          function getMonth()  
           {  
            return ($this->createtime-$this->gettime)/(60*60*24*30);  
           }  
           function getYear()  
           {  
            return ($this->createtime-$this->gettime)/(60*60*24*30*12);  
           }  
           function index()  
           {  
                if($this->getYear() > 1)  
                {  
                     if($this->getYear() > 2)  
                        {  
                            return date("Y-m-d",$this->gettime);  
                            exit();  
                        }  
                    return intval($this->getYear())." 年前";  
                    exit();  
                }  
                 if($this->getMonth() > 1)  
                {  
                    return intval($this->getMonth())." 月前";  
                    exit();  
                }  
                 if($this->getDay() > 1)  
                {  
                    return intval($this->getDay())." 天前";  
                    exit();  
                }  
                 if($this->getHours() > 1)  
                {  
                    return intval($this->getHours())." 小时前";  
                    exit();  
                }  
                 if($this->getMinutes() > 1)  
                {  
                    return intval($this->getMinutes())." 分钟前";  
                    exit();  
                }  
               if($this->getSeconds() > 1)  
                {  
                    return intval($this->getSeconds()-1)." 秒前";  
                    exit();  
                }  
           }  
      }  
    //类的使用实例  
    /* 
     * 
     * 调用类输出方式 
     * 
     * $a = new Mygettime(time(),strtotime('-25 month')); 
     * echo iconv('utf-8', 'gb2312', $a->index())?iconv('utf-8', 'gb2312', $a->index()):iconv('utf-8', 'gb2312', '当前'); 
     * 
     */  
{% endhighlight %}
<br>



{% highlight bash %}
referer:http://blog.csdn.net/china_skag/article/details/37569505
{% endhighlight %}
