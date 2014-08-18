---
layout: post
title: "vim 一键添加注释 自动添加文件头注释"
categories: linux
tags: [vim, linux, vimplugin]
date: 2014-08-18 12:27:08
---

估计大家也都和我一样用过不少的编辑器，什么notepad2，emeditor，editplus，ultraedit，vs2005，sourceinsight，slickedit，emacs，vim(gvim)，别看多，我其实还是比许多编辑器疯狂玩家（注意，真的是玩家）收敛多了，当然最后还是本分的从了vim(gvim)，呵呵，因为Vim实在能带给我其他编辑器所没有的高效。

很多编辑器都支持在源代码中自动添加作者信息的功能，据我所致sourceinsight就支持，虽然我们的Vim(gvim)默认没有这个功能，但是只需要几行代码自己配置一下，我们一样可以让Vim(gvim)支持自动添加作者信息！

还是照例，先贴个图给大家解解馋：

估计大家也都和我一样用过不少的编辑器，什么notepad2，emeditor，editplus，ultraedit，vs2005，sourceinsight，slickedit，emacs，vim(gvim)，别看多，我其实还是比许多编辑器疯狂玩家（注意，真的是玩家）收敛多了，当然最后还是本分的从了vim(gvim)，呵呵，因为Vim实在能带给我其他编辑器所没有的高效。

很多编辑器都支持在源代码中自动添加作者信息的功能，据我所致sourceinsight就支持，虽然我们的Vim(gvim)默认没有这个功能，但是只需要几行代码自己配置一下，我们一样可以让Vim(gvim)支持自动添加作者信息！

还是照例，先贴个图给大家解解馋：
<img src="/upload/images/031628558757581.png" >
好啦，现在贴出代码如下：
{% highlight bash %}
"进行版权声明的设置
"添加或更新头
map <F4> :call TitleDet()<cr>'s
function AddTitle()
    call append(0,"/*=============================================================================")
    call append(1,"#")
    call append(2,"# Author: dantezhu - dantezhu@vip.qq.com")
    call append(3,"#")
    call append(4,"# QQ : 327775604")
    call append(5,"#")
    call append(6,"# Last modified: ".strftime("%Y-%m-%d %H:%M"))
    call append(7,"#")
    call append(8,"# Filename: ".expand("%:t"))
    call append(9,"#")
    call append(10,"# Description: ")
    call append(11,"#")
    call append(12,"=============================================================================*/")
    echohl WarningMsg | echo "Successful in adding the copyright." | echohl None
endf
"更新最近修改时间和文件名
function UpdateTitle()
    normal m'
    execute '/# *Last modified:/s@:.*$@\=strftime(":\t%Y-%m-%d %H:%M")@'
    normal ''
    normal mk
    execute '/# *Filename:/s@:.*$@\=":\t\t".expand("%:t")@'
    execute "noh"
    normal 'k
    echohl WarningMsg | echo "Successful in updating the copy right." | echohl None
endfunction
"判断前10行代码里面，是否有Last modified这个单词，
"如果没有的话，代表没有添加过作者信息，需要新添加；
"如果有的话，那么只需要更新即可
function TitleDet()
    let n=1
    "默认为添加
    while n < 10
        let line = getline(n)
        if line =~ '^\#\s*\S*Last\smodified:\S*.*$'
            call UpdateTitle()
            return
        endif
        let n = n + 1
    endwhile
    call AddTitle()
endfunction

{% endhighlight %}

这段代码在linux和windows下（vim/gvim）均可运行正常。
不知道大家看懂了没有，实际上在一个C/C++/C#/JAVA文件中，只需要按下F4，那么信息就自动给你添加到文件开头啦；如果已经存在版权信息，那么vim会帮你自动更新到最新状态。
另外还要帮大家提到一个小细节，即

<pre>
normal m'
normal ''
</pre>

这两行，他们实际上是调用了vim(gvim)内置的标记位置的方法，在执行完相应操作之后，又跳回到原来的位置。所以当用F4添加/更新作者信息的时候，不用担心光标的位置会被移动啦~~

好啦，在自己的Vim里面试一下吧，是不是比原来方便了很多啊，有用的话要记得请我吃饭啊~~哈哈

版权所有，转载请注明出处。http://www.vimer.cn
