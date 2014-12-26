---
layout: post
title: "python 捕捉退出事件"
categories: python
tags: [python, signal]
date: 2014-12-26 17:28:09
---

最近写了个python脚本，在服务器上运行，经常莫名其妙的退出，也不知道原因，后面查了资料得到下面两个方法去捕捉退出的发生，一个是捕捉kill信号，另一个是注册atexit函数

例子：


<pre>
import os
import sys
import time
import atexit
import signal
import traceback

def term_sig_handler(signum, frame):
    print 'catched singal: %d' % signum
    sys.exit()

@atexit.register
def atexit_fun():
    print 'i am exit, stack track:'

    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)

if __name__ == '__main__':
    # catch term signal
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    while True:
        print 'hello'
        time.sleep(3)
</pre>

输出：


<pre>
hello
hello
hello
hello
hello
hello
hello
catched singal: 15
i am exit, stack track: None

<pre>

注意：atexit_fun不能在main之后，不然不会执行

