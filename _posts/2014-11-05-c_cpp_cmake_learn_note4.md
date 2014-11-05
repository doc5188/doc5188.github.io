---
layout: post
title: "cmake 学习笔记(四)"
categories: c/c++
tags: [cmake, 系列教程]
date: 2014-11-05 12:58:21
---

<p><span style="font-family:Arial,'Lucida Grande',sans-serif; font-size:16px; color:#000000; border-collapse:separate; font-style:normal; font-variant:normal; font-weight:normal; letter-spacing:normal; line-height:normal; orphans:2; text-indent:0px; text-transform:none; white-space:normal; widows:2; word-spacing:0px"></span></p>
<p class="line874">接前面的一二三，学习一下 CMakeCache.txt 相关的东西。</p>
<h2 id="CMakeCache.txt" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
CMakeCache.txt</h2>
<p class="line874">可以将其想象成一个配置文件(在Unix环境下，我们可以认为它等价于传递给configure的参数)。</p>
<ul>
<li>CMakeLists.txt 中通过 set(... CACHE ...) 设置的变量</li><li>CMakeLists.txt 中的 option() 提供的选项</li><li>CMakeLists.txt 中find_package() 等find命令引入变量</li><li>
<p class="line862" style="margin:0.25em 0px">命令行<span>&nbsp;</span><tt>cmake&nbsp;.&nbsp;-D&nbsp;&lt;var&gt;:&lt;type&gt;=&lt;value&gt;</tt><span>&nbsp;</span>定义变量</p>
</li></ul>
<p class="line874">cmake 第一次运行时将生成 CMakeCache.txt 文件，我们可以通过ccmake或cmake-gui或make edit_cache对其进行编辑。</p>
<p class="line862">对应于命令行 -D 定义变量，-U 用来删除变量（支持globbing_expr），比如<span>&nbsp;</span><tt>cmake&nbsp;-U/*QT/*</tt><span>&nbsp;</span>将删除所有名字中带有QT的cache项。</p>
<h2 id="A.2BU9iRz04O-Cache" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
变量与Cache</h2>
<p class="line874">cmake 的变量系统远比第一&#30524;看上去复杂:</p>
<ul>
<li>有些变量被cache，有些则不被cache</li><li>被cache的变量
<ul>
<li>有的不能通过ccmake等进行编辑(internal)</li><li>有的(带有描述和类型)可以被编辑(external)
<ul>
<li>有的只在ccmake的 advanced 模式出现</li></ul>
</li></ul>
</li></ul>
<p class="line874">看个例子：</p>
<ul>
<li>SET(var1 13)
<ul>
<li>变量 var1 被设置成 13</li><li>如果 var1 在cache中已经存在，该命令不会overwrite cache中的&#20540;</li></ul>
</li><li>SET(var1 13 ... CACHE ...)
<ul>
<li>如果cache存在该变量，使用cache中变量</li><li>如果cache中不存在，将该&#20540;写入cache</li></ul>
</li><li>SET(var1 13 ... CACHE ... FORCE)
<ul>
<li>不论cache中是否存在，始终使用该&#20540;</li></ul>
</li></ul>
<p class="line874">要习惯用帮助</p>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">cmake --help-command SET</pre>
<h2 id="find_xxx" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
find_xxx</h2>
<p class="line874">为了避免每次运行都要进行头文件和库文件的探测，以及考虑到允许用户通过ccmake设置头文件路径和库文件的重要性，这些东西必须进行cache。</p>
<ul>
<li>find_path 和 find_library 会自动cache他们的变量，如果变量已经存在且是一个有效&#20540;（即不是 -NOTFOUND 或 undefined）,他们将什么都不做。</li><li>
<p class="line862" style="margin:0.25em 0px">另一方面，模块查找时输出的变量（&lt;name&gt;_FOUND,&lt;name&gt;_INCLUDE_DIRS,&lt;name&gt;_LIBRARIES）不应该被cache</p>
</li></ul>
<h2 id="A.2BU8KAAw-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
参考</h2>
<ul>
<li>
<p class="line891" style="margin:0.25em 0px"><a class="http" href="http://www.kdedevelopers.org/node/4385" style="color:#047307; border-width:0px">http://www.kdedevelopers.org/node/4385</a></p>
</li><li>
<p class="line891" style="margin:0.25em 0px"><a class="http" href="http://www.cmake.org/cmake/help/runningcmake.html" style="color:#047307; border-width:0px">http://www.cmake.org/cmake/help/runningcmake.html</a></p>
</li><li>
<p class="line891" style="margin:0.25em 0px"><a class="http" href="http://www.cmake.org/Wiki/CMake:How_To_Find_Libraries" style="color:#047307; border-width:0px">http://www.cmake.org/Wiki/CMake:How_To_Find_Libraries</a></p>
</li></ul>



<pre>
referer:http://blog.csdn.net/dbzhang800/article/details/6340102
</pre>
