---
layout: post
title: "BitTorrent协议规范(BitTorrent Protocol Specification)系列之B编码(Bencoding)-第一部分"
categories: 网络
tags: [bittorrent, p2p, dht]
date: 2014-10-29 11:39:00
---

<p>鉴定<br />BitTorrent是由布莱姆&#183;科恩设计的一个端对端(peer to peer)文件共享协议，此协议使多个peers通过不可信任的网络的文件传输变得更容易。</p>
<p>目的<br />此规范的目的是详细介绍 BitTorrent 协议规范 v1.0 。Bram 的协议规范网站 http://www.bittorrent.com/protocol.html 简要地叙述了此协议，在部分范围缺少详细的行为阐述。该文档使用清楚明确的措辞书写，希望它能够成为一个正式的规范，当然也可用于将来实现和讨论的基础。</p>
<p>此文档旨在由 BitTorrent 开发社区维护和使用。欢迎大家为它做贡献，其中的内容仅代表当前协议，但它已经被目前许多存在的客户端实现所采用。</p>
<p>应用范围<br />本文档适用于 BitTorrent 协议规范的第一版（v1.0）。目前，这份文档应用于 torrent 文件结构规范、peer wire协议规范和Tracker HTTP/HTTPS 协议规范。如果某个协议有了新的修订，请到对应页面查看，而不是在这里。</p>
<p>(译者注：在本文档翻译过程中，如果遇到没有对应标准翻译的术语，一律不予翻译，例如torrent，peer，tracker等)</p>
<p>约定<br />为了简明和准确地表达信息，在本文档中，使用了许多约定。</p>
<p>peer v/s 客户端(client)：在本文档中，一个peer可以是任何参与下载的 BitTorrent 客户端。客户端也是一个peer，尽管 BitTorrent 客户端运行在本地机器上。本规范的读者可能会认为自己是连接了许多peer的客户端。 <br />片(piece) v/s 块(block)：在本文档中，片是指在元信息文件(metainfo file)中描述的一部分已下载的数据，它可通过 SHA-1 hash 来验证。而块是指客户端向peer请求的一部分数据。两块或更多块组成一个完整的可以被验证的片。 <br />实际标准(defacto standard)：粗斜体文本指出一个规则在许多不同的BitTorrent客户端实现中如此通用，以致于该规则被当做是一个实际标准。 <br />(译者注：peer一般翻译成&#8216;端&#8217;，所以p2p应该翻译成端对端，但是这并没有一个标准的译法，因此在本文中不作翻译，同时读者应该将peer to peer和数据链路层的点对点协议(也缩写为p2p)区分开)</p>
<p>B编码(Bencoding)<br />B编码是一种以简洁的格式描述和组织数据的方法。支持下列类型：字节串、整数、lists和dictionaries。</p>
<p>字节串<br />字节串按如下方式编码：&lt;以十进制ASCII编码的串长度&gt;：&lt;串数据&gt;<br />注意：字节串编码没有开始和结束分隔符。 </p>
<p>例：4:spam表示字节串&#8220;spam&#8221;</p>
<p>整数<br />整数按如下方式编码：i&lt;以十进制ASCII编码的整数&gt;e<br />开始的&#8220;i&#8221;与结尾的&#8220;e&#8221;分别是开始和结束分隔符。可以使用如&#8220;i-3e&#8221;之类的负数。但是你不能把&#8220;0&#8221;放到数字的前面，如&#8220;i04e&#8221;。另外，&#8220;i0e&#8221;是有效的。<br />例：&#8220;i3e&#8221;表示整数&#8220;3&#8221;</p>
<p>注意：对于这个整数的最大位数规范并没有做出规定，（待译）</p>
<p>lists<br />lists按如下方式编码：l&lt;B编码值&gt;e<br />开始的&#8220;l&#8221;(l是小写的L，而不是大写的i)与结尾的&#8220;e&#8221;分别是开始和结束分隔符。lists可以包含任何B编码的类型，包括整数、串、dictionaries和其他的lists。<br />例：l4:spam4:eggse 表示含有两个串的lists:[&#8220;spam&#8221;、&#8220;eggs&#8221;]</p>
<p>dictionaries<br />dictionaries按如下方式编码：d&lt;B编码串&gt;&lt;B编码元素&gt;e<br />开始的&#8220;d&#8221;与结尾的&#8220;e&#8221;分别是开始和结束分隔符。 注意键（key）必须被B编码为串。值可以是任何B编码的类型，包括整数、串、lists和其他的dictionaries。键（key）必须是串，并且以排序的顺序出现（以原始串排列，而不是以字母数字顺序）。串采用二进制比较方式，而不是特定于某种文化的自然比较（即既不是按照中文的比较方式，也不是按照英文的排序方式）。<br />例1：d3:cow3:moo4:spam4:eggse 表示dictionary { "cow" =&gt; "moo", "spam" =&gt; "eggs" }<br />例2：d4:spaml1:a1:bee 表示dictionary { "spam" =&gt; ["a", "b"] }</p>
<p>例3：d9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee表示dictionary&nbsp; { "publisher" =&gt; "bob", "publisher-webpage" =&gt; "www.example.com", "publisher.location" =&gt; "home" } </p>
<p>(译者注：对于string和integer，目前已经存在官方的翻译，但是list和dictionary并没有存在一个统一的译法，在此以原文示之，相信学过Java和c#的人不会对这两个术语感到陌生)</p>
<p>B编码实现<br />C <br />Perl <br />Java <br />Python by Hackeron <br />Decoding encoding bencoded data with haskell by Edi <br />Objective-C by Chrome</p>
