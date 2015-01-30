---
layout: post
title: "利用gcc的__attribute__编译属性section子项构建初始化函数表"
categories: 技术文章
tags: []
date: 2015-01-30 13:38:10
---

<p> gcc的__attribute__编译属性有很多子项，用于改变作用对象的特性。这里讨论section子项的作用。 </p> 
<p> <span style="color:#111111;font-family:Arial, Helvetica, sans-serif;line-height:21px;background-color:#FFFFFF;">__attribute__的section子项使用方式为：</span> </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">__attribute__((section("section_name")))</pre> 
<span style="color:#111111;font-family:Arial, Helvetica, sans-serif;line-height:21px;background-color:#FFFFFF;">其作用是将作用的函数或数据放入指定名为"section_name"的段。</span> 
<p> 看以下程序片段： </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">#include &lt;unistd.h&gt;
#include &lt;stdint.h&gt;
#include &lt;stdio.h&gt;

typedef void (*myown_call)(void);

extern myown_call _myown_start;
extern myown_call _myown_end;

#define _init __attribute__((unused, section(".myown")))
#define func_init(func) myown_call _fn_##func _init = func

static void mspec1(void)
{
        write(1, "aha!\n", 5);
}

static void mspec2(void)
{
        write(1, "aloha!\n", 7);
}

static void mspec3(void)
{
        write(1, "hello!\n", 7);
}

func_init(mspec1);
func_init(mspec2);
func_init(mspec3);

/* exactly like below:
static myown_call mc1  __attribute__((unused, section(".myown"))) = mspec1;
static myown_call mc2  __attribute__((unused, section(".myown"))) = mspec2;
static myown_call mc3  __attribute__((unused, section(".myown"))) = mspec3;
*/

void do_initcalls(void)
{
        myown_call *call_ptr = &amp;_myown_start;
        do {
                fprintf (stderr, "call_ptr: %p\n", call_ptr);
                (*call_ptr)();
                ++call_ptr;
        } while (call_ptr &lt; &amp;_myown_end);

}

int main(void)
{
        do_initcalls();
        return 0;
}</pre> 在自定义的.myown段依次填入mspec1/mspec2/mspec3的函数指针，并在do_initcalls中依次调用，从而达到构造并调用初始化函数列表的目的。 
<p> 两个extern变量： </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">extern myown_call _myown_start;
extern myown_call _myown_end;</pre> 来自ld的链接脚本，可以使用： 
<pre class="brush:shell; toolbar: true; auto-links: false;">ld --verbose</pre> 获取内置lds脚本，并在： 
<pre class="brush:shell; toolbar: true; auto-links: false;">__bss_start = .;</pre> 之前添加以下内容： 
<pre class="brush:shell; toolbar: true; auto-links: false;">_myown_start = .;
  .myown           : { *(.myown) } = 0x90000000
  _myown_end = .;
  code_segment    : { *(code_segment) }</pre> 即定义了.myown段及_myown_start/_myown_end变量（0x90000000这个数值可能需要调整）。 
<p> 保存修改后的链接器脚本，假设程序为s.c，链接器脚本保存为s.lds，使用以下命令编译： </p> 
<pre class="brush:shell; toolbar: true; auto-links: false;">gcc s.c -Wl,-Ts.lds</pre> 执行结果： 
<pre class="brush:shell; toolbar: true; auto-links: false;">[root@localhost ]# ./a.out 
call_ptr: 0x8049768
aha!
call_ptr: 0x804976c
aloha!
call_ptr: 0x8049770
hello!</pre> Have Fun!



<pre>
referer:http://my.oschina.net/u/180497/blog/177206
</pre>
