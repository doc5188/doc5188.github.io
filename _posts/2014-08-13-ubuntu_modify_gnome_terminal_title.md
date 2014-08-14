---
layout: post
date: 2014-08-13 17:58:00
categories: ubuntu linux
title: "ubuntu 10.04 TLS 根据当前目录修改终端窗口的title"
---

常常有许多的终端窗口，每个终端窗口对应一个工程的编译shell。

参考帖子【http://ubuntuforums.org/showthread.php?t=448614&page=2】中最后一层楼的内容

知道如何编写一个能够改变命令行终端的窗口标题的函数。

 

由于这里定义的函数需要在别的脚本中调用到，所以需要用到export命令，参考文章【http://www.cyberciti.biz/faq/bash-shell-script-function-examples/】中的介绍。

 

最终需要修改~/.bashrc，在文件的最末尾处增加如下内容：

{% highlight bash %}

    if [ "$color_prompt" = yes ]; then  
        PS1_NOTITLE='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '  
    else  
        PS1_NOTITLE='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '  
    fi  
    unset color_prompt force_color_prompt  
    PS1=$PS1_NOTITLE  
      
    function nameTerminal {  
        PS1=$PS1_NOTITLE  
        echo -en "\033]2;$1\007"  
    }  
      
    export -f nameTerminal  

{% endhighlight %} 

 

接着编写一个脚本，能够获取到当前终端的命令行所在路径的文件夹名称，并且改变窗口的title，脚本代码如下：

{% highlight bash %}
    cur_path=`pwd`;  
    title=`echo ${cur_path##/*/}`;  
    nameTerminal $title;  
{% endhighlight %} 

 

存放在路径：/usr/bin/folder-title.sh

 

而后赋予所有用户执行该脚本的权限：

{% highlight bash %}
    $ sudo chmod o+x /usr/bin/folder-title.sh  
{% endhighlight %}

 

接着就能来到一个目录下做一下实验了：

比如当前路径为：/home/xxx/docs

 

执行 folder-title.sh

 

就能看到窗口的标题变成【docs】。

 

后记：

如果执行不成功，有可能是因为~/.bashrc中定义的函数没有生效，在重启操作系统之前，如果想先尝试一下效果，可以先执行一下命令：

 
{% highlight bash %}
    source ~/.bashrc  
{% endhighlight %}

  
