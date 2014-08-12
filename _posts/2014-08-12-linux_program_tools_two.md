---
layout: post
title: 编程工具系列之二------使用GDB的源代码查看功能
date:   2014-08-12 15:50:11
categories: Linux gdb
---

<pre>
      在调试程序的过程中，可以自由地查看相关的源代码（如果有源代码的话）是一项最基本的特性。
      一些IDE在这方面做得相当好，GDB当然也提供了这项特性，虽然不如IDE直观，但在一定程度上要比IDE更加灵活和快捷。
      GDB之所以能够知道对应的源代码，是因为调试版的可执行程序中记录了源代码的位置；因为源代码的位置在编译之后可能会移动到其它地方，所以GDB还会在当前目录中查找源代码，另外GDB也允许明确指定源代码的搜索位置。默认情况下，GDB在编译时目录中搜索，如果失败则在当前目录中搜索，即$cdir:$cwd，其中$cdir指的是编译时目录（compilation directory），$cwd指的是当前工作目录（current working directory）。
      在GDB中使用查看源代码相关的命令时，有一个当前文件的概念，当命令的位置参数没有限定一个文件的时候（不论是明确限定还是隐含限定），将使用当前文件。当前文件默认是main函数所在文件，如果程序当前正处于断点位置，则断点所在文件即为当前文件。
      与当前文件的概念类似，还存在一个当前行的概念，它默认为main函数的开始处。如果使用gdb载入一个可执行文件，然后单单执行一条简单的list命令，你会发现输出的源代码并非是从第一行开始的，这是因为当前行默认在main函数附近处的缘故。
      1.设置和获取源代码显示数量：
         默认情况下，GDB显示指定位置处以及其前后的10行代码，但是这是一个可设置的值。
         set listsize count：设置list命令显示的源代码数量最多为count行，0表示不限制行数。
         show listsize：显示listsize的值。
      2.编辑源代码：
         在一些情况下，我们希望在编辑器中显示或者编辑源代码，GDB允许我们使用自己喜欢的编辑器。
         可在环境变量EDITOR中指定GDB使用的编辑器，例如：EDITOR=/usr/bin/gedit;export EDITOR;gdb
         edit location：在编辑器中编辑位置location处的源代码，如果省略location，则编辑当前位置。
      3.搜索源代码：
         有的时候，我们希望在当前文件中进行搜索，GDB提供了这样的命令。
         search regexp：从当前行的下一行开始向前搜索。
         rev regexp ：从当前行的上一行开始向后搜索。
         有的时候，你会发现search命令总是提示“Expression not found”，这是因为当前行可能已经是最后一行了，特别是文件很短的时候。这里需要注意的是，任何list命令都会影响当前行的位置，并且由于每次都是多行输出，所以对当前行的影响并非简单地向前一行或者向后一行。
          search命令本身也会影响当前行的位置。
      4.源代码位置：
         GDB之所以可以查看到源代码，是因为它知道源代码放在哪里。
         在一个调试会话中，GDB维护了一个源代码查找目录列表，默认值是编译目录和当前工作目录。当GDB需要一个源文件的时候，它依次在这些目录中查找，直到找到一个或者抛出错误。
         GDB还维护了一个路径替换规则，将要搜索的原始路径按照找到的第一个规则做前缀替换，然后再在源码搜索目录中查找文件。
         GDB允许明确指定源代码位置，或者路径替换规则，以应付源代码位置迁移的情况。
         directory path-list：将一个或者多个源代码搜索目录加入到当前源码搜索目录列表的前面，目录之间使用空格间隔。
         directory：不带参数的directory将源码搜索目录恢复为默认值。
         set directories path-list：将源码目录设置为path-list，但是会补上默认目录。
         show directories：显示源码搜索目录列表。
         set substitute-path from to：设置目录替换规则，放置在规则列表的末端。
         unset substitute-path [path]：删除path对应的替换规则，或者删除所有的替换规则。
         show substitute-path [path]：显示path对应的替换规则，或者显示所有的替换规则。
      5.查看机器码：
        在一些必要的时候，我们需要查看汇编代码来诊断问题。GDB提供了这种可能。
        GDB提供了两种能力：显示源代码位置与指令地址之间的映射；显示指定位置的汇编代码。
        info line linespec：显示源代码linespec处对应的汇编地址范围。
        info line *addr：显示地址addr处对应的源代码位置。
        disassemble，disassemble /m，disassemble /r：显示指定地址范围内的汇编代码，有4种使用形式，第一种不带参数，显示当前正在执行的函数的汇编代码；第二           种是一个参数，显示该地址所在函数的汇编代码；第三种是两个参数的disassemble start,end，显示地址［start，end）内的汇编代码；第四种是两个参数的                       disassemble start,+length，显示地址［start，start+length）内的汇编代码。参数可以是16进制的地址，也可以是函数名。/m表示混合输出源代码和汇编代码，/r表           示混合输出二进制和汇编代码。
        set disassembly-flavor instruction-set：设置显示汇编代码时使用的风格，目前只针对intel x86系列，可取的值为att和intel，默认是att。
        show disassembly-flavor：显示disassembly-flavor设置
        set disassemble-next-line on|off|auto：当程序停止下来的时候，是否显示下一行源代码的汇编代码，默认为off。
        show disassemble-next-line：显示disassemble-next-line设置。
      6.显示指定位置的源代码：
        list命令可用于显示指定位置处的源代码。list命令会影响当前行和当前文件。
        list命令有多种方式指定要显示的源代码范围，可以是行号，函数名，甚至是指令地址。
        常用的如下：
        list linenum：显示指定行数附近的代码。
        list function：显示指定函数附近的代码。
        list ＊addr：显示指定地址附近的代码。
</pre>
