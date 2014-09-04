---
layout: post
title: "关于pxssh -----用于在远程linux上执行命令"
categories: python
tags: [python, linux, pexpect, pxssh]
date: 2014-09-04 17:50:21
---
<pre>
>>> import pxssh
>>> s = pxssh.pxssh(timeout=300)
>>> s.login('192.168.217.20','root','sbfnje')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/usr/lib/python2.6/site-packages/pxssh.py", line 243, in login
if not self.synch_original_prompt():
File "/usr/lib/python2.6/site-packages/pxssh.py", line 134, in synch_original_prompt
self.read_nonblocking(size=10000,timeout=1) # GAS: Clear out the cache before getting the prompt
File "/usr/lib/python2.6/site-packages/pexpect.py", line 824, in read_nonblocking
raise TIMEOUT ('Timeout exceeded in read_nonblocking().')
pexpect.TIMEOUT: Timeout exceeded in read_nonblocking().
>>>
>>>
</pre>

解决方法：

修改site-packages/pxssh.py

在def synch_original_prompt (self):方法下第一个self.read_nonblocking(size=10000,timeout=1) 前面增加两行代码

<pre>
self.sendline()

time.sleep(0.5)
</pre>
