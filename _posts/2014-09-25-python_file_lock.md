---
layout: post
title: "python的文件锁"
categories: python
tags: [linux, 文件锁]
date: 2014-09-25 23:13:48
---

python中文件操作往往会涉及到多个进程向同一个文件write的情况，这时要想保证同时只有一个进程写文件，可以采用如下方法：

使用fcntl.flock.

{% highlight python %}
    #coding:utf-8  
      
    """ 
    文件锁测试 
    """  
      
    import fcntl  
    import time  
      
    fp = open('hello.txt','w')  
    fcntl.flock(fp, fcntl.LOCK_EX)  
    print '文件锁开始执行'  
    time.sleep(100)  
    fcntl.flock(fp, fcntl.LOCK_UN)  
    fp.close()  
{% endhighlight %}
