---
layout: post
date: 2014-09-05 12:46:21
categories: linux
tags: [linux, squid]
title: "基于认证的代理平台搭建配置squid-20130730"
---

功能：通过squid代理实现
<pre>
(1)基于用户名密码认证的出口ip路由选择
(2)基于client源ip的出口ip路由选择
(3)基于连接本机ip的出口ip路由选择
(4)实现高度匿名代理
(5)通过snmp使用cacti监控squid的状态
</pre>


一、squid 安装过程
{% highlight bash %}
# wget http://www.squid-cache.org/Versions/v3/3.3/squid-3.3.8.tar.gz
# tar xzvf squid-3.3.8.tar.gz 
# cd squid-3.3.8
# ./configure --prefix=/usr/local/squid
# make
# make install
{% endhighlight %}


二、开启多个公网ip

公网网卡挂接多个ip地址
{% highlight bash %}
# cp /etc/sysconfig/network-scripts/ifcfg-em2   /etc/sysconfig/network-scripts/ifcfg-em2:1
# cp /etc/sysconfig/network-scripts/ifcfg-em2   /etc/sysconfig/network-scripts/ifcfg-em2:2
# cp /etc/sysconfig/network-scripts/ifcfg-em2   /etc/sysconfig/network-scripts/ifcfg-em2:3

{% endhighlight %}

修改里面的DEVICE和ip行，如下：
{% highlight bash %}
# more ifcfg-em2:1
DEVICE=em2:1
BOOTPROTO=none
HWADDR=90:b1:1c:37:a9:16
IPV6INIT=no
NM_CONTROLLED=yes
ONBOOT=yes
TYPE=Ethernet
UUID="db3f67fb-b389-4b64-a765-92ada4f0ce0a"
USERCTL=no
IPADDR=1.1.134.117
NETMASK=255.255.255.224
{% endhighlight %}


重启网络
{% highlight bash %}
# /etc/init.d/network restart
{% endhighlight %}


查看公网ip是否在线
{% highlight bash %}
# ifconfig 
{% endhighlight %}


三、安装所需软件包
因用户认证需要htpasswd及ab压力测试需要，故需要安装httpd
{% highlight bash %}
# yum install httpd
{% endhighlight %}


因squid的snmp功能需要通过net-snmp代理，故需安装
{% highlight bash %}
# yum install -y net-snmp-utils
{% endhighlight %}




四、squid配置文件：
{% highlight bash %}
# more /usr/local/squid/etc/squid_multi_instance_conf/squid_multi_instance.conf 
####configured by laijingli


###only listen on private ip 
http_port 192.168.0.6:65500
#http_port 1.1.134.122:65500


###允许使用代理的ip段
acl ip_allow src 1.1.134.0/24 2.2.235.0/24 192.168.0.0/24 


###lable for debugging
visible_hostname squid_inst_30
cache_mgr laijingli


##auth
auth_param basic program /usr/local/squid/libexec/basic_ncsa_auth /usr/local/squid/etc/squid_multi_instance_conf/users.txt
auth_param basic children 10
auth_param basic realm  proxy server
auth_param basic credentialsttl 12 hours
auth_param basic casesensitive off


##enable auth,and only allow ip_allow and authed user to use this proxy
acl ncsa_users proxy_auth REQUIRED
http_access allow all
#http_access allow ip_allow ncsa_users
#http_access allow ncsa_users


##route outgoing ip address by authed user name
acl u1 proxy_auth u1
acl u2 proxy_auth u2
acl u3 proxy_auth u3
tcp_outgoing_address 1.1.134.117 u1
tcp_outgoing_address 1.1.134.118 u2
tcp_outgoing_address 1.1.134.119 u3


##route outgoing ip address by connected ip or client's source ip
#acl ip1  myip 1.1.134.123 
acl ip1  src 192.168.0.200
tcp_outgoing_address 1.1.134.107 ip1


#acl ip2  src 192.168.0.15
#tcp_outgoing_address 1.1.134.124 ip2


#acl ip3  src 192.168.0.0/24
#tcp_outgoing_address 1.1.134.125 ip3




###logs
pid_filename /usr/local/squid/var/logs/squid_30.pid
cache_log /usr/local/squid/var/logs/cache_30.log 
access_log /usr/local/squid/var/logs/access_30.log


###snmp monitor by cacti
acl CactiServer src 127.0.0.1 #写本机,因为要用net-snmp做代理
acl SNMP snmp_community community_cacti
snmp_port 3401
snmp_access allow SNMP CactiServer
snmp_access deny ALL




### anonymous 匿名代理
#forwarded_for off #HTTP_X_FORWARDED_FOR: unknown
request_header_access Allow allow all
request_header_access Authorization allow all
request_header_access WWW-Authenticate allow all
request_header_access Proxy-Authorization allow all
request_header_access Proxy-Authenticate allow all
request_header_access Cache-Control allow all
request_header_access Content-Encoding allow all
request_header_access Content-Length allow all
request_header_access Content-Type allow all
request_header_access Date allow all
request_header_access Expires allow all
request_header_access Host allow all
request_header_access If-Modified-Since allow all
request_header_access Last-Modified allow all
request_header_access Location allow all
request_header_access Pragma allow all
request_header_access Accept allow all
request_header_access Accept-Charset allow all
request_header_access Accept-Encoding allow all
request_header_access Accept-Language allow all
request_header_access Content-Language allow all
request_header_access Mime-Version allow all
request_header_access Retry-After allow all
request_header_access Title allow all
request_header_access Connection allow all
request_header_access Proxy-Connection allow all
request_header_access User-Agent allow all
request_header_access Cookie allow all
request_header_access All deny all

{% endhighlight %}




五、start、stop命令

squid启动脚本
{% highlight bash %}
# more /usr/local/squid/etc/squid_multi_instance_conf/start_squid.sh 
#!/bin/bash
/usr/local/squid/sbin/squid -f /usr/local/squid/etc/squid_multi_instance_conf/squid_multi_instance.conf 
netstat -anp|grep LIST|grep squid 
{% endhighlight %}


squid关闭脚本
{% highlight bash %}
# more /usr/local/squid/etc/squid_multi_instance_conf/stop_squid.sh 
#!/bin/bash
ps aux|grep squid|grep -v grep|awk '{print $2}'|xargs kill -9
{% endhighlight %}


六、检查squid运行是否正常
检查squid是否正常启动
{% highlight bash %}
# netstat -anp|grep LIST|grep squid
tcp        0      0 192.168.0.6:65500           0.0.0.0:*                   LISTEN      31077/(squid-1)     

{% endhighlight %}

检查squid是否正常启动
{% highlight bash %}
# ps uax|grep squid                
root     31074  0.0  0.0  50184  1796 ?        Ss   15:59   0:00 /usr/local/squid/sbin/squid -f 


/usr/local/squid/etc/squid_multi_instance_conf/squid_multi_instance.conf
nobody   31077  0.1  0.1  88824 19820 ?        S    15:59   0:00 (squid-1) -f 


/usr/local/squid/etc/squid_multi_instance_conf/squid_multi_instance.conf
root     31091  0.0  0.0 103244   832 pts/1    S+   15:59   0:00 grep squid
{% endhighlight %}


检查squid snmp支持是否
{% highlight bash %}
# snmpwalk -v 1 -c community_cacti 127.0.0.1:3401 .1.3.6.1.4.1.3495.1 
{% endhighlight %}


配置使用snmp代理
{% highlight bash %}
# more /etc/snmp/snmpd.conf 
##snmp proxy
proxy -v 1 -c community_cacti 127.0.0.1:3401 .1.3.6.1.4.1.3495.1
{% endhighlight %}


检查使用snmp代理后是否可以获取oid信息
{% highlight bash %}
# snmpwalk -v 1 -c community_cacti localhost:161 .1.3.6.1.4.1.3495.1
{% endhighlight %}


安装cacti监控模板（略）
{% highlight bash %}
https://github.com/dezwart/cacti-squid
{% endhighlight %}

cacti监控截图
<img src="/upload/images/20130730094847562.png">




测试代理是否正确工作
{% highlight bash %}
# curl -U u4:123456  -x 192.168.0.32:65500 --proxy-basic  http://1.1.134.112/myip.php;echo 
{% endhighlight %}


测试是否使用了匿名代理
http://www.iprivacytools.com/proxy-checker-anonymity-test/


七、代理性能测试

测试页面：
{% highlight bash %}
# more /var/www/app1/myip.php 
<?php
$iipp=$_SERVER["REMOTE_ADDR"];
echo $iipp;
?>
{% endhighlight %}

{% highlight bash %}


# ab -c 100 -n 10000  http://1.1.134.112/myip.php      
# ab -c 100 -n 10000 -X 192.168.0.6:65500 http://1.1.134.112/myip.php 
{% endhighlight %}


<table width="802" height="345" style="width:601.5pt; border-collapse:collapse">
<colgroup><col width="169"><col width="93"><col width="120"><col width="167"><col width="253"></colgroup>
<tbody>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
&nbsp;ab&nbsp;-c&nbsp;1&nbsp;-n&nbsp;10000&nbsp;</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
耗时（秒）</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
请求丢失个数</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每秒请求数（约）</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每个并发请求耗时（毫秒）</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
不使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
6.5</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
1538</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.65</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
13</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
769</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
1.3</td>
</tr>
<tr height="23">
<td width="169" height="23" style="width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="93" height="23" style="width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="120" height="23" style="width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="167" height="23" style="width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="253" height="23" style="width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
&nbsp;ab&nbsp;-c&nbsp;10&nbsp;-n&nbsp;10000&nbsp;</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
耗时（秒）</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
请求丢失个数</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每秒请求数（约）</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每个并发请求耗时（毫秒）</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
不使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
4.8</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
2083</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.048</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
4.2</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
2380</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.042</td>
</tr>
<tr height="23">
<td width="169" height="23" style="width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="93" height="23" style="width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="120" height="23" style="width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="167" height="23" style="width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="253" height="23" style="width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
&nbsp;ab&nbsp;-c&nbsp;50&nbsp;-n&nbsp;10000&nbsp;</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
耗时（秒）</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
请求丢失个数</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每秒请求数（约）</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每个并发请求耗时（毫秒）</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
不使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
3.6</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
2777</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.0072</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
3.5</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
2857</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.007</td>
</tr>
<tr height="23">
<td width="169" height="23" style="width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="93" height="23" style="width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="120" height="23" style="width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="167" height="23" style="width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
<td width="253" height="23" style="width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et3">
&nbsp;</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
&nbsp;ab&nbsp;-c&nbsp;100&nbsp;-n&nbsp;10000&nbsp;</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
耗时（秒）</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
请求丢失个数</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每秒请求数（约）</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
平均每个并发请求耗时（毫秒）</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
不使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
3.4</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
2941</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.0034</td>
</tr>
<tr height="23">
<td width="169" height="23" style="border:0.5pt solid rgb(0,0,0); width:126.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
使用代理</td>
<td width="93" height="23" style="border:0.5pt solid rgb(0,0,0); width:69.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
3.6</td>
<td width="120" height="23" style="border:0.5pt solid rgb(0,0,0); width:90pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0</td>
<td width="167" height="23" style="border:0.5pt solid rgb(0,0,0); width:125.25pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
2777</td>
<td width="253" height="23" style="border:0.5pt solid rgb(0,0,0); width:189.75pt; height:17.25pt; font-size:12pt; vertical-align:middle" class="et2">
0.0036</td>
</tr>
</tbody>
</table>

结论：

使用显示ip地址的简单php页面做了一下测试：ab并发100连续请求10000次，直接测试耗时3.4秒，使用代理测试耗时3.5秒，多次测试都没有出现请求失败的


情况，平均每秒可以处理2800个请求。

<pre>
原文：
http://blog.csdn.net/xuyaqun/article/details/9623635
</pre>
