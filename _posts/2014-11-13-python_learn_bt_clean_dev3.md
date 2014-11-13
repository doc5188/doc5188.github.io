---
layout: post
title: "Python边学边用--BT客户端实现之(三)Peer协议设计"
categories: python
tags: [python, bt开发, dht开发, 系列教程]
date: 2014-11-13 11:45:01
---

<p>与peer建立tcp连接后，首先发送handshake消息进行握手</p>
<p>handshake消息格式如下：</p>
<p>一个字节0x19 + 一个字符串'<span>BitTorrent protocol' + 8 byte 保留字节默认值为0（draft中对保留字节有定义）</span></p>
<p><span>+ 种子文件中info 部分的sha1字，大小为20个字节 + 20个自己的peer id（从tracker获取到的peer信息大多没有peerid，这个可以使用本地的peer id）</span></p>
<p><span>如果handshake信息协商不上，tcp连接将被关闭。</span></p>
<p><span>&nbsp;</span></p>
<p>BT标准BEP-3中定义了8种peer消息：消息格式为msg_len(4个字节) + msg_type(1一个字节) + payload</p>
<p>0 - choke &nbsp;--发送该消息表示本段发送阻塞，对端将不能获取到piece数据，payload 为 0</p>
<p>1 - unchoke &nbsp;--发送该消息表示解阻塞，对端可以开始发送请求获取piece数据，payload 为 0</p>
<p>2 - interested &nbsp;--发送该消息，表示对对端的pieces数据有兴趣，payload 为 0</p>
<p>3 - not interested &nbsp;---发送该消息，表示对对端的pieces数据没有兴趣了，payload 为 0</p>
<p>4 - have &nbsp; &nbsp; &nbsp;&nbsp;---发送该消息，通告对端 本段拥有的pieces，payload为4个字节的piece index</p>
<p>5 - bitfield&nbsp;&nbsp;---发送该消息，通告对端 本段拥有的pieces，为bit map的方式表示每个piece index在本端是否拥有。piece index所在bit位为1，表示拥有。</p>
<p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;该消息为handshake成功后的第一个消息。</p>
<p>6 - request &nbsp; ---piece请求消息，payload为：<span>&nbsp;index, begin, and length，都是4个字节表示，length一般实现为0x8000, 最大不能超过0x20000。</span></p>
<p>7 - piece &nbsp; &nbsp; ---piece &nbsp;数据，payload为：&nbsp;index, begin,data&nbsp;</p>
<p>8 - cancel &nbsp; &nbsp;---发送该消息，表示本端取消了某个piece请求。payload为：index, begin, and length</p>
<p>&nbsp;</p>
<p>使用python的异步socket接口实现，为了减少处理过程被socket阻塞，使用多个线程处理每个peer。</p>
<p>每个peer包括3个线程：request timeout timer ，socket send data thread， socket receive data thread，使用select 函数判断socket是否可读、可写。</p>
<p>对socket读写操作时使用RLock进行保护，select阻塞进程时不加锁，避免阻塞其他线程。</p>
<p>发送数据数据时先写一个队列，然后通过set threading.Event 变量出发socket send data thread发送数据，保证发送数据的线程不阻塞</p>
<p>由于 python没有结束线程的接口，socket send data thread， socket receive data thread 需要依赖特殊变量的赋值，使socket处理进程结束。</p>
<p>使用同步调用来触发下载过程运转，尽量不使用timer轮询的方式，可以降低cpu使用率并加快下载过程。</p>
<p>但是，多线程间的同步调用由于锁的存在，会导致性能下降并容易引入信号量死锁的问题。需要仔细设计好多线程的运行轨迹避免死锁。</p>
<p>draft BEP中定义的功能暂未实现，peer的上传流控未实现，peer质量分级未实现。</p>
<div class="cnblogs_code" onclick="cnblogs_code_show('49d4de56-6506-4d99-96d6-7fdc4477fde9')"><img id="code_img_closed_49d4de56-6506-4d99-96d6-7fdc4477fde9" class="code_img_closed" src="http://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif" alt="" /><img id="code_img_opened_49d4de56-6506-4d99-96d6-7fdc4477fde9" class="code_img_opened" style="display: none;" onclick="cnblogs_code_hide('49d4de56-6506-4d99-96d6-7fdc4477fde9',event)" src="http://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif" alt="" /><span class="cnblogs_code_collapse">PeerConnect</span>
<div id="cnblogs_code_open_49d4de56-6506-4d99-96d6-7fdc4477fde9" class="cnblogs_code_hide">
<pre><span style="color: #008080;">  1</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  2</span> <span style="color: #800000;">Created on 2012-10-3
</span><span style="color: #008080;">  3</span> 
<span style="color: #008080;">  4</span> <span style="color: #800000;">@author: ddt
</span><span style="color: #008080;">  5</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  6</span> <span style="color: #0000ff;">from</span> socket <span style="color: #0000ff;">import</span> *
<span style="color: #008080;">  7</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> threading
</span><span style="color: #008080;">  8</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> log_info
</span><span style="color: #008080;">  9</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> select
</span><span style="color: #008080;"> 10</span> 
<span style="color: #008080;"> 11</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> PeerConnect(object):
</span><span style="color: #008080;"> 12</span>     <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 13</span> <span style="color: #800000;">    TODO: upload flow control
</span><span style="color: #008080;"> 14</span> <span style="color: #800000;">    TODO: peer quality management
</span><span style="color: #008080;"> 15</span>     <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 16</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__init__</span><span style="color: #000000;">(self, ip, port, task_info):
</span><span style="color: #008080;"> 17</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 18</span> <span style="color: #800000;">        Constructor
</span><span style="color: #008080;"> 19</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 20</span>         self.<span style="color: #800080;">__ip</span> =<span style="color: #000000;"> ip
</span><span style="color: #008080;"> 21</span>         self.<span style="color: #800080;">__port</span> =<span style="color: #000000;"> port
</span><span style="color: #008080;"> 22</span>         
<span style="color: #008080;"> 23</span>         self.<span style="color: #800080;">__info_hash</span> =<span style="color: #000000;"> task_info.get_info_hash()
</span><span style="color: #008080;"> 24</span>         self.<span style="color: #800080;">__local_id</span> =<span style="color: #000000;"> task_info.get_local_id()
</span><span style="color: #008080;"> 25</span>         self.<span style="color: #800080;">__task_info</span> =<span style="color: #000000;"> task_info
</span><span style="color: #008080;"> 26</span>         
<span style="color: #008080;"> 27</span>         leading_string = chr(19)+<span style="color: #800000;">'</span><span style="color: #800000;">BitTorrent protocol</span><span style="color: #800000;">'</span>
<span style="color: #008080;"> 28</span>         reserved_string = chr(0)*8
<span style="color: #008080;"> 29</span>         self.<span style="color: #800080;">__handshake_info</span> = leading_string +<span style="color: #000000;"> reserved_string 
</span><span style="color: #008080;"> 30</span>         self.<span style="color: #800080;">__handshake_info</span> += self.<span style="color: #800080;">__info_hash</span> + self.<span style="color: #800080;">__local_id</span>
<span style="color: #008080;"> 31</span>     
<span style="color: #008080;"> 32</span>         self.<span style="color: #800080;">__request_piece_len</span> = 0x4000
<span style="color: #008080;"> 33</span>         self.<span style="color: #800080;">__receive_data_len</span> = 0x8000
<span style="color: #008080;"> 34</span>         
<span style="color: #008080;"> 35</span>         self.<span style="color: #800080;">__tcp_con</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 36</span>         self.<span style="color: #800080;">__tcp_connect_timeout</span> = 60
<span style="color: #008080;"> 37</span>         
<span style="color: #008080;"> 38</span>         self.<span style="color: #800080;">__tcp_handshake_timeout</span> = 60
<span style="color: #008080;"> 39</span>         
<span style="color: #008080;"> 40</span>         self.<span style="color: #800080;">__keepalive_timer</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 41</span>         self.<span style="color: #800080;">__sck_send_thread</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 42</span>         
<span style="color: #008080;"> 43</span>         self.<span style="color: #800080;">__retry_timer</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 44</span>         self.<span style="color: #800080;">__retry_intvl</span> = 2 <span style="color: #008000;">#</span><span style="color: #008000;"> second</span>
<span style="color: #008080;"> 45</span>         self.<span style="color: #800080;">__retry_times</span> =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 46</span>         self.<span style="color: #800080;">__max_retrys</span> = 10
<span style="color: #008080;"> 47</span>         
<span style="color: #008080;"> 48</span>         self.<span style="color: #800080;">__local_choked</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;"> 49</span>         self.<span style="color: #800080;">__peer_choked</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;"> 50</span>         self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;"> 51</span>         self.<span style="color: #800080;">__peer_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;"> 52</span>         
<span style="color: #008080;"> 53</span>         self.<span style="color: #800080;">__peer_have_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 54</span> 
<span style="color: #008080;"> 55</span>     
<span style="color: #008080;"> 56</span>         self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> False;
</span><span style="color: #008080;"> 57</span>         self.<span style="color: #800080;">__local_requesting_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 58</span>         self.<span style="color: #800080;">__local_max_requesting</span> = 10
<span style="color: #008080;"> 59</span>         self.<span style="color: #800080;">__local_requesting_timer</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 60</span>         self.<span style="color: #800080;">__local_requesting_timeout_intvl</span> = 30
<span style="color: #008080;"> 61</span>             
<span style="color: #008080;"> 62</span>         self.<span style="color: #800080;">__receiving_cache</span> = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 63</span>     
<span style="color: #008080;"> 64</span>         self.<span style="color: #800080;">__peer_pending_request</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 65</span>         self.<span style="color: #800080;">__local_pending_request</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 66</span>         
<span style="color: #008080;"> 67</span>         self.<span style="color: #800080;">__local_pending_request_less</span> = 10
<span style="color: #008080;"> 68</span>         self.<span style="color: #800080;">__peer_have_pieces_pending</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 69</span>         
<span style="color: #008080;"> 70</span>         self.<span style="color: #800080;">__local_sending_queue</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 71</span>         self.<span style="color: #800080;">__rlock_sck_send</span> =<span style="color: #000000;"> threading.RLock() 
</span><span style="color: #008080;"> 72</span>         self.<span style="color: #800080;">__local_sending_event</span> =<span style="color: #000000;"> threading.Event()
</span><span style="color: #008080;"> 73</span>         self.<span style="color: #800080;">__min_sck_send_msg</span> = 0x1000
<span style="color: #008080;"> 74</span>         
<span style="color: #008080;"> 75</span>         self.<span style="color: #800080;">__rlock_common</span> =<span style="color: #000000;"> threading.RLock()
</span><span style="color: #008080;"> 76</span>         
<span style="color: #008080;"> 77</span>         self.<span style="color: #800080;">__peer_started</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;"> 78</span>         
<span style="color: #008080;"> 79</span>         self.<span style="color: #800080;">__peer_choked_timer</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 80</span>         self.<span style="color: #800080;">__peer_choked_timeout_intvl</span> = 180
<span style="color: #008080;"> 81</span>         
<span style="color: #008080;"> 82</span>         self.<span style="color: #800080;">__dispatch_timer</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 83</span>         self.<span style="color: #800080;">__dispatch_timeout</span> = 5
<span style="color: #008080;"> 84</span> 
<span style="color: #008080;"> 85</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> start(self):
</span><span style="color: #008080;"> 86</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 87</span>             <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__peer_started</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 88</span>                 self.<span style="color: #800080;">__retry_times</span> =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 89</span>                 self.<span style="color: #800080;">__startup_thread</span> = threading.Thread(target=PeerConnect.<span style="color: #800080;">__connect</span>,args=<span style="color: #000000;">(self,))
</span><span style="color: #008080;"> 90</span>                 self.<span style="color: #800080;">__peer_started</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;"> 91</span>                 self.<span style="color: #800080;">__startup_thread</span><span style="color: #000000;">.start()
</span><span style="color: #008080;"> 92</span>     
<span style="color: #008080;"> 93</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> stop(self):
</span><span style="color: #008080;"> 94</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 95</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_started</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 96</span>                 self.<span style="color: #800080;">__retry_times</span> = self.<span style="color: #800080;">__max_retrys</span>
<span style="color: #008080;"> 97</span>                 self.<span style="color: #800080;">__disconnect</span><span style="color: #000000;">()
</span><span style="color: #008080;"> 98</span>                 self.<span style="color: #800080;">__peer_started</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;"> 99</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">100</span> 
<span style="color: #008080;">101</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> dispatch_pieces(self,pieces, piece_len):
</span><span style="color: #008080;">102</span>         
<span style="color: #008080;">103</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">104</span>         
<span style="color: #008080;">105</span>             self.<span style="color: #800080;">__write_log</span><span style="color: #000000;">(str(pieces))
</span><span style="color: #008080;">106</span>             self.<span style="color: #800080;">__write_log</span>(str(self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">))
</span><span style="color: #008080;">107</span>             
<span style="color: #008080;">108</span>             <span style="color: #0000ff;">if</span> len(pieces) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">109</span>                 <span style="color: #0000ff;">return</span><span style="color: #000000;"> False
</span><span style="color: #008080;">110</span>             
<span style="color: #008080;">111</span>             <span style="color: #0000ff;">for</span> piece_index <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:
</span><span style="color: #008080;">112</span>                 <span style="color: #0000ff;">if</span> piece_index <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">:
</span><span style="color: #008080;">113</span>                     <span style="color: #0000ff;">return</span><span style="color: #000000;"> False 
</span><span style="color: #008080;">114</span>                  
<span style="color: #008080;">115</span>             <span style="color: #0000ff;">for</span> piece_index <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:       
</span><span style="color: #008080;">116</span>                 <span style="color: #0000ff;">for</span> offset <span style="color: #0000ff;">in</span> range(0, piece_len, self.<span style="color: #800080;">__request_piece_len</span><span style="color: #000000;">):
</span><span style="color: #008080;">117</span>                     length = self.<span style="color: #800080;">__request_piece_len</span>
<span style="color: #008080;">118</span>                     <span style="color: #0000ff;">if</span> offset+length &gt;<span style="color: #000000;"> piece_len:
</span><span style="color: #008080;">119</span>                         length = piece_len -<span style="color: #000000;"> offset
</span><span style="color: #008080;">120</span>                     piece =<span style="color: #000000;"> (piece_index, offset, length)
</span><span style="color: #008080;">121</span>                     <span style="color: #0000ff;">if</span> piece <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">122</span>                         self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">.append(piece)
</span><span style="color: #008080;">123</span>             
<span style="color: #008080;">124</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__dispatch_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">125</span>                 self.<span style="color: #800080;">__dispatch_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">126</span>             
<span style="color: #008080;">127</span>             self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">128</span>             
<span style="color: #008080;">129</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_choked</span><span style="color: #000000;">:
</span><span style="color: #008080;">130</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_choked_timer</span> == None <span style="color: #0000ff;">or</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__peer_choked_timer</span><span style="color: #000000;">.is_alive():
</span><span style="color: #008080;">131</span>                     self.<span style="color: #800080;">__peer_choked_timer</span> = threading.Timer(self.<span style="color: #800080;">__peer_choked_timeout_intvl</span>, PeerConnect.<span style="color: #800080;">__peer_choked_timeout</span><span style="color: #000000;">, [self,])
</span><span style="color: #008080;">132</span>                     self.<span style="color: #800080;">__peer_choked_timer</span><span style="color: #000000;">.start()
</span><span style="color: #008080;">133</span>         
<span style="color: #008080;">134</span>             
<span style="color: #008080;">135</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> True
</span><span style="color: #008080;">136</span>     
<span style="color: #008080;">137</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> cancel_pieces(self, pieces):
</span><span style="color: #008080;">138</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">139</span>             <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">140</span>                 <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:
</span><span style="color: #008080;">141</span>                     self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">.remove(piece)
</span><span style="color: #008080;">142</span>                     
<span style="color: #008080;">143</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">144</span>                 <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_requesting_pieces</span><span style="color: #000000;">:
</span><span style="color: #008080;">145</span>                     <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:
</span><span style="color: #008080;">146</span>                         self.<span style="color: #800080;">__send_cancel</span><span style="color: #000000;">(piece)
</span><span style="color: #008080;">147</span>                         self.<span style="color: #800080;">__local_requesting_pieces</span><span style="color: #000000;">.remove(piece)
</span><span style="color: #008080;">148</span>                 <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_requesting_pieces</span>) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">149</span>                     self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">150</span>                     <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">151</span>                         self.<span style="color: #800080;">__local_requesting_timer</span><span style="color: #000000;">.cancel()       
</span><span style="color: #008080;">152</span>                 self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">153</span> 
<span style="color: #008080;">154</span>         
<span style="color: #008080;">155</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> set_choke_state(self, choked):
</span><span style="color: #008080;">156</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">157</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_choked</span> !=<span style="color: #000000;"> choked:
</span><span style="color: #008080;">158</span>                 <span style="color: #0000ff;">if</span><span style="color: #000000;"> choked:
</span><span style="color: #008080;">159</span>                     self.<span style="color: #800080;">__send_choked</span><span style="color: #000000;">()
</span><span style="color: #008080;">160</span>                 <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">161</span>                     self.<span style="color: #800080;">__send_unchoked</span><span style="color: #000000;">()
</span><span style="color: #008080;">162</span>                     self.<span style="color: #800080;">__check_peer_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">163</span>             <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">164</span>         
<span style="color: #008080;">165</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_peer_have_pieces(self):
</span><span style="color: #008080;">166</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">167</span>             <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__peer_have_pieces</span>
<span style="color: #008080;">168</span>     
<span style="color: #008080;">169</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> notify_local_have_pieces(self, pieces):
</span><span style="color: #008080;">170</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">171</span>             self.<span style="color: #800080;">__send_have</span><span style="color: #000000;">(pieces)
</span><span style="color: #008080;">172</span>          
<span style="color: #008080;">173</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> is_dead_peer(self):
</span><span style="color: #008080;">174</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">175</span>             <span style="color: #0000ff;">return</span>  self.<span style="color: #800080;">__retry_times</span> &gt; self.<span style="color: #800080;">__max_retrys</span>
<span style="color: #008080;">176</span>     
<span style="color: #008080;">177</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_local_pending_pieces(self):
</span><span style="color: #008080;">178</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">179</span>             pieces_index =<span style="color: #000000;"> []
</span><span style="color: #008080;">180</span>             <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">181</span>                 <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces_index:
</span><span style="color: #008080;">182</span> <span style="color: #000000;">                    pieces_index.append(piece[0])
</span><span style="color: #008080;">183</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">184</span>                 <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_requesting_pieces</span><span style="color: #000000;">: 
</span><span style="color: #008080;">185</span>                     <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces_index:
</span><span style="color: #008080;">186</span> <span style="color: #000000;">                        pieces_index.append(piece[0])
</span><span style="color: #008080;">187</span> 
<span style="color: #008080;">188</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> pieces_index
</span><span style="color: #008080;">189</span>     
<span style="color: #008080;">190</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_peer_addr(self):
</span><span style="color: #008080;">191</span>         <span style="color: #0000ff;">return</span> (self.<span style="color: #800080;">__ip</span>, self.<span style="color: #800080;">__port</span><span style="color: #000000;">)
</span><span style="color: #008080;">192</span>         
<span style="color: #008080;">193</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__connect</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">194</span> 
<span style="color: #008080;">195</span>         self.<span style="color: #800080;">__tcp_con</span> =<span style="color: #000000;"> socket(AF_INET, SOCK_STREAM)
</span><span style="color: #008080;">196</span>         self.<span style="color: #800080;">__tcp_con</span>.settimeout(self.<span style="color: #800080;">__tcp_connect_timeout</span><span style="color: #000000;">)
</span><span style="color: #008080;">197</span> 
<span style="color: #008080;">198</span>         <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;">199</span>             self.<span style="color: #800080;">__tcp_con</span>.connect((self.<span style="color: #800080;">__ip</span>,self.<span style="color: #800080;">__port</span><span style="color: #000000;">))
</span><span style="color: #008080;">200</span>         <span style="color: #0000ff;">except</span><span style="color: #000000;"> error , e:
</span><span style="color: #008080;">201</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">peer connect error: %s, retry</span><span style="color: #800000;">'</span> %<span style="color: #000000;">e)
</span><span style="color: #008080;">202</span>             self.<span style="color: #800080;">__retry_connect</span><span style="color: #000000;">()
</span><span style="color: #008080;">203</span>             <span style="color: #0000ff;">return</span>
<span style="color: #008080;">204</span>         
<span style="color: #008080;">205</span>         self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">.settimeout(None)
</span><span style="color: #008080;">206</span>         
<span style="color: #008080;">207</span>         self.<span style="color: #800080;">__start_send_proc</span><span style="color: #000000;">()
</span><span style="color: #008080;">208</span> 
<span style="color: #008080;">209</span>         <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__handshake</span><span style="color: #000000;">():
</span><span style="color: #008080;">210</span>             self.<span style="color: #800080;">__retry_connect</span><span style="color: #000000;">()
</span><span style="color: #008080;">211</span>             <span style="color: #0000ff;">return</span>
<span style="color: #008080;">212</span>         
<span style="color: #008080;">213</span>         self.<span style="color: #800080;">__send_bitfield</span><span style="color: #000000;">()
</span><span style="color: #008080;">214</span>         self.<span style="color: #800080;">__send_unchoked</span><span style="color: #000000;">()
</span><span style="color: #008080;">215</span>         self.<span style="color: #800080;">__start_keepalive_timer</span><span style="color: #000000;">()      
</span><span style="color: #008080;">216</span> 
<span style="color: #008080;">217</span>         self.<span style="color: #800080;">__recv_loop</span><span style="color: #000000;">()
</span><span style="color: #008080;">218</span>     <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">219</span> 
<span style="color: #008080;">220</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__disconnect</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">221</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__disconnect:begin</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">222</span>         
<span style="color: #008080;">223</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__retry_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">224</span>             self.<span style="color: #800080;">__retry_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">225</span>         
<span style="color: #008080;">226</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__keepalive_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">227</span>             self.<span style="color: #800080;">__keepalive_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">228</span>             
<span style="color: #008080;">229</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_sending_queue</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">230</span>             self.<span style="color: #800080;">__local_sending_queue</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;">231</span>             self.<span style="color: #800080;">__local_sending_event</span><span style="color: #000000;">.set()
</span><span style="color: #008080;">232</span>             
<span style="color: #008080;">233</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_choked_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">234</span>             self.<span style="color: #800080;">__peer_choked_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">235</span>             
<span style="color: #008080;">236</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__dispatch_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">237</span>             self.<span style="color: #800080;">__dispatch_timer</span><span style="color: #000000;">.cancel()    
</span><span style="color: #008080;">238</span> 
<span style="color: #008080;">239</span>         
<span style="color: #008080;">240</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">241</span>             self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">242</span>             self.<span style="color: #800080;">__local_pending_request</span> = self.<span style="color: #800080;">__local_requesting_pieces</span> + self.<span style="color: #800080;">__local_pending_request</span>
<span style="color: #008080;">243</span>             self.<span style="color: #800080;">__local_requesting_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">244</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">245</span>                 self.<span style="color: #800080;">__local_requesting_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">246</span>         
<span style="color: #008080;">247</span>         self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">.close()
</span><span style="color: #008080;">248</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__disconnect: self.__tcp_con.closed</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">249</span>         
<span style="color: #008080;">250</span>         self.<span style="color: #800080;">__receiving_cache</span> = <span style="color: #800000;">''</span>
<span style="color: #008080;">251</span>         
<span style="color: #008080;">252</span>         self.<span style="color: #800080;">__local_choked</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">253</span>         self.<span style="color: #800080;">__peer_choked</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">254</span>         self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">255</span>         self.<span style="color: #800080;">__peer_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">256</span>         self.<span style="color: #800080;">__local_requesting_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">257</span>         self.<span style="color: #800080;">__peer_pending_request</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">258</span>         self.<span style="color: #800080;">__peer_have_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">259</span>         self.<span style="color: #800080;">__peer_have_pieces_pending</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">260</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">261</span>     
<span style="color: #008080;">262</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__start_keepalive_timer</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">263</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__keepalive_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">264</span>             self.<span style="color: #800080;">__keepalive_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">265</span>         self.<span style="color: #800080;">__keepalive_timer</span> = threading.Timer(120,PeerConnect.<span style="color: #800080;">__send_keepalive_timeout</span><span style="color: #000000;">,[self,])
</span><span style="color: #008080;">266</span>         self.<span style="color: #800080;">__keepalive_timer</span><span style="color: #000000;">.start()
</span><span style="color: #008080;">267</span>         
<span style="color: #008080;">268</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_keepalive_timeout</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">269</span>         
<span style="color: #008080;">270</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">271</span>             self.<span style="color: #800080;">__send_keepalive</span><span style="color: #000000;">()
</span><span style="color: #008080;">272</span>             self.<span style="color: #800080;">__start_keepalive_timer</span><span style="color: #000000;">()
</span><span style="color: #008080;">273</span>         
<span style="color: #008080;">274</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__recv_loop</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">275</span>         self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">.setblocking(False)
</span><span style="color: #008080;">276</span>         <span style="color: #0000ff;">while</span><span style="color: #000000;"> True:
</span><span style="color: #008080;">277</span>             ready_r, ready_w, in_err = select.select([self.<span style="color: #800080;">__tcp_con</span>,], [], [self.<span style="color: #800080;">__tcp_con</span>,], 600<span style="color: #000000;">)
</span><span style="color: #008080;">278</span>             
<span style="color: #008080;">279</span>             with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">280</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tcp_con</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> in_err:
</span><span style="color: #008080;">281</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__recv_loop: socket in error select result:%s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">str(in_err))
</span><span style="color: #008080;">282</span>                     self.<span style="color: #800080;">__retry_connect</span><span style="color: #000000;">()
</span><span style="color: #008080;">283</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;">284</span>                 
<span style="color: #008080;">285</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tcp_con</span> <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> ready_r:
</span><span style="color: #008080;">286</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__recv_loop: unexpected select result!</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">287</span>                     <span style="color: #0000ff;">continue</span> 
<span style="color: #008080;">288</span>                 
<span style="color: #008080;">289</span>                 <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;">290</span>                     received_data = self.<span style="color: #800080;">__tcp_con</span>.recv(self.<span style="color: #800080;">__receive_data_len</span><span style="color: #000000;">)
</span><span style="color: #008080;">291</span>                         
<span style="color: #008080;">292</span>                 <span style="color: #0000ff;">except</span><span style="color: #000000;"> error, e:
</span><span style="color: #008080;">293</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">receive data failed, error:%s, retry</span><span style="color: #800000;">"</span> %<span style="color: #000000;">e)
</span><span style="color: #008080;">294</span>                     self.<span style="color: #800080;">__retry_connect</span><span style="color: #000000;">()
</span><span style="color: #008080;">295</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;">296</span>             
<span style="color: #008080;">297</span>                 <span style="color: #0000ff;">if</span> len(received_data) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">298</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">have received null data</span><span style="color: #800000;">"</span><span style="color: #000000;">)
</span><span style="color: #008080;">299</span>                     self.<span style="color: #800080;">__retry_connect</span><span style="color: #000000;">()
</span><span style="color: #008080;">300</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;">301</span>             
<span style="color: #008080;">302</span>                 self.<span style="color: #800080;">__reveived_data</span><span style="color: #000000;">(received_data)
</span><span style="color: #008080;">303</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">304</span>     
<span style="color: #008080;">305</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__start_send_proc</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">306</span>         with self.<span style="color: #800080;">__rlock_sck_send</span><span style="color: #000000;">:
</span><span style="color: #008080;">307</span>             self.<span style="color: #800080;">__local_sending_queue</span> = <span style="color: #800000;">''</span>
<span style="color: #008080;">308</span>         self.<span style="color: #800080;">__sck_send_thread</span> = threading.Thread(target=PeerConnect.<span style="color: #800080;">__proc_sending</span>, args=<span style="color: #000000;">(self,))
</span><span style="color: #008080;">309</span>         self.<span style="color: #800080;">__sck_send_thread</span><span style="color: #000000;">.start()
</span><span style="color: #008080;">310</span>         
<span style="color: #008080;">311</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__proc_sending</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">312</span>         <span style="color: #0000ff;">while</span> self.<span style="color: #800080;">__local_sending_queue</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">313</span>                         
<span style="color: #008080;">314</span>             ready_r, ready_w, in_err = select.select([], [self.<span style="color: #800080;">__tcp_con</span>,], [self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">,])
</span><span style="color: #008080;">315</span>             
<span style="color: #008080;">316</span>             self.<span style="color: #800080;">__local_sending_event</span><span style="color: #000000;">.wait()
</span><span style="color: #008080;">317</span> 
<span style="color: #008080;">318</span>             with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">319</span>                 
<span style="color: #008080;">320</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tcp_con</span>  <span style="color: #0000ff;">in</span><span style="color: #000000;"> in_err:
</span><span style="color: #008080;">321</span>                     self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">.close()
</span><span style="color: #008080;">322</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;">323</span>                 
<span style="color: #008080;">324</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tcp_con</span> <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> ready_w:
</span><span style="color: #008080;">325</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__proc_sending: unexpected select result!</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">326</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;">327</span>                 
<span style="color: #008080;">328</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_sending_queue</span> ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">329</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;">330</span>                 
<span style="color: #008080;">331</span>                 <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;">332</span>                     sent_len = self.<span style="color: #800080;">__tcp_con</span>.send(self.<span style="color: #800080;">__local_sending_queue</span><span style="color: #000000;">)
</span><span style="color: #008080;">333</span>                     self.<span style="color: #800080;">__local_sending_queue</span> = self.<span style="color: #800080;">__local_sending_queue</span><span style="color: #000000;">[sent_len:]
</span><span style="color: #008080;">334</span>                     
<span style="color: #008080;">335</span>                 <span style="color: #0000ff;">except</span><span style="color: #000000;"> error,e:
</span><span style="color: #008080;">336</span>                     self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">.close()
</span><span style="color: #008080;">337</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__proc_sending failed! error:%s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">str(e))
</span><span style="color: #008080;">338</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;">339</span>                     
<span style="color: #008080;">340</span>                 <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_sending_queue</span>) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">341</span>                     self.<span style="color: #800080;">__local_sending_event</span><span style="color: #000000;">.clear()
</span><span style="color: #008080;">342</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">343</span>     
<span style="color: #008080;">344</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__check_peer_request</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">345</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_interested</span> <span style="color: #0000ff;">and</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__local_choked</span><span style="color: #000000;">:
</span><span style="color: #008080;">346</span>             <span style="color: #0000ff;">while</span> len(self.<span style="color: #800080;">__peer_pending_request</span>) &gt;<span style="color: #000000;"> 0:
</span><span style="color: #008080;">347</span>                 piece = self.<span style="color: #800080;">__peer_pending_request</span><span style="color: #000000;">.pop(0)
</span><span style="color: #008080;">348</span>                 piece_index, offset, length =<span style="color: #000000;"> piece
</span><span style="color: #008080;">349</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_have</span><span style="color: #000000;">(piece_index):
</span><span style="color: #008080;">350</span>                     data = self.<span style="color: #800080;">__read_piecedata</span><span style="color: #000000;">(piece_index,offset, length)
</span><span style="color: #008080;">351</span>                     self.<span style="color: #800080;">__send_piece</span><span style="color: #000000;">(piece_index, offset, data)
</span><span style="color: #008080;">352</span>                 <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">353</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">peer request piece:%d not have.</span><span style="color: #800000;">'</span> %<span style="color: #000000;">piece_index)
</span><span style="color: #008080;">354</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">355</span> 
<span style="color: #008080;">356</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__check_local_request</span><span style="color: #000000;">(self): 
</span><span style="color: #008080;">357</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">358</span>             self.<span style="color: #800080;">__check_interested</span><span style="color: #000000;">() 
</span><span style="color: #008080;">359</span>             
<span style="color: #008080;">360</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span> <span style="color: #0000ff;">and</span> len(self.<span style="color: #800080;">__local_requesting_pieces</span>) &gt;= self.<span style="color: #800080;">__local_max_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">361</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;">362</span>             
<span style="color: #008080;">363</span>             <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_pending_request</span>) !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">364</span>                 <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__local_interested</span><span style="color: #000000;">:
</span><span style="color: #008080;">365</span>                     self.<span style="color: #800080;">__send_interested</span><span style="color: #000000;">()
</span><span style="color: #008080;">366</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">367</span>                 <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__peer_have_pieces</span>) !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">368</span>                     <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__dispatch_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">369</span>                         self.<span style="color: #800080;">__dispatch_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">370</span>                         
<span style="color: #008080;">371</span>                     self.<span style="color: #800080;">__dispatch_timer</span> = threading.Timer(self.<span style="color: #800080;">__dispatch_timeout</span>,PeerConnect.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;"> ,[self,])
</span><span style="color: #008080;">372</span>                     self.<span style="color: #800080;">__dispatch_timer</span><span style="color: #000000;">.start()
</span><span style="color: #008080;">373</span>                     self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">374</span>                     self.<span style="color: #800080;">__notify_pieces_completed</span><span style="color: #000000;">()
</span><span style="color: #008080;">375</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;">376</span>             
<span style="color: #008080;">377</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_choked</span><span style="color: #000000;">:
</span><span style="color: #008080;">378</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;">379</span>         
<span style="color: #008080;">380</span>             adding_piece = self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">.pop(0)
</span><span style="color: #008080;">381</span>             <span style="color: #0000ff;">if</span> adding_piece[0] <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">:
</span><span style="color: #008080;">382</span>                 <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">383</span>                     <span style="color: #0000ff;">if</span> piece[0] ==<span style="color: #000000;"> adding_piece[0]:
</span><span style="color: #008080;">384</span>                         self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">.remove(piece)
</span><span style="color: #008080;">385</span>                 self.<span style="color: #800080;">__notify_pieces_canceled</span><span style="color: #000000;">([adding_piece[0],])
</span><span style="color: #008080;">386</span>                 self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">387</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">388</span>                 self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">389</span>                 self.<span style="color: #800080;">__local_requesting_pieces</span><span style="color: #000000;">.append(adding_piece)    
</span><span style="color: #008080;">390</span>                 self.<span style="color: #800080;">__send_request</span><span style="color: #000000;">(adding_piece)
</span><span style="color: #008080;">391</span>                 self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">392</span>                 
<span style="color: #008080;">393</span>                 <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting_timer</span> == None <span style="color: #0000ff;">or</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__local_requesting_timer</span><span style="color: #000000;">.is_alive():
</span><span style="color: #008080;">394</span>                     self.<span style="color: #800080;">__local_requesting_timer</span> = threading.Timer(self.<span style="color: #800080;">__local_requesting_timeout_intvl</span>, PeerConnect.<span style="color: #800080;">__local_requesting_timeout</span><span style="color: #000000;">, [self,])
</span><span style="color: #008080;">395</span>                     self.<span style="color: #800080;">__local_requesting_timer</span><span style="color: #000000;">.start()
</span><span style="color: #008080;">396</span>             <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">397</span>     
<span style="color: #008080;">398</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__local_requesting_timeout</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">399</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">400</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">401</span>                 self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">402</span>                 self.<span style="color: #800080;">__local_pending_request</span> = self.<span style="color: #800080;">__local_requesting_pieces</span> + self.<span style="color: #800080;">__local_pending_request</span>
<span style="color: #008080;">403</span>                 self.<span style="color: #800080;">__local_requesting_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">404</span>                 self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">405</span>                 self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">406</span> 
<span style="color: #008080;">407</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">408</span>     
<span style="color: #008080;">409</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__peer_choked_timeout</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">410</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">411</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_choked</span><span style="color: #000000;">:
</span><span style="color: #008080;">412</span>                 pending_pieces =<span style="color: #000000;"> []
</span><span style="color: #008080;">413</span>                 <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">414</span>                     <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> pending_pieces:
</span><span style="color: #008080;">415</span> <span style="color: #000000;">                        pending_pieces.append(piece[0])
</span><span style="color: #008080;">416</span>                 <span style="color: #0000ff;">if</span> len(pending_pieces) !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">417</span>                     self.<span style="color: #800080;">__notify_pieces_canceled</span><span style="color: #000000;">(pending_pieces)
</span><span style="color: #008080;">418</span>                     self.<span style="color: #800080;">__local_pending_request</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">419</span>         
<span style="color: #008080;">420</span>                     
<span style="color: #008080;">421</span>     
<span style="color: #008080;">422</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__check_interested</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">423</span>         <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">424</span>             <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_pending_request</span>) != 0 <span style="color: #0000ff;">and</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__local_interested</span><span style="color: #000000;">:
</span><span style="color: #008080;">425</span>                 self.<span style="color: #800080;">__send_interested</span><span style="color: #000000;">()
</span><span style="color: #008080;">426</span>                 
<span style="color: #008080;">427</span>         <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span> self.<span style="color: #800080;">__local_requesting</span> <span style="color: #0000ff;">and</span> len(self.<span style="color: #800080;">__local_pending_request</span>) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">428</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_interested</span><span style="color: #000000;">:
</span><span style="color: #008080;">429</span>                 self.<span style="color: #800080;">__send_notintrested</span><span style="color: #000000;">()
</span><span style="color: #008080;">430</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">431</span>                 
<span style="color: #008080;">432</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__retry_connect</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">433</span>         
<span style="color: #008080;">434</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">__retry_connect</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">435</span>         pending_pieces =<span style="color: #000000;"> []
</span><span style="color: #008080;">436</span>         peer_dead =<span style="color: #000000;"> False
</span><span style="color: #008080;">437</span>          
<span style="color: #008080;">438</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">439</span>             self.<span style="color: #800080;">__disconnect</span><span style="color: #000000;">()
</span><span style="color: #008080;">440</span>             
<span style="color: #008080;">441</span>             <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">442</span>                 <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> pending_pieces:
</span><span style="color: #008080;">443</span> <span style="color: #000000;">                    pending_pieces.append(piece[0])
</span><span style="color: #008080;">444</span>                     
<span style="color: #008080;">445</span>             self.<span style="color: #800080;">__retry_times</span> += 1
<span style="color: #008080;">446</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__retry_times</span> &gt; self.<span style="color: #800080;">__max_retrys</span><span style="color: #000000;">:
</span><span style="color: #008080;">447</span>                 peer_dead =<span style="color: #000000;"> True
</span><span style="color: #008080;">448</span> 
<span style="color: #008080;">449</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">450</span>                 self.<span style="color: #800080;">__retry_timer</span> = threading.Timer(self.<span style="color: #800080;">__retry_intvl</span>**self.<span style="color: #800080;">__retry_times</span>, PeerConnect.<span style="color: #800080;">__connect</span><span style="color: #000000;">, [self,])
</span><span style="color: #008080;">451</span>                 self.<span style="color: #800080;">__retry_timer</span><span style="color: #000000;">.start()
</span><span style="color: #008080;">452</span>                 
<span style="color: #008080;">453</span>         <span style="color: #0000ff;">if</span> peer_dead ==<span style="color: #000000;"> True:        
</span><span style="color: #008080;">454</span>             self.<span style="color: #800080;">__notify_peer_dead</span><span style="color: #000000;">()
</span><span style="color: #008080;">455</span>             
<span style="color: #008080;">456</span>         <span style="color: #0000ff;">if</span> len(pending_pieces) !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">457</span>             self.<span style="color: #800080;">__notify_pieces_canceled</span><span style="color: #000000;">(pending_pieces)
</span><span style="color: #008080;">458</span>             self.<span style="color: #800080;">__local_pending_request</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">459</span> 
<span style="color: #008080;">460</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__reveived_data</span><span style="color: #000000;">(self, data):
</span><span style="color: #008080;">461</span>         self.<span style="color: #800080;">__receiving_cache</span> +=<span style="color: #000000;"> data
</span><span style="color: #008080;">462</span>             
<span style="color: #008080;">463</span>         <span style="color: #0000ff;">while</span> len(self.<span style="color: #800080;">__receiving_cache</span>) &gt;= 4<span style="color: #000000;">:
</span><span style="color: #008080;">464</span>             msg_len = _str_ntohl(self.<span style="color: #800080;">__receiving_cache</span>[0:4<span style="color: #000000;">])
</span><span style="color: #008080;">465</span>             
<span style="color: #008080;">466</span>             <span style="color: #0000ff;">if</span> (len(self.<span style="color: #800080;">__receiving_cache</span>)-4) &gt;=<span style="color: #000000;"> msg_len:
</span><span style="color: #008080;">467</span>                 self.<span style="color: #800080;">__proc_msg</span>(self.<span style="color: #800080;">__receiving_cache</span>[4:(4+<span style="color: #000000;">msg_len)])
</span><span style="color: #008080;">468</span>                 self.<span style="color: #800080;">__receiving_cache</span> = data[4+<span style="color: #000000;">msg_len:]
</span><span style="color: #008080;">469</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">470</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">471</span>                     
<span style="color: #008080;">472</span>                 
<span style="color: #008080;">473</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__proc_msg</span><span style="color: #000000;">(self, msg):
</span><span style="color: #008080;">474</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">475</span>             <span style="color: #0000ff;">if</span> len(msg) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">476</span>                 self.<span style="color: #800080;">__received_keepalive</span><span style="color: #000000;">()
</span><span style="color: #008080;">477</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">: 
</span><span style="color: #008080;">478</span>                 msg_type =<span style="color: #000000;"> msg[0]
</span><span style="color: #008080;">479</span>                 <span style="color: #0000ff;">if</span> msg_type ==<span style="color: #000000;"> chr(0):
</span><span style="color: #008080;">480</span>                     self.<span style="color: #800080;">__received_choked</span><span style="color: #000000;">()
</span><span style="color: #008080;">481</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(1<span style="color: #000000;">):
</span><span style="color: #008080;">482</span>                     self.<span style="color: #800080;">__received_unchoked</span><span style="color: #000000;">()
</span><span style="color: #008080;">483</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(2<span style="color: #000000;">):
</span><span style="color: #008080;">484</span>                     self.<span style="color: #800080;">__received_interested</span><span style="color: #000000;">()
</span><span style="color: #008080;">485</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(3<span style="color: #000000;">):
</span><span style="color: #008080;">486</span>                     self.<span style="color: #800080;">__received_notinterested</span><span style="color: #000000;">()
</span><span style="color: #008080;">487</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(4<span style="color: #000000;">):
</span><span style="color: #008080;">488</span>                     self.<span style="color: #800080;">__received_have</span>(msg[1<span style="color: #000000;">:])                                
</span><span style="color: #008080;">489</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(5<span style="color: #000000;">):
</span><span style="color: #008080;">490</span>                     self.<span style="color: #800080;">__received_bitfield</span>(msg[1<span style="color: #000000;">:])
</span><span style="color: #008080;">491</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(6<span style="color: #000000;">):
</span><span style="color: #008080;">492</span>                     self.<span style="color: #800080;">__received_request</span>(msg[1<span style="color: #000000;">:])             
</span><span style="color: #008080;">493</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(7<span style="color: #000000;">):
</span><span style="color: #008080;">494</span>                     self.<span style="color: #800080;">__received_piece</span>(msg[1<span style="color: #000000;">:])
</span><span style="color: #008080;">495</span>                 <span style="color: #0000ff;">elif</span> msg_type == chr(8<span style="color: #000000;">):
</span><span style="color: #008080;">496</span>                     self.<span style="color: #800080;">__received_cancel</span>(msg[1<span style="color: #000000;">:]) 
</span><span style="color: #008080;">497</span>                 <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">498</span>                     self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received unknown msg :%s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">499</span>     
<span style="color: #008080;">500</span>     <span style="color: #0000ff;">def</span>  <span style="color: #800080;">__handshake</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">501</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send handshake: %s</span><span style="color: #800000;">'</span> %list(self.<span style="color: #800080;">__handshake_info</span><span style="color: #000000;">))
</span><span style="color: #008080;">502</span>         self.<span style="color: #800080;">__tcp_con</span>.sendall(self.<span style="color: #800080;">__handshake_info</span><span style="color: #000000;">)
</span><span style="color: #008080;">503</span>         
<span style="color: #008080;">504</span>         <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;">505</span>             self.<span style="color: #800080;">__tcp_con</span>.settimeout(self.<span style="color: #800080;">__tcp_handshake_timeout</span><span style="color: #000000;">)
</span><span style="color: #008080;">506</span>             rsp = self.<span style="color: #800080;">__tcp_con</span>.recv(68<span style="color: #000000;">)
</span><span style="color: #008080;">507</span>             
<span style="color: #008080;">508</span>             <span style="color: #0000ff;">if</span> len(rsp) != 68<span style="color: #000000;">:
</span><span style="color: #008080;">509</span>                 <span style="color: #0000ff;">return</span><span style="color: #000000;"> False
</span><span style="color: #008080;">510</span>             
<span style="color: #008080;">511</span>             self.<span style="color: #800080;">__tcp_con</span><span style="color: #000000;">.settimeout(None)
</span><span style="color: #008080;">512</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">recived handshake rsp: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(rsp))
</span><span style="color: #008080;">513</span>             self.<span style="color: #800080;">__peer_id</span> = rsp[47:67<span style="color: #000000;">]
</span><span style="color: #008080;">514</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">peer_id:%s</span><span style="color: #800000;">'</span> %self.<span style="color: #800080;">__peer_id</span><span style="color: #000000;">)
</span><span style="color: #008080;">515</span>             
<span style="color: #008080;">516</span>         <span style="color: #0000ff;">except</span><span style="color: #000000;"> (error,timeout), e:
</span><span style="color: #008080;">517</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">handshake failed, error:%s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">e)
</span><span style="color: #008080;">518</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> False
</span><span style="color: #008080;">519</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> True
</span><span style="color: #008080;">520</span>     
<span style="color: #008080;">521</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_keepalive</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">522</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received keepalive</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">523</span>         <span style="color: #008000;">#</span><span style="color: #008000;">self.__send_keepalive()</span>
<span style="color: #008080;">524</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">525</span>             
<span style="color: #008080;">526</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_choked</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">527</span> 
<span style="color: #008080;">528</span>         self.<span style="color: #800080;">__peer_choked</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">529</span>         
<span style="color: #008080;">530</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">531</span>             self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">532</span>             self.<span style="color: #800080;">__local_pending_request</span> =  self.<span style="color: #800080;">__local_requesting_pieces</span> + self.<span style="color: #800080;">__local_pending_request</span>
<span style="color: #008080;">533</span>             self.<span style="color: #800080;">__local_requesting_pieces</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">534</span>             
<span style="color: #008080;">535</span>         self.<span style="color: #800080;">__notify_peer_choked</span><span style="color: #000000;">()
</span><span style="color: #008080;">536</span>         
<span style="color: #008080;">537</span>         <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_pending_request</span>) !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">538</span>             pending_pieces =<span style="color: #000000;"> []
</span><span style="color: #008080;">539</span>             <span style="color: #0000ff;">for</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">540</span>                 <span style="color: #0000ff;">if</span> piece[0] <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> pending_pieces:
</span><span style="color: #008080;">541</span> <span style="color: #000000;">                    pending_pieces.append(piece[0])
</span><span style="color: #008080;">542</span>             self.<span style="color: #800080;">__notify_pieces_canceled</span><span style="color: #000000;">(pending_pieces)
</span><span style="color: #008080;">543</span>             self.<span style="color: #800080;">__local_pending_request</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">544</span>             self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">545</span>             
<span style="color: #008080;">546</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received choked</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">547</span>         
<span style="color: #008080;">548</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_unchoked</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">549</span>         self.<span style="color: #800080;">__peer_choked</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">550</span>         
<span style="color: #008080;">551</span>         self.<span style="color: #800080;">__notify_peer_unchoked</span><span style="color: #000000;">()
</span><span style="color: #008080;">552</span>         
<span style="color: #008080;">553</span>         <span style="color: #008000;">#</span><span style="color: #008000;">if len(self.__local_pending_request) &lt; self.__local_pending_request_less:</span>
<span style="color: #008080;">554</span>         self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">555</span>         
<span style="color: #008080;">556</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_choked_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">557</span>             self.<span style="color: #800080;">__peer_choked_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">558</span>             
<span style="color: #008080;">559</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received unchoked</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">560</span>         
<span style="color: #008080;">561</span>     
<span style="color: #008080;">562</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_interested</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">563</span>         self.<span style="color: #800080;">__peer_interested</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">564</span>         <span style="color: #008000;">#</span><span style="color: #008000;">self.__send_unchoked()</span>
<span style="color: #008080;">565</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received interested</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">566</span>         
<span style="color: #008080;">567</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_notinterested</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">568</span>         self.<span style="color: #800080;">__peer_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">569</span>         self.<span style="color: #800080;">__peer_pending_request</span> =<span style="color: #000000;"> [] 
</span><span style="color: #008080;">570</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received notinterested</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">571</span>         
<span style="color: #008080;">572</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_have</span><span style="color: #000000;">(self, data):
</span><span style="color: #008080;">573</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;">574</span> <span style="color: #800000;">        TODO:Notify peer have pieces changed
</span><span style="color: #008080;">575</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;">576</span>         piece_index = _str_ntohl(data[0:4<span style="color: #000000;">])
</span><span style="color: #008080;">577</span>         <span style="color: #0000ff;">if</span> piece_index <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">:
</span><span style="color: #008080;">578</span>             self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">.append(piece_index)
</span><span style="color: #008080;">579</span>             self.<span style="color: #800080;">__peer_have_pieces_pending</span><span style="color: #000000;">.append(piece_index)
</span><span style="color: #008080;">580</span>             <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_pending_request</span>) &lt; self.<span style="color: #800080;">__local_pending_request_less</span><span style="color: #000000;">:
</span><span style="color: #008080;">581</span>                 self.<span style="color: #800080;">__notify_pieces_have</span>(self.<span style="color: #800080;">__peer_have_pieces_pending</span><span style="color: #000000;">)
</span><span style="color: #008080;">582</span>                 self.<span style="color: #800080;">__peer_have_pieces_pending</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;">583</span>             
<span style="color: #008080;">584</span>             
<span style="color: #008080;">585</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received have piece:%d</span><span style="color: #800000;">'</span> %<span style="color: #000000;">piece_index)
</span><span style="color: #008080;">586</span> 
<span style="color: #008080;">587</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_bitfield</span><span style="color: #000000;">(self, data):
</span><span style="color: #008080;">588</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;">589</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;">590</span>         bitfield_len =<span style="color: #000000;"> len(data)
</span><span style="color: #008080;">591</span>         <span style="color: #0000ff;">for</span> i <span style="color: #0000ff;">in</span><span style="color: #000000;"> range(0,bitfield_len):
</span><span style="color: #008080;">592</span>             byte =<span style="color: #000000;"> data[i]
</span><span style="color: #008080;">593</span>             <span style="color: #0000ff;">for</span> j <span style="color: #0000ff;">in</span> range(0,8<span style="color: #000000;">):
</span><span style="color: #008080;">594</span>                 byte_mask = 1&lt;&lt;(7-<span style="color: #000000;">j)
</span><span style="color: #008080;">595</span>                 piece_index = i*8+<span style="color: #000000;">j
</span><span style="color: #008080;">596</span>                 have = ord(byte)&amp;<span style="color: #000000;">byte_mask
</span><span style="color: #008080;">597</span>                 <span style="color: #0000ff;">if</span> have !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">598</span>                     <span style="color: #0000ff;">if</span> piece_index <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">:
</span><span style="color: #008080;">599</span>                         self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">.append(piece_index)
</span><span style="color: #008080;">600</span>                         
<span style="color: #008080;">601</span>         self.<span style="color: #800080;">__notify_pieces_have</span>(self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">)
</span><span style="color: #008080;">602</span> 
<span style="color: #008080;">603</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">received bitfield ,peer have pieces:%s</span><span style="color: #800000;">'</span> %self.<span style="color: #800080;">__peer_have_pieces</span><span style="color: #000000;">)
</span><span style="color: #008080;">604</span> 
<span style="color: #008080;">605</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_request</span><span style="color: #000000;">(self, data):
</span><span style="color: #008080;">606</span>         piece_index = _str_ntohl(data[0:4<span style="color: #000000;">])
</span><span style="color: #008080;">607</span>         offset      = _str_ntohl(data[4:8<span style="color: #000000;">])
</span><span style="color: #008080;">608</span>         data_len    = _str_ntohl(data[8:12<span style="color: #000000;">])
</span><span style="color: #008080;">609</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__peer_interested</span><span style="color: #000000;">:
</span><span style="color: #008080;">610</span>                 self.<span style="color: #800080;">__peer_pending_request</span><span style="color: #000000;">.append((piece_index, offset, data_len))
</span><span style="color: #008080;">611</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">612</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">received request piece:%d , but peer not interested</span><span style="color: #800000;">"</span> %<span style="color: #000000;">piece_index)
</span><span style="color: #008080;">613</span>         
<span style="color: #008080;">614</span>         self.<span style="color: #800080;">__check_peer_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">615</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">received request piece:%d </span><span style="color: #800000;">"</span> %<span style="color: #000000;">piece_index)
</span><span style="color: #008080;">616</span>     
<span style="color: #008080;">617</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_piece</span><span style="color: #000000;">(self, data):
</span><span style="color: #008080;">618</span>         piece_index = _str_ntohl(data[0:4<span style="color: #000000;">])
</span><span style="color: #008080;">619</span>         offset      = _str_ntohl(data[4:8<span style="color: #000000;">])
</span><span style="color: #008080;">620</span>         piece = (piece_index, offset, len(data)-8<span style="color: #000000;">)
</span><span style="color: #008080;">621</span>         
<span style="color: #008080;">622</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting</span><span style="color: #000000;">:
</span><span style="color: #008080;">623</span>             <span style="color: #0000ff;">if</span> piece <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__local_requesting_pieces</span><span style="color: #000000;">:
</span><span style="color: #008080;">624</span>                 self.<span style="color: #800080;">__write_piecedata</span>(piece_index, offset, data[8<span style="color: #000000;">:])
</span><span style="color: #008080;">625</span>                 self.<span style="color: #800080;">__local_requesting_pieces</span><span style="color: #000000;">.remove(piece)
</span><span style="color: #008080;">626</span>                 
<span style="color: #008080;">627</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_requesting_timer</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">628</span>                 self.<span style="color: #800080;">__local_requesting_timer</span><span style="color: #000000;">.cancel()
</span><span style="color: #008080;">629</span>                 
<span style="color: #008080;">630</span>             <span style="color: #0000ff;">if</span> len(self.<span style="color: #800080;">__local_requesting_pieces</span>) ==<span style="color: #000000;"> 0:  
</span><span style="color: #008080;">631</span>                 self.<span style="color: #800080;">__local_requesting</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">632</span>                 
<span style="color: #008080;">633</span>             self.<span style="color: #800080;">__check_local_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">634</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">received  piece: %s</span><span style="color: #800000;">"</span> %str((piece_index, offset, len(data)-8<span style="color: #000000;">)))
</span><span style="color: #008080;">635</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">636</span>             self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">received unexpected piece: %s</span><span style="color: #800000;">"</span> %str((piece_index, offset, len(data)-8<span style="color: #000000;">)))
</span><span style="color: #008080;">637</span> 
<span style="color: #008080;">638</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__received_cancel</span><span style="color: #000000;">(self, data):
</span><span style="color: #008080;">639</span>         piece_index = _str_ntohl(data[0:4<span style="color: #000000;">])
</span><span style="color: #008080;">640</span>         offset      = _str_ntohl(data[4:8<span style="color: #000000;">])
</span><span style="color: #008080;">641</span>         data_len    = _str_ntohl(data[8:12<span style="color: #000000;">])
</span><span style="color: #008080;">642</span>         request =<span style="color: #000000;"> (piece_index, offset, data_len)
</span><span style="color: #008080;">643</span>         <span style="color: #0000ff;">if</span> request <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__peer_pending_request</span><span style="color: #000000;">:
</span><span style="color: #008080;">644</span>             self.<span style="color: #800080;">__peer_pending_request</span><span style="color: #000000;">.remove(request)
</span><span style="color: #008080;">645</span>         self.<span style="color: #800080;">__check_peer_request</span><span style="color: #000000;">()
</span><span style="color: #008080;">646</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">"</span><span style="color: #800000;">received cancel: %s</span><span style="color: #800000;">"</span> %<span style="color: #000000;">str((piece_index,offset,data_len)))
</span><span style="color: #008080;">647</span>             
<span style="color: #008080;">648</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_keepalive</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">649</span>         msg_len =<span style="color: #000000;"> 0
</span><span style="color: #008080;">650</span>         msg =<span style="color: #000000;"> _htonl_str(msg_len)
</span><span style="color: #008080;">651</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send keepalive: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">652</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">653</span>         
<span style="color: #008080;">654</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_choked</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">655</span>         self.<span style="color: #800080;">__local_choked</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">656</span>         msg_type =<span style="color: #000000;"> chr(0)
</span><span style="color: #008080;">657</span>         msg_len = 1
<span style="color: #008080;">658</span>         msg = _htonl_str(msg_len) +<span style="color: #000000;"> msg_type
</span><span style="color: #008080;">659</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send choked: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">660</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">661</span>         
<span style="color: #008080;">662</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_unchoked</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">663</span>         self.<span style="color: #800080;">__local_choked</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">664</span>         msg_type = chr(1<span style="color: #000000;">)
</span><span style="color: #008080;">665</span>         msg_len = 1
<span style="color: #008080;">666</span>         msg = _htonl_str(msg_len) +<span style="color: #000000;"> msg_type
</span><span style="color: #008080;">667</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send unchoked: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">668</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)    
</span><span style="color: #008080;">669</span>         
<span style="color: #008080;">670</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_interested</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">671</span>         self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> True
</span><span style="color: #008080;">672</span>         msg_type = chr(2<span style="color: #000000;">)
</span><span style="color: #008080;">673</span>         msg_len = 1
<span style="color: #008080;">674</span>         msg = _htonl_str(msg_len) +<span style="color: #000000;"> msg_type
</span><span style="color: #008080;">675</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send intrested: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">676</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">677</span>         
<span style="color: #008080;">678</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_notintrested</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">679</span>         self.<span style="color: #800080;">__local_interested</span> =<span style="color: #000000;"> False
</span><span style="color: #008080;">680</span>         msg_type = chr(3<span style="color: #000000;">)
</span><span style="color: #008080;">681</span>         msg_len = 1
<span style="color: #008080;">682</span>         msg = _htonl_str(msg_len) +<span style="color: #000000;"> msg_type
</span><span style="color: #008080;">683</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send notintrested: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">684</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">685</span>         
<span style="color: #008080;">686</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_have</span><span style="color: #000000;">(self,pieces):
</span><span style="color: #008080;">687</span>         msg = <span style="color: #800000;">''</span>
<span style="color: #008080;">688</span>         msg_type = chr(4<span style="color: #000000;">)
</span><span style="color: #008080;">689</span>         msg_len = 5
<span style="color: #008080;">690</span>         <span style="color: #0000ff;">for</span> piece_index <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:
</span><span style="color: #008080;">691</span>             msg += _htonl_str(msg_len) + msg_type +<span style="color: #000000;">  _htonl_str(piece_index)
</span><span style="color: #008080;">692</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send have: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">str(list(msg)))
</span><span style="color: #008080;">693</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">694</span>         
<span style="color: #008080;">695</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_bitfield</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">696</span>         bitfield = self.<span style="color: #800080;">__get_local_bitfield</span><span style="color: #000000;">()
</span><span style="color: #008080;">697</span>         msg_type = chr(5<span style="color: #000000;">)
</span><span style="color: #008080;">698</span>         msg_len = 1 +<span style="color: #000000;"> len(bitfield)
</span><span style="color: #008080;">699</span>         msg = _htonl_str(msg_len) + msg_type +<span style="color: #000000;"> bitfield
</span><span style="color: #008080;">700</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">701</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send bitfield: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">702</span>         
<span style="color: #008080;">703</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_request</span><span style="color: #000000;">(self, piece):
</span><span style="color: #008080;">704</span>         msg = <span style="color: #800000;">''</span>
<span style="color: #008080;">705</span>         msg_type = chr(6<span style="color: #000000;">)
</span><span style="color: #008080;">706</span>         msg_len = 13
<span style="color: #008080;">707</span>         (piece_index, begin, length) =<span style="color: #000000;"> piece
</span><span style="color: #008080;">708</span>         msg += _htonl_str(msg_len) + msg_type + _htonl_str(piece_index) + _htonl_str(begin) +<span style="color: #000000;"> _htonl_str(length)
</span><span style="color: #008080;">709</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send request: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">710</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">711</span>     
<span style="color: #008080;">712</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_piece</span><span style="color: #000000;">(self, piece_index, offset, data):
</span><span style="color: #008080;">713</span>         msg = <span style="color: #800000;">''</span>
<span style="color: #008080;">714</span>         msg_type = chr(7<span style="color: #000000;">)
</span><span style="color: #008080;">715</span>         data_len =<span style="color: #000000;"> len(data)
</span><span style="color: #008080;">716</span>         msg_len = 1 + 4 + 4 +<span style="color: #000000;"> data_len
</span><span style="color: #008080;">717</span>         msg += _htonl_str(msg_len) + msg_type + _htonl_str(piece_index) +<span style="color: #000000;"> _htonl_str(offset)
</span><span style="color: #008080;">718</span>         msg +=<span style="color: #000000;"> data
</span><span style="color: #008080;">719</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send piece (%d,%d)</span><span style="color: #800000;">'</span> %<span style="color: #000000;">(piece_index, offset))
</span><span style="color: #008080;">720</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">721</span>         
<span style="color: #008080;">722</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__send_cancel</span><span style="color: #000000;">(self, piece_index, offset, length):
</span><span style="color: #008080;">723</span>         msg = <span style="color: #800000;">''</span>
<span style="color: #008080;">724</span>         msg_type = chr(8<span style="color: #000000;">)
</span><span style="color: #008080;">725</span>         msg_len = 13
<span style="color: #008080;">726</span>         msg += _htonl_str(msg_len) + msg_type + _htonl_str(piece_index) + _htonl_str(offset) +<span style="color: #000000;"> _htonl_str(length)
</span><span style="color: #008080;">727</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">send cancel: %s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">list(msg))
</span><span style="color: #008080;">728</span>         self.<span style="color: #800080;">__sck_send</span><span style="color: #000000;">(msg)
</span><span style="color: #008080;">729</span>             
<span style="color: #008080;">730</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__sck_send</span><span style="color: #000000;">(self, msg):
</span><span style="color: #008080;">731</span>         with self.<span style="color: #800080;">__rlock_common</span><span style="color: #000000;">:
</span><span style="color: #008080;">732</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__local_sending_queue</span> ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">733</span>                 self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">sck send msg failed, because queue is none!</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">734</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;">735</span>             
<span style="color: #008080;">736</span>             self.<span style="color: #800080;">__local_sending_queue</span> +=<span style="color: #000000;"> msg
</span><span style="color: #008080;">737</span>             self.<span style="color: #800080;">__local_sending_event</span><span style="color: #000000;">.set()
</span><span style="color: #008080;">738</span>             <span style="color: #008000;">#</span><span style="color: #008000;">self.__tcp_con.sendall(msg)</span>
<span style="color: #008080;">739</span> 
<span style="color: #008080;">740</span>         
<span style="color: #008080;">741</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__local_have</span><span style="color: #000000;">(self,piece_index):
</span><span style="color: #008080;">742</span>         pieces = self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.get_local_have_pieces()
</span><span style="color: #008080;">743</span>         <span style="color: #0000ff;">if</span> piece_index <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:
</span><span style="color: #008080;">744</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> True
</span><span style="color: #008080;">745</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">746</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> False
</span><span style="color: #008080;">747</span> 
<span style="color: #008080;">748</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__read_piecedata</span><span style="color: #000000;">(self, piece_index, offset, data_len):
</span><span style="color: #008080;">749</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.read_piecedata(piece_index, offset, data_len)
</span><span style="color: #008080;">750</span>     
<span style="color: #008080;">751</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__write_piecedata</span><span style="color: #000000;">(self, piece_index, offset, data):
</span><span style="color: #008080;">752</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.write_piecedata(piece_index, offset, data)
</span><span style="color: #008080;">753</span>     
<span style="color: #008080;">754</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__notify_pieces_canceled</span><span style="color: #000000;">(self, pieces):
</span><span style="color: #008080;">755</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">notify taskinfo canceled pieces</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">756</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.peer_pieces_canceled(self, pieces)
</span><span style="color: #008080;">757</span>     
<span style="color: #008080;">758</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__notify_pieces_have</span><span style="color: #000000;">(self, pieces):
</span><span style="color: #008080;">759</span>         self.<span style="color: #800080;">__write_log</span>(<span style="color: #800000;">'</span><span style="color: #800000;">notify taskinfo peeer have pieces</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">760</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.peer_have_pieces(self, pieces)
</span><span style="color: #008080;">761</span>         
<span style="color: #008080;">762</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__notify_pieces_completed</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">763</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.peer_pieces_completed(self)
</span><span style="color: #008080;">764</span>     
<span style="color: #008080;">765</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__notify_peer_choked</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">766</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.peer_choked(self)
</span><span style="color: #008080;">767</span>         
<span style="color: #008080;">768</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__notify_peer_unchoked</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">769</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.peer_unchoked(self)
</span><span style="color: #008080;">770</span>         
<span style="color: #008080;">771</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__notify_peer_dead</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">772</span>         self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.peer_dead(self)
</span><span style="color: #008080;">773</span>     
<span style="color: #008080;">774</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__get_local_bitfield</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">775</span>         pieces_num = self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.get_pieces_num()
</span><span style="color: #008080;">776</span>         bitfield_len = pieces_num/8
<span style="color: #008080;">777</span>         <span style="color: #0000ff;">if</span> pieces_num%8 !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">778</span>             bitfield_len += 1
<span style="color: #008080;">779</span>         bitfield = [chr(0),]*<span style="color: #000000;">bitfield_len
</span><span style="color: #008080;">780</span>         
<span style="color: #008080;">781</span>         pieces = self.<span style="color: #800080;">__task_info</span><span style="color: #000000;">.get_local_have_pieces()
</span><span style="color: #008080;">782</span>         <span style="color: #0000ff;">for</span> index <span style="color: #0000ff;">in</span><span style="color: #000000;"> pieces:
</span><span style="color: #008080;">783</span>             bit_filed_index = index / 8
<span style="color: #008080;">784</span>             bit_field_offset = index % 8
<span style="color: #008080;">785</span>             byte_mask = 1&lt;&lt;<span style="color: #000000;">bit_field_offset
</span><span style="color: #008080;">786</span>             byte =<span style="color: #000000;"> ord(bitfield[bit_filed_index])
</span><span style="color: #008080;">787</span>             byte |=<span style="color: #000000;"> byte_mask
</span><span style="color: #008080;">788</span>             bitfield[bit_filed_index] =<span style="color: #000000;"> chr(byte)
</span><span style="color: #008080;">789</span>         <span style="color: #0000ff;">return</span> <span style="color: #800000;">''</span><span style="color: #000000;">.join(bitfield)
</span><span style="color: #008080;">790</span>     
<span style="color: #008080;">791</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__write_log</span><span style="color: #000000;">(self, info):
</span><span style="color: #008080;">792</span>         log_info.write_log(<span style="color: #800000;">'</span><span style="color: #800000;">#peer_connect[%s]# </span><span style="color: #800000;">'</span>  %self.<span style="color: #800080;">__ip</span> +<span style="color: #000000;"> info)
</span><span style="color: #008080;">793</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">794</span>          
<span style="color: #008080;">795</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _htonl_str(integer):
</span><span style="color: #008080;">796</span>     msg = <span style="color: #800000;">''</span>
<span style="color: #008080;">797</span>     msg += chr((integer&gt;&gt;24)%0x100<span style="color: #000000;">)
</span><span style="color: #008080;">798</span>     msg += chr((integer&gt;&gt;16)%0x100<span style="color: #000000;">)
</span><span style="color: #008080;">799</span>     msg += chr((integer&gt;&gt;8)%0x100<span style="color: #000000;">)
</span><span style="color: #008080;">800</span>     msg += chr(integer%0x100<span style="color: #000000;">)
</span><span style="color: #008080;">801</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> msg
</span><span style="color: #008080;">802</span> 
<span style="color: #008080;">803</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _str_ntohl(msg):
</span><span style="color: #008080;">804</span>     integer =<span style="color: #000000;"> 0
</span><span style="color: #008080;">805</span>     integer += ord(msg[0])&lt;&lt;24
<span style="color: #008080;">806</span>     integer += ord(msg[1])&lt;&lt;16
<span style="color: #008080;">807</span>     integer += ord(msg[2])&lt;&lt;8
<span style="color: #008080;">808</span>     integer += ord(msg[3<span style="color: #000000;">])
</span><span style="color: #008080;">809</span>     <span style="color: #0000ff;">return</span> integer</pre>
</div>
</div>



<pre>
referer:http://www.cnblogs.com/piaoliu/archive/2012/10/07/2714598.html
</pre>
