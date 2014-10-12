---
layout: post
title: "Python动态创建类［总结］"
categories: python
tags: [python]
date: 2014-10-12 21:32:49
---

理论：

1. globals()

全局变量那就 globals().update(dic).这样就可以将一个字典变量弄成全局变量.

创建动态类两种方式：

{% highlight python %}
from new import classobj
myClass = classobj('className',(baseClass,),{dictAttr:dictValue,...})
{% endhighlight %}

参数说明：
<pre>
classobj(类名，基类列表--必须是tuple,属性字典)
这个时候类的名字不等于类的索引，上面创建的类需要通过myClass来使用。
如果想要把类自己的名字来引用，就像传统的class关键字定义那样，则需要把类的名字加入到全局作用域globals()
globals()['className'] = type('className',(baseClass,),{dictAttr:dictValue,...})
</pre>

2. 来看示例

{% highlight python %}
class Base(object):
    name = "yao"
    age = 23
    def setUp(self):
        if hasattr(self, "name"):
            print "setUp, %s" % getattr(self, "name")

from new import classobj
myClass= classobj("HelloClass", (Base, ), {"***":"boy", "school":"hn"})
myobject = myClass()
myobject.setUp()
print myobject.*** + " ->" + str(myobject.age)
# >>> 
print getattr(myobject, "school")


def initParent():
    globals()['MyChildClass']=type("MyChildClass", (Base, ), {"***":"girl",
        "school":"nn"})

initParent()
myobject = MyChildClass()
myobject.newAttr = "hello"  #动态创建属性

print myobject.***, myobject.school
print getattr(myobject, "newAttr")

class A(MyChildClass):      #MyChildClass就是动态创建的类。
    def testup(self):
        if hasattr(self, "***"):
            print " have *** attritue, %s" % getattr(self, "***")
        
        if hasattr(self, "newAttr"):  #这样的属性就没有了
            print "HAVEing!"
a = A()
a.testup()
输出：
setUp, yao
boy ->23
hn
girl nn
hello
have *** attritue, girl


{% endhighlight %}
一种应用的场景：

比如在CMDB里面会有多种manfiest设备类型，会有多种类型会有各种不一样的child方法。

这样如果 需要创建多个父类的话可以传递一个变量进去就可以生成多个类。然后就可以继承

可以节省不少的代码量.
