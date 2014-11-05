---
layout: post
title: "cmake学习笔记(五)"
categories: c/c++
tags: [cmake, 系列教程]
date: 2014-11-05 12:58:22
---

<p><span style="font-family:Arial,'Lucida Grande',sans-serif; font-size:16px; color:#000000; border-collapse:separate; font-style:normal; font-variant:normal; font-weight:normal; letter-spacing:normal; line-height:normal; orphans:2; text-indent:0px; text-transform:none; white-space:normal; widows:2; word-spacing:0px"></span></p>
<p class="line862">在<a href="http://blog.csdn.net/dbzhang800/archive/2011/04/17/6329314.aspx">cmake 学习笔记(三)</a><span>&nbsp;</span>中简单学习了 find_package 的 model 模式，在<a href="http://blog.csdn.net/dbzhang800/archive/2011/04/21/6340102.aspx">cmake 学习笔记(四)</a>中了解一个CMakeCache相关的东西。但靠这些知识还是不能看懂PySide使用CMakeLists文件，接下来继续学习find_package的
 config 模式及package configure文件相关知识</p>
<h2 id="find_package_.2BdoQ_config_.2BaiFfDw-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
find_package 的 config 模式</h2>
<p class="line874">当CMakeLists.txt中使用find_package命令时，首先启用的是 module 模式：</p>
<ul>
<li>
<p class="line862" style="margin:0.25em 0px">按照 CMAKE_MODULE_PATH 路径和cmake的安装路径去搜索finder文件 Find&lt;package&gt;.cmake</p>
</li></ul>
<p class="line874">如果finder未找到，则开始 config 模式：</p>
<ul>
<li>
<p class="line862" style="margin:0.25em 0px">将在下列路径下查找 配置 文件 &lt;name&gt;Config.cmake 或 &lt;lower-case-name&gt;-config.cmake</p>
</li></ul>
<div>
<table border="0" style="margin:0.5em 0px 0px 0.5em; border-collapse:collapse">
<tbody>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(W)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/(cmake|CMake)/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(W)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/&lt;name&gt;*/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(W)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/&lt;name&gt;*/(cmake|CMake)/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(W)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/(share|lib)/cmake/&lt;name&gt;*/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(U)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/(share|lib)/&lt;name&gt;*/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(U)</p>
</td>
</tr>
<tr>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">&lt;prefix&gt;/(share|lib)/&lt;name&gt;*/(cmake|CMake)/</p>
</td>
<td style="padding:0.25em 0.5em; border:1px solid #047307">
<p class="line862" style="margin:0px; padding:0px">(U)</p>
</td>
</tr>
</tbody>
</table>



<pre>
referer:http://blog.csdn.net/dbzhang800/article/details/6341029
</pre>
