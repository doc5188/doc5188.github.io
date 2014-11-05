---
layout: post
title: "第十一天：centos6.5的&nbsp;shell基础学习"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:19
---

<p>1. ~ 就是 /home目录的缩写形式：</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> cd ~
就是返回当前的用户目录下，</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> cp
1.txt&nbsp;<wbr>
/home/fuwei/mytools&nbsp;<wbr>&nbsp;<wbr>
这样的命令和&nbsp;<wbr> cp 1.txt ~/mytools 是一样的作用。</P>
<p>2.commnad1; command2 执行完命令1，然后再执行命令2，不管命令1是否执行成功，直接再执行命令2</P>
<p>3.command1 &amp;&amp; command2 &amp;&amp; commandn,
命令1成功，再执行2，以此类推，如果命令没成功，则停止执行</P>
<p>4.jobs 列出当前终端运行的程序</P>
<p>&nbsp;<wbr> 命令的后面加上
&amp;&nbsp;<wbr>&nbsp;<wbr> 放到后台执行。</P>
<p>&nbsp;<wbr>ctrl +z 挂起当前的程序</P>
<p>&nbsp;<wbr>bg&nbsp;<wbr>&nbsp;<wbr>
将挂起的程序放到后台去执行。</P>
<p>5. command1&nbsp;<wbr> &amp;&nbsp;<wbr> &gt;
/dev/null&nbsp;<wbr> &amp;&nbsp;<wbr>
将程序放到后台执行，将结果输出到/dev/null 送到这里的信息都消失了。</P>
<p>6. less $(locate 1.txt)&nbsp;<wbr> $()命令</P>
<p>7.重定向 | 管道命令</P>
<p>&nbsp;<wbr> ls -l |
less&nbsp;<wbr>&nbsp;<wbr> 第一部分是
列出目录&nbsp;<wbr> ，紧接着送到less 来阅读。</P>
<p>rpm -qa | grep&nbsp;<wbr> vsftpd | less
列出所有的安装包&nbsp;<wbr> 过滤出 vsftpd这个包 送到 less来看下。</P>
<p>8.定向到文件：</P>
<p>&nbsp;<wbr>&nbsp;<wbr> command &gt; filename</P>
<p>ls&nbsp;<wbr> &gt;
dirname&nbsp;<wbr>&nbsp;<wbr> 将当前显示的目录名 输出到
dirname文件中。</P>
<p>9. command&nbsp;<wbr> &lt; filename<br />
&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr>
将文件filenname 的内容送到command中，</P>
<p>&nbsp;<wbr> sort &lt; filename &gt;
sortfilename&nbsp;<wbr>
将文件filename的内容发给sort，通过sort排序后，将排序后的内容发送给sortfilename文件，结果就完成了排序的功能。</P>
<p>10. &gt;&gt;&nbsp;<wbr>&nbsp;<wbr>
双&gt;&gt;&nbsp;<wbr> 表示追加文件内容的意思，</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> echo
"good" &gt;&gt; filenanem&nbsp;<wbr> 将 字符串 good 追加到
filenanme文件的后面。</P>
<p>11.&nbsp;<wbr> .bash的定制:</P>
<p>&nbsp;<wbr>&nbsp;<wbr>&nbsp;<wbr> set
列出当前的环境变量</P>
<p>别名alise&nbsp;<wbr> ~/.bashrec 文件&nbsp;<wbr>
.bashrc文件，命令可以用别名，精简。</P>
<p>12.补齐命令 ，tab 打出一个字母，会自动显示出要选择的目录或者文件名.</P>
<p>先用这几个，有需要的再补充我,.</P>
