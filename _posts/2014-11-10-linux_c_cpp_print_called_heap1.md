---
layout: post
title: "在Linux中打印函数调用堆栈"
categories: c/c++
tags: [c/c++, 函数调用堆栈]
date: 2014-11-10 22:30:11
---

在编写Java程序时，Exception类的printStacktrace()可以打印异常堆栈，这个小工具极大的提高了调试效率；虽然不是一个好习惯，却很实用。习惯了Java编程，很希望 C/C++里也有这样的小工具可以帮助调试程序.

经过几天查找，发现其实每个系统都提供了打印调用堆栈的函数；这些函数是系统相关，这里仅以Linux下的函数作说明.

Linux中共提供了三个函数用于打印调用堆栈：

<pre>
int backtrace(void **buffer, int size);
char **backtrace_symbols(void *const *buffer, int size);
void backtrace_symbols_fd(void *const *buffer, int size, int fd);
</pre>

<pre>
#include <execinfo.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
  
void myfunc3(void)
{
    int j, nptrs;
    #define SIZE 100
    void *buffer[100];
    char **strings;
  
    nptrs = backtrace(buffer, SIZE);
    printf("backtrace() returned %d addresses\n", nptrs);
  
    backtrace_symbols_fd(buffer, nptrs, STDOUT_FILENO);
}
  
void myfunc(void)
{
    myfunc3();
}
  
int main(int argc, char *argv[])
{
    myfunc();
    return 0;
}
</pre>

程序运行结果：

<pre>
[dma@bp860-10 ~]$ g++ -rdynamic t.cpp -o t  #这里的参数 -rdynamic 是必须
[dma@bp860-10 ~]$ ./t
backtrace() returned 5 addresses
./t(_Z7myfunc3v+0x1c)[0x4008c4]
./t(_Z6myfuncv+0x9)[0x4008f9]
./t(main+0x14)[0x400910]
/lib64/tls/libc.so.6(__libc_start_main+0xdb)[0x3f37c1c40b]
./t(__gxx_personality_v0+0x3a)[0x40081a]
[dma@bp860-10 ~]$
</pre>
 
虽然现在的程序可以输出函数调用的堆栈，但是函数多了一些前缀，比如：./t(_Z7myfunc3v+0x1c)；这个问题可以通过c++fileter这个工具来解决：

<pre>
[dma@bp860-10 ~]$ ./t | c++filt
./t(myfunc3()+0x1c)[0x4008c4]
./t(myfunc()+0x9)[0x4008f9]
./t(main+0x14)[0x400910]
/lib64/tls/libc.so.6(__libc_start_main+0xdb)[0x3f37c1c40b]
./t(__gxx_personality_v0+0x3a)[0x40081a]
backtrace() returned 5 addresses
</pre>
