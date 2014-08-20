---
layout: post
date: 2014-08-19 12:37:23
title: "让Shell终端下的svn diff支持颜色高亮"
categories: linux
tags: [linux, svn]
---


Mac 系统

下载：colordiff，Mountain Lion 也可以使用。

http://code.google.com/p/rudix/wiki/colordiff

在 ~/.subversion/config 內修改:
<pre>
[helpers]
diff-cmd = colordiff
</pre>

如果需要修改颜色：sudo vim /usr/local/etc/colordiffrc

Ubuntu 系统

sudo apt-get install colordiff

在 ~/.subversion/config 內修改:

<pre>
[helpers]
diff-cmd = colordiff
</pre>

如果需要修改颜色：sudo vim /etc/colordiffrc

