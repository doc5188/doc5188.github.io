---
layout: post
title: vim中打开man手册
categories: linux
tags: [vim, linux]
date: 2014-10-08 16:03:57
---


软件版本：
<pre>
　　ubuntu10.04
　　Linux version 2.6.32-42-generic
　　VIM - Vi IMproved 7.2
</pre>

目录：
<pre>
　　1. 简介

　　2. 安装使用

　　3. 效果
</pre>

* 1. 简介

　　在编程的过程中，可能需要用到某个系统函数，却一时间记不住它的参数，或头文件。这时候就需要用到 man 去查阅该函数。但是退出 vim 或者 切换窗口去查阅就显得很费时了。我们需要在 vim 内部也支持调起 man 。

* 2. 安装使用

　　在 $HOME/.vimrc 文件中添加一些内容：

<pre>
" 查看方法输入:Man api_name
:source $VIMRUNTIME/ftplugin/man.vim
" 映射之后就可以少按一下 Shift 键。
cmap man Man
" 在普通模式下按下 K （大写）即可启动 man 查看光标下的函数。
nmap K :Man <cword><CR>
</pre>

* 3. 效果

　　在普通模式下输入 :Man 2 open ，如下图所示：

<img src="/upload/images/2012091310351661.png" /> 
