---
layout: post
title: "python如何判断一个变量/类是否存在"
categories: python 
tags: [python]
date: 2015-01-08 14:58:04
---

<pre>
Python 2.5.4 (r254:67916, Dec 23 2008, 15:10:54) [MSC v.1310 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.

    ****************************************************************
    Personal firewall software may warn about the connection IDLE
    makes to its subprocess using this computer's internal loopback
    interface.  This connection is not visible on any external
    interface and no data is sent to or received from the Internet.
    ****************************************************************
   
IDLE 1.2.4      
>>> dir()
['__builtins__', '__doc__', '__name__']
>>> 's' in dir()
False
>>> s = 'hello, python'
>>> 's' in dir()
True
>>>

<pre>
