---
layout: post
title: "【原】Netsnmp调试方法"
categories: 网络
tags: [netsnmpd]
date: 2014-10-17 12:17:39
---

Netsnmp调试方法

由于snmpd是一个daemon进程，刚接触netsnmp时不知如何调试，学习一段时间之后发现可以有下面几个调试方法。

1. 启动snmpd时使用-D选项

netsnmp/include/net-snmp/net-snmp-config.h 文件中有关于-D选项的调试宏。

（1）编译-D调试信息，修改下面宏：
<pre>
#undef NETSNMP_NO_DEBUGGING

#define NETSNMP_ALWAYS_DEBUG 0

</pre>

此时DEBUGMSG（）系列的调试信息编译到程序中。在启动snmpd时加上-Daaa:bbb就可以开启带有aaa:bbb字符串的调试信息，-Dbbb则开启带有bbb字符串的调试信息，字符串中以冒号做为分隔符。DEBUGMSG()系列调试宏在netsnmp/include/net-snmp/library/snmp_debug.h文件中。

例：DEBUGMSGTL(("aaa:bbb", "debugging of something %s related\n", "snmp"));

<pre>
snmpd –Daaa   或 snmpd –Dbbb 或snmpd –Daaa:bbb,  都能使该调试语句在终端打印信息。

DEBUGMSG（）系列函数还能打印整型变量，例：

DEBUGMSGTL(("aaa:bbb", "num = \n", num));
</pre>

浮点型的没有试过。

说明：使用上面的宏定义是将调试信息成为程序的一部分。带调试信息的程序比没有带的大出很多，在产品发布时不需要带调试信息。不建议使用NETSNMP_ALWAYS_DEBUG，这样开启所有调试，不能选择需要的调试。

（2）不编译调试信息，修改上面的宏：

<pre>
#define NETSNMP_NO_DEBUGGING 1

#define NETSNMP_ALWAYS_DEBUG 0
</pre>

2. 启动snmpd时使用-f选项

使用-f选项时，snmpd不成为daemon，而是一般进程。这种情况下可以使用我们常用的printf了。为了能够选择是否编译调试信息，建议使用如下的调试方法，使用宏来控制调试信息的编译。这个方法在开发其它程序时也能用。具体意思就不再说明了，其中define中使用了“#”，起替换的作用。

<pre>
 #define DEBUG_RS232MIB
 //#undef DEBUG_RS232MIB
 #ifdef DEBUG_RS232MIB
  #define DPRINT(expr) printf(#expr " = %d\n",expr)
  #define SPRINT(expr) printf(#expr " = %s\n",expr)
  #define XPRINT(expr) printf(#expr " = %x\n",expr)
  #define DPRINT_2(expr1,expr2)  printf(#expr1 ":" #expr2" = %d\n",expr2)
  #define SPRINT_2(expr1,expr2)  printf(#expr1 ":" #expr2" = %s\n",expr2)
  #define PRINT_POS() printf("%s, %s, %d\n",__FILE__,__FUNCTION__, __LINE__)
  #define PRINT_POS_2(expr)  printf(#expr ":%s, %s, %d\n", __FILE__,__FUNCTION__, __LINE__)
  #define PDEBUG(fmt, args...) printf(fmt, ## args)
 #else
  #define DPRINT(expr)
  #define SPRINT(expr)
  #define XPRINT(expr)
  #define DPRINT_2(expr1,expr2)
  #define SPRINT_2(expr1,expr2)
  #define PRINT_POS()
  #define PRINT_POS_2(expr)
  #define PDEBUG(fmt, args...)
 #endif  
</pre>
