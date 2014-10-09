---
layout: post
title: "python开发的 dht网络爬虫" 
categories: python 
tags: [python, dht爬虫, dht采集]
date: 2014-10-09 12:08:50
---
<div class="BlogContent"><p>使用 libtorrent 的python绑定库实现一个dht网络爬虫，抓取dht网络中的磁力链接。</p> 
<p><br></p> 
<span id="OSC_h2_1"></span>
<h2>dht 网络简介</h2> 
<span id="OSC_h3_2"></span>
<h3>p2p网络</h3> 
<p>在P2P网络中，通过种子文件下载资源时，要知道资源在P2P网络中哪些计算机中，这些传输资源的计算机称作peer。在传统的P2P网络中，使用tracker服务器跟踪资源的peer。要下载资源，首先需要取得这些peer。</p> 
<p><br></p> 
<span id="OSC_h3_3"></span>
<h3>dht网络</h3> 
<p>tracker服务器面临一些版权和法律问题。于是出现了DHT，它把tracker上的资源peer信息分散到了整个网络中。dht网络是由分布 式节点构成，节点(node)是实现了DHT协议的p2p客户端。P2P客户端程序既是peer也是node。DHT网络有多种算法，常用的有 Kademlia。</p> 
<p><br></p> 
<span id="OSC_h3_4"></span>
<h3>dht网络下载</h3> 
<p>P2P客户端使用种子文件下载资源时，如果没有tracker服务器，它就向DHT网络查询资源的peer列表， 然后从peer下载资源。</p> 
<p><br></p> 
<span id="OSC_h3_5"></span>
<h3>Magnet是磁力链接</h3> 
<p>资源的标识在DHT网络中称为infohash，是一个通过sha1算法得到的20字节长的字符串。infohash是使用种子文件的文件描述信息 计算得到。磁力链接是把infohash编码成16进制字符串得到。P2P客户端使用磁力链接，下载资源的种子文件，然后根据种子文件下载资源。</p> 
<p><br></p> 
<span id="OSC_h3_6"></span>
<h3>Kademlia 算法</h3> 
<p>Kademlia是DHT网络的一种实现， 具体的算法参见：<a href="http://www.bittorrent.org/beps/bep_0005.html" rel="nofollow">DHT协议</a></p> 
<p><br></p> 
<span id="OSC_h3_7"></span>
<h3>KRPC 协议</h3> 
<p>KRPC 是节点之间的交互协议，使用UDP来传送。</p> 
<p>包括4种请求：ping，find_node，get_peer，announce_peer。其中get_peer和announce_peer是节点间查询资源的主要消息。</p> 
<p><br></p> 
<span id="OSC_h3_8"></span>
<h3>dht 爬虫原理</h3> 
<p>主要的思路就是伪装为p2p客户端，加入dht网络，收集dht网络中的get_peer和announce_peer消息，这些消息是其他node发送给伪装的p2p客户端的udp消息。</p> 
<p><br></p> 
<span id="OSC_h2_9"></span>
<h2>本文dht爬虫的实现</h2> 
<span id="OSC_h3_10"></span>
<h3>爬虫运行环境</h3> 
<ol> 
 <li><p>linux 系统</p></li> 
 <li><p>python 2.7</p></li> 
 <li><p>libtorrent 库的python绑定</p></li> 
 <li><p>twisted 网络库</p></li> 
 <li><p>防火墙开启固定的udp和tcp端口</p></li> 
</ol> 
<p><br></p> 
<span id="OSC_h3_11"></span>
<h3>libtorrent 库的介绍</h3> 
<p>libtorrent库是p2p下载的客户端库，有丰富的接口，可以用来开发下载p2p网络上的资源。它有python的绑定库，本爬虫就是使用它的python库开发的。</p> 
<p>在libtorrent中有几个概念需要解释下。 session 相当于p2p客户端，session开启一个tcp和一个udp端口，用来与其他p2p客户端交换数据。可以在一个进程内定义多个session，也就是多个p2p客户端，来加快收集速度。</p> 
<p>alert是libtorrent中用来收集各种消息的队列，每个session都有一个自己的alert消息队列。KRPC协议的get_peer和announce_peer消息也是从这个队列中获取，就是用这两个消息收集磁力链接的。</p> 
<p><br></p> 
<span id="OSC_h3_12"></span>
<h3>主要实现代码</h3> 
<p>爬虫实现的主要代码比较简单</p> 
<pre>#&nbsp;事件通知处理函数
&nbsp;&nbsp;&nbsp;&nbsp;def&nbsp;_handle_alerts(self,&nbsp;session,&nbsp;alerts):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;while&nbsp;len(alerts):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;alert&nbsp;=&nbsp;alerts.pop()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;获取dht_announce_alert和dht_get_peer_alert消息
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;从这两消息收集磁力链接
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;isinstance(alert,&nbsp;lt.add_torrent_alert):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;alert.handle.set_upload_limit(self._torrent_upload_limit)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;alert.handle.set_download_limit(self._torrent_download_limit)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;elif&nbsp;isinstance(alert,&nbsp;lt.dht_announce_alert):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;info_hash&nbsp;=&nbsp;alert.info_hash.to_string().encode('hex')
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;info_hash&nbsp;in&nbsp;self._meta_list:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._meta_list[info_hash]&nbsp;+=&nbsp;1
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;else:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._meta_list[info_hash]&nbsp;=&nbsp;1
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._current_meta_count&nbsp;+=&nbsp;1
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;elif&nbsp;isinstance(alert,&nbsp;lt.dht_get_peers_alert):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;info_hash&nbsp;=&nbsp;alert.info_hash.to_string().encode('hex')
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;info_hash&nbsp;in&nbsp;self._meta_list:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._meta_list[info_hash]&nbsp;+=&nbsp;1
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;else:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._infohash_queue_from_getpeers.append(info_hash)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._meta_list[info_hash]&nbsp;=&nbsp;1
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._current_meta_count&nbsp;+=&nbsp;1

&nbsp;&nbsp;&nbsp;&nbsp;def&nbsp;start_work(self):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'''主工作循环，检查消息，显示状态'''
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;清理屏幕
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;begin_time&nbsp;=&nbsp;time.time()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_interval&nbsp;=&nbsp;self._delay_interval
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;while&nbsp;True:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for&nbsp;session&nbsp;in&nbsp;self._sessions:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;session.post_torrent_updates()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;从队列中获取信息
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._handle_alerts(session,&nbsp;session.pop_alerts())
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;time.sleep(self._sleep_time)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;show_interval&nbsp;&gt;&nbsp;0:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_interval&nbsp;-=&nbsp;1
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;continue
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_interval&nbsp;=&nbsp;self._delay_interval

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;统计信息显示
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content&nbsp;=&nbsp;['torrents:']
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;interval&nbsp;=&nbsp;time.time()&nbsp;-&nbsp;begin_time
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;pid:&nbsp;%s'&nbsp;%&nbsp;os.getpid())
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;time:&nbsp;%s'&nbsp;%
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;time.strftime('%Y-%m-%d&nbsp;%H:%M:%S'))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;run&nbsp;time:&nbsp;%s'&nbsp;%&nbsp;self._get_runtime(interval))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;start&nbsp;port:&nbsp;%d'&nbsp;%&nbsp;self._start_port)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;collect&nbsp;session&nbsp;num:&nbsp;%d'&nbsp;%
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;len(self._sessions))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;info&nbsp;hash&nbsp;nums&nbsp;from&nbsp;get&nbsp;peers:&nbsp;%d'&nbsp;%
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;len(self._infohash_queue_from_getpeers))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;torrent&nbsp;collection&nbsp;rate:&nbsp;%f&nbsp;/minute'&nbsp;%
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(self._current_meta_count&nbsp;*&nbsp;60&nbsp;/&nbsp;interval))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;current&nbsp;torrent&nbsp;count:&nbsp;%d'&nbsp;%
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._current_meta_count)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('&nbsp;&nbsp;total&nbsp;torrent&nbsp;count:&nbsp;%d'&nbsp;%
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;len(self._meta_list))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show_content.append('\n')

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;存储运行状态到文件
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;try:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with&nbsp;open(self._stat_file,&nbsp;'wb')&nbsp;as&nbsp;f:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;f.write('\n'.join(show_content))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with&nbsp;open(self._result_file,&nbsp;'wb')&nbsp;as&nbsp;f:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;json.dump(self._meta_list,&nbsp;f)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;except&nbsp;Exception&nbsp;as&nbsp;err:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pass

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;测试是否到达退出时间
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;interval&nbsp;&gt;=&nbsp;self._exit_time:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;stop
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;每天结束备份结果文件
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self._backup_result()

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;销毁p2p客户端
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for&nbsp;session&nbsp;in&nbsp;self._sessions:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;torrents&nbsp;=&nbsp;session.get_torrents()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for&nbsp;torrent&nbsp;in&nbsp;torrents:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;session.remove_torrent(torrent)</pre> 
<p><br></p> 
<span id="OSC_h3_13"></span>
<h3>运行效率</h3> 
<p>在我的一台512M内存，单cpu机器上。爬虫刚开始运行稍慢，运行几分钟后收集速度稳定在 180个每分钟，1小时采集10000左右。</p> 
<p>运行状态</p> 
<pre>run&nbsp;times:&nbsp;12

torrents:
&nbsp;&nbsp;pid:&nbsp;11480&nbsp;&nbsp;time:&nbsp;2014-08-18&nbsp;22:45:01
&nbsp;&nbsp;run&nbsp;time:&nbsp;day:&nbsp;0,&nbsp;hour:&nbsp;0,&nbsp;minute:&nbsp;12,&nbsp;second:&nbsp;25
&nbsp;&nbsp;start&nbsp;port:&nbsp;32900
&nbsp;&nbsp;collect&nbsp;session&nbsp;num:&nbsp;20
&nbsp;&nbsp;info&nbsp;hash&nbsp;nums&nbsp;from&nbsp;get&nbsp;peers:&nbsp;2222
&nbsp;&nbsp;torrent&nbsp;collection&nbsp;rate:&nbsp;179.098480&nbsp;/minute
&nbsp;&nbsp;current&nbsp;torrent&nbsp;count:&nbsp;2224
&nbsp;&nbsp;total&nbsp;torrent&nbsp;count:&nbsp;58037</pre> 
<p><br></p> 
<span id="OSC_h3_14"></span>
<h3>爬虫完整代码</h3> 
<p>完整的代码参见：<a href="https://github.com/blueskyz/DHTCrawler" rel="nofollow">https://github.com/blueskyz/DHTCrawler</a></p> 
<p>还包括一个基于twisted的监控进程，用来查看爬虫状态，在爬虫进程退出后重新启动。</p> 
<p><br></p> 
<p>原文链接：http://www.hopez.org/blog/9/1408369618<br></a></p> 
<p><br></p></div>
