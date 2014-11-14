---
layout: post
title: "python with(__enter__, __exit__)关键字用法"
categories: python 
tags: [python, with, __enter__, __exit__]
date: 2014-11-14 10:33:03
---
<pre>
with从Python 2.5就有，需要from __future__ import with_statement。
自python 2.6开始，成为默认关键字。
在What's new in python2.6/3.0中，明确提到：
The 'with' statement is a control-flow structure whose basic structure is:
with expression [as variable]: with-block
也就是说with是一个控制流语句，跟if/for/while/try之类的是一类的，with可以用来简化try finally代码，看起来可以比try finally更清晰。
这里新引入了一个"上下文管理协议"context management protocol，实现方法是为一个类定义__enter__和__exit__两个函数。
with expresion as variable的执行过程是，首先执行__enter__函数，它的返回值会赋给as后面的variable，想让它返回什么就返回什么，只要你知道怎么处理就可以了，如果不写as variable，返回值会被忽略。
然后，开始执行with-block中的语句，不论成功失败(比如发生异常、错误，设置sys.exit())，在with-block执行完成后，会执行__exit__函数。
这样的过程其实等价于：
try:
执行 __enter__的内容
执行 with_block.
finally:
执行 __exit__内容
只不过，现在把一部分代码封装成了__enter__函数，清理代码封装成__exit__函数。
我们可以自己实现一个例子：
import sys
class test:
def __enter__(self):
       print("enter")
       return 1
def __exit__(self,*args):
       print("exit")
       return True
with test() as t:
print("t is not the result of test(), it is __enter__ returned")
print("t is 1, yes, it is {0}".format(t))
raise NameError("Hi there")
sys.exit()
print("Never here")
注意:
1，t不是test()的值，test()返回的是"context manager object"，是给with用的。t获得的是__enter__函数的返回值，这是with拿到test()的对象执行之后的结果。t的值是1.
2，__exit__函数的返回值用来指示with-block部分发生的异常是否要re-raise，如果返回False，则会re-raise with-block的异常，如果返回True，则就像什么都没发生。
符合这种特征的实现就是符合“上下文管理协议”了，就可以跟with联合使用了。
as关键字的另一个用法是except XXX as e，而不是以前的except XXX,e的方式了。
此外，还可以使用contextlib模块中的contextmanager，方法是:
@contextmanager
...
yield something
...
的方式，具体需要看看文档和手册了。
yield的用法还是很神奇的，一句两句搞不清楚，如果您已经弄懂，看看文档就明白了，如果不懂yield，根据自己的需要去弄懂或者干脆不理他也可以，反正用到的时候，您一定回去搞懂的:-
其实with很像一个wrapper或者盒子，把with-block部分的代码包装起来，加一个头，加一个尾，头是__enter__，尾是__exit__，无论如何，头尾都是始终要执行的。


</pre>
