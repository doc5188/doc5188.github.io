---
layout: post
title: "python如何将(u'\\xb3\\xc2\\xbd\\xa8\\xc3\\xf4',) 转为字符串"
categories: python
tags: [python]
date: 2014-10-11 09:16:01
---

python中从数据库中取得的gbk编码的字符数据。

rs = cursor.fetchone()

rs 取得数据为(u'\xb3\xc2\xbd\xa8\xc3\xf4',) 如何将其转为字符串。





==========================================



<pre>
>>> s = u'\xb3\xc2\xbd\xa8\xc3\xf4'
>>> a = s.encode('unicode_escape').decode('string_escape')
>>> a
'\xb3\xc2\xbd\xa8\xc3\xf4'
>>> print a
陈建敏
>>>  




翻了下手册有个raw_unicode_escape编码：

>>> s = u'\xb3\xc2\xbd\xa8\xc3\xf4'
>>> s.encode('raw_unicode_escape')
'\xb3\xc2\xbd\xa8\xc3\xf4'
>>>  


</pre>
