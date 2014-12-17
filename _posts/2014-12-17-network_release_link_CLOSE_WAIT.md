---
layout: post
title: "网络连接无法释放—— CLOSE_WAIT"
categories: 网络
tags: [网络, CLOST_WAIT, TCP/IP, socket]
date: 2014-12-17 13:15:17
---

<span class="Apple-style-span" style="color: rgb(68, 68, 68); font-family: Verdana; font-size: 13px; line-height: 22px;">
<h4 id="subjcns!2DAA368B386E6AEA!618" style="margin: 4px 0px; line-height: 185%; font-weight: bold; font-size: 108%;">网络连接无法释放—— CLOSE_WAIT</h4>
<br>
<p style="line-height: 170%;"><span class="Apple-style-span" style="font-weight: bold;">转自:&nbsp;<span class="Apple-style-span" style="font-weight: normal;">http://pengjiaheng.spaces.live.com/blog/cns!2DAA368B386E6AEA!618.entry</span></span></p>
<p style="line-height: 170%;"><strong style="line-height: 170%; font-weight: bold;"></strong>&nbsp;</p>
<p style="line-height: 170%;"><strong style="line-height: 170%; font-weight: bold;">问题描述：</strong>最
近性能测试碰到的一个问题。客户端使用NIO，服务器还是一般的Socket连接。当测试进行一段时间以后，发现服务器端的系统出现大量未释放的网络连
接。用netstat -na查看，连接状态为CLOSE_WAIT。这就奇怪了，为什么Socket已经关闭而连接依然未释放。</p>
<p style="line-height: 170%;">&nbsp;</p>
<p style="line-height: 170%;"><strong style="line-height: 170%; font-weight: bold;">解决：</strong>Google
了半天，发现关于CLOSE_WAIT的问题一般是C的，Java似乎碰到这个问题的不多（这有一篇不错的，也是解决CLOSE_WAIT的，但是好像没
有根本解决，而是选择了一个折中的办法）。接着找，由于使用了NIO，所以怀疑可能是这方面的问题，结果找到了这篇。顺着帖子翻下去，其中有几个人说到了
一个问题——&nbsp;<font style="line-height: normal;" color="#ff0000"><strong style="line-height: 170%; font-weight: bold;">一端的Socket调用close后，另一端的Socket没有调用close</strong></font>.于是查了一下代码，果然发现Server端在某些异常情况时，没有关闭Socket。改正后问题解决。</p>
<p style="line-height: 170%;">时间基本上花在Google上了，不过也学到不少东西。下面为一张TCP连接的状态转换图：</p>
<p style="line-height: 170%;">&nbsp;</p>
<p style="line-height: 170%;"><img src="http://image8.360doc.com/DownloadImg/2010/04/1416/2865765_1" style="line-height: 170%;" height="594" width="420"></p>
<p style="line-height: 170%;">&nbsp;</p>
<p style="line-height: 170%;">说明：虚线和实线分别对应服务器端(被连接端)和客户端端(主动连接端)。</p>
<p style="line-height: 170%;">结合上图使用netstat -na命令即可知道到当前的TCP连接状态。一般LISTEN、ESTABLISHED、TIME_WAIT是比较常见。</p>
<p style="line-height: 170%;">&nbsp;</p>
<p style="line-height: 170%;"><strong style="line-height: 170%; font-weight: bold;">分析：</strong></p>
<p style="line-height: 170%;">上面我碰到的这个问题主要因为TCP的结束流程未走完，造成连接未释放。现设客户端主动断开连接，流程如下</p>
<p style="line-height: 170%;">&nbsp;</p>
<p style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong style="line-height: 170%; font-weight: bold;">Client&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消息&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Server</strong></p>
<p style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; close()<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;------ FIN -------&gt;<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; FIN_WAIT1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CLOSE_WAIT<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;----- ACK -------<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FIN_WAIT2&nbsp;<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;close()<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;------ FIN ------&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TIME_WAIT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LAST_ACK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
<p style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ------ ACK -------&gt;&nbsp;&nbsp;<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;CLOSED<br style="line-height: 170%;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CLOSED</p>
<p style="line-height: 170%;">&nbsp;</p>
<p style="line-height: 170%;">如上图所示，由于Server的Socket在客户端已经关闭时而没有调用关闭，造成服务器端的连接处在“挂起”状态，而客户端则处在等待应答的状态上。此问题的典型特征是：<strong style="line-height: 170%; font-weight: bold;"><font style="line-height: normal;" color="#ff0000">一端处于FIN_WAIT2&nbsp;，而另一端处于CLOSE_WAIT</font></strong>. 不过，根本问题还是程序写的不好，有待提高。</p>
</span>
