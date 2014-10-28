---
layout: post
title: "Python urlencode 编码和url拼接"
categories: python
tags: [python, urlencode]
date: 2014-10-28 23:44:56
---

urlencode 调用方法

urlencode的参数必须是Dictionary

{% highlight bash %}
import urllib
d = {'name1':'www.pythontab.com','name2':'bbs.pythontab.com'}
print urllib.urlencode(d)

输出：

name2=bbs.pythontab.com&name1=www.pythontab.com
{% endhighlight %}

相当于拼接两个url参数，这个用法类似于PHP中的http_build_query(),这里就不多数PHP中怎么用了，有兴趣的自己去查一下。

urlencode 编码
函数urlencode不会改变传入参数的原始编码，也就是说需要在调用之前将post或get参数的编码调整好。

问题：现在模拟请求Google和baidu，由于baidu使用的是gb2312编码,google使用的是utf8编码，两个站点提交到URL中的中文参数的urlencode值是不一样，下面以”PythonTab中文网”为例:

{% highlight bash %}
# coding: UTF-8
str = u'PythonTab中文网'
str = str.encode('gb2312')
d = {'name':str}
q = urllib.urlencode(d)
print q
结果：

name=PythonTab%D6%D0%CE%C4%CD%F8
{% endhighlight %}
注意：urlencode的参数必须是Dictionary

其他用法

django中urlencode类似，方法如下：

{% highlight bash %}
from django.utils.http import urlquote
a = urlquote('PythonTab中文网')
print a
{% endhighlight %}
得到汉字的GBK编码

urllib 转换字符串

其实可以用urllib的quote函数对URL中的中文进行转换，将中文转换成GBK的编码，得到的编码是符合URI标准的URL。

{% highlight bash %}
>>> import urllib
>>> a = "PythonTab中文网"
>>> a
'PythonTab\xe4\xb8\xad\xe6\x96\x87\xe7\xbd\x91'
>>> urllib.quote(a)
'PythonTab%E4%B8%AD%E6%96%87%E7%BD%91'
>>>
{% endhighlight %}

