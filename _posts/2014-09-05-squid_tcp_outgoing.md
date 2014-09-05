---
layout: post
title: "squid代理服务器 用户验证访问，tcp_outgoing_address 出口IP随机调用"
categories: linux
tags: [squid, linux, 代理]
date: 2014-09-05 09:00:12
---

squid 代理服务器，使用用户名和密码访问代理，对于出口ip的不同方式的调用或者以随机的方式调用，因为服务器使用的是squid 2.7版本的，根据官方手册 3.2版本的有 acl xxx random 1/24 可以随机（未测试）

{% highlight bash %}
http_port 142.4.106.1:3128
http_port 142.4.106.xx:3128
http_port 142.4.106.xx:3128
auth_param basic program /user/lib/squid/libexec/ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid proxy-caching web server
auth_param basic credentialsttl 12 hours
auth_param basic casesensitive off
#使用用户或者用户组来确定出口的IP
#acl wltony proxy_auth wltony
#acl wltony1 proxy_auth wltony1
#tcp_outgoing_address 142.4.106.xxx wltony
#根据被访问服务器 IP 来确定出口IP
#acl no1 myip 142.4.106.xxx
#tcp_outgoing_address 142.4.106.xxx no1
acl src_73 src 142.4.106.xxx
acl src_74 src 142.4.106.xxx
tcp_outgoing_address 142.4.106.xxx src_73
tcp_outgoing_address 142.4.106.xxx src_74
#first_req 为主访问IP
acl first_req src 142.4.106.1
acl second_req src 142.4.106.xxx
acl second_req src 142.4.106.xxx
cache_peer 142.4.106.xxx parent 3128 0 round-robin no-query login=wltony:xxx
cache_peer 142.4.106.xxx parent 3128 0 round-robin no-query login=wltony:xxx
cache_peer_access 142.4.106.xxx allow first_req
cache_peer_access 142.4.106.xxx allow first_req
cache_peer_access 142.4.106.xxx deny second_req
cache_peer_access 142.4.106.xxx deny second_req
never_direct allow first_req
never_direct deny second_req
#close cache www.111cn.net
acl NCACHE method GET
no_cache deny NCACHE
acl ncsa_users proxy_auth REQUIRED
acl all src all
header_access Via deny all
header_access X-Forwarded-For deny all
http_access allow ncsa_users
#http_access allow wltony
#http_access allow wltony1
http_access deny all
{% endhighlight %}
