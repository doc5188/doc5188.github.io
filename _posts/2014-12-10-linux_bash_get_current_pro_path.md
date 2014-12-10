---
layout: post
title: "bash shell 获取当前绝对路径"
categories: linux
tags: [linux, bash]
date: 2014-12-10 13:11:26
---

<pre>
#获取当前绝对路径
function xrsh_getcurpath()
{
  local _xrsh_tmp=`echo $0| grep "^/"`
  if test "${_xrsh_tmp}"; then
    dirname $0
  else
    dirname `pwd`/$0
  fi
}
 
#使用 which 命令获取给定目标的路径
#参数：1目标名称; 2 获取失败时返回路径（可选）
#例子：
#    获取 gcc 的路径，如果失败使用 /usr/bin/gcc
#    xrsh_getexepath "gcc" "/usr/bin/gcc"
function xrsh_getexepath()
{
  local _xrsh_tmp=`which $1`
  _xrsh_tmp=`echo $_xrsh_tmp| grep "/$1"`
  if test "${_xrsh_tmp}"; then
    echo $_xrsh_tmp
  else
    echo "$2"
  fi
}

</pre>


<pre>
referer:http://blog.csdn.net/xrdks/article/details/7759446
</pre>
