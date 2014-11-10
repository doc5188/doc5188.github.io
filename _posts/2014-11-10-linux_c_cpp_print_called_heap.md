---
layout: post
title: "在程序中打印调用堆栈"
categories: c/c++ 
tags: [linux c/c++, 调用堆栈]
date: 2014-11-10 22:27:34
---

一直以来都没有花太多精力放在学习调试方面，主要还是平时调试的机会相对较少，一般情况下，用strace、gdb、以及通过打印log基本上就能解决问题了，还有就是，与其花精力去提高调试技能，还不如在设计、防御式编程和单元测试等能力去提高，以及提高自已编码的质量，减少BUG的出现或者缩少BUG的范围。

但是，有时使用调试工具并不是为了查找BUG，在阅读和分析源代码时也非常有用，下面的代码演示如何在自已的程序中打印调用堆栈，有时你想知道某一个函数在某一时刻被哪一个函数调用了，只要在这个函数中打印一下调用堆栈即可，在一些不方便使用调试工具的场合（例如程序在开发板上运行时）还是比较有用的。

下面的示例代码我从网络上找来的，我去掉了注释，并在上面加上了我自已的注释，可以通过看注释来了解是怎么实现的，注意在用gcc编译代码时，要加上选项-rdynamic和-g：

<pre>
#include <stdio.h>
#include <execinfo.h>
void print_trace(void);
void funcC()
{
    /* 打印调用堆栈，看看谁调用了本函数 */
    print_trace();
}
void funcB()
{
    funcC();
}
void funcA()
{
    funcB();
}
int main (void)
{
    funcA();
    return 0;
}
void print_trace(void)
{
    int i;
    const int MAX_CALLSTACK_DEPTH = 32;    /* 需要打印堆栈的最大深度 */
    void *traceback[MAX_CALLSTACK_DEPTH];  /* 用来存储调用堆栈中的地址 */
    /* 利用 addr2line 命令可以打印出一个函数地址所在的源代码位置 
     * 调用格式为： addr2line -f -e /tmp/a.out 0x400618
     * 使用前，源代码编译时要加上 -rdynamic -g 选项
     */
    char cmd[512] = "addr2line -f -e ";
    char *prog = cmd + strlen(cmd);
    /* 得到当前可执行程序的路径和文件名 */
    int r = readlink("/proc/self/exe",prog,sizeof(cmd)-(prog-cmd)-1);
    /* popen会fork出一个子进程来调用/bin/sh, 并执行cmd字符串中的命令，
     * 同时，会创建一个管道，由于参数是'w', 管道将与标准输入相连接，
     * 并返回一个FILE的指针fp指向所创建的管道，以后只要用fp往管理里写任何内容，
     * 内容都会被送往到标准输入，
     * 在下面的代码中，会将调用堆栈中的函数地址写入管道中，
     * addr2line程序会从标准输入中得到该函数地址，然后根据地址打印出源代码位置和函数名。
     */
    FILE *fp = popen(cmd, "w");
    /* 得到当前调用堆栈中的所有函数地址，放到traceback数组中 */
    int depth = backtrace(traceback, MAX_CALLSTACK_DEPTH);
    for (i = 0; i < depth; i++)
    {
        /* 得到调用堆栈中的函数的地址，然后将地址发送给 addr2line */
        fprintf(fp, "%p/n", traceback[i]);
        /* addr2line 命令在收到地址后，会将函数地址所在的源代码位置打印到标准输出 */
    }
    fclose(fp);
}

</pre>




<pre>
referer: http://blog.csdn.net/kwiner/article/details/4066590
</pre>
