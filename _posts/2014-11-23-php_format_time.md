---
layout: post
title: "PHP 格式化显示时间 date 函数"
categories: php
tags: [php]
date: 2014-11-23 14:27:13
---
<h1>PHP 格式化显示时间 date 函数</h1><h2>格式化时间</h2>

<p>

date() 函数用于格式化时间，返回一个字符串。

</p>

<p>

语法：

</p>

<pre>

string date( string format [, int timestamp] )

</pre>

<p>

参数 format 表示时间格式化的方式，可能的方式如下：

</p>

<table class="table">

<caption>格式化方式说明：</caption>

<tr>

<th width="15%">格式化方式</th>

<th>说明</th>

</tr>

<tr>

<td>Y</td>

<td>4位数字年，y为2位数字，如99即1999年</td>

</tr>

<tr>

<td>m</td>

<td>数字月份，前面有前导0，如01。n 为无前导0数字月份</td>

</tr>

<tr>

<td>F</td>

<td>月份，完整的文本格式，例如 January 或者 March</td>

</tr>

<tr>

<td>M</td>

<td>三个字母缩写表示的月份，例如 Jan 或者 Mar</td>

</tr>

<tr>

<td>d</td>

<td>月份中的第几天，前面有前导0，如03。j 为无前导0的天数</td>

</tr>

<tr>

<td>w</td>

<td>星期中的第几天，以数字表示，0表示星期天</td>

</tr>

<tr>

<td>z</td>

<td>年份中的第几天，范围0-366</td>

</tr>

<tr>

<td>W</td>

<td>年份中的第几周，如第32周</td>

</tr>

<tr>

<td>H</td>

<td>24小时格式，有前导0，h为12小时格式</td>

</tr>

<tr>

<td>G</td>

<td>24小时格式，无前导0，g为对应12小时格式</td>

</tr>

<tr>

<td>i</td>

<td>分钟格式，有前导0</td>

</tr>

<tr>

<td>s</td>

<td>秒格式，有前导0</td>

</tr>

<tr>

<td>A</td>

<td>大写上下午，如AM，a为小写</td>

</tr>

</table>

<p>

可选参数 timestamp 表示时间戳，默认为 time() ，即当前时间戳。

</p>

<p>

我们可以通过 date() 函数提供的丰富格式化来显示需要的时间日期，如下面的例子：

</p>

<pre>

date(&quot;Y-m-d&quot;,time());		//显示格式如 2008-12-01

date(&quot;Y.m.d&quot;,time());		//显示格式如 2008.12.01

date(&quot;M d Y&quot;,time());		//显示格式如 Dec 01 2008

date(&quot;Y-m-d H:i&quot;,time());	//显示格式如 2008-12-01 12:01

</pre>

<h3>提示</h3>

<p>

如果您输出的时间和实际时间差8个小时（假设您采用的北京时区）的话，请检查php.ini文件，做如下设置：

</p>

