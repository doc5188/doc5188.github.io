---
layout: post
title: "makefile中使用echo -e引发的思考（涉及dash和bash）"
categories: linux
tags: [makefile, bash, dash]
date: 2014-10-11 15:07:59
---

背景

有次我在写makfile时，用echo -e要显示带颜色的文字，命令如下：

<pre>
echo -e "Full Version is:\033[31m\033[1m v1.0 \033[0m";
</pre>

该命令在控制台中单独执行都显示正常，效果如下：

Full Version is: <span style="color: rgb(255, 0, 0);">v1.0</span>
<span style="color: rgb(255, 0, 0);">v1.0</span>

可以放在makefile中一运行， 结果把-e也显示出来：

-e Full Version is: v1.0

原因

该问题折腾我许久，百思不解，寻谷歌，问度娘，终于明白其中缘由。这是由于不同的shell（一个是bash，一个是dash）造成的两种不同的结果，即在bash下正常，在dash下就多显示了一个-e。

从Ubuntu 6.10开始，默认使用的shell是dash，而不是bash，原因是dash更快、更高效，使用dash可以加快启动速度。

我们可以做如下实验来验证下，先启用bash运行下指令，在启用dash试试：

{% highlight bash %}
#
# /bin/bash

# echo -e "Full Version is:\033[31m\033[1m v1.0 \033[0m";

Full Version is: v1.0

# exit

exit

#

# /bin/dash

# echo -e "Full Version is:\033[31m\033[1m v1.0 \033[0m";

-e Full Version is: v1.0

# exit

#

{% endhighlight %}
makefile用的是哪个shell

makefile用的shell默认是/bin/sh。但/bin/sh紧紧是个链接文件，到底用的是什么shell程序可以通过ls查看：

{% highlight bash %}
# ls -ls /bin/sh

0 lrwxrwxrwx 1 root root 4  6月 20 2012 /bin/sh -> dash
{% endhighlight %}

而系统默认的shell可以通过系统环境变量SHELL查看，当前shell可以通$0查看：

{% highlight bash %}
# echo $SHELL

/bin/bash

# echo $0

-bash
{% endhighlight %}

至此，在我的环境下，之所以会出现前面所述的问题，就是这个原因了：在makefile中用的是/bin/dash程序，而在控制台中用的是/bin/bash。

 

那makefile能不能显示的指定哪个shell程序来运行命令呢？答案肯定的。makefile本身有个环境变量也叫SHELL（跟系统环境变量SHELL同名，但不一样），我们可以在makefile中明确的给他赋值，以指明用哪个shell程序来解析命令。如SHELL = /bin/bash。

 

我在makefile最前面加上SHELL = /bin/bash，问题就解决了。
