---
layout: post
title: "python中动态调用函数与判断类属性是否存在"
categories: python
tags: [python]
date: 2015-01-08 15:02:34
---

一.实现动态执行某个类中的函数<br>
<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr>#<span style="margin: 0px; padding: 0px; font-style: italic;">实例化类对象</span><br>

&nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr></span><span style="margin: 0px; padding: 0px; font-weight: bold;">atObj=ActTest()</span>&nbsp;<wbr>&nbsp;<wbr><br>

<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr>#<span style="margin: 0px; padding: 0px; font-style: italic;">动态调用类函数语句</span>&nbsp;<wbr><br>

<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr>
&nbsp;<wbr>getattr(</span></span><span style="margin: 0px; padding: 0px; font-weight: bold;">atObj&nbsp;<wbr></span><span style="margin: 0px; padding: 0px;"><span style="margin: 0px; padding: 0px; font-weight: bold;">,funcName)(args)</span>&nbsp;<wbr>#<span style="margin: 0px; padding: 0px; font-style: italic;">funcName-&gt;要调用的函数名，args-&gt;函数的参数</span><br>

<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr>
&nbsp;<wbr>简单吧！不过这样调用如果funcName传入的是ActTest类中不存在的函数或属性，就会抛出异常，就需要下面的判断过程。<br>

<span style="margin: 0px; padding: 0px;">二.判断类属性是否存在&nbsp;<wbr><br>
<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr>#<span style="margin: 0px; padding: 0px; font-style: italic;">我一般用callable来实现属性是否存在的判断，代码如下</span><br>

&nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr><span style="margin: 0px; padding: 0px; font-weight: bold;">if
callable(</span></span></span></span></span><span style="margin: 0px; padding: 0px; font-weight: bold;">getattr(atObj&nbsp;<wbr>,funcName)):</span></div>
<div style="margin: 0px; padding: 0px; font-family: Tahoma,'Microsoft Yahei'; line-height: 22px; background-color: rgb(255, 255, 255);">
<span style="margin: 0px; padding: 0px;"><span style="margin: 0px; padding: 0px;"><span style="margin: 0px; padding: 0px;"><span style="margin: 0px; padding: 0px;"><span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr></span></span></span></span></span><span style="margin: 0px; padding: 0px; font-weight: bold;">getattr(atObj&nbsp;<wbr>,funcName)(args)</span>&nbsp;<wbr><br>

<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr>#<span style="margin: 0px; padding: 0px; font-style: italic;">上面的语句还需要ActTest这样实现</span><br>

<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr><span style="margin: 0px; padding: 0px; font-weight: bold;">class
ActTest(object):<br>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr> def __init__(self):<br>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
self.xx='123'&nbsp;<wbr></span><br>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr></span></span>#<span style="margin: 0px; padding: 0px; font-style: italic;">&nbsp;<wbr>这个函数是关键，作用是获取属性！</span>&nbsp;<wbr><span style="margin: 0px; padding: 0px;"><br>

<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr> def&nbsp;<wbr></span></span><span style="margin: 0px; padding: 0px; font-weight: bold;">__getattribute__(self,
name): &nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr></span></div>
<div style="margin: 0px; padding: 0px; font-family: Tahoma,'Microsoft Yahei'; line-height: 22px; background-color: rgb(255, 255, 255);">
<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>try:</span></div>
<div style="margin: 0px; padding: 0px; font-family: Tahoma,'Microsoft Yahei'; line-height: 22px; background-color: rgb(255, 255, 255);">
<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>r=object.__getattribute__(self,
name)</span></div>
<div style="margin: 0px; padding: 0px; font-family: Tahoma,'Microsoft Yahei'; line-height: 22px; background-color: rgb(255, 255, 255);">
<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>except:</span></div>
<div style="margin: 0px; padding: 0px; font-family: Tahoma,'Microsoft Yahei'; line-height: 22px; background-color: rgb(255, 255, 255);">
<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
&nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>r=None&nbsp;<wbr></span></div>
<div style="margin: 0px; padding: 0px; font-family: Tahoma,'Microsoft Yahei'; line-height: 22px; background-color: rgb(255, 255, 255);">
<span style="margin: 0px; padding: 0px; font-weight: bold;">&nbsp;<wbr>
&nbsp;<wbr> &nbsp;<wbr>
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
return r</span><br>
<span style="margin: 0px; padding: 0px;">&nbsp;<wbr>
&nbsp;<wbr>
python在调用类属性时就会执行&nbsp;<wbr></span>__getattribute__，当获取异常时（这里只认为属性不存在），返回None；<br>

&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>那么callable(getattr(atObj&nbsp;<wbr>,funcName))就会返回false，我们就能根据这个结果决定是否动态调用函数了！<br>

<span style="margin: 0px; padding: 0px;"><br>
这是工作总结性的，不过已经简明的表述了一些要点，希望看到的也会有所帮助！&nbsp;<wbr></span>
