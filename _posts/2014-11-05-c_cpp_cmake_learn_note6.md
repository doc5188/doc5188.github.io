---
layout: post
title: "cmake 学习笔记(六)"
categories: c/c++
tags: [cmake, 系列教程]
date: 2014-11-05 12:58:23
---

<p><span style="font-family:Arial,'Lucida Grande',sans-serif; font-size:16px; color:#000000; border-collapse:separate; font-style:normal; font-variant:normal; font-weight:normal; letter-spacing:normal; line-height:normal; orphans:2; text-indent:0px; text-transform:none; white-space:normal; widows:2; word-spacing:0px"></span></p>
<p class="line862">希望这是现阶段阻碍阅读shiboken和PySide源码的涉及cmake的最后一个障碍<span> ^ </span>_^</p>
<p class="line874">学习 cmake 的单元测试部分 ctest。</p>
<h2 id="A.2Be4BTVU9.2FdSg-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
简单使用</h2>
<p class="line874">最简单的使用ctest的方法，就是在 CMakeLists.txt 添加命令：</p>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">enable_testing()</pre>
<ul>
<li style="list-style-type:none">该命令需要在源码的根目录文件内。</li></ul>
<p class="line874">从这一刻起，就可以在工程中添加add_test命令了</p>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">add_test(NAME &lt;name&gt; [CONFIGURATIONS [Debug|Release|...]]
           [WORKING_DIRECTORY dir]
           COMMAND &lt;command&gt; [arg1 [arg2 ...]])</pre>
<ul>
<li>name 指定一个名字</li><li>Debug|Release 控制那种配置下生效</li><li>dir 设置工作目录</li><li>command
<ul>
<li>如果是可执行程序目标，则会被cmake替换成生成的程序的全路径</li><li>
<p class="line862" style="margin:0.25em 0px">后面的参数可以使用 $&lt;...&gt; 这种语法，比如 $&lt;TARGET_FILE:tgt&gt; 指代tgt这个目标的全名</p>
</li></ul>
</li></ul>
<h2 id="ApiExtractor" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
ApiExtractor</h2>
<p class="line862">继续以 ApiExtractor 为例学习ctest的使用</p>
<p class="line874">顶层的CMakeLists.txt文件的内容片段：</p>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">option(BUILD_TESTS &quot;Build tests.&quot; TRUE)
if (BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()</pre>
<p class="line874">创建选项，让用户控制是否启用单元测试。如果启用，则添加进 tests 子目录，我们看其CMakeLists.txt文件</p>
<ul>
<li>首先是创建一个declare_test的宏
<ul>
<li>使用 qt4_automoc 进行moc处理</li><li>生成可执行文件</li><li>调用 add_test 加入测试</li></ul>
</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">macro(declare_test testname)
    qt4_automoc(&quot;${testname}.cpp&quot;)
    add_executable(${testname} &quot;${testname}.cpp&quot;)
    include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR} ${apiextractor_SOURCE_DIR})
    target_link_libraries(${testname} ${QT_QTTEST_LIBRARY} ${QT_QTCORE_LIBRARY} ${QT_QTGUI_LIBRARY} apiextractor)
    add_test(${testname} ${testname})
endmacro(declare_test testname)</pre>
<ul>
<li>后续就简单了,需要的配置文件直接使用configure_file 的 COPYONLY</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">declare_test(testabstractmetaclass)
declare_test(testabstractmetatype)
declare_test(testaddfunction)
declare_test(testarrayargument)
declare_test(testcodeinjection)
configure_file(&quot;${CMAKE_CURRENT_SOURCE_DIR}/utf8code.txt&quot;
                &quot;${CMAKE_CURRENT_BINARY_DIR}/utf8code.txt&quot; COPYONLY)
declare_test(testcontainer)</pre>
<h2 id="Qt.2BU1VRQ21Li9U-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
Qt单元测试</h2>
<p class="line874">QTestLib 模块用起来还是很简单的，我们这儿稍微一下cmake和qmake的一点不同。</p>
<ul>
<li>使用qmake时，我们只需要一个源文件，比如测试 QString 类时，写一个 testqstring.cpp 文件</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0"> #include &lt;QtTest/QtTest&gt;

 class TestQString: public QObject
 {
     Q_OBJECT
 private slots:
     void toUpper();
 };

 void TestQString::toUpper()
 {
     QString str = &quot;Hello&quot;;
     QCOMPARE(str.toUpper(), QString(&quot;HELLO&quot;));
 }

 QTEST_MAIN(TestQString)
 #include &quot;testqstring.moc&quot;</pre>
<p class="line874">然后pro文件内启用 testlib 模块，其他和普通Qt程序一样了。</p>
<ul>
<li>使用 cmake 时，我们将其分成两个文件</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">//testqstring.h
 #include &lt;QtTest/QtTest&gt;

 class TestQString: public QObject
 {
     Q_OBJECT
 private slots:
     void toUpper();
 };</pre>
<p class="line874">与</p>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">//testqstring.cpp
 void TestQString::toUpper()
 {
     QString str = &quot;Hello&quot;;
     QCOMPARE(str.toUpper(), QString(&quot;HELLO&quot;));
 }

 QTEST_MAIN(TestQString)
 #include &quot;testqstring.moc&quot;</pre>
<p class="line874">然后处理方式就是我们前面看到的那个宏了。</p>
<h2 id="QTest" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">QTest宏</h2>
<p class="line874">随便看下QTest的宏</p>
<ul>
<li>QTEST_APPLESS_MAIN</li><li>QTEST_NOOP_MAIN</li><li>QTEST_MAIN</li></ul>
<pre style="padding:0.5em; font-family:courier,monospace; background-color:#f0ece6; white-space:pre-wrap; word-wrap:break-word; border:1pt solid #c0c0c0">#define QTEST_APPLESS_MAIN(TestObject) /
int main(int argc, char *argv[]) /
{ /
    TestObject tc; /
    return QTest::qExec(&amp;tc, argc, argv); /
}

#define QTEST_NOOP_MAIN /
int main(int argc, char *argv[]) /
{ /
    QObject tc; /
    return QTest::qExec(&amp;tc, argc, argv); /
}

#define QTEST_MAIN(TestObject) /
int main(int argc, char *argv[]) /
{ /
    QCoreApplication app(argc, argv); /
    TestObject tc; /
    return QTest::qExec(&amp;tc, argc, argv); /
}</pre>
<p class="line874">最终都是调用QTest::qExec,Manual中对其有不少介绍了(略)。</p>
<h2 id="A.2BU8KAAw-" style="padding:0px 0px 0.3em; border-bottom:3px solid #047307">
参考</h2>
<ul>
<li>
<p class="line891" style="margin:0.25em 0px"><a class="http" href="http://www.itk.org/Wiki/CMake_Testing_With_CTest" style="color:#047307; border-width:0px">http://www.itk.org/Wiki/CMake_Testing_With_CTest</a></p>
</li><li>
<p class="line891" style="margin:0.25em 0px"><a class="http" href="http://www.cmake.org/cmake/help/cmake-2-8-docs.html#command:add_test" style="color:#047307; border-width:0px">http://www.cmake.org/cmake/help/cmake-2-8-docs.html#command:add_test</a></p>
</li></ul>
<p>&nbsp;</p>



<pre>
referer:http://blog.csdn.net/dbzhang800/article/details/6341803
</pre>
