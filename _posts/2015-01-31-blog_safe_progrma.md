---
layout: post
title: "学习安全编程的方法"
categories: 技术文章
tags: [安全编程]
date: 2015-02-04 14:39:34
---

<pre>
用下列好的编程习惯和安全软件指导来写软件，在设计技巧、系统调用和库调用上使用合适的信息，在Simson　Garfinkle和Gene Spafford的《ractical　Unix　and　Internet　Securiy》一书的第23章里有许多关于安全编程和非安全编程技巧的信息。下面是其精髓所在。

安全的编程方法

检查所有的命令行参数；
检查所有的系统调用参数和返回代码；
检查环境参数，不要依靠Unix环境变量；
确定所有的缓存都被检查过；
在变量的内容被拷贝到本地缓存之前对变量进行边界检查；
如果创建一个新文件,使用O_EXCL和O_CREATE标志来确定文件没有已经存在；
使用lstat()来确定文件不是一个符号连接；
使用下面的这些库调用：fgets(),　strncpy(),　strncat(),　snprintf()　而不是其它类似的函数，可以说，只使用检查了长度的函数。
同样的，小心的使用execve()，如果你必须衍生一个进程。
在程序开始时显式的更改目录(chdir())到适当的地方；
限制当程序失败时产生的core文件，core文件里有可能含有密码和其它内存状态信息；
如果使用临时文件，考虑使用系统调用tmpfile()或mktemp()来创建它们(虽然很多mktemp()库调用可能有race　condition的情况)；
内部有做完整性检查的代码；
做大量的日志记录，包括日期、时间、uid和effective uid、gid和effe ctive gid、终端信息、pid、命令行参数、错误和主机名；
使程序的核心尽可能小和简单；
永远用全路径名做文件参数，检查用户的输入，确保只有"好"的字符；
使用好的工具如lint，理解race　conditions，包括死锁状态和顺序状态；
在网络读请求的程序里设置timeouts和负荷级别的限制；
在网络写请求里放置timeouts；
使用会话加密来避免会话抢劫和隐藏验证信息；
尽可能使用chroot()设置程序环境；
如果可能，静态连接安全程序；
当需要主机名时使用DNS逆向解释；
在网络服务程序里分散和限制过多的负载；
在网络的读和写里放置适当的timeout限制；
如果合适，防止服务程序运行超过一个以上的拷贝

不安全的编程方法

防止使用在处理字符串时不检查buffer边界的函数，如gets()、strcpy()、strcat()、sprintf()、fscanf()、scanf()、vsprin tf()、realpath()、getopt()、getpass()、streadd()、strecpy()和strtrns()，同样，避免使用execlp()和execvp()。永远不要用system()和popen()系统调用；
不要将文件创建文件在全部人可写的目录里；
通常，不要设置setuid或者setgid的shell scripts；
不要假想端口号码，应该用getservbyname()函数；
不要假设来自小数字的端口号的连接是合法和可信任的；
不要相信任何IP地址，如果要验证，用密码算法；
不要用明文方式验证信息；
不要尝试从严重的错误中恢复，要输出详细信息然后中断；
考虑使用perl　-T或taintperl写setuid的perl程序

测试程序安全

用cracker的方法来做软件测试：
尝试使程序里的所有缓存溢出；
尝试使用任意的命令行选项；
尝试建立可能的race condition；
设计者做代码重阅和测试；
读所有的代码，象cracker一样思维来找漏洞；
使用这些应该可以提高软件质量，减少代码bug，特别是安全漏洞。

</pre>
