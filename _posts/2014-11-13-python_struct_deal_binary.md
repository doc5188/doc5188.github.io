---
layout: post
title: "Python使用struct处理二进制"
categories: python
tags: [python struct, construct]
date: 2014-11-13 15:39:57
---


<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
有的时候需要用python处理二进制数据，比如，存取文件，socket操作时.这时候，可以使用python的struct模块来完成.可以用 struct来处理c语言中的结构体.<br>
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
struct模块中最重要的三个函数是pack(), unpack(), calcsize()</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
pack(fmt, v1, v2, ...) &nbsp; &nbsp; 按照给定的格式(fmt)，把数据封装成字符串(实际上是类似于c结构体的字节流)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
unpack(fmt, string) &nbsp; &nbsp; &nbsp; 按照给定的格式(fmt)解析字节流string，返回解析出来的tuple</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
calcsize(fmt) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 计算给定的格式(fmt)占用多少字节的内存<br>
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
struct中支持的格式如下表：</p>
<table class="docutils" style="border: 1px solid silver; border-collapse: collapse; color: rgb(0, 0, 0); font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;" border="1">
<thead valign="bottom">
<tr>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
Format</th>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
C Type</th>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
Python</th>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
字节数</th>
</tr>
</thead>
<tbody valign="top">
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">x</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">pad byte</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">no value</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">c</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">char</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">string of length 1</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">b</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">signed</span>&nbsp;<span class="pre">char</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">B</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">unsigned</span>&nbsp;<span class="pre">char</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">?</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">_Bool</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">bool</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">h</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">short</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">2</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">H</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">unsigned</span>&nbsp;<span class="pre">short</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">2</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">i</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">int</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">4</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">I</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">unsigned</span>&nbsp;<span class="pre">int</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer or long</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">4</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">l</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">long</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">integer</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">4</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">L</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">unsigned</span>&nbsp;<span class="pre">long</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">long</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">4</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">q</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">long</span>&nbsp;<span class="pre">long</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">long</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">8</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">Q</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">unsigned</span>&nbsp;<span class="pre">long</span>&nbsp;<span class="pre">long</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">long</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">8</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">f</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">float</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">float</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">4</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">d</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">double</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">float</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">8</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">s</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">char[]</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">string</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">p</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span class="pre"><span style="font-family: 新宋体;">char[]</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">string</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">1</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">P</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="xref docutils literal"><span style="font-family: 新宋体;"><span class="pre">void</span>&nbsp;<span class="pre">*</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">long</td>
</tr>
</tbody>
</table>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
注1.q和Q只在机器支持64位操作时有意思</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
注2.每个格式前可以有一个数字，表示个数</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
注3.s格式表示一定长度的字符串，4s表示长度为4的字符串，但是p表示的是pascal字符串</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
注4.P用来转换一个指针，其长度和机器字长相关</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
注5.最后一个可以用来表示指针类型的，占4个字节<br>
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
为了同c中的结构体交换数据，还要考虑有的c或c++编译器使用了字节对齐，通常是以4个字节为单位的32位系统，故而struct根据本地机器字节顺序转换.可以用格式中的第一个字符来改变对齐方式.定义如下：</p>
<table class="docutils" style="border: 1px solid silver; border-collapse: collapse; color: rgb(0, 0, 0); font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;" border="1">
<thead valign="bottom">
<tr>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
Character</th>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
Byte order</th>
<th class="head" style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
Size and alignment</th>
</tr>
</thead>
<tbody valign="top">
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">@</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">native</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">native&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 凑够4个字节</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">=</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">native</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 按原字节数</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">&lt;</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">little-endian</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 按原字节数</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">&gt;</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">big-endian</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 按原字节数</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><tt class="docutils literal"><span class="pre"><span style="font-family: 新宋体;">!</span></span></tt></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">network (= big-endian)</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">
<p style="margin: 10px auto;">standard&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 按原字节数</p>
</td>
</tr>
</tbody>
</table>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
使用方法是放在fmt的第一个位置，就像'@5s6sif'<br>
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
<strong>示例一：</strong></p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
比如有一个结构体</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
struct Header</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
{</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp; &nbsp; unsigned short id;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp; &nbsp; char[4] tag;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp; &nbsp; unsigned int version;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp; &nbsp; unsigned int count;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
}</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
通过socket.recv接收到了一个上面的结构体数据，存在字符串s中，现在需要把它解析出来，可以使用unpack()函数.</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
import struct</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
id, tag, version, count = struct.unpack("!H4s2I", s)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
上面的格式字符串中，!表示我们要使用网络字节顺序解析，因为我们的数据是从网络中接收到的，在网络上传送的时候它是网络字节顺序的.后面的H表示 一个unsigned short的id,4s表示4字节长的字符串，2I表示有两个unsigned int类型的数据.<br>
<br>
<br>
就通过一个unpack，现在id, tag, version, count里已经保存好我们的信息了.</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
同样，也可以很方便的把本地数据再pack成struct格式.</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
ss = struct.pack("!H4s2I", id, tag, version, count);</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
pack函数就把id, tag, version, count按照指定的格式转换成了结构体Header，ss现在是一个字符串(实际上是类似于c结构体的字节流)，可以通过 socket.send(ss)把这个字符串发送出去.</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
<strong><br>
示例二：</strong></p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
import struct</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
a=12.34</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
#将a变为二进制</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
bytes=struct.pack('i',a)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
此时bytes就是一个string字符串，字符串按字节同a的二进制存储内容相同。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
<br>
再进行反操作</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
现有二进制数据bytes，（其实就是字符串），将它反过来转换成python的数据类型：</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
a,=struct.unpack('i',bytes)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
注意，unpack返回的是tuple</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
所以如果只有一个变量的话：</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
bytes=struct.pack('i',a)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
那么，解码的时候需要这样</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
a,=struct.unpack('i',bytes) 或者 (a,)=struct.unpack('i',bytes)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
如果直接用a=struct.unpack('i',bytes)，那么 a=(12.34,) ，是一个tuple而不是原来的浮点数了。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
<br>
如果是由多个数据构成的，可以这样：</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
a='hello'</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
b='world!'</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
c=2</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
d=45.123</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
bytes=struct.pack('5s6sif',a,b,c,d)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
此时的bytes就是二进制形式的数据了，可以直接写入文件比如 binfile.write(bytes)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
然后，当我们需要时可以再读出来，bytes=binfile.read()</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
再通过struct.unpack()解码成python变量</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
a,b,c,d=struct.unpack('5s6sif',bytes)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
'5s6sif'这个叫做fmt，就是格式化字符串，由数字加字符构成，5s表示占5个字符的字符串，2i，表示2个整数等等，下面是可用的字符及类型，ctype表示可以与python中的类型一一对应。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
<strong><br>
注意：二进制文件处理时会碰到的问题</strong></p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
我们使用处理二进制文件时，需要用如下方法</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
binfile=open(filepath,'rb') &nbsp; &nbsp;读二进制文件</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
binfile=open(filepath,'wb') &nbsp; &nbsp;写二进制文件</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
那么和binfile=open(filepath,'r')的结果到底有何不同呢？</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
不同之处有两个地方：</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
第一，使用'r'的时候如果碰到'0x1A'，就会视为文件结束，这就是EOF。使用'rb'则不存在这个问题。即，如果你用二进制写入再用文本读出的话，如果其中存在'0X1A'，就只会读出文件的一部分。使用'rb'的时候会一直读到文件末尾。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
第二，对于字符串x='abc\ndef'，我们可用len(x)得到它的长度为7，\n我们称之为换行符，实际上是'0X0A'。当我们用'w'即文本方式写的时候，在windows平台上会自动将'0X0A'变成两个字符'0X0D'，'0X0A'，即文件长度实际上变成8.。当用'r'文本方式读取时，又自动的转换成原来的换行符。如果换成'wb'二进制方式来写的话，则会保持一个字符不变，读取时也是原样读取。所以如果用文本方式写入，用二进制方式读取的话，就要考虑这多出的一个字节了。'0X0D'又称回车符。linux下不会变。因为linux只使用'0X0A'来表示换行。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
附加:</p>
<div style="font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
<span style="color: rgb(0, 0, 255);">import</span>&nbsp;struct&nbsp;<br>
<br>
<span style="color: rgb(0, 128, 0);">#</span><span style="color: rgb(0, 128, 0);">&nbsp;native byteorder&nbsp;</span><span style="color: rgb(0, 128, 0);"><br>
</span>buffer&nbsp;=&nbsp;struct.pack(<span style="color: rgb(128, 0, 0);">"</span><span style="color: rgb(128, 0, 0);">ihb</span><span style="color: rgb(128, 0, 0);">"</span>,&nbsp;1,&nbsp;2,&nbsp;3)&nbsp;<br>
<span style="color: rgb(0, 0, 255);">print</span>&nbsp;repr(buffer)&nbsp;<br>
<span style="color: rgb(0, 0, 255);">print</span>&nbsp;struct.unpack(<span style="color: rgb(128, 0, 0);">"</span><span style="color: rgb(128, 0, 0);">ihb</span><span style="color: rgb(128, 0, 0);">"</span>, buffer)&nbsp;<br>
<br>
<span style="color: rgb(0, 128, 0);">#</span><span style="color: rgb(0, 128, 0);">&nbsp;data from a sequence, network byteorder&nbsp;</span><span style="color: rgb(0, 128, 0);"><br>
</span>data&nbsp;=&nbsp;[1,&nbsp;2,&nbsp;3]&nbsp;<br>
buffer&nbsp;=&nbsp;struct.pack(<span style="color: rgb(128, 0, 0);">"</span><span style="color: rgb(128, 0, 0);">!ihb</span><span style="color: rgb(128, 0, 0);">"</span>,&nbsp;*data)<br>
<span style="color: rgb(0, 0, 255);">print</span>&nbsp;repr(buffer)&nbsp;<br>
<span style="color: rgb(0, 0, 255);">print</span>&nbsp;struct.unpack(<span style="color: rgb(128, 0, 0);">"</span><span style="color: rgb(128, 0, 0);">!ihb</span><span style="color: rgb(128, 0, 0);">"</span>, buffer)</div>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
Output:</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
'\x01\x00\x00\x00\x02\x00\x03'<br>
(1, 2, 3)<br>
'\x00\x00\x00\x01\x00\x02\x03'<br>
(1, 2, 3)</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
首先将参数1,2,3打包，打包前1,2,3明显属于python数据类型中的integer,pack后就变成了C结构的二进制串，转成 python的string类型来显示就是　　'\x01\x00\x00\x00\x02\x00\x03'。由于本机是小端('little- endian',关于大端和小端的区别请参照<a target="_blank" href="http://249wangmang.blog.163.com/blog/static/5263076520119481313433/" style="color: rgb(0, 102, 170); text-decoration: none;">这里</a>,故而高位放在低地址段。i
 代表C struct中的int类型，故而本机占4位，1则表示为01000000;h 代表C struct中的short类型，占2位，故表示为0200;同理b 代表C struct中的signed char类型，占1位，故而表示为03。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
其他结构的转换也类似，有些特别的可以参考Manual。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
在Format string 的首位，有一个可选字符来决定大端和小端，列表如下：</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp;</p>
<table style="border: 1px solid silver; border-collapse: collapse; color: rgb(0, 0, 0); font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;" border="1">
<thead>
<tr>
<th style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">&nbsp;</th>
<th style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">&nbsp;</th>
<th style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">&nbsp;</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><span style="font-family: NSimsun;">@</span></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">native</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">native</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><span style="font-family: NSimsun;">=</span></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">native</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><span style="font-family: NSimsun;">&lt;</span></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">little-endian</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><span style="font-family: NSimsun;">&gt;</span></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">big-endian</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard</td>
</tr>
<tr>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;"><span style="font-family: NSimsun;">!</span></td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">network (= big-endian)</td>
<td style="border: 1px solid silver; border-collapse: collapse; padding: 3px;">standard</td>
</tr>
</tbody>
</table>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
&nbsp;</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
如果没有附加，默认为@，即使用本机的字符顺序(大端or小端)，对于C结构的大小和内存中的对齐方式也是与本机相一致的(native)，比如有的机器integer为2位而有的机器则为四位;有的机器内存对其位四位对齐，有的则是n位对齐(n未知，我也不知道多少)。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
还有一个标准的选项，被描述为：如果使用标准的，则任何类型都无内存对齐。</p>
<p style="margin: 10px auto; font-family: Verdana,Geneva,Arial,Helvetica,sans-serif; font-size: 13px; line-height: 24px;">
比如刚才的小程序的后半部分，使用的format string中首位为！，即为大端模式标准对齐方式，故而输出的为'\x00\x00\x00\x01\x00\x02\x03'，其中高位自己就被放在内存的高地址位了。</p>


<pre>
referer: http://blog.csdn.net/iloveyin/article/details/40743399
</pre>
