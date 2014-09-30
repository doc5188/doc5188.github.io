---
layout: post
title: "自定义VIM的语法高亮模式(添加自定义文件后缀)" 
categories: linux
tags: [linux, vim, filetype,vimsyntax]
date: 2014-09-30 14:23:03
---

大家都知道使用syntax on 可以打开vim的代码高亮，但这通常是根据文件的扩展名来自动匹配设置的，目前遇到一个问题，我想让*.ejs的文件使用HTML的高亮模式，要怎么办呢？

通过一番查阅VIM的使用手册，终于找到了方法，在命令模式下输入：
<pre>
:setfiletype html
</pre>
或者:

<pre>
:set filetype html
</pre>
但是这样必须要在打开文件之后开启，最好是可以自动根据文件扩展名开启，这便要修改.vimrc文件了，在.vimrc文件中添加

<pre>
au BufRead,BufNewFile *.ejs setfiletype html
</pre>

上面分别对应设置打开文件和新建文件时，遇到扩展名为ejs的文件，设置为html文件类型。

对于其它类型的文件，同样可以这样来设置，比如.less文件：

<pre>
au BufRead,BufNewFile *.less setfiletype css'

au BufRead,BufNewFile *.less setfiletype css'
</pre>

