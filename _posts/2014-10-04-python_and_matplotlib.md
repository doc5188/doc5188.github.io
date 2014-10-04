---
layout: post
title: "用 Python / Matplotlib 画出来的股票 K线图"
categories: python
tags: [python, matplotlib]
date: 2014-10-04 14:25:54
---



---- 过年后开始真正学用 Matplotlib 画一些实际的图形，以下是最新的改进结果：
<img src="/upload/images/600644.png" />

 

---- 股票是 600644，原始数据来自网络。就不总结要点了，Matplotlib 十分给力！

---- 下一步打算在标示价格的 Y 轴上使用对数坐标。得精确计算图片的尺寸，使代表相同涨幅的图线看起来具有相同的长度，而且要精确定位坐标点。另外还可以加上一定的注释和图例。

 

补记：已实现，如下图，注意 Y 轴对数坐标：


<img src="/upload/images/600644_exp.png" />

<pre>
来源:http://bluegene8210.is-programmer.com/posts/24606.html
</pre>
