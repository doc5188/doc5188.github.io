---
layout: post
title: "python的加密模块(md5,sha,crypt)学习"
categories: python
tags: [python, python加密]
date: 2015-01-08 15:11:16
---

md5(Message-Digest Algorithm 5) 模块用于计算信息密文（信息摘要），得出一个128位的密文。sha模块跟md5相似，但生成的是160位的签名。使用方法是相同的。

如下实例是使用md5的：

<pre>

# /usr/bin/python
# -*- coding:utf-8 -*-
import base64
try:
    import hashlib
    hash = hashlib.md5()
except ImportError:
    # for Python << 2.5
    import md5
    hash = md5.new()
hash.update('spam,spam,and egges')
value = hash.digest()
print repr(value)   #得到的是二进制的字符串
print hash.hexdigest()  #得到的是一个十六进制的值
print base64.encodestring(value) #得到base64的值
</pre>


<pre>
# /usr/bin/python
# -*- coding:utf-8 -*-
# 客户端与服务器端通信的信息的验证

import string
import random

def getchallenge():
    challenge = map(lambda i: chr(random.randint(0,255)),range(16))
    return string.join(challenge,"")

def getresponse(password,challenge):
    try:
        import hashlib
        hash = hashlib.md5()
    except ImportError:
        # for Python << 2.5
        import md5
        hash = md5.new()
    hash.update(password)
    hash.update(challenge)
    return  hash.digest()

print "client: ","connect"
challenge= getchallenge()
print "server: ",repr(challenge)
client_response = getresponse("trustno1",challenge)
print "client: ",repr(client_response)
server_response = getresponse("trustno1",challenge)
if client_response == server_response:
    print "server:","login ok"
</pre>


crypt 模块(只用于 Unix)实现了单向的 DES 加密, Unix 系统使用这个加密算法来储存密码, 这个模块真正也就只在检查这样的密码时有用.
如下实例 展示了如何使用 crypt.crypt 来加密一个密码, 将密码和 salt组合起来然后传递给函数, 这里的 salt 包含两位随机字符.现在你可以扔掉原密码而只保存加密后的字符串了.


<pre>
# /usr/bin/python
# -*- coding:utf-8 -*-

import crypt
import random,string

def getsalt(chars = string.letters+string.digits):
    return random.choice(chars)+random.choice(chars)

salt = getsalt()
print salt
print crypt.crypt('bananas',salt)
</pre>


 
