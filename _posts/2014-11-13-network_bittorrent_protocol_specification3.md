---
layout: post
title: "BitTorrent协议规范(BitTorrent Protocol Specification)之Tracker HTTP/HTTPS Protocol-第三部分"
categories: 网络
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范]
date: 2014-11-13 12:33:45
---

<p>Tracker HTTP/HTTPS Protocol <br />Tracker是一个响应HTTP GET请求的HTTP/HTTPS服务。这个请求包含来自客户端的度量信息，这些信息能够帮助Tracker全面地统计torrent。Tracker的响应包含一个peers列表，这个列表能够帮助客户端加入到torrent中。Base URL由元数据文件(即以.torrent为后缀的文件)中定义的announce URL组成，然后使用标准的CGI方式将这些请求参数追加到这个URL后面(CGI方式即在announce URL后面紧跟一个&#8217;?&#8217;，然后是一个以&#8217;&amp;&#8217;分隔的&#8217;param=value&#8217;序列)。</p>
<p>&nbsp;</p>
<p>注意：URL中的所有二进制数据(特别是info_hash和peer_id)必须适当地进行转义。这意味着不在集合{0-9, a-z, A-Z, &#8216;.&#8217;, &#8216;-&#8217;, &#8216;_&#8217;, &#8216;~&#8217;}中的字节必须以&#8217;%nn&#8217;方式编码，其中nn是这个字节的十六进制值。</p>
<p>&nbsp;</p>
<p>对于一个20字节的散列值 &#8220;\x12\x34\x56\x78\x9a\xbc\xde\xf1\x23\x45\x67\x89\xab\xcd\xef\</p>
<p>x12\x34\x56\x78\x9a&#8221;，其正确的编码形式是&#8220;%124Vx%9A%BC%DE%F1%23Eg%89%AB%CD%EF</p>
<p>%124Vx%9A&#8220;。</p>
<p>Tracker Request Parameters<br />从客户端发送到Tracker的请求包含如下参数：</p>
<p>l&nbsp; info_hash：URL编码的20字节SHA1散列，这个散列是元信息文件中info键所对应的值的SHA1散列。注意info键所对应的值是一个B编码的dictionary，关于info键的定义请参考我的上一篇博文。</p>
<p>l&nbsp; peer_id：使用URL编码的20字节串，用于标识客户端的唯一ID，由客户端启动时生成。这个ID可以是任意值，甚至可能是二进制数据。目前没有生成该ID的标准准则，尽管如此，实现者必须保证该ID对于本地主机是唯一的，因此可以通过包含进程ID和启动时记录的时间戳(timestamp)来达到这个目的。关于这个字段的常用客户端编码，请参考我的下一篇博文。</p>
<p>l&nbsp; port：客户端正在监听的端口号。为BitTorrent协议保留的端口号是6881-6889。如果不能使用该区间的数字建立端口号，客户端有可能拒绝建立连接。 </p>
<p>l&nbsp; uploaded：客户端已经上传的总量(从客户端发送&#8217;started&#8217;事件到Tracker算起)，以十进制ASCII表示。尽管官方规范没有显式指定，大部分情况下是指已经下载的字节总数。 </p>
<p>l&nbsp; downloaded：已下载的字节总量(从客户端发送&#8217;started&#8217;事件到Tracker算起)，以十进制ASCII表示。尽管官方规范没有显式指定，大部分情况下是指已经下载的字节总数。</p>
<p>l&nbsp; left：客户端还没有下载的字节数，以十进制ASCII表示。</p>
<p>l&nbsp; compact：如果设置为1，表示客户端接收压缩的响应包。这时peers列表将被peers串代替，在这个peers串中，每个peer占六个字节。这六个字节的前四个字节表示主机信息(以大端表示即以网络字节序)，后两个字节表示端口号(以大端表示即以网络字节序)。需要注意的是，为了节约带宽，有些Tracker只支持返回压缩的响应包，如果没有将compact设置为1，Tracker将拒绝这个请求或者如果请求中不包括compact=0这个参数，Tracker将返回压缩的响应包。</p>
<p>l&nbsp; no_peer_id：表示Tracker将省略peers dictionary中的id字段。如果启用compact，那么就会忽略这个选项。</p>
<p>l&nbsp; event：如果指定的话，必须是started, completed, stopped和空(和不指定的意义一样)中的一个。如果一个请求不指定event，表明它只是每隔一定间隔发送的请求。</p>
<p>n&nbsp; started：第一个发送到Tracker的请求其event值必须是该值。</p>
<p>n&nbsp; stopped：如果正常关闭客户端，必须发送改事件到Tracker。 </p>
<p>n&nbsp; completed：如果下载完毕，必须发送改事件到Tracker。如果客户端启动之前，已经下载完成的话，则没有必要发送该事件。Tracker仅仅基于该事件增加已经完成的下载数。 </p>
<p>l&nbsp; ip：(可选)，客户主机的IP地址，点分十进制IPv4或者RFC3513指定的十六进制Ipv6地址。注意：一般情况下这个参数没有必要，因为IP地址可以从HTTP请求中得到。只有当请求中的IP地址不是客户端的IP地址时，才需要这个参数(只有客户端通过代理和tracker 交互时才会发生这种情况)。如果客户端和Tracker都在NAT网关的同一侧，这个时候这个参数就是必要的。原因是Tracker会公布不能路由的客户端物理地址。因此客户端必须显示指出自己的IP地址，以将信息公布给外部的peers。不同的Tracker对待该参数的方式不同。一些Tracker只有当请求中的IP地址在RFC1918空间才使用它，有一些则无条件使用，另一些则根本不使用。如果是Ipv6地址，它表示这个客户端只能通过IPv6交互。 </p>
<p>l&nbsp; numwant：(可选)，客户端希望从Tracker接受到的peers数，如果省略，则默认是50个。</p>
<p>l&nbsp; key：(可选)，不和其他用户共享的附加标识。当客户端IP地址改变时，可以使用该标识来证明自己的身份。</p>
<p>l&nbsp; trackerid：(可选)，如果之前的announce包含一个tracker id，那么当前的请求必须设置该参数。</p>
<p>Tracker Response<br />Tracker以&#8221;text/plain&#8221;文本响应客户端的请求，这个响应文本由B编码的dictionary组成，而这个dictionary则包含如下的键(key)：</p>
<p>l&nbsp; failure reason：如果dictionary中包含这个键(key)，那么其他的键(key)就不会出现，该键(key)对应的值是一个可读的错误消息，它告诉用户的请求为什么会失败。(字符串类型)</p>
<p>l&nbsp; warning message：(新加入，可选) 类似于failure reason，但是即使存在这个键，这个响应还会正常地处理下去。warning message显示为一个错误。(字符串类型)</p>
<p>l&nbsp; interval：客户端每隔一定间隔就会向Tracker发送一个请求，这个键(key)以秒为单位指出这个间隔的大小。(整数类型)</p>
<p>l&nbsp; min interval：(可选)，最小的请求间隔，它表示客户端不能在这个时间间隔之内向Tracker重发请求。 (整数类型)</p>
<p>l&nbsp; tracker id：客户端发送其下一个请求时必须返回给Tracker的一个字符串。如果缺失，但是上一个请求发送了tracker id，那么不要丢弃旧值，重复利用即可。 </p>
<p>l&nbsp; complete：完成整个文件下载的peers数，即做种者的数量。 (整数类型) </p>
<p>l&nbsp; incomplete：非做种的peers数(还没有完成该文件下载的peers数)，即&#8220;占他人便宜者&#8221;数。(整数类型) </p>
<p>l&nbsp; peers：(dictionary model) 该键(key)对应的值是一个dictionary list(列表)，该list中的每一个dictionary都包含如下的键(key)：</p>
<p>n&nbsp; peer id：peer自己选择的用来标识自己的ID，上文在描述Tracker请求时已经说明。 (字符串类型) </p>
<p>n&nbsp; ip：peer的IP地址，可以是Ipv6/Ipv4/DNS name。(字符串类型)</p>
<p>n&nbsp; port：peer的端口号。(整数类型)</p>
<p>l&nbsp; peers：(binary model) 不是使用上面描述的dictionary model，binary model下，该键(key)对应的值可以有多个六字节组成的字符串。这六个字节中的前四个是IP地址，后两个是端口号。IP地址和端口号均以网络字节序(大端)表示。 </p>
<p>综上所述，默认情况下peers列表的长度是50，如果torrent中的peers比较少，那么这个列表长度会更短。否则如果torrent中的peers比较多，那么tracker就得从这些peers中随机选择一些放入响应中。当响应请求时，Tracker需要使用一个智能的机制来进行peer选择。例如：向做种者报告种子就得避免(意思说如果没有好的机制，就有可能出现这种情况)。</p>
<p>&nbsp;</p>
<p>如果有一个事件发生(即stopped或者completed)或者客户端需要获得更多的peers时，客户端发送请求的频率肯定高于指定的间隔。尽管如此，不断地向Tracker发送请求以获得更多的peers绝对不是一个好主意。如果一个客户端想在其响应中包含一个更长的peer列表，那么它应该通过指定numwant参数来达到目的。</p>
<p>&nbsp;</p>
<p>BitTorrent实现者注意：30个peers已经是一个很大的数目了，官方的客户端版本3在peers少于30的情况，会积极地向Tracker建立连接已获得更多的peers，但是如果客户端已经有55个peers的情况下，客户端将拒绝和Tracker建立连接。这个值的选择对于性能非常重要。当一个片(piece)已经下载完成后，客户端需要将HAVE消息(参考下文)发送给大多数活跃的peers。结果是广播通信的代价与peers数量成正比。这个数高于25之后，新加入的peers不太可能提升下载速度。强烈建议UI设计者使这个数模糊和很难修改，因为这样做没有任何作用。</p>
<p>Tracker 'scrape' Convention <br />按照惯例：大部分Tracker支持另一种形式的请求，这种方式查询Tracker正在管理的给定torrent(或者所有的torrent)。这种方式通常被称为&#8221;scrape page&#8221;，因为这种方式会自动进行另一个单调乏味的流程：&#8221;screen scraping&#8221; Tracker的统计页。</p>
<p>&nbsp;</p>
<p>类似于上面描述的URL，scrape URL也是一个HTTP GET方法。尽管如此，它们的Base URL是不相同的。想要得到scrape URL，请使用如下步骤：从announce URL开始，找到该announce URL中的最后一个&#8217;/&#8217;，如果该&#8217;/&#8217;之后的内容不是&#8217;announce&#8217;，那么说明这个Tracker不支持scrape。如果这个Tracker支持scrape，那么使用&#8217;scrape&#8217;代替&#8217;announce&#8217;就可以得到scrape页。</p>
<p>&nbsp;</p>
<p>例：(announce URL -&gt; scrape URL)</p>
<p>&nbsp; ~http://example.com/announce&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -&gt;&nbsp; ~http://example.com/scrape</p>
<p>&nbsp; ~http://example.com/x/announce&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -&gt;&nbsp; ~http://example.com/x/scrape</p>
<p>&nbsp; ~http://example.com/announce.php&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -&gt;&nbsp; ~http://example.com/scrape.php</p>
<p>&nbsp; ~http://example.com/a&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -&gt;&nbsp; (scrape not supported)</p>
<p>&nbsp; ~http://example.com/announce?x2%0644&nbsp; -&gt;&nbsp; ~http://example.com/scrape?x2%0644</p>
<p>&nbsp; ~http://example.com/announce?x=2/4&nbsp;&nbsp;&nbsp;&nbsp; -&gt;&nbsp; (scrape not supported)</p>
<p>&nbsp; ~http://example.com/x%064announce&nbsp;&nbsp;&nbsp;&nbsp; -&gt;&nbsp; (scrape not supported)</p>
<p>&nbsp;</p>
<p>scrape URL可以作为可选参数info_hash(上文描述的一个20字节值)的一个补充。但是这样限制了Tracker向那个特殊的torrent发送报告。否则tracker正在管理的所有torrent的统计数据将会返回。强烈建议软件编写者尽可能使用info_hash参数，这样就能够减少Tracker的负载和带宽。</p>
<p>你也可以指定多个info_hash参数给Tracker (得支持多个info_hash参数)。这不是官方规范的一部分，但是已经成为了实际标准，例如：</p>
<p>http://example.com/scrape.php?info_hash=aaaaaaaaaaaaaaaaaaaa&amp;info_hash=bbbbbbbbbbbbbbbbbbbb&amp;info_hash=cccccccccccccccccccc</p>
<p>&nbsp;</p>
<p>这个HTTP GET方法的响应是一个&#8217;text/plain&#8217;或者有时候是用gzip压缩的文本，这个文本由一个B编码的dictionary组成，这个dictionary包含如下的键(key)：</p>
<p>l&nbsp; files：这是一个B编码的dictionary，在该dictionary中，每一个torrent文件都有其相应的键/值，这个键/值是相应torrent文件的统计数据。每一个键(key)由20字节的二进制info_hash组成。而该键所对应的值也是dictionary，它包含如下的键(key)：</p>
<p>n&nbsp; complete：完成文件下载的peer数，即做种者的数量。(整数类型) </p>
<p>n&nbsp; downloaded：已向tracker注册的下载完成的总次数("event=complete"，即一个客户端完成了下载) 。(整数类型)</p>
<p>n&nbsp; incomplete：非做种的peers数(还没有完成该文件下载的peers数)，即&#8220;占他人便宜者&#8221;。 (整数类型) </p>
<p>n&nbsp; name：(可选的)，torrent的内部名，由.torrent文件中info键所对应值中的name指定。</p>
<p>注意这个响应有三层dictionary嵌套。例如：</p>
<p>d5:filesd20:....................d8:completei5e10:downloadedi50e10:incompletei10eeee </p>
<p>表示....................是一个20字节的info_hash，有5个做种者，5个正在下载者以及50个已经完成的下载。</p>
<p>Unofficial extensions to scrape(scrape的非正式扩展)<br />下面的响应键是非官方的。因为它们都是非官方的，因此都是可选的。</p>
<p>&nbsp;</p>
<p>l&nbsp; failure reason：可读的错误信息，这个信息告诉客户端请求失败的原因(字符串类型)。使用该键的知名客户端：Azureus。</p>
<p>l&nbsp; flags：这是一个B编码的dictionary，它包含多个标志。flags键对应的值是另一个嵌套的dictionary，可能包含如下键(key)：</p>
<p>n&nbsp; min_request_interval：这个键所对应的值是一个整数，该整数指定两个scraping操作之间的最小间隔秒数。发送该键(key)的知名Tracker是BNBT。使用该键(key)的知名客户端是Azureus。</p>



<pre>
referer:http://www.cnblogs.com/MaxWoods/archive/2009/07/25/1530851.html
</pre>
