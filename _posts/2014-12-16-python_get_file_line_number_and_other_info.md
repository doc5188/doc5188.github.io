---
layout: post
title: "python获取当前位置所在的行号和函数名"
categories: python
tags: [python]
date: 2014-12-16 14:44:40
---


最近给函数打log时，想指出加入Log的地方，包括时间、文件名、函数名、行号，这样以后找起来会比较容易。通过设这logging的fomatter可以实现，但每次都做太费劲了，于是找了个得到这些信息的方法，也是使用了logging里面的做法，通过异常得到执行信息。

<pre>
import sys
from datetime import *

def get_head_info():
	try:
		raise Exception
	except:
		f = sys.exc_info()[2].tb_frame.f_back
		return '%s, %s, %s, %s, ' % (str(datetime.now()), f.f_code.co_filename, f.f_code.co_name, str(f.f_lineno))


print get_head_info()


if __name__ == '__main__':
		print get_head_info()
</pre>

