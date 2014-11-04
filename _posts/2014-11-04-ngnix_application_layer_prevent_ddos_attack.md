---
layout: post
title: "Nginx针对应用层DDOS攻击的对策"
categories: linux
tags: []
date: 2014-11-04 11:25:08
---

最近博客接连碰到几次短时间的DDOS攻击，这些攻击的特点是瞬间猛增，连预警的时间都没有，大约是每台每秒3000-50000+的HTTP请求包，然后Nginx在苦撑90秒到120秒之后挂掉。这些流量还是很恐怖的，要知道我们最前面有20几台Nginx。让人郁闷的是，Nginx挂掉以后，服务器彻底挂了，需要重启才能恢复应用。

以下为我们的一些对策，希望尽可能的保证Nginx能撑更多的连接与时间，延缓服务的挂掉，保证正常的服务请求。在攻击过后，能迅速恢复。

* 1、限制Nginx的最高连接数，Nginx不应当负担超过它物理资源限制的负载，这样不至于Nginx整个系统拖垮。

而物理资源的限制主要是内存，CPU等，CPU不知道怎么去衡量，一般是让worker数目与CPU相等。我大概计算了下，大概2G的内存可以支撑5W的连接，所以Nginx的配置最好不要超过这个值。比如我的CPU是双核的，而内存是2G，则最好这样配置：
<pre>
worker_processes  2;
events {
    worker_connections  20000;
}
</pre>

* 2、缩短超时时间，减少资源累计的消耗

由于我们Nginx都是作反向代理用的，Nginx会维持客户端与上游服务器两个连接，这些是比较耗资源的。攻击时，出现大量后端请求超时和拒绝连接，说明后端应用服务器已经不能再处理新的请求了，所以我们认为应当减小与后端连接超时，默认的时间太长了，有60秒。还有就是前端keepalive的超时：
<pre>
keepalive_timeout 5;
proxy_connect_timeout 5;
proxy_read_timeout 5;
proxy_send_timeout 5;
</pre>

* 3、巧用limit_req模块

通过分析，我们发现，这些DDOS攻击的形式是HTTP应用层的攻击，而不是通常意义上的SYN-flood之类的攻击，所以我们可以在应用层上做一些限制。

a、限制单个ip的并发连接数。当然DDOS攻击时其实由于ip众多，大家后来也就是拼体力了。

<pre>
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s

server {
 ...
location /some {
limit_req zone=one burst=50;
}
}
</pre>

b、通过分析，我们发现这些请求的host或者url都很集中，基本就是几个博客，而我们用的都是泛域名，类似xxx.blog.163.com，所以我们可以配置限制host或其他限制的变量。

<pre>
limit_req_zone $host zone=two:20m rate=500r/s

server {
...
location /some {
limit_req zone=two burst=1000;
}
}
</pre>

就算有些名人博客，我觉得500人每秒的并发访问已经很恐怖了，一般应该够了吧。

* 4、分析攻击的包，比如攻击包的user-agent是比较特殊的，可以通过变量来直接禁止。

* 5、如果他们攻击的是根目录，也就是没法通过域名变量来禁止，都是正常的包，那就通过把动态GET请求转为静态来实现，那样系统处理能力可以增加很多。比如可以用Nginx的cache功能，或者前面加varnish、squid都可以。

* 6、如果还不行，而且经常受攻击，那就去买ddos攻击的防火墙吧。。。。或者用CDN估计也可以。

<pre>
referer: http://yaoweibin2008.blog.163.com/blog/static/1103139201092654039315/
</pre>
