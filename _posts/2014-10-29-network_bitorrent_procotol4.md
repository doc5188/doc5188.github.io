---
layout: post
title: "BitTorrent协议规范(BitTorrent Protocol Specification)之Peer Wire协议(Peer Wire Protocol)-第四部分"
categories: 网络
tags: [bittorrent, p2p, dht]
date: 2014-10-29 11:39:01
---

<p>Peer wire protocol (TCP)<br />概述<br />peer(端)协议使片(piece)的交换变得容易，片的描述请参考元信息文件。</p>
<p>注意：原来的规范在描述peer协议时，也使用术语piece&#8220;(片)&#8221;，但是这不同于元信息文件里面的术语&#8220;piece(片)&#8221;，由于这个原因，在本规范中，将使用术语&#8220;块(block)&#8221;来描述peers(端)之间交换的数据。</p>
<p>一个客户端(client)必须维持其与每一个远程peer(端)连接的状态信息：</p>
<p>l&nbsp; choked: 远程peer(端)是否已经choke本客户端。当一个peer(端) choke本客户端后，它是在通知本客户端，除非它unchoke本客户端，否则它不会应答该客户端所发出的任何请求。本客户端也不应该试图向远程peer发送数据请求，并且应该认为所有没有应答的请求已经被远程peer丢弃。</p>
<p>l&nbsp; interested: 远程peer(端)是否对本客户端提供的数据感兴趣。这是远程peer在通知本客户端，当本客户端unchoke他们时，远程客户端将开始请求块(block)。</p>
<p>注意这也意味着本客户端需要记录它是否对远程peer(端)感兴趣，以及它是否choke/unchoke远程peer。因此真正的列表看起来像这样：</p>
<p>l&nbsp; am_choking: 本客户端正在choke远程peer。</p>
<p>l&nbsp; am_interested: 本客户端对远程peer感兴趣。</p>
<p>l&nbsp; peer_choking: 远程peer正choke本客户端。</p>
<p>l&nbsp; peer_interested: 远程peer对本客户端感兴趣。</p>
<p>客户端连接开始时状态是choke和not interested(不感兴趣)。换句话就是：</p>
<p>l&nbsp; am_choking = 1 </p>
<p>l&nbsp; am_interested = 0 </p>
<p>l&nbsp; peer_choking = 1 </p>
<p>l&nbsp; peer_interested = 0 </p>
<p>当一个客户端对一个远程peer感兴趣并且那个远程peer没有choke这个客户端，那么这个客户端就可以从远程peer下载块(block)。当一个客户端没有choke一个peer，并且那个peer对这个客户端这个感兴趣时，这个客户端就会上传块(block)。</p>
<p>客户端必须不断通知它的peers，它是否对它们感兴趣，这一点是很重要的。客户端和每个端的状态信息必须保持最新，即使本客户端被choke。这允许所有的peer知道，当它们unchoke该客户端后，该客户端是否开始下载(反之亦然)。</p>
<p>数据类型<br />如果没有用其他的方法指定，在peer wire协议中的所有整数都会编码为4个字节的大端(big-endian)值。这也包括在握手之后，所有报文(Message)的长度前缀。</p>
<p>报文流(Message flow)<br />(译者注：因为ICMP-Internet控制报文协议中的Message翻译成报文，同时IP/TCP层中传输的数据都翻译为数据报，应用层传输的数据都翻译成报文，因此在这里Message翻译成报文)</p>
<p>peer wire协议由一个初始的握手组成。握手之后，peers通过以长度为前缀消息的交换进行通信。长度前缀就是上面描述的整数。</p>
<p>握手(HandShake)<br />握手是一个必需的报文，并且必须是客户端发送的第一个报文。该握手报文的长度是(49+len(pstr))字节。</p>
<p>握手：handshake: &lt;pstrlen&gt;&lt;pstr&gt;&lt;reserved&gt;&lt;info_hash&gt;&lt;peer_id&gt;</p>
<p>l&nbsp; pstrlen: &lt;pstr&gt;的字符串长度，单个字节。</p>
<p>l&nbsp; pstr: 协议的标识符，字符串类型。</p>
<p>l&nbsp; reserved: 8个保留字节。当前的所有实现都使用全0.这些字节里面的每一个字节都可以用来改变协议的行为。来自Bram的邮件建议应该首先使用后面的位，以便可以使用前面的位来改变后面位的意义。</p>
<p>l&nbsp; info_hash: 元信息文件中info键(key)对应值的20字节SHA1哈希。这个info_hash和在tracker请求中info_hash是同一个。 </p>
<p>l&nbsp; peer_id: 用于唯一标识客户端的20字节字符串。这个peer_id通常跟在tracker请求中传送的peer_id相同(但也不尽然，例如在Azureus，就有一个匿名选项)。 </p>
<p>在BitTorrent协议1.0版本，pstrlen = 19, pstr = &#8220;BitTorrent protocol&#8221;。</p>
<p>连接的发起者应该立即发送握手报文。如果接收方能够同时地服务多个torrent，它会等待发起者的握手报文(torrent由infohash唯一标识)。尽管如此，一旦接收方看到握手报文中的info_hash部分，接收方必须尽快响应。tracker的NAT-checking特性不会发送握手报文的peer_id字段。</p>
<p>如果一个客户端接收到一个握手报文，并且该客户端没有服务这个报文的info_hash，那么该客户端必须丢弃该连接。</p>
<p>如果一个连接发起者接收到一个握手报文，并且该报文中peer_id与期望的peer_id不匹配，那么连接发起者应该丢弃该连接。注意发起者可能接收来自tracker的peer信息，该信息包含peer注册的peer_id。来自于tracker的peer_id需要匹配握手报文中的peer_id。</p>
<p>peer_id<br />peer_id长20个字节。至于怎么将客户端和客户端版本信息编码成peer_id，现在主要有两种惯例：Azureus风格和Shadow风格。</p>
<p>Azureus风格使用如下编码方式：&#8217;-&#8217;, 紧接着是2个字符的client id，再接着是4个数字的版本号，&#8217;-&#8217;，后面跟着随机数。</p>
<p>例如：'-AZ2060-'...</p>
<p>使用这种编码风格的知名客户端是：</p>
<p>l&nbsp; 'AG' - Ares </p>
<p>l&nbsp; 'A~' - Ares </p>
<p>l&nbsp; 'AR' - Arctic </p>
<p>l&nbsp; 'AT' - Artemis </p>
<p>l&nbsp; 'AX' - BitPump </p>
<p>l&nbsp; 'AZ' - Azureus </p>
<p>l&nbsp; 'BB' - BitBuddy </p>
<p>l&nbsp; 'BC' - BitComet </p>
<p>l&nbsp; 'BF' - Bitflu </p>
<p>l&nbsp; 'BG' - BTG (uses Rasterbar libtorrent) </p>
<p>l&nbsp; 'BP' - BitTorrent Pro (Azureus + spyware) </p>
<p>l&nbsp; 'BR' - BitRocket </p>
<p>l&nbsp; 'BS' - BTSlave </p>
<p>l&nbsp; 'BW' - BitWombat </p>
<p>l&nbsp; 'BX' - ~Bittorrent X </p>
<p>l&nbsp; 'CD' - Enhanced CTorrent </p>
<p>l&nbsp; 'CT' - CTorrent </p>
<p>l&nbsp; 'DE' - DelugeTorrent </p>
<p>l&nbsp; 'DP' - Propagate Data Client </p>
<p>l&nbsp; 'EB' - EBit </p>
<p>l&nbsp; 'ES' - electric sheep </p>
<p>l&nbsp; 'FC' - FileCroc </p>
<p>l&nbsp; 'FT' - FoxTorrent </p>
<p>l&nbsp; 'GS' - GSTorrent </p>
<p>l&nbsp; 'HL' - Halite </p>
<p>l&nbsp; 'HN' - Hydranode </p>
<p>l&nbsp; 'KG' - KGet </p>
<p>l&nbsp; 'KT' - KTorrent </p>
<p>l&nbsp; 'LC' - LeechCraft </p>
<p>l&nbsp; 'LH' - LH-ABC </p>
<p>l&nbsp; 'LP' - Lphant </p>
<p>l&nbsp; 'LT' - libtorrent </p>
<p>l&nbsp; 'lt' - libTorrent </p>
<p>l&nbsp; 'LW' - LimeWire </p>
<p>l&nbsp; 'MO' - MonoTorrent </p>
<p>l&nbsp; 'MP' - MooPolice </p>
<p>l&nbsp; 'MR' - Miro </p>
<p>l&nbsp; 'MT' - MoonlightTorrent </p>
<p>l&nbsp; 'NX' - Net Transport </p>
<p>l&nbsp; 'OT' - OmegaTorrent </p>
<p>l&nbsp; 'PD' - Pando </p>
<p>l&nbsp; 'qB' - qBittorrent </p>
<p>l&nbsp; 'QD' - QQDownload </p>
<p>l&nbsp; 'QT' - Qt 4 Torrent example </p>
<p>l&nbsp; 'RT' - Retriever </p>
<p>l&nbsp; 'RZ' - RezTorrent </p>
<p>l&nbsp; 'S~' - Shareaza alpha/beta </p>
<p>l&nbsp; 'SB' - ~Swiftbit </p>
<p>l&nbsp; 'SS' - SwarmScope </p>
<p>l&nbsp; 'ST' - SymTorrent </p>
<p>l&nbsp; 'st' - sharktorrent </p>
<p>l&nbsp; 'SZ' - Shareaza </p>
<p>l&nbsp; 'TN' - TorrentDotNET </p>
<p>l&nbsp; 'TR' - Transmission </p>
<p>l&nbsp; 'TS' - Torrentstorm </p>
<p>l&nbsp; 'TT' - TuoTu </p>
<p>l&nbsp; 'UL' - uLeecher! </p>
<p>l&nbsp; 'UM' - &#181;Torrent for Mac </p>
<p>l&nbsp; 'UT' - &#181;Torrent </p>
<p>l&nbsp; 'VG' - Vagaa </p>
<p>l&nbsp; 'WT' - BitLet </p>
<p>l&nbsp; 'WY' - FireTorrent </p>
<p>l&nbsp; 'XL' - Xunlei </p>
<p>l&nbsp; 'XT' - XanTorrent </p>
<p>l&nbsp; 'XX' - Xtorrent </p>
<p>l&nbsp; 'ZT' - ZipTorrent </p>
<p>另外还需要识别的客户端有：</p>
<p>l&nbsp; 'BD' (例如: -BD0300-) </p>
<p>l&nbsp; 'NP' (例如: -NP0201-) </p>
<p>l&nbsp; 'SD' (例如: -SD0100-) </p>
<p>l&nbsp; 'wF' (例如: -wF2200-) </p>
<p>l&nbsp; 'hk' (例如: -hk0010-) 中国IP地址，IP address, unrequestedly sends info dict in message 0xA, reconnects immediately after being disconnected, reserved bytes = 01,01,01,01,00,00,02,01</p>
<p>Shadow风格使用如下编码方式：一个用于客户端标识的ASCII字母数字，多达五个字符的版本号(如果少于5个，则以&#8217;-&#8217;填充)，紧接着是3个字符(通常是&#8217;---&#8217;，但也不总是这样)，最后跟着随机数。版本字符串中的每一个字符表示一个0到63的数字。'0'=0, ..., '9'=9, 'A'=10, ..., 'Z'=35, 'a'=36, ..., 'z'=61, '.'=62, '-'=63。</p>
<p>你可以在这找到关于shadow编码风格(包含关于版本字符串后的三个字符用法的习惯)的详细说明。</p>
<p>例如：用于Shadow 5.8.11的&#8217;S58B-----&#8216;...</p>
<p>使用这种编码风格的知名客户端是：</p>
<p>l&nbsp; 'A' - ABC </p>
<p>l&nbsp; 'O' - Osprey Permaseed </p>
<p>l&nbsp; 'Q' - BTQueue </p>
<p>l&nbsp; 'R' - Tribler </p>
<p>l&nbsp; 'S' - Shadow's client </p>
<p>l&nbsp; 'T' - BitTornado </p>
<p>l&nbsp; 'U' - UPnP NAT Bit Torrent </p>
<p>Bram的客户端现在使用这种风格：'M3-4-2--' or 'M4-20-8-'。</p>
<p>BitComet使用不同的编码风格。它的peer_id由4个ASCII字符&#8217;exbc&#8217;组成，接着是2个字节的x和y，最后是随机字符。版本号中的x在小数点前面，y是版本号后的两个数字。BitLord使用相同的方案，但是在版本号后面添加&#8217;LORD&#8217;。BitComet的一个非正式补丁曾经使用&#8217;FUTB&#8217;代替&#8217;exbc&#8217;。自版本0.59开始，BitComet peer id的编码使用Azureus风格。</p>
<p>XBT客户端也使用其特有的风格。它的peer_id由三个大写字母&#8217;XBT&#8217;以及紧随其后的代表版本号的三个ASCII数字组成。如果客户端是debug版本，第七个字节是小写字符&#8217;d&#8217;，否则就是&#8217;-&#8216;。接着就是&#8217;-&#8216;，然后是随机数，大写和小写字母。例如：peer_id的开始部分为'XBT054d-'表明该客户端是版本号为0.5.4的debug版本。</p>
<p>Opera 8预览版和Opera 9.x发行版使用以下的peer_id方案：开始的两个字符是&#8217;OP&#8217;，后面的四个数字是开发代号。接着的字符是随机的小写十六进制数字。</p>
<p>MLdonkey使用如下的peer_id方案：开始的字符是&#8217;-ML&#8217;，后面跟着点式版本，然后就是一个&#8217;-&#8217;，最后跟着随机字符串。例如：'-ML2.7.2-kgjjfkd'。</p>
<p>Bit on Wheels使用模式'-BOWxxx-yyyyyyyyyyyy'，其中y是随机的(大写字母)，x依赖于版本。如果版本为1.0.6，那么xxx = AOC。</p>
<p>Queen Bee使用Bram的新风格：'Q1-0-0--' or 'Q1-10-0-'之后紧随着随机字节。</p>
<p>BitTyrant是Azureus的一个分支，在它的1.1版本，其peer id使用'AZ2500BT' + 随机字节的方式。</p>
<p>TorrenTopia版本1.90自称是或源自于Mainline 3.4.6。它的peer ID以'346------'开始。</p>
<p>BitSpirit有几种编码peer ID的方式。一种模式是读取它的peer ID然后使用开始的八个字节作为它peer ID的基础来重新连接。它的实际ID使用'\0\3BS'(c 标记法)作为版本3.x的前四个字节，使用'\0\2BS'作为版本2.x的前四个字节。所有方式都使用'UDP0'作为结尾。</p>
<p>Rufus使用它的十进制ASCII版本值作为开始的两个字节。第三个和第四个字节是'RS'。紧随其后的是用户的昵称和一些随机字节。</p>
<p>C3 Torrent的peer ID以&#8217;-G3&#8217;开始，然后追加多达9个表示用户昵称的字符。</p>
<p>FlashGet使用Azureus风格，但是前面字符是&#8217;FG&#8217;，没有&#8217;-&#8217;。版本 1.82.1002 仍然使用版本数字 '0180'。</p>
<p>BT Next Evolution源自于BitTornado，但是试着模仿Azureus风格。结果是它的peer ID以&#8217;-NE&#8217;开始，接着是四个数字的版本号，最后就是以shadow peer id风格描述客户端类型的三个字符。</p>
<p>AllPeers takes the sha1 hash of a user dependent string(这个不好翻译，待译)，使用"AP" + version string + "-"代替开始的一些字符。</p>
<p>Qvod的id以四个字母"QVOD"开始，接着是4个十进制数字的开发代号(目前是&#8221; 0054&#8221;)。最后的12个字符是随机的大写十六进制数字。中国有一个修改版，该版本以随机字节代替前四个字符。</p>
<p>许多客户端全部使用随机数或者随机数后面跟12个全0(像Bram客户端的老版本)。</p>
<p>报文(Messages)<br />接下来协议的所有报文采用如下的结构：&lt;length prefix&gt;&lt;message ID&gt;&lt;payload&gt;。length prefix(长度前缀)是一个4字节的大端(big-endian)值。message ID是单个十进制值。playload与消息相关。</p>
<p>l&nbsp; keep-alive: &lt;len=0000&gt;</p>
<p>keep-alive消息是一个0字节的消息，将length prefix设置成0。没有message ID和payload。如果peers在一个固定时间段内没有收到任何报文(keep-alive或其他任何报文)，那么peers应该关掉这个连接，因此如果在一个给定的时间内没有发出任何命令的话，peers必须发送一个keep-alive报文保持这个连接激活。通常情况下，这个时间是2分钟。</p>
<p>l&nbsp; choke: &lt;len=0001&gt;&lt;id=0&gt;</p>
<p>choke报文长度固定，并且没有payload。</p>
<p>l&nbsp; unchoke: &lt;len=0001&gt;&lt;id=1&gt; </p>
<p>unchoke报文长度固定，并且没有payload。</p>
<p>l&nbsp; interested: &lt;len=0001&gt;&lt;id=2&gt; </p>
<p>interested报文长度固定，并且没有payload。</p>
<p>l&nbsp; not interested: &lt;len=0001&gt;&lt;id=3&gt; </p>
<p>not interested报文长度固定，并且没有payload。</p>
<p>l&nbsp; have: &lt;len=0005&gt;&lt;id=4&gt;&lt;piece index&gt; </p>
<p>have报文长度固定。payload是piece(片)的从零开始的索引，该片已经成功下载并且通过hash校验。</p>
<p>实现者注意：实际上，一些客户端必须严格实现该定义。因为peers不太可能下载他们已经拥有的piece(片)，一个peer不应该通知另一个peer它拥有一个piece(片)，如果另一个peer拥有这个piece(片)。最低限度&#8221;HAVE suppresion&#8221;会使用have报文数量减半，总的来说，大致减少25-35%的HAVE报文。同时，给一个拥有piece(片)的peer发送HAVE报文是值得的，因为这有助于决定哪个piece是稀缺的。</p>
<p>一个恶意的peer可能向其他的peer广播它们不可能下载的piece(片)。Due to this attempting to model peers using this information is a bad idea. </p>
<p>l&nbsp; bitfield: &lt;len=0001+X&gt;&lt;id=5&gt;&lt;bitfield&gt; </p>
<p>bitfield报文可能仅在握手序列发送之后，其他消息发送之前立即发送。它是可选的，如果一个客户端没有piece(片)，就不需要发送该报文。</p>
<p>bitfield报文长度可变，其中x是bitfield的长度。payload是一个bitfield，该bitfield表示已经成功下载的piece(片)。第一个字节的高位相当于piece索引0。设置为0的位表示一个没有的piece，设置为1的位表示有效的和可用的piece。末尾的冗余位设置为0。</p>
<p>长度不对的bitfield将被认为是一个错误。如果客户端接收到长度不对的bitfield或者bitfield有任一冗余位集，它应该丢弃这个连接。</p>
<p>l&nbsp; request: &lt;len=0013&gt;&lt;id=6&gt;&lt;index&gt;&lt;begin&gt;&lt;length&gt; </p>
<p>request报文长度固定，用于请求一个块(block)。payload包含如下信息：</p>
<p>n&nbsp; index: 整数，指定从零开始的piece索引。</p>
<p>n&nbsp; begin: 整数，指定piece中从零开始的字节偏移。</p>
<p>n&nbsp; length: 整数，指定请求的长度。</p>
<p>l&nbsp; piece: &lt;len=0009+X&gt;&lt;id=7&gt;&lt;index&gt;&lt;begin&gt;&lt;block&gt;</p>
<p>piece报文长度可变，其中x是块的长度。payload包含如下信息：</p>
<p>n&nbsp; index: 整数，指定从零开始的piece索引。</p>
<p>n&nbsp; begin: 整数，指定piece中从零开始的字节偏移。</p>
<p>n&nbsp; block: 数据块，它是由索引指定的piece的子集。</p>
<p>l&nbsp; cancel: &lt;len=0013&gt;&lt;id&lt;=8&gt;&lt;index&gt;&lt;begin&gt;&lt;length&gt;</p>
<p>cancel报文长度固定，用于取消块请求。playload与request报文的playload相同。一般情况下用于结束下载。</p>
<p>l&nbsp; port: &lt;len=0003&gt;&lt;id=9&gt;&lt;listen-port&gt; </p>
<p>port报文由新版本的Mainline发送，新版本Mainline实现了一个DHT tracker。该监听端口是peer的DHT节点正在监听的端口。这个peer应该插入本地路由表(如果支持DHT tracker的话)。</p>
