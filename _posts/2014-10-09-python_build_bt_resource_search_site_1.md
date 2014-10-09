---
layout: post
title: "Python搭建BT资源搜索站（一）"
categories: python
tags: [python, BT资源搜索站]
date: 2014-10-09 17:50:59
---

任何一门编程语言初学者最难的是不知道如何下手，各种电子书实体书搞到一堆一堆，书中都是从语言的历史、基本语法开始谈起。按照书中的例子都一个一个去实践过了。但做了几百个for循环，几百个print 'hello world'，先不说学了后边忘记前边，准备下手做一个项目时候才发现怎么将几百遍for和print组成一个按照自己想法来实现的项目完全没有任何思路……

我对于任何编程语言的学习都倾向于做一个实际的小项目作为入门课程。我一直觉着书和手册是会查就可以了，没必要通读一整本书或者翻遍全部手册。

* 安装必备软件
<pre>
    python2.7.*，本人使用的32位Python2.7系列，一个是win7当时安装的32位，另外2.7系列第三方插件和教程都多。

    setuptools-0.6c11.win32-py2.7.exe，配合python的第三方插件

    requests，从官方github下载的版本（有一阵子了，下载最新版本就可以了）
</pre>

Python安装一路下一步即可，安装完成后将安装目录配置到环境变量里（具体操作自己问Google或者百度），这样就可以在任何目录通过执行python xxxx.py来运行写好的python脚本了。

setuptools按照提示同样安装好。

requests解压开后可以看到目录中有一个setup.py文件，win+r调出运行，输入cmd，然后就能打开『命令提示符』，也有人喜欢叫它DOS的黑窗口。cd到解压开的requests目录，例如我例子中的目录就是『e:\python\02git\requests\』

最终如图：

<img src="/upload/images/8e6a3aabec2edfdd9d26dc78584141ad_600.jpg" />

在此目录下输入python setup.py install回车运行此命令安装requests插件，在出现一堆提示之后应该会出现类似如下图的成功提示：

<img src="/upload/images/716d8e1b5a84c54d011210165954756e_600.jpg" />

* 开始写一个简单的『爬虫』程序来收集一些BT资源

1. 收集的资源位于国外的http://torrage.com/这个BT文件托管站。

2.  『爬虫』仅仅有简单的内容抓取和文件下载功能，不会像类似Google或者百度这样搜索引擎的蜘蛛那么智能，正确的说法这个应该就是个简单的采集器。

3. 新建一个目录，比如我建的目录名字为bt-search，完整路径为e:\python\01hg\bt-search

4. 在这个目录中新建一个文件torrage.py（可以新建一个txt文件，然后修改成.py后缀）

5. 编辑torrage.py的内容为：或者直接下载我编辑好的文件。

{% highlight bash %}
# -*- coding:utf-8 -*-
import requests #引入requests第三方库支持
#定义一个函数，下载torrage.com上的文件
def download():
    _url = 'http://torrage.com/sync/20130820.txt' #要下载的文件
    _content = requests.get(_url, timeout=3).content #通过requests抓取到要下载的文件的具体内容
    open('20130820.txt', 'wb').write(_content) #保存到e:\python\01hg\bt-search\这个目录下（需提前建好这个目录）

if __name__ == "__main__":
    download() #执行download函数
{% endhighlight %}

6. 同样在『命令提示符』中cd到e:\python\01hg\bt-search目录，执行python torrage.py，即可看到在此目录生成了一个20130820.txt文件，内容是好多行的字符串。

7. 这样一个简单的文件下载『爬虫』就完成了。

<pre>
原文:http://www.au92.com/archives/P-y-t-h-o-n-da-jian-B-T-zi-yuan-sou-suo-zhan-yi.html
</pre>
