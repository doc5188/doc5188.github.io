---
layout: post
title: "cmake 学习笔记(二)"
categories: c/c++
tags: [cmake, 系列教程]
date: 2014-11-05 12:58:19
---

<p><span style="font-family:Arial,'Lucida Grande',sans-serif; font-size:16px; color:#000000; border-collapse:separate; font-style:normal; font-variant:normal; font-weight:normal; letter-spacing:normal; line-height:normal; orphans:2; text-indent:0px; text-transform:none; white-space:normal; widows:2; word-spacing:0px"></span></p>
<p class="line862">在<span>&nbsp;</span><a href="http://blog.csdn.net/dbzhang800/archive/2011/04/10/6314073.aspx" style="color:#047307; border:0px initial initial">Cmake学习笔记一</a><span>&nbsp;</span>中通过一串小例子简单学习了cmake 的使用方式。</p>
<p class="line874">这次应该简单看看语法和常用的命令了。</p>
<h2 id="A.2Be4BTVXaEi.2B1s1Q-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
简单的语法</h2>
<ul>
<li>注释</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0"># 我是注释</pre>
<ul>
<li>命令语法</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">COMMAND(参数1 参数2 ...)</pre>
<ul>
<li>字符串列表</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">A;B;C # 分号分割或空&#26684;分隔的&#20540;</pre>
<ul>
<li>变量(字符串或字符串列表)</li></ul>
<div>
<table border="0" style="margin:0.5em 0px 0px 0.5em; border-collapse:collapse">
<tbody>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">set(Foo a b c)</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">设置变量 Foo</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">command(${Foo})</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">等价于 command(a b c)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">command(&quot;${Foo}&quot;)</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">等价于 command(&quot;a b c&quot;)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">command(&quot;/${Foo}&quot;)</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">转义，和 a b c无关联</p>
</td>
</tr>
</tbody>
</table>



<pre>
referer:http://blog.csdn.net/dbzhang800/article/details/6329068
</pre>
