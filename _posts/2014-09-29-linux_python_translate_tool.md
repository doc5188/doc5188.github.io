---
layout: post
title: "用Python写个翻译工具"
categories: python
tags: [linux, python]
date: 2014-09-29 17:55:32
---

2010-11-22 10:20 by CleverDeng, 2690 阅读, 11 评论, 收藏, 编辑

在英语词典方面，Linux环境下的软件远不及Win环境下，由于工作一般都在Linux环境下，并且希望在堆码的时候不用离开vim编辑器，于是花了一点时间写了个翻译的小工具，主要方便我在Linux环境下遇到不认识的英语单词时充当翻译小助手。这个小工具使用Python语言编写完成，其中使用到这些类库（urllib,BeautifulSoup），前者主要负责网络通讯方面，后者负责HTML的解析。这也是Python语言生态圈的强大之处，写个这样的小工具，毫不费力。

在线翻译的原理：首先根据用户输入的单词提交给<a href="http://dict.baidu.com">百度词典</a>，其次读取百度词典返回的数据并解析，最后将处理过的数据显示给用户。以下是该工具的具体代码（Translate.py）：

 
{% highlight python %}
import urllib
import codecs
from BeautifulSoup import BeautifulSoup
from sys import argv
import re,time

class Translate:
def Start(self):
self._get_html_sourse()
self._get_content("enc")
self._remove_tag()
self.print_result()

def _get_html_sourse(self):
word=argv[1] if len(argv)>1 else ''
url="http://dict.baidu.com/s?wd=%s&tn=dict" % word
self.htmlsourse=unicode(urllib.urlopen(url).read(),"gb2312","ignore").encode("utf-8","ignore")

def _get_content(self,div_id):
soup=BeautifulSoup("".join(self.htmlsourse))
self.data=str(soup.find("div",{"id":div_id}))

def _remove_tag(self):
soup=BeautifulSoup(self.data)
self.outtext=''.join([element for element in soup.recursiveChildGenerator() if isinstance(element,unicode)])

def print_result(self):
for item in range(1,10):
self.outtext=self.outtext.replace(str(item),"\n%s" % str(item))
self.outtext=self.outtext.replace(" ","\n")
print self.outtext

if __name__=="__main__":
Translate().Start()
{% endhighlight %}

 

如果您的运行环境安装了BeautifulSoup类库，那么执行类似这样的命令:Python Translate.py computer，您将会看到下面这样的结果：

后记，目前这个小工具在输出排版方面还不太满意。
