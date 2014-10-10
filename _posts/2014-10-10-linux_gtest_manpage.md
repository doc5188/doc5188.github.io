---
layout: post
title: "linux下gtest超级新手入门"
categories: c/c++
tags: [gtest入门, gtest教程]
date: 2014-10-10 10:56:12
---

* （0）gtest是什么

gtest是一个跨平台的C++测试框架，google作品。

它支持自动发现测试，断言集，用户定义的断言，death测试，致命与非致命的失败，类型参数化测试，各类运行测试的选项和XML的测试报告。

* （1）下载gtest

地址：

http://code.google.com/p/googletest/downloads/list

笔者下载的版本是1.6.0

http://googletest.googlecode.com/files/gtest-1.6.0.zip

* （2）安装gtest
{% highlight bash %}
# unzip gtest-1.6.0.zip
# cd gtest-1.6.0
# ./configure
# make
{% endhighlight %}

确认lib目录下生成了libgtest.a和libgtest_main.a，

这两个库是后续测试程序需要链接的库。

* （3）测试gtest

不妨设我们需要测试foo.h中的一个max函数（求两个数中较大的一个）

foo.h文件内如如下：

{% highlight bash %}	
#ifndef __FOO_H__
#define __FOO_H__
int max(int a, int b)
{
return a>b?a:b;
}
#endif
{% endhighlight %}

撰写测试程序foo_test.cpp来对foo进行测试：

foo_test.cpp文件内如如下：
	
{% highlight bash %}
#include "gtest/gtest.h"
#include "foo.h"
 
TEST(foo, max)
{
EXPECT_EQ(2, max(2,-1));
EXPECT_EQ(3, max(2,3));
}
 
int main(int argc, char** argv)
{
::testing::InitGoogleTest(&argc, argv);
return RUN_ALL_TESTS();
}
{% endhighlight %}

编译foo_test.cpp，编译命令如下：
	
{% highlight bash %}
# g++ -g foo_test.cpp -o foo_test \
-I./gtest-1.6.0/include \
-L./gtest-1.6.0/lib -lgtest -lgtest_main -lpthread
{% endhighlight %}

需要注意的是，要链接pthread这个库。

执行结果如下：
<pre>
[==========] Running 1 test from 1 test case.
[==========] Global test environment set-up.
[==========] 1 test from foo
[ RUN       ] foo.max
[             OK ] foo.max (0 ms)
[==========] 1 test from foo (0 ms total)

[==========] Global test environment tear-down
[==========] 1 test from 1 test case ran. (0 ms total)
[ PASSED ] 1 test.
</pre>

* （4）简要说明
	
{% highlight bash %}
TEST(name1, name2)
{
EXPECT_EQ(value1, value2);
}
{% endhighlight %}

这是要执行的测试用例，后面是执行内容

name1：测试用例名称

name2：测试名称

这两个参数都只起到提示作用，我们也可以这么使用

name1：类名

name2：方法名

或者

name1：文件名

name2：函数名

EXPECT_EQ(value1, value2);

用例执行成功时，期望value1和value2是相等的，相等才算通过测试，如上例中的：

EXPECT_EQ(2, max(2,-1));

max(2, -1)的执行结果值期望是2如果不等，则用例运行失败。
	
{% highlight bash %}
TEST(name1, name2)
int main(int argc, char** argv)
{
::testing::InitGoogleTest(&argc, argv);
return RUN_ALL_TESTS();
}
{% endhighlight %}

这个是main函数，InitGoogleTest会初始化一些环境变量，RUN_ALL_TESTS()会调用所有的TEST(name1, name2)

* （6）结束语

想了解更详细的关于gtest的信息，见官网：

http://code.google.com/p/googletest/
