---
layout: post
title: "Python模块学习 filecmp 文件比较"
categories: python
tags: [python, filecmp]
date: 2014-11-13 16:20:06
---


filecmp模块用于比较文件及文件夹的内容，它是一个轻量级的工具，使用非常简单。python标准库还提供了difflib模块用于比较文件的内容。关于difflib模块，且听下回分解

filecmp定义了两个函数，用于方便地比较文件与文件夹：

filecmp.cmp(f1, f2[, shallow])：

比较两个文件的内容是否匹配。参数f1, f2指定要比较的文件的路径。可选参数shallow指定比较文件时是否需要考虑文件本身的属性（通过os.stat函数可以获得文件属性）。如果文件内容匹配，函数返回True，否则返回False。

filecmp.cmpfiles(dir1, dir2, common[, shallow])：

比较两个文件夹内指定文件是否相等。参数dir1, dir2指定要比较的文件夹，参数common指定要比较的文件名列表。函数返回包含3个list元素的元组，分别表示匹配、不匹配以及错误的文件列表。错误的文件指的是不存在的文件，或文件被琐定不可读，或没权限读文件，或者由于其他原因访问不了该文件。

filecmp模块中定义了一个dircmp类，用于比较文件夹，通过该类比较两个文件夹，可以获取一些详细的比较结果（如只在A文件夹存在的文件列表），并支持子文件夹的递归比较。

dircmp提供了三个方法用于报告比较的结果：
<pre>
•report()：只比较指定文件夹中的内容（文件与文件夹）
•report_partial_closure()：比较文件夹及第一级子文件夹的内容
•report_full_closure()：递归比较所有的文件夹的内容
</pre>
dircmp还提供了下面这些属性用于获取比较的详细结果：

<pre>
•left_list：左边文件夹中的文件与文件夹列表；
•right_list：右边文件夹中的文件与文件夹列表；
•common：两边文件夹中都存在的文件或文件夹；
•left_only：只在左边文件夹中存在的文件或文件夹；
•right_only：只在右边文件夹中存在的文件或文件夹；
•common_dirs：两边文件夹都存在的子文件夹；
•common_files：两边文件夹都存在的子文件；
•common_funny：两边文件夹都存在的子文件夹；
•same_files：匹配的文件；
•diff_files：不匹配的文件；
•funny_files：两边文件夹中都存在，但无法比较的文件；
•subdirs：我没看明白这个属性的意思，python手册中的解释如下：A dictionary mapping names in common_dirs to dircmp objects
</pre>

简单就是美！我只要文件比较的结果，不想去关心文件是如何是比较的，hey，就用python吧~~ 
