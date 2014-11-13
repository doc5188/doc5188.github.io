---
layout: post
title: "Python边学边用--BT客户端实现之(二)Peers获取"
categories: python
tags: [python, bt开发, dht开发, 系列教程]
date: 2014-11-13 11:45:00
---

<p>解析完torrent文件之后，需要从Tracker服务器获取拥有每个piece的peer列表。</p>
<p>tracker服务器使用http协议提供支持，使用get的方式获取请求内容。也有使用udp协议的，暂时还没有分析。</p>
<p>get 格式如下：</p>
<p>announce-url?<span>info_hash=xxxxxxxxxxxxxxxxxxxxx,peer_id=xxxxxxxxxxxxxxxxxxxx,ip=x.x.x.x,port=xxxx,uploaded=xx,downloaded=xx,left=xx,event=x</span></p>
<p>url中各参数需要经过url扰码处理。</p>
<p>其中，info_hash为torrent文件中info属性的value部分(bencode格式)的SHA1 hash，peer_id为任务启动时bt客户端为自己随即分配的20字节的ID, ip为本机外网ip，port为bt客户端监听的端口，uploaded，downloaded，left为本节点的下载属性。event为可选字段，包括 started,completed,stoped</p>
<p>&nbsp;</p>
<p>tracker服务器的返回内容为经过bencode的dict类型，如果返回失败，会包含"failure reason" 键值，内容为可读的失败原因。</p>
<p>如果返回成功会包含以下几项内容：</p>
<p>"interval" --像tracker服务器发起常规查询的间隔时间（我理解为peers信息的刷新时间，自己需要定期向tracker报告下载状态，同时获取最新的peer信息）</p>
<p>"peers" &nbsp;--为一个peer list，每个peer包含以下几项内容：</p>
<p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"peer id" &nbsp;--20字节的peer自分配id</p>
<p>　　　 &nbsp;"ip" &nbsp;--peer ip地址</p>
<p>&nbsp;&nbsp;　　　"port" --peer 监听端口</p>
<p>&nbsp; &nbsp; &nbsp;</p>
<p>关于peers项，当前大多支持bep-23中第一的compact peers以减少返回内容的长度，该该格式下peers属性为一个string</p>
<p>每六个字节为一组，每组表示一个peer，其中前4个字节 表示peer ip，后两个字节表示peer port，均为大头模式表示。没有peer id，但是不影响后面的下载操作。 &nbsp;</p>
<p>&nbsp;</p>
<div class="cnblogs_code" onclick="cnblogs_code_show('7933e3fd-fd31-4bbc-b2fc-6fd7535133be')"><img id="code_img_closed_7933e3fd-fd31-4bbc-b2fc-6fd7535133be" class="code_img_closed" src="http://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif" alt="" /><img id="code_img_opened_7933e3fd-fd31-4bbc-b2fc-6fd7535133be" class="code_img_opened" style="display: none;" onclick="cnblogs_code_hide('7933e3fd-fd31-4bbc-b2fc-6fd7535133be',event)" src="http://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif" alt="" /><span class="cnblogs_code_collapse">trackers_info.py</span>
<div id="cnblogs_code_open_7933e3fd-fd31-4bbc-b2fc-6fd7535133be" class="cnblogs_code_hide">
<pre><span style="color: #008080;">  1</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  2</span> <span style="color: #800000;">Created on 2012-10-2
</span><span style="color: #008080;">  3</span> 
<span style="color: #008080;">  4</span> <span style="color: #800000;">@author: ddt
</span><span style="color: #008080;">  5</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  6</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> httplib
</span><span style="color: #008080;">  7</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> urllib
</span><span style="color: #008080;">  8</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> bcodec
</span><span style="color: #008080;">  9</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> re
</span><span style="color: #008080;"> 10</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> torrent_file
</span><span style="color: #008080;"> 11</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> threading
</span><span style="color: #008080;"> 12</span> 
<span style="color: #008080;"> 13</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> TrackersInfo(object):
</span><span style="color: #008080;"> 14</span>     <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 15</span> <span style="color: #800000;">    TODO: UDP tracker support
</span><span style="color: #008080;"> 16</span> <span style="color: #800000;">    TODO: tracker polling support
</span><span style="color: #008080;"> 17</span>     <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 18</span> 
<span style="color: #008080;"> 19</span>     <span style="color: #800080;">__info_hash</span> = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 20</span>     
<span style="color: #008080;"> 21</span>     <span style="color: #800080;">__peer_id</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 22</span>     <span style="color: #800080;">__host_ip</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 23</span>     <span style="color: #800080;">__host_port</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 24</span>     
<span style="color: #008080;"> 25</span>     <span style="color: #800080;">__trackers</span> =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 26</span>     <span style="color: #800080;">__tracker_check_timeout</span> = 0 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 27</span>     <span style="color: #800080;">__tracker_get_timeout</span> = 0 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 28</span>     <span style="color: #800080;">__tracker_max_retrys</span> =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 29</span>     
<span style="color: #008080;"> 30</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__init__</span><span style="color: #000000;">(self, announce_list, host_info, info_hash):
</span><span style="color: #008080;"> 31</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 32</span> <span style="color: #800000;">        Constructor
</span><span style="color: #008080;"> 33</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 34</span>         self.<span style="color: #800080;">__info_hash</span> =<span style="color: #000000;"> info_hash
</span><span style="color: #008080;"> 35</span>         self.<span style="color: #800080;">__peer_id</span>, self.<span style="color: #800080;">__host_ip</span>, self.<span style="color: #800080;">__host_port</span> =<span style="color: #000000;"> host_info
</span><span style="color: #008080;"> 36</span>         
<span style="color: #008080;"> 37</span>         self.<span style="color: #800080;">__tracker_check_timeout</span> = 3 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 38</span>         self.<span style="color: #800080;">__tracker_get_timeout</span> = 10 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 39</span>         self.<span style="color: #800080;">__tracker_max_retrys</span> = 2
<span style="color: #008080;"> 40</span>         
<span style="color: #008080;"> 41</span>         <span style="color: #008000;">#</span><span style="color: #008000;">init trackers</span>
<span style="color: #008080;"> 42</span>         <span style="color: #0000ff;">for</span> tier <span style="color: #0000ff;">in</span><span style="color: #000000;"> announce_list:
</span><span style="color: #008080;"> 43</span>             <span style="color: #0000ff;">for</span> announce <span style="color: #0000ff;">in</span><span style="color: #000000;"> tier:
</span><span style="color: #008080;"> 44</span>                 tracker =<span style="color: #000000;"> {}
</span><span style="color: #008080;"> 45</span>                 tracker_addr = self.<span style="color: #800080;">__get_tracker_addr</span><span style="color: #000000;">(announce)
</span><span style="color: #008080;"> 46</span>                 <span style="color: #0000ff;">if</span> tracker_addr ==<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 47</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;"> 48</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> tracker_addr
</span><span style="color: #008080;"> 49</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">rsp</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 50</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>]  =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 51</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">error</span><span style="color: #800000;">'</span>] = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 52</span>                 self.<span style="color: #800080;">__trackers</span><span style="color: #000000;">.append(tracker)
</span><span style="color: #008080;"> 53</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;"> 54</span>         
<span style="color: #008080;"> 55</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_peers(self):
</span><span style="color: #008080;"> 56</span>         peers =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 57</span>         <span style="color: #0000ff;">for</span> tracker <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__trackers</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 58</span>             rsp = tracker[<span style="color: #800000;">'</span><span style="color: #800000;">rsp</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;"> 59</span>             <span style="color: #0000ff;">if</span> rsp !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 60</span>                 <span style="color: #0000ff;">for</span> peer <span style="color: #0000ff;">in</span> rsp[<span style="color: #800000;">'</span><span style="color: #800000;">peers</span><span style="color: #800000;">'</span><span style="color: #000000;">]:
</span><span style="color: #008080;"> 61</span>                     <span style="color: #0000ff;">if</span> peer <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> peers:
</span><span style="color: #008080;"> 62</span> <span style="color: #000000;">                        peers.append(peer)
</span><span style="color: #008080;"> 63</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> peers
</span><span style="color: #008080;"> 64</span>     
<span style="color: #008080;"> 65</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> refresh_trackers(self, download_state, refresh_intvl):
</span><span style="color: #008080;"> 66</span>         rsp_msg =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 67</span>         thread_list =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 68</span>         
<span style="color: #008080;"> 69</span>         <span style="color: #0000ff;">for</span> tracker <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__trackers</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 70</span>             rsp = tracker[<span style="color: #800000;">'</span><span style="color: #800000;">rsp</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;"> 71</span>             <span style="color: #0000ff;">if</span> rsp !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 72</span>                 rsp[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] -=<span style="color: #000000;"> refresh_intvl
</span><span style="color: #008080;"> 73</span>                 <span style="color: #0000ff;">if</span> rsp[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] &gt;<span style="color: #000000;"> 0:
</span><span style="color: #008080;"> 74</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;"> 75</span>                 <span style="color: #0000ff;">if</span> rsp[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] &lt;<span style="color: #000000;"> 0:
</span><span style="color: #008080;"> 76</span>                     rsp[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 77</span>                     
<span style="color: #008080;"> 78</span>             <span style="color: #0000ff;">if</span> tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>] &lt; self.<span style="color: #800080;">__tracker_max_retrys</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 79</span>                 thread = threading.Thread(target=TrackersInfo.<span style="color: #800080;">__request_tracker</span>,args=<span style="color: #000000;">(self,tracker,download_state))
</span><span style="color: #008080;"> 80</span> <span style="color: #000000;">                thread.start()
</span><span style="color: #008080;"> 81</span> <span style="color: #000000;">                thread_list.append(thread)
</span><span style="color: #008080;"> 82</span>                 <span style="color: #008000;">#</span><span style="color: #008000;">self.__request_tracker(tracker, download_state)</span>
<span style="color: #008080;"> 83</span>         <span style="color: #0000ff;">for</span> thread <span style="color: #0000ff;">in</span><span style="color: #000000;"> thread_list:
</span><span style="color: #008080;"> 84</span> <span style="color: #000000;">            thread.join()
</span><span style="color: #008080;"> 85</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;"> 86</span>     
<span style="color: #008080;"> 87</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__request_tracker</span><span style="color: #000000;">(self, tracker, download_state):
</span><span style="color: #008080;"> 88</span>         <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">request_tracker: </span><span style="color: #800000;">"</span>,  tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;"> 89</span>         
<span style="color: #008080;"> 90</span>         web_addr,web_port,page_url = tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;"> 91</span>         tracker_con = httplib.HTTPConnection(web_addr, web_port,timeout=self.<span style="color: #800080;">__tracker_get_timeout</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 92</span>         piece_request = self.<span style="color: #800080;">__generate_request</span><span style="color: #000000;">(download_state)
</span><span style="color: #008080;"> 93</span>         <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span><span style="color: #000000;"> page_url:
</span><span style="color: #008080;"> 94</span>             page_url = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 95</span>         url = page_url + <span style="color: #800000;">'</span><span style="color: #800000;">?</span><span style="color: #800000;">'</span> +<span style="color: #000000;"> piece_request
</span><span style="color: #008080;"> 96</span>         <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">http://</span><span style="color: #800000;">'</span>+web_addr+<span style="color: #000000;">url
</span><span style="color: #008080;"> 97</span>         <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 98</span>             tracker_con.request(<span style="color: #800000;">"</span><span style="color: #800000;">GET</span><span style="color: #800000;">"</span><span style="color: #000000;">, url)
</span><span style="color: #008080;"> 99</span>             response =<span style="color: #000000;"> tracker_con.getresponse() 
</span><span style="color: #008080;">100</span>             <span style="color: #0000ff;">print</span><span style="color: #000000;">  response.status, response.reason
</span><span style="color: #008080;">101</span>             <span style="color: #0000ff;">if</span> response.reason.upper() != <span style="color: #800000;">'</span><span style="color: #800000;">OK</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;">102</span>                 <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! tracker:%s</span><span style="color: #800000;">'</span> %(response.reason, tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span><span style="color: #000000;">])
</span><span style="color: #008080;">103</span> <span style="color: #000000;">                tracker_con.close()
</span><span style="color: #008080;">104</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">error</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> response.reason
</span><span style="color: #008080;">105</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>] += 1
<span style="color: #008080;">106</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;">107</span>             msg_encoded =<span style="color: #000000;"> response.read()
</span><span style="color: #008080;">108</span> <span style="color: #000000;">            tracker_con.close()
</span><span style="color: #008080;">109</span>             rsp_msg =<span style="color: #000000;"> bcodec.bdecode(msg_encoded)
</span><span style="color: #008080;">110</span>             <span style="color: #0000ff;">if</span> rsp_msg ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">111</span>                 <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! tracker:%s</span><span style="color: #800000;">'</span> %(msg_encoded, tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span><span style="color: #000000;">])
</span><span style="color: #008080;">112</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">error</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> msg_encoded
</span><span style="color: #008080;">113</span>                 tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>] += 1
<span style="color: #008080;">114</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;">115</span>             
<span style="color: #008080;">116</span>         <span style="color: #0000ff;">except</span><span style="color: #000000;"> Exception,e:
</span><span style="color: #008080;">117</span> <span style="color: #000000;">            tracker_con.close()
</span><span style="color: #008080;">118</span>             <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! tracker:%s</span><span style="color: #800000;">'</span> %(e.message, tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span><span style="color: #000000;">])
</span><span style="color: #008080;">119</span>             tracker[<span style="color: #800000;">'</span><span style="color: #800000;">error</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> e.message
</span><span style="color: #008080;">120</span>             tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>] += 1
<span style="color: #008080;">121</span>             <span style="color: #0000ff;">return</span>
<span style="color: #008080;">122</span>         
<span style="color: #008080;">123</span>         <span style="color: #0000ff;">if</span> <span style="color: #800000;">'</span><span style="color: #800000;">failure reason</span><span style="color: #800000;">'</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> rsp_msg.keys():
</span><span style="color: #008080;">124</span>             <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! tracker:%s</span><span style="color: #800000;">'</span> %(rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">failure reason</span><span style="color: #800000;">'</span>], tracker[<span style="color: #800000;">'</span><span style="color: #800000;">addr</span><span style="color: #800000;">'</span><span style="color: #000000;">])
</span><span style="color: #008080;">125</span>             tracker[<span style="color: #800000;">'</span><span style="color: #800000;">error</span><span style="color: #800000;">'</span>] = rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">failure reason</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">126</span>             tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>] += 1
<span style="color: #008080;">127</span>             <span style="color: #0000ff;">return</span>
<span style="color: #008080;">128</span>         <span style="color: #0000ff;">print</span><span style="color: #000000;"> rsp_msg 
</span><span style="color: #008080;">129</span>         peers_msg = rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">peers</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">130</span>         peer_list =<span style="color: #000000;"> []
</span><span style="color: #008080;">131</span>         <span style="color: #0000ff;">if</span> type(peers_msg) == type(<span style="color: #800000;">''</span><span style="color: #000000;">):
</span><span style="color: #008080;">132</span>             <span style="color: #0000ff;">for</span> i <span style="color: #0000ff;">in</span> range(0,len(peers_msg)-5,6<span style="color: #000000;">):
</span><span style="color: #008080;">133</span>                 one_peer = peers_msg[i:i+6<span style="color: #000000;">]
</span><span style="color: #008080;">134</span>                 <span style="color: #008000;">#</span><span style="color: #008000;">peer_id = ''</span>
<span style="color: #008080;">135</span>                 ip = one_peer[0:4<span style="color: #000000;">]
</span><span style="color: #008080;">136</span>                 port = one_peer[4:6<span style="color: #000000;">]
</span><span style="color: #008080;">137</span>                 ip = <span style="color: #800000;">'</span><span style="color: #800000;">%d.%d.%d.%d</span><span style="color: #800000;">'</span> %(ord(ip[0]),ord(ip[1]),ord(ip[2]),ord(ip[3<span style="color: #000000;">]),)
</span><span style="color: #008080;">138</span>                 port = ord(port[0])*256+ord(port[1<span style="color: #000000;">])
</span><span style="color: #008080;">139</span> <span style="color: #000000;">                peer_list.append((ip,port))
</span><span style="color: #008080;">140</span>             rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">peers</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> peer_list 
</span><span style="color: #008080;">141</span>             <span style="color: #0000ff;">print</span><span style="color: #000000;">  peer_list
</span><span style="color: #008080;">142</span>         <span style="color: #0000ff;">elif</span> type(peers_msg) ==<span style="color: #000000;"> type([]):
</span><span style="color: #008080;">143</span>             <span style="color: #0000ff;">for</span> peer <span style="color: #0000ff;">in</span><span style="color: #000000;"> peers_msg:
</span><span style="color: #008080;">144</span>                 peer_list.append((peer[<span style="color: #800000;">'</span><span style="color: #800000;">ip</span><span style="color: #800000;">'</span>],peer[<span style="color: #800000;">'</span><span style="color: #800000;">port</span><span style="color: #800000;">'</span><span style="color: #000000;">]))
</span><span style="color: #008080;">145</span>         tracker[<span style="color: #800000;">'</span><span style="color: #800000;">rsp</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> rsp_msg
</span><span style="color: #008080;">146</span>         tracker[<span style="color: #800000;">'</span><span style="color: #800000;">retrys</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> 0
</span><span style="color: #008080;">147</span>     
<span style="color: #008080;">148</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__generate_request</span><span style="color: #000000;">(self, download_state):
</span><span style="color: #008080;">149</span>         
<span style="color: #008080;">150</span>         downloaded = download_state[<span style="color: #800000;">'</span><span style="color: #800000;">downloaded</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">151</span>         uploaded = download_state[<span style="color: #800000;">'</span><span style="color: #800000;">uploaded</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">152</span>         left = download_state[<span style="color: #800000;">'</span><span style="color: #800000;">left</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">153</span>         event = download_state[<span style="color: #800000;">'</span><span style="color: #800000;">event</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">154</span>         
<span style="color: #008080;">155</span>         request =<span style="color: #000000;"> {}
</span><span style="color: #008080;">156</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">info_hash</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__info_hash</span>
<span style="color: #008080;">157</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">peer_id</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__peer_id</span>
<span style="color: #008080;">158</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">ip</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__host_ip</span>
<span style="color: #008080;">159</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">port</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__host_port</span>
<span style="color: #008080;">160</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">uploaded</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> uploaded
</span><span style="color: #008080;">161</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">downloaded</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> downloaded
</span><span style="color: #008080;">162</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">left</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> left
</span><span style="color: #008080;">163</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">event</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> event
</span><span style="color: #008080;">164</span>         request =<span style="color: #000000;"> urllib.urlencode(request)
</span><span style="color: #008080;">165</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> request
</span><span style="color: #008080;">166</span>     
<span style="color: #008080;">167</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__get_tracker_addr</span><span style="color: #000000;">(self, announce):
</span><span style="color: #008080;">168</span>         tracker_addr =<span style="color: #000000;"> None
</span><span style="color: #008080;">169</span>         m = re.match(r<span style="color: #800000;">'</span><span style="color: #800000;">(http://)([^/,:]*)(:(\d*))?(/.*)?</span><span style="color: #800000;">'</span><span style="color: #000000;">,announce)
</span><span style="color: #008080;">170</span>         <span style="color: #0000ff;">if</span> m !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">171</span>             web_addr = m.groups()[1<span style="color: #000000;">]
</span><span style="color: #008080;">172</span>             web_port = m.groups()[3<span style="color: #000000;">]
</span><span style="color: #008080;">173</span>             page_url = m.groups()[4<span style="color: #000000;">]
</span><span style="color: #008080;">174</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">175</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;">176</span>         
<span style="color: #008080;">177</span>         <span style="color: #0000ff;">if</span> web_port !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">178</span>             web_port =<span style="color: #000000;"> int(web_port)
</span><span style="color: #008080;">179</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">180</span>             web_port = 80
<span style="color: #008080;">181</span>         
<span style="color: #008080;">182</span>         tracker_addr =<span style="color: #000000;"> (web_addr,web_port, page_url)
</span><span style="color: #008080;">183</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> tracker_addr
</span><span style="color: #008080;">184</span>     
<span style="color: #008080;">185</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__get_valid_tracker</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">186</span>         
<span style="color: #008080;">187</span>         tracker_addr =<span style="color: #000000;"> None
</span><span style="color: #008080;">188</span>         
<span style="color: #008080;">189</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__annouce_list</span> == None <span style="color: #0000ff;">or</span> len(self.<span style="color: #800080;">__annouce_list</span>) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">190</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;">191</span>         
<span style="color: #008080;">192</span>         tracker_con =<span style="color: #000000;"> None
</span><span style="color: #008080;">193</span>         found_current =<span style="color: #000000;"> False
</span><span style="color: #008080;">194</span>         <span style="color: #0000ff;">for</span> tier <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__annouce_list</span><span style="color: #000000;">:
</span><span style="color: #008080;">195</span>             <span style="color: #0000ff;">for</span> announce <span style="color: #0000ff;">in</span><span style="color: #000000;"> tier:
</span><span style="color: #008080;">196</span>                 tracker_addr = self.<span style="color: #800080;">__get_tracker_addr</span><span style="color: #000000;">(announce)
</span><span style="color: #008080;">197</span>                 <span style="color: #0000ff;">if</span> tracker_addr ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">198</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;">199</span>                 
<span style="color: #008080;">200</span>                 (web_addr,web_port, page_url) =<span style="color: #000000;"> tracker_addr
</span><span style="color: #008080;">201</span>                     
<span style="color: #008080;">202</span>                 tracker_con = httplib.HTTPConnection(web_addr, web_port,timeout=self.<span style="color: #800080;">__tracker_check_timeout</span><span style="color: #000000;">) 
</span><span style="color: #008080;">203</span>                 <span style="color: #0000ff;">try</span><span style="color: #000000;">: 
</span><span style="color: #008080;">204</span> <span style="color: #000000;">                    tracker_con.connect()
</span><span style="color: #008080;">205</span>                 <span style="color: #0000ff;">except</span><span style="color: #000000;"> Exception, e:
</span><span style="color: #008080;">206</span>                     <span style="color: #0000ff;">print</span><span style="color: #000000;"> e
</span><span style="color: #008080;">207</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;">208</span>                
<span style="color: #008080;">209</span> <span style="color: #000000;">                tier.remove(announce)
</span><span style="color: #008080;">210</span> <span style="color: #000000;">                tier.insert(0,announce)
</span><span style="color: #008080;">211</span> <span style="color: #000000;">                tracker_con.close()
</span><span style="color: #008080;">212</span>                 tracker_addr =<span style="color: #000000;"> (web_addr,web_port, page_url)
</span><span style="color: #008080;">213</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">214</span>             
<span style="color: #008080;">215</span>             <span style="color: #008000;">#</span><span style="color: #008000;"># tiers sorting, none standard</span>
<span style="color: #008080;">216</span>             <span style="color: #0000ff;">if</span> tracker_addr !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">217</span>                 self.<span style="color: #800080;">__annouce_list</span><span style="color: #000000;">.remove(tier)
</span><span style="color: #008080;">218</span>                 self.<span style="color: #800080;">__annouce_list</span><span style="color: #000000;">.insert(0,tier)
</span><span style="color: #008080;">219</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">220</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> tracker_addr
</span><span style="color: #008080;">221</span>     
<span style="color: #008080;">222</span> <span style="color: #0000ff;">if</span> <span style="color: #800080;">__name__</span> == <span style="color: #800000;">'</span><span style="color: #800000;">__main__</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;">223</span>     <span style="color: #0000ff;">import</span><span style="color: #000000;"> down_load_task
</span><span style="color: #008080;">224</span>     filename = r<span style="color: #800000;">"</span><span style="color: #800000;">.\narodo.torrent</span><span style="color: #800000;">"</span>
<span style="color: #008080;">225</span>     torrent =<span style="color: #000000;"> torrent_file.TorrentFile()
</span><span style="color: #008080;">226</span> <span style="color: #000000;">    torrent.read_file(filename)
</span><span style="color: #008080;">227</span>     info_hash =<span style="color: #000000;"> (torrent.get_info_hash())
</span><span style="color: #008080;">228</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">info_hash: </span><span style="color: #800000;">"</span><span style="color: #000000;">, list(info_hash)
</span><span style="color: #008080;">229</span>     announce_list =<span style="color: #000000;"> torrent.get_announces()
</span><span style="color: #008080;">230</span>     peer_id =<span style="color: #000000;"> down_load_task._generate_peerid()
</span><span style="color: #008080;">231</span>     listening_addr =<span style="color: #000000;"> down_load_task._get_listening_addr()
</span><span style="color: #008080;">232</span>     host_info = (peer_id,) +<span style="color: #000000;"> listening_addr
</span><span style="color: #008080;">233</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">host_info: </span><span style="color: #800000;">'</span><span style="color: #000000;">, host_info
</span><span style="color: #008080;">234</span>     trackers =<span style="color: #000000;"> TrackersInfo(announce_list, host_info, info_hash)
</span><span style="color: #008080;">235</span>     download_state =<span style="color: #000000;"> {}
</span><span style="color: #008080;">236</span>     download_state[<span style="color: #800000;">'</span><span style="color: #800000;">downloaded</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> 0
</span><span style="color: #008080;">237</span>     download_state[<span style="color: #800000;">'</span><span style="color: #800000;">uploaded</span><span style="color: #800000;">'</span>]  =<span style="color: #000000;"> 0
</span><span style="color: #008080;">238</span>     download_state[<span style="color: #800000;">'</span><span style="color: #800000;">left</span><span style="color: #800000;">'</span>] = 364575
<span style="color: #008080;">239</span>     download_state[<span style="color: #800000;">'</span><span style="color: #800000;">event</span><span style="color: #800000;">'</span>] = <span style="color: #800000;">'</span><span style="color: #800000;">started</span><span style="color: #800000;">'</span>
<span style="color: #008080;">240</span>     trackers.refresh_trackers(download_state, 20<span style="color: #000000;">)
</span><span style="color: #008080;">241</span>     peers =<span style="color: #000000;"> trackers.get_peers()
</span><span style="color: #008080;">242</span>     <span style="color: #0000ff;">print</span> peers</pre>
</div>
</div>
<p>&nbsp;</p>
<div class="cnblogs_code" onclick="cnblogs_code_show('767b7ddc-b144-4718-8d84-3dba68b8034d')">
<div id="cnblogs_code_open_767b7ddc-b144-4718-8d84-3dba68b8034d" class="cnblogs_code_hide">
<pre><span style="color: #008080;">  1</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  2</span> <span style="color: #800000;">Created on 2012-10-2
</span><span style="color: #008080;">  3</span> 
<span style="color: #008080;">  4</span> <span style="color: #800000;">@author: ddt
</span><span style="color: #008080;">  5</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  6</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> httplib
</span><span style="color: #008080;">  7</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> urllib
</span><span style="color: #008080;">  8</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> bcodec
</span><span style="color: #008080;">  9</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> re
</span><span style="color: #008080;"> 10</span> 
<span style="color: #008080;"> 11</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> TrackerInfo(object):
</span><span style="color: #008080;"> 12</span>     <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 13</span> <span style="color: #800000;">    TODO: multiple tracker support
</span><span style="color: #008080;"> 14</span> <span style="color: #800000;">    TODO: UDP tracker support
</span><span style="color: #008080;"> 15</span> <span style="color: #800000;">    TODO: tracker polling support
</span><span style="color: #008080;"> 16</span>     <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 17</span>     <span style="color: #800080;">__announce_list</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 18</span> 
<span style="color: #008080;"> 19</span>     <span style="color: #800080;">__piece_index</span> =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 20</span>     
<span style="color: #008080;"> 21</span>     <span style="color: #800080;">__peer_id</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 22</span>     <span style="color: #800080;">__host_ip</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 23</span>     <span style="color: #800080;">__host_port</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 24</span>     
<span style="color: #008080;"> 25</span>     <span style="color: #800080;">__tracker_addr</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 26</span>     <span style="color: #800080;">__tracker_rsp</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 27</span>     
<span style="color: #008080;"> 28</span>     <span style="color: #800080;">__tracker_check_timeout</span> = 0 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 29</span>     <span style="color: #800080;">__tracker_get_timeout</span> = 0 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 30</span>     
<span style="color: #008080;"> 31</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__init__</span><span style="color: #000000;">(self, announce_list, host_info, piece_index):
</span><span style="color: #008080;"> 32</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 33</span> <span style="color: #800000;">        Constructor
</span><span style="color: #008080;"> 34</span>         <span style="color: #800000;">'''</span>
<span style="color: #008080;"> 35</span>         self.<span style="color: #800080;">__annouce_list</span> =<span style="color: #000000;"> announce_list
</span><span style="color: #008080;"> 36</span>         self.<span style="color: #800080;">__piece_index</span> =<span style="color: #000000;"> piece_index
</span><span style="color: #008080;"> 37</span>         self.<span style="color: #800080;">__peer_id</span>, self.<span style="color: #800080;">__host_ip</span>, self.<span style="color: #800080;">__host_port</span> =<span style="color: #000000;"> host_info
</span><span style="color: #008080;"> 38</span>         
<span style="color: #008080;"> 39</span>         self.<span style="color: #800080;">__tracker_check_timeout</span> = 3 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 40</span>         self.<span style="color: #800080;">__tracker_get_timeout</span> = 10 <span style="color: #008000;">#</span><span style="color: #008000;">second</span>
<span style="color: #008080;"> 41</span>         
<span style="color: #008080;"> 42</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> refresh_tracker(self, piece_state, intvl):
</span><span style="color: #008080;"> 43</span>         rsp_msg =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 44</span>         
<span style="color: #008080;"> 45</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tracker_rsp</span> !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 46</span>             self.<span style="color: #800080;">__tracker_rsp</span>[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] -=<span style="color: #000000;">  intvl
</span><span style="color: #008080;"> 47</span>             <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tracker_rsp</span>[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] &gt;<span style="color: #000000;"> 0:
</span><span style="color: #008080;"> 48</span>                 <span style="color: #0000ff;">return</span>
<span style="color: #008080;"> 49</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 50</span>                 self.<span style="color: #800080;">__tracker_rsp</span>[<span style="color: #800000;">'</span><span style="color: #800000;">interval</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> 0
</span><span style="color: #008080;"> 51</span>             
<span style="color: #008080;"> 52</span>         
<span style="color: #008080;"> 53</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__tracker_addr</span> ==<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 54</span>             self.<span style="color: #800080;">__tracker_addr</span> = self.<span style="color: #800080;">__get_valid_tracker</span><span style="color: #000000;">()
</span><span style="color: #008080;"> 55</span>                
<span style="color: #008080;"> 56</span>         tracker_addr = self.<span style="color: #800080;">__tracker_addr</span>
<span style="color: #008080;"> 57</span>         
<span style="color: #008080;"> 58</span>         <span style="color: #0000ff;">while</span> tracker_addr !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 59</span>             
<span style="color: #008080;"> 60</span>             web_addr,web_port,page_url = self.<span style="color: #800080;">__tracker_addr</span>
<span style="color: #008080;"> 61</span>             
<span style="color: #008080;"> 62</span>             tracker_con = httplib.HTTPConnection(web_addr, web_port,timeout=self.<span style="color: #800080;">__tracker_get_timeout</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 63</span>             piece_request = self.<span style="color: #800080;">__generate_request</span><span style="color: #000000;">(piece_state)
</span><span style="color: #008080;"> 64</span>             <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span><span style="color: #000000;"> page_url:
</span><span style="color: #008080;"> 65</span>                 page_url = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 66</span>             url = page_url + <span style="color: #800000;">'</span><span style="color: #800000;">?</span><span style="color: #800000;">'</span> +<span style="color: #000000;"> piece_request
</span><span style="color: #008080;"> 67</span>             <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">http://</span><span style="color: #800000;">'</span>+web_addr+<span style="color: #000000;">url
</span><span style="color: #008080;"> 68</span>             <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 69</span> <span style="color: #000000;">                tracker_con.connect()
</span><span style="color: #008080;"> 70</span>                 tracker_con.request(<span style="color: #800000;">"</span><span style="color: #800000;">GET</span><span style="color: #800000;">"</span><span style="color: #000000;">, url)
</span><span style="color: #008080;"> 71</span>                 response =<span style="color: #000000;"> tracker_con.getresponse() 
</span><span style="color: #008080;"> 72</span>                 <span style="color: #0000ff;">print</span><span style="color: #000000;">  response.status, response.reason
</span><span style="color: #008080;"> 73</span>                 <span style="color: #0000ff;">if</span> response.reason.upper() != <span style="color: #800000;">'</span><span style="color: #800000;">OK</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 74</span>                     <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! piece_index:%d</span><span style="color: #800000;">'</span> %(response.reason, self.<span style="color: #800080;">__piece_index</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 75</span> <span style="color: #000000;">                    tracker_con.close()
</span><span style="color: #008080;"> 76</span>                     <span style="color: #008000;">#</span><span style="color: #008000;">tracker_addr = self.__get_valid_tracker(tracker_addr)</span>
<span style="color: #008080;"> 77</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;"> 78</span>                 msg_encoded =<span style="color: #000000;"> response.read()
</span><span style="color: #008080;"> 79</span> <span style="color: #000000;">                tracker_con.close()
</span><span style="color: #008080;"> 80</span>                 rsp_msg =<span style="color: #000000;"> bcodec.bdecode(msg_encoded)
</span><span style="color: #008080;"> 81</span>                 <span style="color: #0000ff;">if</span> rsp_msg ==<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 82</span>                     <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! piece_index:%d</span><span style="color: #800000;">'</span> %(msg_encoded, self.<span style="color: #800080;">__piece_index</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 83</span>                     <span style="color: #008000;">#</span><span style="color: #008000;">tracker_addr = self.__get_valid_tracker(tracker_addr)</span>
<span style="color: #008080;"> 84</span>                     <span style="color: #0000ff;">break</span>
<span style="color: #008080;"> 85</span>                 
<span style="color: #008080;"> 86</span>             <span style="color: #0000ff;">except</span><span style="color: #000000;"> Exception,e:
</span><span style="color: #008080;"> 87</span> <span style="color: #000000;">                tracker_con.close()
</span><span style="color: #008080;"> 88</span>                 <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! piece_index:%d</span><span style="color: #800000;">'</span> %(e.message, self.<span style="color: #800080;">__piece_index</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 89</span>                 <span style="color: #008000;">#</span><span style="color: #008000;">tracker_addr = self.__get_valid_tracker(tracker_addr)</span>
<span style="color: #008080;"> 90</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;"> 91</span>             
<span style="color: #008080;"> 92</span>             <span style="color: #0000ff;">if</span> <span style="color: #800000;">'</span><span style="color: #800000;">failure reason</span><span style="color: #800000;">'</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> rsp_msg.keys():
</span><span style="color: #008080;"> 93</span>                 <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">Get tracker info error:%s! piece_index:%d</span><span style="color: #800000;">'</span> %(rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">failure reason</span><span style="color: #800000;">'</span>], self.<span style="color: #800080;">__piece_index</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 94</span>                 <span style="color: #008000;">#</span><span style="color: #008000;">tracker_addr = self.__get_valid_tracker(tracker_addr)</span>
<span style="color: #008080;"> 95</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;"> 96</span>              
<span style="color: #008080;"> 97</span>             peers_msg = rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">peers</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;"> 98</span>             peer_list =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 99</span>             <span style="color: #0000ff;">if</span> type(peers_msg) == type(<span style="color: #800000;">''</span><span style="color: #000000;">):
</span><span style="color: #008080;">100</span>                 <span style="color: #0000ff;">for</span> i <span style="color: #0000ff;">in</span> range(0,len(peers_msg)-5,6<span style="color: #000000;">):
</span><span style="color: #008080;">101</span>                     one_peer = peers_msg[i:i+6<span style="color: #000000;">]
</span><span style="color: #008080;">102</span>                     peer_id = <span style="color: #800000;">''</span>
<span style="color: #008080;">103</span>                     ip = one_peer[0:4<span style="color: #000000;">]
</span><span style="color: #008080;">104</span>                     port = one_peer[4:6<span style="color: #000000;">]
</span><span style="color: #008080;">105</span>                     ip = <span style="color: #800000;">'</span><span style="color: #800000;">%d.%d.%d.%d</span><span style="color: #800000;">'</span> %(ord(ip[0]),ord(ip[1]),ord(ip[2]),ord(ip[3<span style="color: #000000;">]),)
</span><span style="color: #008080;">106</span>                     port = ord(port[0])*255+ord(port[1<span style="color: #000000;">])
</span><span style="color: #008080;">107</span>                     peer_list.append({<span style="color: #800000;">'</span><span style="color: #800000;">peer_id</span><span style="color: #800000;">'</span>:peer_id,<span style="color: #800000;">'</span><span style="color: #800000;">ip</span><span style="color: #800000;">'</span>:ip,<span style="color: #800000;">'</span><span style="color: #800000;">port</span><span style="color: #800000;">'</span><span style="color: #000000;">:port})
</span><span style="color: #008080;">108</span>                 rsp_msg[<span style="color: #800000;">'</span><span style="color: #800000;">peers</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> peer_list   
</span><span style="color: #008080;">109</span>             self.<span style="color: #800080;">__tracker_addr</span> =<span style="color: #000000;"> tracker_addr
</span><span style="color: #008080;">110</span>             self.<span style="color: #800080;">__tracker_rsp</span> =<span style="color: #000000;"> rsp_msg
</span><span style="color: #008080;">111</span>             <span style="color: #0000ff;">break</span>
<span style="color: #008080;">112</span>         <span style="color: #0000ff;">pass</span>
<span style="color: #008080;">113</span>     
<span style="color: #008080;">114</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__generate_request</span><span style="color: #000000;">(self, piece_state):
</span><span style="color: #008080;">115</span>         
<span style="color: #008080;">116</span>         downloaded = piece_state[<span style="color: #800000;">'</span><span style="color: #800000;">downloaded</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">117</span>         uploaded = piece_state[<span style="color: #800000;">'</span><span style="color: #800000;">uploaded</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">118</span>         left = piece_state[<span style="color: #800000;">'</span><span style="color: #800000;">left</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">119</span>         event = piece_state[<span style="color: #800000;">'</span><span style="color: #800000;">event</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">120</span>         request =<span style="color: #000000;"> {}
</span><span style="color: #008080;">121</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">info_hash</span><span style="color: #800000;">'</span>] = piece_state[<span style="color: #800000;">'</span><span style="color: #800000;">info_hash</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">122</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">peer_id</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__peer_id</span>
<span style="color: #008080;">123</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">ip</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__host_ip</span>
<span style="color: #008080;">124</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">port</span><span style="color: #800000;">'</span>] = self.<span style="color: #800080;">__host_port</span>
<span style="color: #008080;">125</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">uploaded</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> uploaded
</span><span style="color: #008080;">126</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">downloaded</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> downloaded
</span><span style="color: #008080;">127</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">left</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> left
</span><span style="color: #008080;">128</span>         request[<span style="color: #800000;">'</span><span style="color: #800000;">event</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> event
</span><span style="color: #008080;">129</span>         request =<span style="color: #000000;"> urllib.urlencode(request)
</span><span style="color: #008080;">130</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> request
</span><span style="color: #008080;">131</span>     
<span style="color: #008080;">132</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__get_valid_tracker</span>(self, old_tracker=<span style="color: #000000;">None):
</span><span style="color: #008080;">133</span>         
<span style="color: #008080;">134</span>         tracker_addr =<span style="color: #000000;"> None
</span><span style="color: #008080;">135</span>         
<span style="color: #008080;">136</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__annouce_list</span> == None <span style="color: #0000ff;">or</span> len(self.<span style="color: #800080;">__annouce_list</span>) ==<span style="color: #000000;"> 0:
</span><span style="color: #008080;">137</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;">138</span>         
<span style="color: #008080;">139</span>         tracker_con =<span style="color: #000000;"> None
</span><span style="color: #008080;">140</span>         found_current =<span style="color: #000000;"> False
</span><span style="color: #008080;">141</span>         <span style="color: #0000ff;">for</span> tier <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__annouce_list</span><span style="color: #000000;">:
</span><span style="color: #008080;">142</span>             <span style="color: #0000ff;">for</span> announce <span style="color: #0000ff;">in</span><span style="color: #000000;"> tier:
</span><span style="color: #008080;">143</span>                 <span style="color: #008000;">#</span><span style="color: #008000;">print tracker_addr</span>
<span style="color: #008080;">144</span>                 m = re.match(r<span style="color: #800000;">'</span><span style="color: #800000;">(http://)([^/,:]*)(:(\d*))?(/.*)?</span><span style="color: #800000;">'</span><span style="color: #000000;">,announce)
</span><span style="color: #008080;">145</span>                 <span style="color: #0000ff;">if</span> m !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">146</span>                     web_addr = m.groups()[1<span style="color: #000000;">]
</span><span style="color: #008080;">147</span>                     web_port = m.groups()[3<span style="color: #000000;">]
</span><span style="color: #008080;">148</span>                     page_url = m.groups()[4<span style="color: #000000;">]
</span><span style="color: #008080;">149</span>                 <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">150</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;">151</span>                 
<span style="color: #008080;">152</span>                 <span style="color: #0000ff;">if</span> web_port !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">153</span>                     web_port =<span style="color: #000000;"> int(web_port)
</span><span style="color: #008080;">154</span>                 <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">155</span>                     web_port = 80
<span style="color: #008080;">156</span>                     
<span style="color: #008080;">157</span>                 <span style="color: #0000ff;">if</span> old_tracker !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">158</span>                     <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span><span style="color: #000000;"> found_current:
</span><span style="color: #008080;">159</span>                         <span style="color: #0000ff;">if</span> old_tracker ==<span style="color: #000000;"> (web_addr,web_port,page_url):
</span><span style="color: #008080;">160</span>                             found_current =<span style="color: #000000;"> True
</span><span style="color: #008080;">161</span>                         <span style="color: #0000ff;">continue</span>
<span style="color: #008080;">162</span>                     
<span style="color: #008080;">163</span>                 tracker_con = httplib.HTTPConnection(web_addr, web_port,timeout=self.<span style="color: #800080;">__tracker_check_timeout</span><span style="color: #000000;">) 
</span><span style="color: #008080;">164</span>                 <span style="color: #0000ff;">try</span><span style="color: #000000;">: 
</span><span style="color: #008080;">165</span> <span style="color: #000000;">                    tracker_con.connect()
</span><span style="color: #008080;">166</span>                 <span style="color: #0000ff;">except</span><span style="color: #000000;"> Exception, e:
</span><span style="color: #008080;">167</span>                     <span style="color: #0000ff;">print</span><span style="color: #000000;"> e
</span><span style="color: #008080;">168</span>                     <span style="color: #0000ff;">continue</span>
<span style="color: #008080;">169</span>                
<span style="color: #008080;">170</span> <span style="color: #000000;">                tier.remove(announce)
</span><span style="color: #008080;">171</span> <span style="color: #000000;">                tier.insert(0,announce)
</span><span style="color: #008080;">172</span> <span style="color: #000000;">                tracker_con.close()
</span><span style="color: #008080;">173</span>                 tracker_addr =<span style="color: #000000;"> (web_addr,web_port, page_url)
</span><span style="color: #008080;">174</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">175</span>             
<span style="color: #008080;">176</span>             <span style="color: #008000;">#</span><span style="color: #008000;"># tiers sorting, none standard</span>
<span style="color: #008080;">177</span>             <span style="color: #0000ff;">if</span> tracker_addr !=<span style="color: #000000;"> None:
</span><span style="color: #008080;">178</span>                 self.<span style="color: #800080;">__annouce_list</span><span style="color: #000000;">.remove(tier)
</span><span style="color: #008080;">179</span>                 self.<span style="color: #800080;">__annouce_list</span><span style="color: #000000;">.insert(0,tier)
</span><span style="color: #008080;">180</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">181</span>         <span style="color: #0000ff;">return</span> tracker_addr</pre>
</div>
</div>



<pre>
referer:http://www.cnblogs.com/piaoliu/archive/2012/10/02/2710517.html
</pre>
