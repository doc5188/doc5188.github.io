---
layout: post
date: 2014-09-25 20:14:34
title: "python遍历文件夹/文件"
categories: python
tags: [python]
---

<pre>
import os
import os.path
rootdir = "d:\data"                                   # 指明被遍历的文件夹

for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
 　　　for dirname in  dirnames:                       #输出文件夹信息
　　　　  print "parent is:" + parent
　　　　  print  "dirname is" + dirname

　　　 for filename in filenames:                        #输出文件信息
　　　　  print "parent is": + parent
　　　　  print "filename is:" + filename
　　     print "the full name of the file is:" + os.path.join(parent,filename) #输出文件路径信息

                                                                         #windows下为：d:\data\query_text\EL_00154
</pre>
