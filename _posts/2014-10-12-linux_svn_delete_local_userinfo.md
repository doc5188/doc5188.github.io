---
layout: post
title: "svn之——linux下清除svn的用户名和密码"
categories: linux
tags: [linux, svn]
date: 2014-11-12 16:13:36
---

问题：之前用的svn账号权限不够，需要使用别的账号，所以提出需求——怎么使用新的svn账号进行操作

* 方法一：

linux下删除~/.subversion/auth即可清除之前的用户名和密码：rm -rf ~/.subversion/auth

以后再操作svn会提示你输入用户名，这时就可以使用新的了

* 方法二：

svn操作时带上--username参数，比如svn --username=smile  co  svn_path local_path

*　方法三: 

vi ~/.subversion/auth/svn.simple/a4f17ba151138ad1dd8aa9fc647fac3e

最后的名称可能不同

删除文件里，你需要清除的用户名，就行了
