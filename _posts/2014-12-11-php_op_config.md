---
layout: post
title: "php 如何去操作config.php"
categories: php
tags: [php]
date: 2014-12-11 01:16:36
---

直接 require_once("config.php") 后, 这个文件里面的 变量就能用了.

写入配置:

{% highlight bash %}
<?php
// .... 假设这些变量都已经更改过了, 譬如通过 post 更改设置, 这里已经拿到:
$cfg = "<?";
$cfg.=<<<EOF
php
\$cl_close=$cl_close;
\$cl_weburl="$cl_weburl";
?
EOF;
$cfg.=">";
file_put_contents("config.php", $cfg);
?>

{% endhighlight %}
   
大概这个样子, 就是用php 输出一份php文件~ php 的 include /require 很好用的.
 
其他建议方法, 采用json_encode/json_decode 来加载/保存配置为 Json格式, 譬如

声明一个配置类:
 
<pre>
class Config {
    var $cl_close=0;
    var $cl_weburl=".....";
   /...
}
</pre>
   
2. 读取配置:
<pre>
 if (file_exists("config.data")) {
     $config = json_decode(file_get_contents("config.data");
}else{
    $config = new Config();
    $config->cl_close=...//初始化
}
echo $config->cl_close; //访问 
$config->cl_close=1; //修改
</pre>
 
3. 写入配置:
  
   
<pre>
$config=.... //假设已经读到
file_put_contents(json_encode($config));
</pre>
