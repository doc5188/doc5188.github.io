---
layout: post
title: "PHP全世界最小最简单的模板引擎------Pain (普通版)"
categories: php
tags: [php模板引擎, Pain]
date: 2014-11-20 13:10:44
---

不同于smarty,所有的变量以{@ @}括起来


Copyright (c) 2011 Pain Song 


{% highlight bash %}
<?php
class Pain
{
    public $var=array();
    public $tpl=array();
         
        //this is the method to assign vars to the template
    public function assign($variable,$value=null)
    {
            $this->var[$variable]=$value;
    }
     
    public function display($template_name,$return_string=false)
    {
        //first find whether the tmp file in tmp dir exists.
        if(file_exists("tmp/temp_file.php"))
        {
            unlink("tmp/temp_file.php");
        }
        extract($this->var);
        $tpl_content=file_get_contents($template_name);
        $tpl_content=str_replace("{@", "<?php echo ", $tpl_content);
        $tpl_content=str_replace("@}", " ?>", $tpl_content);
        //create a file in the /tmp dir and put the $tpl_contentn into it, then
        //use 'include' method to load it!
        $tmp_file_name="temp_file.php";
        //$tmp is the handler
        $tmp=fopen("tmp/".$tmp_file_name, "w");
        fwrite($tmp, $tpl_content);
        include "tmp/".$tmp_file_name;
    }  
}
     
     
?>
{% endhighlight %}


{% highlight bash %}
<pre>
<?php
    require_once "Pain.php";
    $pain=new Pain();
    $songyu="songyu nb";
    $zhangyuan="zhangyuan sb";
    $pain->assign("songyu",$songyu);
    $pain->assign("zhangyuan",$zhangyuan);
    $pain->display("new_file.html");
?>

{% endhighlight %}


{% highlight bash %}
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>new_file</title>
    </head>
    <body>
        {@$songyu@}<br/>
        {@$zhangyuan@}
    </body>
</html>

{% endhighlight %}
