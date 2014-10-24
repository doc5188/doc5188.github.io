---
layout: post
title: "python判断ip是不是大陆的"
categories: python
tags: [判断IP所属国家]
date: 2014-10-23 23:38:24
---

判断ip是不是大陆的，方法如下:

1. 从apnic下载最新版的ipv4分配信息

2. 根据apnic的分配信息，把CN的摘出来

    每条CN的记录改成 开始ip，结束ip 这样的记录，放到list

3. 为了效率考虑，生成一个用于快速定位的字典:

    如: 114.11.11.11 这个ip, 开始先找到 114 在 list中的开始地址，让后在循环比较是不是CN的地址


现在最新的ip分配信息
{% highlight bash %}
wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O ip_apnic
{% endhighlight %}

生成cn的ip数据

{% highlight bash %}
#!/bin/env python
#coding: utf-8
import socket
import struct
 
def ip2int( ip ):
    return struct.unpack('!L',socket.inet_aton(ip))[0]
 
def int2ip( ip ):
    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))
 
if __name__ == '__main__':
    #亚洲区的ip分配记录
    fr = file("ip_apnic")
    #生成的数据文件
    fw = open("cn_net.py",'w')
    o = {}
    fw.write('iplist = [\n')
    #下面三个变量，只要为了效率，定位快一些
    j1 = 0
    j2 = 0
    h1 = ''
    for lin in fr.readlines():
        #注释
        if lin[0] == '#':
            continue
        #用|分开的格式
        v = lin.split('|')
        #只考虑ipv4
        if v[2] != 'ipv4' :
            continue
        #不是大陆的不用考虑
        if v[1] == '*' :
            continue
        if v[1] != 'CN':
            continue
        #为了效率，取ip地址的第一段作为定位
        h = v[3].split(".")
        if h[0] not in o:
            if h1:
                o[h1] = [j2,j1-1]
            j2 = j1
            h1 = h[0]
          
        #把ip转换成数字
        #cn的开始
        bgn_ip = ip2int( v[3] )
        #cn的结束
        end_ip = bgn_ip + int(v[4]) -1
        fw.write('(%d,%d),\n' % (bgn_ip,end_ip) )
        j1 = j1+1
    fw.write('(0,0)\n')
    fw.write(']\n\n')
 
    #最后在把用于快速定位的字典数据写到数据文件中
    fw.write('offset = ')
    fw.write(str(o))
    print o
{% endhighlight %}

CN的ip信息使用方式

{% highlight bash %}
#!/bin/python
#coding: utf-8
import socket
import struct
 
from cn_net import *
 
 
def ip2int( ip ):
    return struct.unpack('!L',socket.inet_aton(ip))[0]
 
def int2ip( ip ):
    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))
 
def iscn( ip ):
    '''检查的方法：
    1. 把ip地址的第一个段拿出来,如果不在offset中，则说明不是cn的地址
    2. 先把ip地址的第一个段拿出来，用于快速定位到iplist的开始位置，减少循环的次数
    3. 从开始位置，到结束位置查找，如果在里面，则是cn的ip '''
    int_ip = ip2int( ip )
    head = ip.split(".")[0]
 
    if head not in offset:
        return False
 
    for i in range(offset[head][0],offset[head][1]+1):
        if int_ip >= iplist[i][0] and int_ip <= iplist[i][1]:
            return True
    return False
 
if __name__ == '__main__':
    print iscn( "113.11.199.56" )
    print iscn( "8.8.8.8" )
    print iscn( "114.114.114.114" )
    print iscn( "114.114.115.115" )
{% endhighlight %}

<pre>
referer: http://www.oschina.net/code/snippet_177666_33250
</pre>
