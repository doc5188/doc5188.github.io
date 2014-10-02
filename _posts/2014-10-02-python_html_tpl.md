---
layout: post
title: "python webpy模版功能" 
categories: python
tags: [python, webpy, webpy模板]
date: 2014-10-02 21:31:14
---

   模版功能的好处，简单说就是让你在写Html页面时更智能、更方便，内容可以实时运算、展开、显示出来。

这种特性在需要与数据库交互时优势更明显，最终显示给用户的是计算完成的页面。

     我接触web是从python开始，从python的王国里找到了webpy，让我从无到有，认识了web，包括前端

html,css,js等等和后端nginx。虽然满世界的人都在讨论web是php 好或者python好，又或者是在php和Python

各自的世界里，哪个框架好。这个是另一个话题了。但是我从webpy中认识了web，因为它很简单。另外它

可以使用python中的很多功能，在后台应用程序中使用很方便。

      这里顺便记录下几个页面

      lajphttps://code.google.com/p/lajp/

     php-python:https://code.google.com/p/ppython/

    讨论pythonweb框架的博客：http://blog.csdn.net/raptor/article/details/8933881

    instagram: http://www.damndigital.com/archives/39684

     python and php:http://developer.51cto.com/art/201208/351651.htm

    不好的消息是webpy发起人挂掉了，现在有其他人在github上更新代码，现在正在往python3.x迁移。

     https://github.com/webpy/webpy/commits/python3

     不过我觉得webpy轮子基本造好了，因为它可以使用很多python的功能，相当于站在巨人肩膀上。

  这样对于前端也够了，毕竟后端有nginx。

       最近忍不住到w3s上看了下php，发现了一些功能我在webpy中没用过，例如Include，函数等等,觉得很好。

我仔细翻了下webpy的文档，发现它的模版里其实也有这样的功能。

    模版功能页面：http://webpy.org/docs/0.3/templetor

   模版功能大体分几大类：$功能，$空格 功能，$冒号  功能，$def 模版功能，$code 纯Python代码块功能，$var 属性功能

1，$功能：就是$的后面跟的是一句python语句 行。例如一些控制语句,for,while。执行某个函数等。

例如控制语句：http://webpy.org/docs/0.3/templetor#controlstructure，这里面的a.pop()可以理解为执行某个函数。

 

2，$空格功能:：如果$后面跟着一个空格，则表示定义一个新变量

例如：http://webpy.org/docs/0.3/templetor#assignments

这里面的get_bug(id)应该是一个函数，函数计算结果返回给一个新变量。

 

3，$冒号功能：如果$后面跟着一个冒号:，则表示冒号后的对象以Html形式显示。否则就会是一些对应的字符串。这个

功能可以对应为php中的include功能。但是webpy为了安全，不支持html中直接import，而是借助于$def with带入。

2，$def 功能：这个可以理解成一个模版，即Html 语法块，语法块中支持$功能和标准Html语法。

3，$code 功能：这个是纯Python代码，即可以在Html中写python代码，但是这个代码不能带Html语法，只能是纯粹的python代码。

4，$var功能：这个可以为当前的渲染页面对象提供一个额外的属性。

 

所以根据以上性质，我们在webpy的html中若有以下需求：

1，引用某个个变量，def函数，或者一个class类。

可以使用$功能，此功能可以像python函数一样执行，你可以在后台应用程序py文件中定义

好这个方法、类或者变量。甚至在html代码中直接用$code去写

2，如果你想类似于c,c++,php风格的include。

你可以在Html代码中生成一个$def 模版，或者在后台应用程序py文件中定义另一个html的render对象，然后作为参数传入。

3，如果你想使用python的函数

如果是内建的函数，例如string里面的upper()，可以在html代码中直接使用。例如$ 'test'.upper()

如果是需要import的，则变为global类型，例如http://webpy.org/docs/0.3/templetor#builtins

这样在html代码中也可以直接使用。比如生成一个日期。

 
