---
layout: post
title: "c++ 引用参数设默认值"
categories: C/C++
tags: [cpp, c]
date: 2014-09-12 12:14:21
---

<pre>
#include <stdio.h>
int bb = 10;
void fun(int &a=bb);

int main(void)
{
    printf("Hello World!");
    fun();

    return 0;
}

void fun(int &a)
{
    printf("%d\n", a);

    return;
}
</pre>
