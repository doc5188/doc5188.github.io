---
layout: post
title: 编程工具系列之一------使用GDB的堆栈跟踪功能
date:   2014-08-12 15:49:11
categories: gdb
tags: [Linux, gdb]
---

      在调试程序的过程中，查看程序的函数调用堆栈是一项最基本的任务，几乎所有的图形调试器都支持这项特性。

      GDB调试器当然也支持这一特性，但是功能更加灵活和丰富。

      GDB将当前函数的栈帧编号为0，为外层函数的栈帧依次加1，这些编号将成为一些GDB命令的参数，以指明将要操作的是哪一个函数的栈帧。

      GDB还支持使用Address作为栈帧的标识符，可在栈帧编号被破坏的情况下使用。

      1.在栈帧之间切换

          GDB中有很多针对调用堆栈的命令，都需要一个目标栈帧，例如打印局部变量值的命令。

          frame args 将当前栈帧设置为args（编号或Address）指定的栈帧，并打印该栈帧的简要信息。

          select-frame args 与frame args相同，但是不打印栈帧信息。

          up n 向上回退n个栈帧（更外层），n默认为1. 

          down n 向下前进n个栈帧（更内层），n默认为1.

          up-silently n 与up n相同，但是不打印信息。

          down-silently n 与down n相同，但是不打印信息。

      2.打印栈帧信息（不移动栈帧）

          frame 打印当前栈帧的简要信息。

          info frame 打印当前栈帧的详细信息。

          info frame args 打印指定栈帧的详细信息。

          info args 打印函数参数信息。

          info locals 打印当前可访问的局部变量的信息。

      3.打印调用堆栈

          backtrace 打印全部栈帧的简要信息，按Ctrl-c可终止打印。

          backtrace n 打印最内层的n个栈帧的简要信息。

          backtrace -n 打印最外层的n个栈帧的简要信息。

          backtrace full 打印全部栈帧的详细信息。

          backtrace full n 打印最内层的n个栈帧的详细信息。

          backtrace full -n 打印最外层的n个栈帧的详细信息。

      4.一些配置项

          set backtrace past-main on 对调用堆栈的打印可越过main函数。

          set backtrace past-main off 对调用堆栈的打印止步于main函数。
