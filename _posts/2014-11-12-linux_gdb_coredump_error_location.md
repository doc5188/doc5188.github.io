---
layout: post
title: "gdb结合coredump定位崩溃进程"
categories: c/c++
tags: [gdb, coredump定位]
date: 2014-11-13 12:48:26
---

<span style="border-collapse: separate;">Linux环境下经常遇到某个进程挂掉而找不到原因，我们可以通过生成core file文件加上gdb来定位。</span></span></span></p>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><strong><span style="font-family: courier new,courier,monospace;"><span style="border-collapse: separate;">如何产生core file?</span></span></strong></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="border-collapse: separate;"><span style="line-height: 19px; background-color: rgb(255, 255, 255);">我们可以使用ulimit这条命令对core file文件的大小进行设定。</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px; background-color: rgb(255, 255, 255);">一般默认情况下，core file的大小被设置为了0，这样系统就不dump出core file了。</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px; background-color: rgb(255, 255, 255);">这时用如下命令进行设置：</span><br style="font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 19px; background-color: rgb(255, 255, 255);">
	<span style="line-height: 19px; background-color: rgb(255, 255, 255);"><font color="#AD0000">ulimit -c unlimited</font></span><br style="font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 19px; background-color: rgb(255, 255, 255);">
	<span style="line-height: 19px; background-color: rgb(255, 255, 255);">这样便把core file的大小设置为了无限大，同时也可以使用数字来替代unlimited，对core file的上限值做更精确的设定。</span></span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><strong><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;">生成的core file在哪里?</span></span></strong></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">core file生成的地方是在/proc/sys/kernel/core_pattern文件定义的。</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">改动到生成到自己定义的目录的方法是：</span><br style="font-size: 13px; background-color: rgb(255, 255, 255);">
	<span style="background-color: rgb(255, 255, 255);">echo "pattern" &gt; /proc/sys/kernel/core_pattern</span><br style="font-size: 13px; background-color: rgb(255, 255, 255);">
	<span style="background-color: rgb(255, 255, 255);">并且只有超级用户可以修改这两个文件。</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">"pattern"类似我们C语言打印字符串的格式，相关标识如下：</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(211, 211, 211);">%%: 相当于%</span><br>
	<span style="background-color: rgb(211, 211, 211);">%p: 相当于&lt;pid&gt;</span><br>
	<span style="background-color: rgb(211, 211, 211);">%u: 相当于&lt;uid&gt;</span><br>
	<span style="background-color: rgb(211, 211, 211);">%g: 相当于&lt;gid&gt;</span><br>
	<span style="background-color: rgb(211, 211, 211);">%s: 相当于导致dump的信号的数字</span><br>
	<span style="background-color: rgb(211, 211, 211);">%t: 相当于dump的时间</span><br>
	<span style="background-color: rgb(211, 211, 211);">%h: 相当于hostname</span><br>
	<span style="background-color: rgb(211, 211, 211);">%e: 相当于执行文件的名称</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;">这时用如下命令设置生成的core file到系统/tmp目录下，并记录pid以及执行文件名</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><font color="#AD0000"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">echo "/tmp/core-%e-%p" &gt;&nbsp;</span></span><span style="line-height: 19px;">/proc/sys/kernel/core_pattern</span></font></span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">测试如下代码</span></span></span></span></div>
<div>
	<div><div id="highlighter_838434" class="syntaxhighlighter  cpp"><div class="toolbar"><span><a href="#" class="toolbar_item command_help help">?</a></span></div><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="gutter"><div class="line number1 index0 alt2">1</div><div class="line number2 index1 alt1">2</div><div class="line number3 index2 alt2">3</div><div class="line number4 index3 alt1">4</div><div class="line number5 index4 alt2">5</div><div class="line number6 index5 alt1">6</div><div class="line number7 index6 alt2">7</div><div class="line number8 index7 alt1">8</div><div class="line number9 index8 alt2">9</div><div class="line number10 index9 alt1">10</div><div class="line number11 index10 alt2">11</div><div class="line number12 index11 alt1">12</div></td><td class="code"><div class="container"><div class="line number1 index0 alt2"><code class="cpp preprocessor">#include &lt;stdio.h&gt;</code></div><div class="line number2 index1 alt1">&nbsp;</div><div class="line number3 index2 alt2"><code class="cpp color1 bold">int</code> <code class="cpp plain">func(</code><code class="cpp color1 bold">int</code> <code class="cpp plain">*p)</code></div><div class="line number4 index3 alt1"><code class="cpp plain">{</code></div><div class="line number5 index4 alt2"><code class="cpp spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="cpp plain">*p = 0;</code></div><div class="line number6 index5 alt1"><code class="cpp plain">}</code></div><div class="line number7 index6 alt2">&nbsp;</div><div class="line number8 index7 alt1"><code class="cpp color1 bold">int</code> <code class="cpp plain">main()</code></div><div class="line number9 index8 alt2"><code class="cpp plain">{</code></div><div class="line number10 index9 alt1"><code class="cpp spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="cpp plain">func(NULL);</code></div><div class="line number11 index10 alt2"><code class="cpp spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="cpp keyword bold">return</code> <code class="cpp plain">0;</code></div><div class="line number12 index11 alt1"><code class="cpp plain">}</code></div></div></td></tr></tbody></table></div></div>
</div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">生成可执行文件并运行</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">gcc -o main a.c</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">root@ubuntu:~# ./main<br>
	Segmentation fault (core dumped)&nbsp;</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">&lt;-----这里出现段错误并生成core文件了。</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">在/tmp目录下发现文件</span></span>core-main-10815&nbsp;</span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><strong><span style="font-family: courier new,courier,monospace;">如何查看进程挂在哪里了?</span></strong></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">我们可以用</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">gdb main /tmp/core-main-10815&nbsp;</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">查看信息，发现能定位到函数了</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">Program terminated with signal 11, Segmentation fault.<br>
	#0&nbsp; 0x080483ba in func ()</span></span></div>
<div>
	&nbsp;</div>
<p>
	<span style="font-size: 14px;"><strong><span style="font-family: courier new,courier,monospace;">如何定位到行?</span></strong></span></p>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">在编译的时候开启-g调试开关就可以了</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="border-collapse: separate;"><span style="line-height: 19px;">gcc -o main&nbsp;<font color="#AD0000">-g</font>&nbsp;a.c</span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="border-collapse: separate;"><span style="line-height: 19px;"><span style="border-collapse: separate; line-height: normal;">gdb main /tmp/core-main-10815&nbsp;</span></span></span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;">最终看到的结果如下，好棒。</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="border-collapse: separate;"><span style="line-height: 19px;">Program terminated with signal 11, Segmentation fault.<br>
	#0&nbsp; 0x080483ba in func (p=0x0) at a.c:5<br>
	5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *p = 0;</span></span></span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="line-height: 19px;">总结一下，需要定位进程挂在哪一行我们只需要4个操作，</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><font color="#AD0000"><span style="line-height: 19px;"><span style="border-collapse: separate; line-height: normal;"><span style="line-height: 19px;">ulimit -c unlimited</span></span></span></font></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><font color="#AD0000"><span style="line-height: 19px;"><span style="border-collapse: separate; line-height: normal;"><span style="line-height: 19px;"><span style="border-collapse: separate; line-height: normal;"><span style="line-height: 19px;"><span style="background-color: rgb(255, 255, 255);">echo "/tmp/core-%e-%p" &gt;&nbsp;</span></span><span style="line-height: 19px;">/proc/sys/kernel/core_pattern</span></span></span></span></span></font></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="color: rgb(173, 0, 0); font-family: 'courier new',courier,monospace; line-height: 19px;">gcc -o main&nbsp;-g&nbsp;a.c</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="color: rgb(173, 0, 0); font-family: 'courier new',courier,monospace;">gdb main /tmp/core-main-10815&nbsp;</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">就可以啦。</span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">补充说明：</span></span></div>
<div>
	<strong><span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">相关常用gdb命令</span></span></strong></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;"><span style="color: rgb(255, 0, 0);">1,(gdb) backtrace /* 查看当前线程函数栈回溯 */</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">以上面的例子为例</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">Program terminated with signal 11, Segmentation fault.</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">#0 &nbsp;0x080483ba in func (p=0x0) at main.c:5</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">5<span class="Apple-tab-span" style="white-space: pre;"> </span>*p = 0;</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">(gdb) backtrace</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">#0 &nbsp;0x080483ba in func (p=0x0) at main.c:5</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">#1 &nbsp;0x080483d4 in main () at main.c:10</span></span></div>
<div>
	<span style="color: rgb(255, 0, 0);"><span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">如果是多线程环境下(gdb) thread apply all backtrace /* 显示所有线程栈回溯 */</span></span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="color: rgb(255, 0, 0);"><span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">2,(gdb) print [var] /* 查看变量值 */</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">(gdb) print p</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">$1 = (int *) 0x0</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">(gdb) print &amp;p</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">$2 = (int **) 0xbf96d4d4</span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="color: rgb(255, 0, 0);"><span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">3,(gdb) x/FMT [Address] /* 根据格式查看地址指向的值 */</span></span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">其中</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">FMT is a repeat count followed by a format letter and a size letter.</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">Format letters are o(octal), x(hex), d(decimal), u(unsigned decimal),</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">&nbsp; t(binary), f(float), a(address), i(instruction), c(char) and s(string).</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">Size letters are b(byte), h(halfword), w(word), g(giant, 8 bytes).</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">The specified number of objects of the specified size are printed</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">according to the format.</span></span></div>
<div>
	&nbsp;</div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">(gdb) x/d 0xbf96d4d4</span></span></div>
<div>
	<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">0xbf96d4d4:<span class="Apple-tab-span" style="white-space: pre;"> </span>0</span></span></div>
<div>
	<div>
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">(gdb) x/c 0xbf96d4d4</span></span></div>
	<div>
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">0xbf96d4d4:<span class="Apple-tab-span" style="white-space: pre;"> </span>0 '\000'</span></span></div>
	<div>
		&nbsp;</div>
</div>
<div>
	<strong><span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">另外能导致产生core file文件的信号有以下10种</span></span></strong></div>
<div>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGQUIT：终端退出符</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGILL：非法硬件指令</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGTRAP：平台相关的硬件错误，现在多用在实现调试时的断点</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGBUS：与平台相关的硬件错误，一般是内存错误</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGABRT：调用abort函数时产生此信号，进程异常终止</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGFPE：算术异常</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGSEGV：segment violation，无效内存引用</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGXCPU：超过了cpu使用资源限制（setrlimit）</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGXFSZ：超过了文件长度限制（setrlimit）</span></span></p>
	<p style="margin-left: 10.5pt;">
		<span style="font-size: 14px;"><span style="font-family: courier new,courier,monospace;">SIGSYS：无效的系统调用</span>
