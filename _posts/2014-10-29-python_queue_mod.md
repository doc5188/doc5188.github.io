---
layout: post
title: "python Queue模块"
categories: python
tags: [python queue]
date: 2014-10-29 22:51:49
---

创建一个“队列”对象

{% highlight bash %}
import Queue
myqueue = Queue.Queue(maxsize = 10)
{% endhighlight %}

Queue.Queue类即是一个队列的同步实现。队列长度可为无限或者有限。可通过Queue的构造函数的可选参数maxsize来设定队列长度。如果maxsize小于1就表示队列长度无限。

将一个值放入队列中

{% highlight bash %}
myqueue.put(10)
{% endhighlight %}

调用队列对象的put()方法在队尾插入一个项目。put()有两个参数，第一个item为必需的，为插入项目的值；第二个block为可选参数，默认为1。如果队列当前为空且block为1，put()方法就使调用线程暂停,直到空出一个数据单元。如果block为0，put方法将引发Full异常。

将一个值从队列中取出

{% highlight bash %}
myqueue.get()
{% endhighlight %}

调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。如果队列为空且block为False，队列将引发Empty异常。


python queue模块有三种队列:
<pre>
1、python queue模块的FIFO队列先进先出。
2、LIFO类似于堆。即先进后出。
3、还有一种是优先级队列级别越低越先出来。 
</pre>

针对这三种队列分别有三个构造函数:
<pre>
1、class Queue.Queue(maxsize) FIFO 
2、class Queue.LifoQueue(maxsize) LIFO 
3、class Queue.PriorityQueue(maxsize) 优先级队列 
</pre>

介绍一下此包中的常用方法:
<pre>
Queue.qsize() 返回队列的大小 
Queue.empty() 如果队列为空，返回True,反之False 
Queue.full() 如果队列满了，返回True,反之False
Queue.full 与 maxsize 大小对应 
Queue.get([block[, timeout]])获取队列，timeout等待时间 
Queue.get_nowait() 相当Queue.get(False)
非阻塞 Queue.put(item) 写入队列，timeout等待时间 
Queue.put_nowait(item) 相当Queue.put(item, False)
Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
Queue.join() 实际上意味着等到队列为空，再执行别的操作
</pre>
 
 
附上一个例子:
{% highlight bash %}
#coding:utf-8  
  
import Queue  
import threading  
import time  
import random  
  
q = Queue.Queue(0) #当有多个线程共享一个东西的时候就可以用它了  
NUM_WORKERS = 3  
  
class MyThread(threading.Thread):  
  
    def __init__(self,input,worktype):  
       self._jobq = input  
       self._work_type = worktype  
       threading.Thread.__init__(self)  
  
    def run(self):  
       while True:  
           if self._jobq.qsize() > 0:  
               self._process_job(self._jobq.get(),self._work_type)  
           else:break  
  
    def _process_job(self, job, worktype):  
       doJob(job,worktype)  
  
def doJob(job, worktype):  
   time.sleep(random.random() * 3)  
    print"doing",job," worktype ",worktype  
  
if __name__ == '__main__':  
    print "begin...."  
    for i inrange(NUM_WORKERS * 2):  
       q.put(i) #放入到任务队列中去  
    print "job qsize:",q.qsize()  
  
    for x inrange(NUM_WORKERS):  
       MyThread(q,x).start()  
{% endhighlight %}
一些需要注意的地方：

1. 阻塞模式

{% highlight bash %}
import Queue

q = Queue.Queue(10)

......
       for i in range(10):
               q.put('A')
               time.sleep(0.5)
{% endhighlight %}
这是一段极其简单的代码（另有两个线程也在操作队列q），我期望每隔0.5秒写一个'A'到队列中，但总是不能如愿：间隔时间有时会远远超过0.5秒。原来，Queue.put（）默认有 block = True 和 timeou 两个参数。当  block = True 时，写入是阻塞式的，阻塞时间由 timeou  确定。当队列q被（其他线程）写满后，这段代码就会阻塞，直至其他线程取走数据。Queue.put（）方法加上 block=False 的参数，即可解决这个隐蔽的问题。但要注意，非阻塞方式写队列，当队列满时会抛出 exception Queue.Full 的异常。

2. 无法捕获 exception Queue.Empty 的异常

{% highlight bash %}
while True:
                ......
                try:
                        data = q.get()
                except Queue.Empty:
                        break
{% endhighlight %}

我的本意是用队列为空时，退出循环，但实际运行起来，却陷入了死循环。这个问题和上面有点类似：Queue.get（）默认的也是阻塞方式读取数据，队列为空时，不会抛出 except Queue.Empty ，而是进入阻塞直至超时。 加上block=False 的参数，问题迎刃而解。
