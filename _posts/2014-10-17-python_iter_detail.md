---
layout: post
title: "python的迭代器与生成器实例详解"
categories: python 
tags: [python, python迭代器, python生成器]
date: 2014-10-17 13:04:05
---

本文以实例详解了python的迭代器与生成器，具体如下所示：

* 1. 迭代器概述：
 
迭代器是访问集合元素的一种方式。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退，不过这也没什么，因为人们很少在迭代途中往后退。
 
* 1.1 使用迭代器的优点
 
对于原生支持随机访问的数据结构（如tuple、list），迭代器和经典for循环的索引访问相比并无优势，反而丢失了索引值（可以使用内建函数enumerate()找回这个索引值）。但对于无法随机访问的数据结构（比如set）而言，迭代器是唯一的访问元素的方式。

另外，迭代器的一大优点是不要求事先准备好整个迭代过程中所有的元素。迭代器仅仅在迭代到某个元素时才计算该元素，而在这之前或之后，元素可以不存在或者被销毁。这个特点使得它特别适合用于遍历一些巨大的或是无限的集合，比如几个G的文件，或是斐波那契数列等等。

迭代器更大的功劳是提供了一个统一的访问集合的接口，只要定义了__iter__()方法对象，就可以使用迭代器访问。
 
迭代器有两个基本的方法
 
<pre>
next方法：返回迭代器的下一个元素
__iter__方法：返回迭代器对象本身
</pre>
下面用生成斐波那契数列为例子，说明为何用迭代器
 
示例代码1
{% highlight bash %}
def fab(max):
 n, a, b = 0, 0, 1
 while n < max:
   print b
   a, b = b, a + b
   n = n + 1
{% endhighlight %}

直接在函数fab(max)中用print打印会导致函数的可复用性变差，因为fab返回None。其他函数无法获得fab函数返回的数列。
 
示例代码2
{% highlight bash %}
def fab(max):
 L = []
 n, a, b = 0, 0, 1
 while n < max:
   L.append(b)
   a, b = b, a + b
   n = n + 1
 return L
{% endhighlight %}

代码2满足了可复用性的需求，但是占用了内存空间，最好不要。
 
示例代码3
 
对比：
	
{% highlight bash %}
for i in range(1000): pass
for i in xrange(1000): pass
{% endhighlight %}

前一个返回1000个元素的列表，而后一个在每次迭代中返回一个元素，因此可以使用迭代器来解决复用可占空间的问题
 
{% highlight bash %}
class Fab(object):
 def __init__(self, max):
   self.max = max
   self.n, self.a, self.b = 0, 0, 1
 
 def __iter__(self):
   return self
 
 def next(self):
   if self.n < self.max:
     r = self.b
     self.a, self.b = self.b, self.a + self.b
     self.n = self.n + 1
     return r
   raise StopIteration()
{% endhighlight %}

执行
<pre>
>>> for key in Fabs(5):
  print key
</pre>

Fabs 类通过 next() 不断返回数列的下一个数，内存占用始终为常数　　

* 1.2 使用迭代器

使用内建的工厂函数iter(iterable)可以获取迭代器对象：
	
<pre>
>>> lst = range(5)
>>> it = iter(lst)
>>> it
<listiterator object at 0x01A63110>
</pre>

使用next()方法可以访问下一个元素：
<pre>
>>> it.next()
  
>>> it.next()
  
>>> it.next()
</pre>

python处理迭代器越界是抛出StopIteration异常
	
{% highlight bash %}
>>> it.next()
  
>>> it.next
<method-wrapper 'next' of listiterator object at 0x01A63110>
>>> it.next()
  
>>> it.next()
  
Traceback (most recent call last):
 File "<pyshell#27>", line 1, in <module>
  it.next()
StopIteration

{% endhighlight %}

了解了StopIteration，可以使用迭代器进行遍历了
	
{% highlight bash %}
lst = range(5)
it = iter(lst)
try:
  while True:
    val = it.next()
    print val
except StopIteration:
  pass
{% endhighlight %}

事实上，因为迭代器如此普遍，python专门为for关键字做了迭代器的语法糖。在for循环中，Python将自动调用工厂函数iter()获得迭代器，自动调用next()获取元素，还完成了检查StopIteration异常的工作。如下
	
<pre>
>>> a = (1, 2, 3, 4)
>>> for key in a:
  print key
</pre>

首先python对关键字in后的对象调用iter函数迭代器，然后调用迭代器的next方法获得元素，直到抛出StopIteration异常。

* 1.3 定义迭代器
 
下面一个例子——斐波那契数列
	
{% highlight bash %}
# -*- coding: cp936 -*-
class Fabs(object):
  def __init__(self,max):
    self.max = max
    self.n, self.a, self.b = 0, 0, 1 #特别指出：第0项是0，第1项是第一个1.整个数列从1开始
  def __iter__(self):
    return self
  def next(self):
    if self.n < self.max:
      r = self.b
      self.a, self.b = self.b, self.a + self.b
      self.n = self.n + 1
      return r
    raise StopIteration()
  
print Fabs(5)
for key in Fabs(5):
  print key
{% endhighlight %}

结果

<__main__.Fabs object at 0x01A63090>

* 2. 生成器 

带有 yield 的函数在 Python 中被称之为 generator（生成器），几个例子说明下（还是用生成斐波那契数列说明）
 
可以看出代码3远没有代码1简洁，生成器（yield）既可以保持代码1的简洁性，又可以保持代码3的效果
 
示例代码4　
	
{% highlight bash %}
def fab(max):
  n, a, b = 0, 0, 1
  while n < max:
    yield b
    a, b = b, a + b
    n = n = 1
{% endhighlight %}

执行
<pre>
>>> for n in fab(5):
  print n
</pre>
简单地讲，yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，调用 fab(5) 不会执行 fab 函数，而是返回一个 iterable 对象！在 for 循环执行时，每次循环都会执行 fab 函数内部的代码，执行到 yield b 时，fab 函数就返回一个迭代值，下次迭代时，代码从 yield b 的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，直到再次遇到 yield。看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，每次中断都会通过 yield 返回当前的迭代值。
 
也可以手动调用 fab(5) 的 next() 方法（因为 fab(5) 是一个 generator 对象，该对象具有 next() 方法），这样我们就可以更清楚地看到 fab 的执行流程：
	
<pre>
>>> f = fab(3)
>>> f.next()
1
>>> f.next()
1
>>> f.next()
2
>>> f.next()
  
Traceback (most recent call last):
 File "<pyshell#62>", line 1, in <module>
  f.next()
StopIteration
</pre>

return作用

在一个生成器中，如果没有return，则默认执行到函数完毕；如果遇到return,如果在执行过程中 return，则直接抛出 StopIteration 终止迭代。例如
 
<pre>
>>> s = fab(5)
>>> s.next()
1
>>> s.next()
  
Traceback (most recent call last):
 File "<pyshell#66>", line 1, in <module>
  s.next()
StopIteration
</pre>

示例代码5  文件读取

{% highlight bash %}
def read_file(fpath):
 BLOCK_SIZE = 1024
 with open(fpath, 'rb') as f:
   while True:
     block = f.read(BLOCK_SIZE)
     if block:
       yield block
     else:
       return

{% endhighlight %}

如果直接对文件对象调用 read() 方法，会导致不可预测的内存占用。好的方法是利用固定长度的缓冲区来不断读取文件内容。通过 yield，我们不再需要编写读文件的迭代类，就可以轻松实现文件读取。
