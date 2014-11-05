---
layout: post
title: "cmake 学习笔记(一)"
categories: c/c++
tags: [cmake,系列教程]
date: 2014-10-08 17:44:53
---


<div id="article_content" class="article_content">

<p><span style="font-family: Arial,'Lucida Grande',sans-serif; font-size: 16px; color: rgb(0, 0, 0); border-collapse: separate; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px;"></span></p>
<ul>
<li>最大的Qt4程序群(KDE4)采用cmake作为构建系统</li><li>Qt4的python绑定(pyside)采用了cmake作为构建系统</li><li>开源的图像处理库 opencv 采用cmake 作为构建系统</li><li>...</li></ul>
<p class="line874">看来不学习一下cmake是不行了，一点一点来吧，找个最简单的C程序，慢慢复杂化，试试看：</p>
<div>
<table style="margin: 0.5em 0px 0px 0.5em; border-collapse: collapse;" border="0">
<tbody>
<tr>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">例子一</p>
</td>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">单个源文件 main.c</p>
</td>
</tr>
<tr>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">例子二</p>
</td>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">==&gt;分解成多个 main.c hello.h hello.c</p>
</td>
</tr>
<tr>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">例子三</p>
</td>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">==&gt;先生成一个静态库，链接该库</p>
</td>
</tr>
<tr>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">例子四</p>
</td>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">==&gt;将源文件放置到不同的目录</p>
</td>
</tr>
<tr>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">例子五</p>
</td>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">==&gt;控制生成的程序和库所在的目录</p>
</td>
</tr>
<tr>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">例子六</p>
</td>
<td style="padding: 0.25em 0.5em; border: 1px solid rgb(4, 115, 7);">
<p class="line862" style="margin: 0px; padding: 0px;">==&gt;使用动态库而不是静态库</p>
</td>
</tr>
</tbody>
</table>
</div>
<h2 id="A.2BT4tbUE4A-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t0"></a>
例子一</h2>
<p class="line874">一个经典的C程序，如何用cmake来进行构建程序呢？</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">//main.c
#include &lt;stdio.h&gt;
int main()
{
    printf("Hello World!/n");
    return 0;
}</pre>
<p class="line874">编写一个 CMakeList.txt 文件(可看做cmake的工程文件)：</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">project(HELLO)
set(SRC_LIST main.c)
add_executable(hello ${SRC_LIST})</pre>
<p class="line874">然后，建立一个任意目录（比如本目录下创建一个build子目录），在该build目录下调用cmake</p>
<ul>
<li>注意：为了简单起见，我们从一开始就采用cmake的 out-of-source 方式来构建（即生成中间产物与源代码分离），并始终坚持这种方法，这也就是此处为什么单独创建一个目录，然后在该目录下执行 cmake 的原因</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">cmake .. -G"NMake Makefiles"
nmake</pre>
<p class="line874">或者</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">cmake .. -G"MinGW Makefiles"
make</pre>
<p class="line874">即可生成可执行程序 hello(.exe)</p>
<p class="line874">目录结构</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">+
| 
+--- main.c
+--- CMakeList.txt
|
/--+ build/
   |
   +--- hello.exe</pre>
<p class="line874">cmake 真的不太好用哈，使用cmake的过程，本身也就是一个编程的过程，只有多练才行。</p>
<p class="line874">我们先看看：前面提到的这些都是什么呢？</p>
<h3 id="CMakeList.txt" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t1"></a>
CMakeList.txt</h3>
<p class="line862">第一行<span>&nbsp;</span><strong>project</strong><span>&nbsp;</span>不是强制性的，但最好始终都加上。这一行会引入两个变量</p>
<ul>
<li>HELLO_BINARY_DIR 和 HELLO_SOURCE_DIR</li></ul>
<p class="line874">同时，cmake自动定义了两个等价的变量</p>
<ul>
<li>
<p class="line891" style="margin: 0.25em 0px;"><strong>PROJECT_BINARY_DIR</strong><span>&nbsp;</span>和<span>&nbsp;</span><strong>PROJECT_SOURCE_DIR</strong></p>
</li></ul>
<p class="line874">因为是out-of-source方式构建，所以我们要时刻区分这两个变量对应的目录</p>
<p class="line862">可以通过<strong>message</strong>来输出变量的值</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">message(${PROJECT_SOURCE_DIR})</pre>
<p class="line867"><strong>set</strong><span>&nbsp;</span>命令用来设置变量</p>
<p class="line867"><strong>add_exectuable</strong><span>&nbsp;</span>告诉工程生成一个可执行文件。</p>
<p class="line867"><strong>add_library</strong><span>&nbsp;</span>则告诉生成一个库文件。</p>
<ul>
<li>注意：CMakeList.txt 文件中，命令名字是不区分大小写的，而参数和变量是大小写相关的。</li></ul>
<h3 id="cmake.2BVH1O5A-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t2"></a>
cmake命令</h3>
<p class="line874">cmake 命令后跟一个路径(..)，用来指出 CMakeList.txt 所在的位置。</p>
<p class="line862">由于系统中可能有多套构建环境，我们可以通过<tt>-G</tt>来制定生成哪种工程文件，通过<span>&nbsp;</span><tt>cmake&nbsp;-h</tt><span>&nbsp;</span>可得到详细信息。</p>
<p class="line874">要显示执行构建过程中详细的信息(比如为了得到更详细的出错信息)，可以在CMakeList.txt内加入：</p>
<ul>
<li>SET( CMAKE_VERBOSE_MAKEFILE on )</li></ul>
<p class="line874">或者执行make时</p>
<ul>
<li>$ make VERBOSE=1</li></ul>
<p class="line874">或者</p>
<ul>
<li>$ export VERBOSE=1</li><li>$ make</li></ul>
<h2 id="A.2BT4tbUE6M-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t3"></a>
例子二</h2>
<p class="line874">一个源文件的例子一似乎没什么意思，拆成3个文件再试试看：</p>
<ul>
<li>hello.h 头文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">#ifndef DBZHANG_HELLO_
#define DBZHANG_HELLO_
void hello(const char* name);
#endif //DBZHANG_HELLO_</pre>
<ul>
<li>hello.c</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">#include &lt;stdio.h&gt;
#include "hello.h"

void hello(const char * name)
{
    printf ("Hello %s!/n", name);
}</pre>
<ul>
<li>main.c</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">#include "hello.h"
int main()
{
    hello("World");
    return 0;
}</pre>
<ul>
<li>然后准备好CMakeList.txt 文件</li></ul>
<p class="line867">&nbsp;</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">project(HELLO)
set(SRC_LIST main.c hello.c)
add_executable(hello ${SRC_LIST})</pre>
<p class="line874">执行cmake的过程同上，目录结构</p>
<p class="line867">&nbsp;</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">+
| 
+--- main.c
+--- hello.h
+--- hello.c
+--- CMakeList.txt
|
/--+ build/
   |
   +--- hello.exe</pre>
<p class="line874">例子很简单，没什么可说的。</p>
<h2 id="A.2BT4tbUE4J-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t4"></a>
例子三</h2>
<p class="line874">接前面的例子，我们将 hello.c 生成一个库，然后再使用会怎么样？</p>
<p class="line874">改写一下前面的CMakeList.txt文件试试：</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">project(HELLO)
set(LIB_SRC hello.c)
set(APP_SRC main.c)
add_library(libhello ${LIB_SRC})
add_executable(hello ${APP_SRC})
target_link_libraries(hello libhello)</pre>
<p class="line874">和前面相比，我们添加了一个新的目标 libhello，并将其链接进hello程序</p>
<p class="line874">然后想前面一样，运行cmake，得到</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">+
| 
+--- main.c
+--- hello.h
+--- hello.c
+--- CMakeList.txt
|
/--+ build/
   |
   +--- hello.exe
   +--- libhello.lib</pre>
<p class="line874">里面有一点不爽，对不？</p>
<ul>
<li>因为我的可执行程序(add_executable)占据了 hello 这个名字，所以 add_library 就不能使用这个名字了</li><li>然后，我们去了个libhello 的名字，这将导致生成的库为 libhello.lib(或 liblibhello.a)，很不爽</li><li>想生成 hello.lib(或libhello.a) 怎么办?</li></ul>
<p class="line874">添加一行</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">set_target_properties(libhello PROPERTIES OUTPUT_NAME "hello")</pre>
<p class="line874">就可以了</p>
<h2 id="A.2BT4tbUFbb-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t5"></a>
例子四</h2>
<p class="line874">在前面，我们成功地使用了库，可是源代码放在同一个路径下，还是不太正规，怎么办呢？分开放呗</p>
<p class="line874">我们期待是这样一种结构</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">+
|
+--- CMakeList.txt
+--+ src/
|  |
|  +--- main.c
|  /--- CMakeList.txt
|
+--+ libhello/
|  |
|  +--- hello.h
|  +--- hello.c
|  /--- CMakeList.txt
|
/--+ build/</pre>
<p class="line874">哇，现在需要3个CMakeList.txt 文件了，每个源文件目录都需要一个，还好，每一个都不是太复杂</p>
<ul>
<li>顶层的CMakeList.txt 文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">project(HELLO)
add_subdirectory(src)
add_subdirectory(libhello)</pre>
<ul>
<li>src 中的 CMakeList.txt 文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">include_directories(${PROJECT_SOURCE_DIR}/libhello)
set(APP_SRC main.c)
add_executable(hello ${APP_SRC})
target_link_libraries(hello libhello)</pre>
<ul>
<li>libhello 中的 CMakeList.txt 文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">set(LIB_SRC hello.c)
add_library(libhello ${LIB_SRC})
set_target_properties(libhello PROPERTIES OUTPUT_NAME "hello")</pre>
<p class="line874">恩，和前面一样，建立一个build目录，在其内运行cmake，然后可以得到</p>
<ul>
<li>build/src/hello.exe</li><li>build/libhello/hello.lib</li></ul>
<p class="line874">回头看看，这次多了点什么，顶层的 CMakeList.txt 文件中使用 add_subdirectory 告诉cmake去子目录寻找新的CMakeList.txt 子文件</p>
<p class="line862">在 src 的 CMakeList.txt 文件中，新增加了<strong>include_directories</strong>，用来指明头文件所在的路径。</p>
<h2 id="A.2BT4tbUE6U-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t6"></a>
例子五</h2>
<p class="line874">前面还是有一点不爽：如果想让可执行文件在 bin 目录，库文件在 lib 目录怎么办？</p>
<p class="line874">就像下面显示的一样：</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">   + build/
   |
   +--+ bin/
   |  |
   |  /--- hello.exe
   |
   /--+ lib/
      |
      /--- hello.lib</pre>
<ul>
<li>一种办法：修改顶级的 CMakeList.txt 文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">project(HELLO)
add_subdirectory(src bin)
add_subdirectory(libhello lib)</pre>
<p class="line874">不是build中的目录默认和源代码中结构一样么，我们可以指定其对应的目录在build中的名字。</p>
<p class="line874">这样一来：build/src 就成了 build/bin 了，可是除了 hello.exe，中间产物也进来了。还不是我们最想要的。</p>
<ul>
<li>另一种方法：不修改顶级的文件，修改其他两个文件</li></ul>
<p class="line874">src/CMakeList.txt 文件</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">include_directories(${PROJECT_SOURCE_DIR}/libhello)
#link_directories(${PROJECT_BINARY_DIR}/lib)
set(APP_SRC main.c)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
add_executable(hello ${APP_SRC})
target_link_libraries(hello libhello)</pre>
<p class="line874">libhello/CMakeList.txt 文件</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">set(LIB_SRC hello.c)
add_library(libhello ${LIB_SRC})
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
set_target_properties(libhello PROPERTIES OUTPUT_NAME "hello")</pre>
<h2 id="A.2BT4tbUFFt-" style="padding: 0px 0px 0.3em; border-bottom: 3px solid rgb(4, 115, 7);"><a name="t7"></a>
例子六</h2>
<p class="line874">在例子三至五中，我们始终用的静态库，那么用动态库应该更酷一点吧。 试着写一下</p>
<p class="line874">如果不考虑windows下，这个例子应该是很简单的，只需要在上个例子的 libhello/CMakeList.txt 文件中的add_library命令中加入一个SHARED参数：</p>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">add_library(libhello SHARED ${LIB_SRC})</pre>
<p class="line874">可是，我们既然用cmake了，还是兼顾不同的平台吧，于是，事情有点复杂：</p>
<ul>
<li>修改 hello.h 文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">#ifndef DBZHANG_HELLO_
#define DBZHANG_HELLO_
#if defined _WIN32
    #if LIBHELLO_BUILD
        #define LIBHELLO_API __declspec(dllexport)
    #else
        #define LIBHELLO_API __declspec(dllimport)
    #endif
#else
    #define LIBHELLO_API
#endif
LIBHELLO_API void hello(const char* name);
#endif //DBZHANG_HELLO_</pre>
<ul>
<li>修改 libhello/CMakeList.txt 文件</li></ul>
<pre style="padding: 0.5em; font-family: courier,monospace; background-color: rgb(240, 236, 230); white-space: pre-wrap; word-wrap: break-word; border: 1pt solid rgb(192, 192, 192);">set(LIB_SRC hello.c)
add_definitions("-DLIBHELLO_BUILD")
add_library(libhello SHARED ${LIB_SRC})
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
set_target_properties(libhello PROPERTIES OUTPUT_NAME "hello")</pre>
<p class="line874">恩，剩下来的工作就和原来一样了。</p>
</div>
