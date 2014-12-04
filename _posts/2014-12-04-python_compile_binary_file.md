---
layout: post
title: "python如何编译生成二进制文件？"
categories: python
tags: [python]
date: 2014-12-04 12:46:08
---

<pre>
python -O -m py_compile file.py  

-O 优化成字节码 
-m 表示把后面的模块当成脚本运行 
-OO 表示优化的同时删除文档字符串 
</pre>

也可以写一个脚本来实现： 

<pre>
import py_compile  
  
py_compile.compile("file_path")

</pre>
