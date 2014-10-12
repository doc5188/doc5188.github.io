---
layout: post
title: "解决UnicodeDecodeError: ‘ascii’ codec can’t decode byte 0xe5 in position 108: ordinal not in range(128"
categories: python
tags: [python]
date: 2014-10-12 21:50:19
---

今天做网页到了测试和数据库交互的地方，其中HTML和数据库都是设置成utf-8格式编码，插入到数据库中是正确的，但是当读取出来的时候就会出错，原因就是python的str默认是ascii编码，和unicode编码冲突，就会报这个标题错误。那么该怎样解决呢？

通过搜集网上的资料，自己多次尝试，问题算是解决了，在代码中加上如下几句即可。

<pre>
import sys
reload(sys)
sys.setdefaultencoding('utf8')

</pre>

<pre>
http://docs.python.org/howto/unicode.html这个是python的unicode编码API文档，英文好的同学可以看一下，加深理解。

参考资料：http://groups.google.com/group/python-cn/browse_thread/thread/f48ef745452740f6?pli=1
</pre>

------------------------------------------------------------------------------------------------------------------------
混淆了 python2 里边的 str 和 unicode 数据类型。

0.

你需要的是让编码用实际编码而不是 ascii

1.

对需要 str->unicode 的代码，可以在前边写上

<pre>
import sys

reload(sys)

sys.setdefaultencoding(‘utf8′)
</pre>

把 str 编码由 ascii 改为 utf8 (或 gb18030)

2.

python3 区分了 unicode str 和 byte arrary，并且默认编码不再是 ascii
