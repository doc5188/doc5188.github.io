---
layout: post
title: "cmake 学习笔记(三)"
categories: c/c++
tags: [cmake, 系列教程]
date: 2014-11-05 12:58:20
---

<p><span style="font-family:Arial,'Lucida Grande',sans-serif; font-size:16px; color:#000000; border-collapse:separate; font-style:normal; font-variant:normal; font-weight:normal; letter-spacing:normal; line-height:normal; orphans:2; text-indent:0px; text-transform:none; white-space:normal; widows:2; word-spacing:0px"></span></p>
<p class="line862">接前面的<span>&nbsp;</span><a href="http://blog.csdn.net/dbzhang800/archive/2011/04/10/6314073.aspx" style="color:#047307; border:0px initial initial">Cmake学习笔记(一)</a><span>&nbsp;</span>与<span>&nbsp;</span><a href="http://blog.csdn.net/dbzhang800/archive/2011/04/17/6329068.aspx" style="color:#047307; border:0px initial initial">Cmake学习笔记(二)</a><span>&nbsp;</span>继续学习
 cmake 的使用。</p>
<p class="line874">学习一下cmake的 finder。</p>
<h3 id="finder.2BZi95XppsThyJf.2F8f-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
finder是神马东西？</h3>
<p class="line874">当编译一个需要使用第三方库的软件时，我们需要知道：</p>
<div>
<table border="0" style="margin:0.5em 0px 0px 0.5em; border-collapse:collapse">
<tbody>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">去哪儿找头文件 .h</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line891" style="margin:0px; padding:0px"><tt>对比GCC的&nbsp;-I&nbsp;参数</tt></p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">去哪儿找库文件 (.so/.dll/.lib/.dylib/...)</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line891" style="margin:0px; padding:0px"><tt>对比GCC的&nbsp;-L&nbsp;参数</tt></p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">需要链接的库文件的名字</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line891" style="margin:0px; padding:0px"><tt>对比GCC的&nbsp;-l&nbsp;参数</tt></p>
</td>
</tr>
</tbody>
</table>



<pre>
referer:http://blog.csdn.net/dbzhang800/article/details/6329314
</pre>
