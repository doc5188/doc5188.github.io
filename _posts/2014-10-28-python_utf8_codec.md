---
layout: post
title: "Python 使用 UTF-8 编码"
categories: python 
tags: [python, python字符编码]
date: 2014-10-28 23:54:17
---

一般我喜欢用 utf-8 编码，在 python 怎么使用呢？

1、在 python 源码文件中用 utf-8 文字。一般会报错，如下：

<pre>
File "F:\workspace\psh\src\test.py", line 2
SyntaxError: Non-ASCII character '\xe4' in file F:\workspace\psh\src\test.py on line 2, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
</pre>

test.py 的内容：

<pre>
print "你好"  
</pre>

如果要正常运行在 test.py 文件前面加编码注释，如：

{% highlight bash %}
#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
print "你好"  
{% endhighlight %}

2、python 对 url encode UTF-8 怎么做呢？

windows 的命令行参数转 utf-8 怎么做呢？

{% highlight bash %}
# -*- coding: utf-8 -*-  
import urllib  
import sys  
  
if __name__ == '__main__':  
    if len(sys.argv) > 1:  
        str = sys.argv[1]  
        str = unicode(str, 'gbk')  
    else:  
        str = "中文"  
  
    print str  
    params = {}  
    params['name'] = str.encode("UTF-8")  
  
    print urllib.urlencode(params)  
{% endhighlight %}
python 内部是用 unicode 吧。

由于 windows 的命令行输入的是 GBK 编码的，可以要先转为 unicode（第三8行）。

要转 url encode 时，先把 str 转为 utf-8。

默认的输出结果：

<pre>
中文
name=%E4%B8%AD%E6%96%87
</pre>

写 python 脚本来做写小事情方便，比如要取些 solr 的数据，solr 的 url 编码是 utf-8 的。

<pre>
参考：http://evanjones.ca/python-utf8.html
</pre>
