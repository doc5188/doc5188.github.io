---
layout: post
title: "启用nginx的fastcgi cache提高网站php访问速度"
categories: linux
tags: [fastcgi cache]
date: 2014-10-10 13:42:18
---

先看下测试数据：

bin\ab.exe -n 100 -c 5 http://www.9enjoy.com

未使用

<pre>
Concurrency Level:      5
Time taken for tests:   9.016 seconds
Complete requests:      100
Failed requests:        0
Write errors:           0
Total transferred:      1696500 bytes
HTML transferred:       1669000 bytes
Requests per second:    11.09 [#/sec] (mean)
Time per request:       450.781 [ms] (mean)
Time per request:       90.156 [ms] (mean, across all concurrent requests)
Transfer rate:          183.76 [Kbytes/sec] received
</pre>

日志里显示，页面执行需要0.004s

<pre>
Concurrency Level:      5
Time taken for tests:   3.203 seconds
Complete requests:      100
Failed requests:        0
Write errors:           0
Total transferred:      1685400 bytes
HTML transferred:       1669000 bytes
Requests per second:    31.22 [#/sec] (mean)
Time per request:       160.156 [ms] (mean)
Time per request:       32.031 [ms] (mean, across all concurrent requests)
Transfer rate:          513.84 [Kbytes/sec] received
</pre>

日志里显示，页面执行时间为0s

提高的很明显！

配置主要参考：http://www.fuchaoqun.com/2011/01/nginx-fastcgi_cache/

配置参数：

http里：
<pre>
fastcgi_cache_path /www/php_cache  levels=1:2  keys_zone=cache_php:30m inactive=1d max_size=10g;
</pre>


<pre>
server里：
    location ~ .*\.php?$
    {
      #fastcgi_pass  unix:/tmp/php-cgi.sock;
      fastcgi_pass  127.0.0.1:9000;
      fastcgi_index index.php;
      include fcgi.conf;
      #以下是fastcgi_cache的配置
      fastcgi_cache   cache_php;
      fastcgi_cache_valid   200 302  1h;
      fastcgi_cache_min_uses  1;
      fastcgi_cache_use_stale error  timeout invalid_header http_500;
      fastcgi_cache_key $host$request_uri;
    }
</pre>


fastcgi_cache_path：fastcgi_cache缓存目录，可以设置目录层级，比如1:2会生成16*256个字目录，cache_php是这个缓存空间的名字，cache是用多少内存（这样热门的内容nginx直接放内存，提高访问速度），inactive表示默认失效时间，max_size表示最多用多少硬盘空间。本来还有个fastcgi_temp_path参数，但发现似乎没用。

fastcgi_cache_valid：定义哪些http头要缓存

fastcgi_cache_min_uses：URL经过多少次请求将被缓存

fastcgi_cache_use_stale：定义哪些情况下用过期缓存

fastcgi_cache_key：定义fastcgi_cache的key，示例中就以请求的URI作为缓存的key，Nginx会取这个key的md5作为缓存文件，如果设置了缓存哈希目录，Nginx会从后往前取相应的位数做为目录

fastcgi_cache：用哪个缓存空间

指定删除某一URL的php文件的缓存的PHP程序

大致代码如下：

{% highlight php %}
$md5 = md5($url);
    
    $cacheFile = '/www/php_cache/' . substr($md5, -1, 1) . '/' . substr($md5, -3, 2) . '/' . $md5;

    if (!file_exists($cacheFile)) {
        exit('缓存不存在。');
    }

    if (@unlink($cacheFile)) {
        echo '清除缓存成功。';
    } else {
        echo '清除缓存失败。';
    }
{% endhighlight %}
