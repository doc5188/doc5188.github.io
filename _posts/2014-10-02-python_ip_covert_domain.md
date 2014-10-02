---
layout: post
title: "用python做ip和域名间的转换"
categories: python
tags: [python]
date: 2014-10-02 21:36:09
---

<pre>
# -*- coding: cp936 -*-
#这是一个域名和IP之间转换的程序

import sys, socket

opt = raw_input('1:通过IP查域名\n2:通过域名查IP')

while opt != '2' and opt != '1':

    print "请按正解的格式输入\n"

    opt = raw_input('1:通过IP查域名\n2:通过域名查IP')
    
if opt == '1':

    addr = raw_input('请输入IP地址:')

    try:

        result = socket.gethostbyaddr(addr)

    except socket.herror,e:

        print "找不到:",e

        raw_input('按任意键退出!')

        exit()

elif opt == '2':

    name = raw_input('请输入域名:')

    try:

        myaddr = socket.getaddrinfo(name,'http')[0][4][0]

        result = socket.gethostbyaddr(myaddr)

    except socket.herror,e:

        print "找不到"+myaddr+":",e

        raw_input('按任意键退出!')

        exit()

    except socket.gaierror, e1:

        print "找不到关于这个域名的信息"

        raw_input('按任意键退出!')

        exit()
        
print "Primary hostname:"

print "  " + result[0]

# Display the list of available addresses that is also returned

print "\nAddresses:"

for item in result[2]:

    print "  " + item

raw_input('按任意键退出!')

</pre>
