---
layout: post
title: "Python定时执行之Timer"
categories: python
tags: [python定时器]
date: 2014-12-26 13:18:35
---



<pre>
    #!/usr/bin/env python  
      
      
    from threading import Timer  
    import time  
      
    timer_interval=1  
    def delayrun():  
        print 'running'  
      
    t=Timer(timer_interval,delayrun)  
    t.start()  
    while True:  
        time.sleep(0.1)  
        print 'main running'  
</pre>

t是一个Timer对象。【估计内部是使用一个线程】delay一秒钟之后执行delayrun函数。

其中time.sleep函数是用来让主线程暂停一点时间再继续执行。

Timer仅执行一次，若需要定时运行，则需要不断的调用。
