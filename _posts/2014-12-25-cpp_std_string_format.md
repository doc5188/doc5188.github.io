---
layout: post
title: "CString、std::string格式化字符串"
categories: c/c++
tags: [c/c++, string格式化]
date: 2014-12-25 17:11:14
---

<p>=============================CString==================================</p>
<p>&nbsp;当有多个字串时，比如 &nbsp; <br>&nbsp; int &nbsp; n1 &nbsp; = &nbsp; 5; &nbsp; <br>&nbsp; int &nbsp; n2 &nbsp; = &nbsp; 10; &nbsp; <br>&nbsp; char &nbsp; sz1[] &nbsp; = &nbsp; "abcdefg"; &nbsp; <br>&nbsp; char &nbsp; sz2[] &nbsp; = &nbsp; "hijklmn"; &nbsp; <br>&nbsp; &nbsp; <br>&nbsp; 用std中的string如何写出最简单的代码得到MFC中CString如下效果： &nbsp; <br>&nbsp; &nbsp; <br>&nbsp; CString &nbsp; s; &nbsp; <br>&nbsp; s.Format(" &nbsp; result: &nbsp; %d &nbsp; + &nbsp; %d &nbsp; = &nbsp; %d/n &nbsp; sz1: &nbsp; %s/n &nbsp; sz2: &nbsp; %s/n", &nbsp; n1, &nbsp; n2, &nbsp; n1+n2, &nbsp; sz1, &nbsp; sz2 &nbsp; );&nbsp;&nbsp; <br></p>
<p>===========================std::string==================================</p>
<p>int &nbsp; n1 &nbsp; = &nbsp; 5;&nbsp;&nbsp;&nbsp;<br>int &nbsp; n2 &nbsp; = &nbsp; 10;&nbsp;&nbsp;&nbsp;<br>char &nbsp; sz1[] &nbsp; = &nbsp; "abcdefg";&nbsp;&nbsp;&nbsp;<br>char &nbsp; sz2[] &nbsp; = &nbsp; "hijklmn"; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; std::ostringstream &nbsp; ostr; &nbsp; // &nbsp; include &nbsp; &lt;sstream&gt; &nbsp; <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ostr &nbsp; &lt;&lt; &nbsp; "result:" &nbsp; &lt;&lt; &nbsp; n1 &nbsp; &lt;&lt; &nbsp; "+" &nbsp; &lt;&lt; &nbsp; n2 &nbsp; &lt;&lt; &nbsp; "=" &nbsp; &lt;&lt; &nbsp; n1+n2 &nbsp; &nbsp; <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &lt;&lt; &nbsp; "/nsz1:" &nbsp; &lt;&lt; &nbsp; sz1 &nbsp; <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &lt;&lt; &nbsp; "/nsz2:" &nbsp; &lt;&lt; &nbsp; sz2; &nbsp; <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; //std::cout &nbsp; &lt;&lt; &nbsp; ostr.str().c_str() &nbsp; &lt;&lt; &nbsp; std::endl;</p>
<p>std::string s = ostr.str();</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>附加说明</p>
<p>在C++有两种 &nbsp; <br>&nbsp; 一个是在&lt;sstream&gt;另一个是&lt;strstream&gt;它们实现的东西基本一样, &nbsp; 区别是前者为前标准. &nbsp; <br>&nbsp; 而前标准里ostringstream::str()是返回std::string的. &nbsp; <br>&nbsp; &nbsp; <br>&nbsp; &lt;strstream&gt;包含 &nbsp; <br>&nbsp; &nbsp; class &nbsp; strstreambuf; &nbsp; <br>&nbsp; &nbsp; class &nbsp; istrstream; &nbsp; <br>&nbsp; &nbsp; class &nbsp; ostrstream; &nbsp; <br>&nbsp; &nbsp; class &nbsp; strstream; &nbsp; <br>&nbsp; 它们是基于char*编写的 &nbsp; <br>&nbsp; &nbsp; <br>&nbsp; &lt;sstream&gt; &nbsp; <br>&nbsp; class &nbsp; istringstream; &nbsp; <br>&nbsp; class &nbsp; ostreamstream; &nbsp; <br>&nbsp; class &nbsp; stringbuf; &nbsp; <br>&nbsp; class &nbsp; stringstream; &nbsp; <br>&nbsp; class &nbsp; ... &nbsp; <br>&nbsp; .... &nbsp; <br>&nbsp; 它们是基于std::string编写的.&nbsp;&nbsp;</p>
<p>&nbsp;</p>
<p>===============char * 有sprintf====================</p>
<p>&nbsp;</p>

<pre>
referer:http://blog.csdn.net/geeeeeeee/article/details/3503956
</pre>
