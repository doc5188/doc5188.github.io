---
layout: post
categories: C/C++
tags: [C/C++]
title: "popen 重定向标准错误输出到管道流的方法"
date: 2014-09-11 09:12:58
---

{% highlight c %}
FILE *popen(const char *command, const char *type);
{% endhighlight %}

当使用type 参数为 “r" 时，popen 会把执行 command 后的标准输出重定向到管道流。但是，command执行中的标准错误输出，在管道流中得不到。

那么，有没有办法来同时获取到 command 执行后的标准输出和标准错误输出呢？答案是肯定的!

只要在 command 中，将标准错误输出重定向到标准输出即可!

例如：

{% highlight c %}
FILE *stream;
stream = popen(, "cp -f 2>&1", "r");

while(fgets(s, 1024, stream))
{
	printf(s);
}
{% endhighlight %}
