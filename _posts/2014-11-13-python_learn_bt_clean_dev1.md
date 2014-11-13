---
layout: post
title: "Python边学边用--BT客户端实现之（一）BitTorrent文件解析"
categories: python
tags: [python, bt开发, dht开发, 系列教程]
date: 2014-11-13 11:44:59
---

<h2 class="postTitle">BitTorrent文件解析：</h2>
<div class="postText">
<div id="cnblogs_post_body">
<p>BitTorrent文件使用bencode编码，其中包括了4种数据类型：</p>
<p>'d' 开头表示是dict类型，'e'表示结束</p>
<p>'l' （小写字母L）开头表示是list类型，'e'表示结束</p>
<p>'i'开头表示是integer类型，'e'表示结束，可以表示负数</p>
<p>以数字开头表示string类型，数字为string长度，长度与string内容以':'分割</p>
<p>默认所有text类型的属性为utf-8编码，但是大多数BitTorrent包含codepage 和 encoding属性，指定了text的编码格式</p>
<p>"announce" -- tracker服务器的地址，为string<br />"info" ---文件信息，为dict类型<br />	   　　"name" --单文件模式，表示文件名，多文件模式表示根目录名。<br />	   　　"length" --单文件模式表示文件长度，多文件模式不存在<br />	   　　"piece length" --文件分片大小<br />	   　　"pieces" --为一个长string, 没20个字节表示一个分片的SHA1 hash值。按照文件分片的顺序排列。<br />	              　　　　　　　　分片是按照所以文件组合在一起进行的，即一个分片可能会跨越多个文件。<br />	   　　"files"  -- 多文件模式存在，为一个文件列表，每个文件为一个dict类型<br />	   				　　　　　　"path"  -- 文件目录列表，最后一项为文件名<br />	   				　　　　　　"length" --文件长度</p>
<p>"peace length" &nbsp;--分片大小</p>
<p>以下为draft bep定义的属性<br />"code page"<br />"announce-list" --tracker列表，为二维数组，即将tracker服务器分为多个组<br />"encoding"  -- Text属性的编码类型，string 类型，如 UTF-8<br />"publisher" -- 发布者<br />"publisher url"  --发布者 URL<br />"creater"        --创建者，如btcomet,btspirit<br />"creation date"  --创建日期，为UTC格式，需要转化为本地时区可读格式<br />"commnent"       --注释<br />"nodes"          -- DHT 节点列表</p>
<p>BitTorrent的标准参见：<a href="http://www.bittorrent.org/beps/bep_0003.html">http://www.bittorrent.org/beps/bep_0003.html</a></p>
<p>以下是自己写的Python实现，初学Python，代码写起来还都是C/C++风格，慢慢改进吧。</p>
<p>&nbsp;修改代码，bittorrent文件的解码使用异常处理解决文件格式错误的情况，简化处理过程。</p>
<div class="cnblogs_code" onclick="cnblogs_code_show('5f3991fc-1b39-4379-ab48-1bdcfa23f609')"><img id="code_img_closed_5f3991fc-1b39-4379-ab48-1bdcfa23f609" class="code_img_closed" src="http://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif" alt="" /><img id="code_img_opened_5f3991fc-1b39-4379-ab48-1bdcfa23f609" class="code_img_opened" style="display: none;" onclick="cnblogs_code_hide('5f3991fc-1b39-4379-ab48-1bdcfa23f609',event)" src="http://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif" alt="" /><span class="cnblogs_code_collapse">bcodec </span>
<div id="cnblogs_code_open_5f3991fc-1b39-4379-ab48-1bdcfa23f609" class="cnblogs_code_hide">
<pre><span style="color: #008080;">  1</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  2</span> <span style="color: #800000;">Created on 2012-9-30
</span><span style="color: #008080;">  3</span> 
<span style="color: #008080;">  4</span> <span style="color: #800000;">@author: ddt
</span><span style="color: #008080;">  5</span> <span style="color: #800000;">'''</span>
<span style="color: #008080;">  6</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> DataEncodedError(BaseException):
</span><span style="color: #008080;">  7</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__str__</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">  8</span>         <span style="color: #0000ff;">return</span> <span style="color: #800000;">'</span><span style="color: #800000;">Data Encoded Error</span><span style="color: #800000;">'</span>
<span style="color: #008080;">  9</span> 
<span style="color: #008080;"> 10</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> DataTypeError(BaseException):
</span><span style="color: #008080;"> 11</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__str__</span><span style="color: #000000;">(self):
</span><span style="color: #008080;"> 12</span>         <span style="color: #0000ff;">return</span> <span style="color: #800000;">'</span><span style="color: #800000;">Data Type Error</span><span style="color: #800000;">'</span>
<span style="color: #008080;"> 13</span>     
<span style="color: #008080;"> 14</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> bdecode(data):
</span><span style="color: #008080;"> 15</span>     <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 16</span>         leading_chr =<span style="color: #000000;"> data[0]
</span><span style="color: #008080;"> 17</span>         <span style="color: #008000;">#</span><span style="color: #008000;">print leading_chr,                 </span>
<span style="color: #008080;"> 18</span>         <span style="color: #0000ff;">if</span><span style="color: #000000;"> leading_chr.isdigit():
</span><span style="color: #008080;"> 19</span>             chunk, length =<span style="color: #000000;"> _read_string(data)
</span><span style="color: #008080;"> 20</span>             <span style="color: #008000;">#</span><span style="color: #008000;">print chunk</span>
<span style="color: #008080;"> 21</span>         <span style="color: #0000ff;">elif</span> leading_chr == <span style="color: #800000;">'</span><span style="color: #800000;">d</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 22</span>             chunk, length =<span style="color: #000000;"> _read_dict(data)
</span><span style="color: #008080;"> 23</span>             <span style="color: #008000;">#</span><span style="color: #008000;">print chunk is None</span>
<span style="color: #008080;"> 24</span>         <span style="color: #0000ff;">elif</span> leading_chr == <span style="color: #800000;">'</span><span style="color: #800000;">i</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 25</span>             chunk, length =<span style="color: #000000;"> _read_integer(data)
</span><span style="color: #008080;"> 26</span>             <span style="color: #008000;">#</span><span style="color: #008000;">print chunk</span>
<span style="color: #008080;"> 27</span>         <span style="color: #0000ff;">elif</span> leading_chr == <span style="color: #800000;">'</span><span style="color: #800000;">l</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 28</span>             chunk, length =<span style="color: #000000;"> _read_list(data)
</span><span style="color: #008080;"> 29</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 30</span>             <span style="color: #0000ff;">raise</span><span style="color: #000000;"> DataEncodedError()
</span><span style="color: #008080;"> 31</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> chunk, length
</span><span style="color: #008080;"> 32</span>     <span style="color: #0000ff;">except</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 33</span>         <span style="color: #0000ff;">raise</span><span style="color: #000000;"> DataEncodedError()
</span><span style="color: #008080;"> 34</span>     
<span style="color: #008080;"> 35</span>                            
<span style="color: #008080;"> 36</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _read_dict(data):
</span><span style="color: #008080;"> 37</span>     chunk =<span style="color: #000000;"> {} 
</span><span style="color: #008080;"> 38</span>     length = 1
<span style="color: #008080;"> 39</span>     
<span style="color: #008080;"> 40</span>     <span style="color: #0000ff;">while</span> data[length] != <span style="color: #800000;">'</span><span style="color: #800000;">e</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 41</span>         key, key_len =<span style="color: #000000;"> bdecode(data[length:])
</span><span style="color: #008080;"> 42</span>         length +=<span style="color: #000000;"> key_len
</span><span style="color: #008080;"> 43</span>         
<span style="color: #008080;"> 44</span>         value, value_len =<span style="color: #000000;"> bdecode(data[length:])
</span><span style="color: #008080;"> 45</span>         length +=<span style="color: #000000;"> value_len
</span><span style="color: #008080;"> 46</span>         
<span style="color: #008080;"> 47</span>         chunk[key] =<span style="color: #000000;"> value
</span><span style="color: #008080;"> 48</span>         <span style="color: #008000;">#</span><span style="color: #008000;">print key</span>
<span style="color: #008080;"> 49</span>         
<span style="color: #008080;"> 50</span>     length += 1
<span style="color: #008080;"> 51</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> chunk, length
</span><span style="color: #008080;"> 52</span> 
<span style="color: #008080;"> 53</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _read_list(data):
</span><span style="color: #008080;"> 54</span>     chunk =<span style="color: #000000;"> []
</span><span style="color: #008080;"> 55</span>     length = 1
<span style="color: #008080;"> 56</span>     <span style="color: #0000ff;">while</span> data[length] != <span style="color: #800000;">'</span><span style="color: #800000;">e</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 57</span>         value, value_len =<span style="color: #000000;"> bdecode(data[length:])
</span><span style="color: #008080;"> 58</span> <span style="color: #000000;">        chunk.append(value)
</span><span style="color: #008080;"> 59</span>         length +=<span style="color: #000000;"> value_len  
</span><span style="color: #008080;"> 60</span>         
<span style="color: #008080;"> 61</span>     length += 1
<span style="color: #008080;"> 62</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> chunk, length
</span><span style="color: #008080;"> 63</span> 
<span style="color: #008080;"> 64</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _read_string(data):
</span><span style="color: #008080;"> 65</span>     comm_index = data.find(<span style="color: #800000;">'</span><span style="color: #800000;">:</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 66</span>     str_len =<span style="color: #000000;"> int(data[:comm_index])
</span><span style="color: #008080;"> 67</span>     value = data[comm_index+1:comm_index+1+<span style="color: #000000;">str_len]
</span><span style="color: #008080;"> 68</span>     
<span style="color: #008080;"> 69</span>     length = comm_index + 1 +<span style="color: #000000;"> str_len
</span><span style="color: #008080;"> 70</span>     <span style="color: #0000ff;">return</span> <span style="color: #800000;">''</span><span style="color: #000000;">.join(value), length
</span><span style="color: #008080;"> 71</span> 
<span style="color: #008080;"> 72</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _read_integer(data):
</span><span style="color: #008080;"> 73</span> 
<span style="color: #008080;"> 74</span>     end_index = data.find(<span style="color: #800000;">'</span><span style="color: #800000;">e</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 75</span>     value = int(data[1<span style="color: #000000;">:end_index])
</span><span style="color: #008080;"> 76</span>     length = end_index + 1
<span style="color: #008080;"> 77</span>     
<span style="color: #008080;"> 78</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;">  value, length
</span><span style="color: #008080;"> 79</span> 
<span style="color: #008080;"> 80</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> bencode(data):
</span><span style="color: #008080;"> 81</span>     data_type =<span style="color: #000000;"> type(data)
</span><span style="color: #008080;"> 82</span>     <span style="color: #0000ff;">if</span> data_type ==<span style="color: #000000;"> type({}):
</span><span style="color: #008080;"> 83</span>         result =<span style="color: #000000;"> _write_dict(data)
</span><span style="color: #008080;"> 84</span>     <span style="color: #0000ff;">elif</span> data_type ==<span style="color: #000000;"> type([]):
</span><span style="color: #008080;"> 85</span>         result =<span style="color: #000000;"> _write_list(data)
</span><span style="color: #008080;"> 86</span>     <span style="color: #0000ff;">elif</span> data_type == type(<span style="color: #800000;">''</span><span style="color: #000000;">):
</span><span style="color: #008080;"> 87</span>         result =<span style="color: #000000;"> _write_string(data)
</span><span style="color: #008080;"> 88</span>     <span style="color: #0000ff;">elif</span> data_type ==<span style="color: #000000;"> type(int(0)):
</span><span style="color: #008080;"> 89</span>         result =<span style="color: #000000;"> _write_integer(data)
</span><span style="color: #008080;"> 90</span>     <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 91</span>         <span style="color: #0000ff;">raise</span><span style="color: #000000;"> DataTypeError()
</span><span style="color: #008080;"> 92</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> result
</span><span style="color: #008080;"> 93</span> 
<span style="color: #008080;"> 94</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _write_dict(data):
</span><span style="color: #008080;"> 95</span>     result = <span style="color: #800000;">'</span><span style="color: #800000;">d</span><span style="color: #800000;">'</span>
<span style="color: #008080;"> 96</span>     <span style="color: #0000ff;">for</span> key, value <span style="color: #0000ff;">in</span><span style="color: #000000;"> data.items():
</span><span style="color: #008080;"> 97</span>         key_encode =<span style="color: #000000;"> bencode(key)
</span><span style="color: #008080;"> 98</span>         value_encode =<span style="color: #000000;"> bencode(value)
</span><span style="color: #008080;"> 99</span>         result +=<span style="color: #000000;"> key_encode
</span><span style="color: #008080;">100</span>         result +=<span style="color: #000000;"> value_encode
</span><span style="color: #008080;">101</span> 
<span style="color: #008080;">102</span>     result += <span style="color: #800000;">'</span><span style="color: #800000;">e</span><span style="color: #800000;">'</span>
<span style="color: #008080;">103</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> result
</span><span style="color: #008080;">104</span> 
<span style="color: #008080;">105</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _write_list(data):
</span><span style="color: #008080;">106</span>     result = <span style="color: #800000;">'</span><span style="color: #800000;">l</span><span style="color: #800000;">'</span>
<span style="color: #008080;">107</span>     <span style="color: #0000ff;">for</span> value <span style="color: #0000ff;">in</span><span style="color: #000000;"> data:
</span><span style="color: #008080;">108</span>         value_encode =<span style="color: #000000;"> bencode(value)
</span><span style="color: #008080;">109</span>         result +=<span style="color: #000000;"> value_encode
</span><span style="color: #008080;">110</span>         
<span style="color: #008080;">111</span>     result += <span style="color: #800000;">'</span><span style="color: #800000;">e</span><span style="color: #800000;">'</span>
<span style="color: #008080;">112</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> result
</span><span style="color: #008080;">113</span> 
<span style="color: #008080;">114</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _write_string(data):
</span><span style="color: #008080;">115</span>     <span style="color: #0000ff;">return</span> <span style="color: #800000;">'</span><span style="color: #800000;">%d:%s</span><span style="color: #800000;">'</span> %<span style="color: #000000;">(len(data), data)
</span><span style="color: #008080;">116</span> 
<span style="color: #008080;">117</span> <span style="color: #0000ff;">def</span><span style="color: #000000;"> _write_integer(data):
</span><span style="color: #008080;">118</span>     <span style="color: #0000ff;">return</span> <span style="color: #800000;">'</span><span style="color: #800000;">i%de</span><span style="color: #800000;">'</span> %<span style="color: #000000;">data
</span><span style="color: #008080;">119</span> 
<span style="color: #008080;">120</span>     </pre>
</div>
</div>
<div class="cnblogs_code" onclick="cnblogs_code_show('576e68bd-1fb9-49cf-8fa2-c690d5b8b6ba')"><img id="code_img_closed_576e68bd-1fb9-49cf-8fa2-c690d5b8b6ba" class="code_img_closed" src="http://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif" alt="" /><img id="code_img_opened_576e68bd-1fb9-49cf-8fa2-c690d5b8b6ba" class="code_img_opened" style="display: none;" onclick="cnblogs_code_hide('576e68bd-1fb9-49cf-8fa2-c690d5b8b6ba',event)" src="http://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif" alt="" /><span class="cnblogs_code_collapse">torrent_file.py</span>
<div id="cnblogs_code_open_576e68bd-1fb9-49cf-8fa2-c690d5b8b6ba" class="cnblogs_code_hide">
<pre><span style="color: #008080;">  1</span> <span style="color: #0000ff;">from</span> datetime <span style="color: #0000ff;">import</span><span style="color: #000000;"> datetime
</span><span style="color: #008080;">  2</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> bcodec
</span><span style="color: #008080;">  3</span> <span style="color: #0000ff;">import</span><span style="color: #000000;"> hashlib
</span><span style="color: #008080;">  4</span> 
<span style="color: #008080;">  5</span> _READ_MAX_LEN = -1
<span style="color: #008080;">  6</span> 
<span style="color: #008080;">  7</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> BTFormatError(BaseException):
</span><span style="color: #008080;">  8</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__str__</span><span style="color: #000000;">(self):
</span><span style="color: #008080;">  9</span>         <span style="color: #0000ff;">return</span> <span style="color: #800000;">'</span><span style="color: #800000;">Torrent File Format Error</span><span style="color: #800000;">'</span>
<span style="color: #008080;"> 10</span> 
<span style="color: #008080;"> 11</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> TorrentFile(object):
</span><span style="color: #008080;"> 12</span>     
<span style="color: #008080;"> 13</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__init__</span><span style="color: #000000;">(self):    
</span><span style="color: #008080;"> 14</span>         self.<span style="color: #800080;">__metainfo</span> =<span style="color: #000000;"> {}
</span><span style="color: #008080;"> 15</span>         self.<span style="color: #800080;">__file_name</span> = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 16</span>         self.<span style="color: #800080;">__bencode_data</span> =<span style="color: #000000;"> None
</span><span style="color: #008080;"> 17</span>     
<span style="color: #008080;"> 18</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> read_file(self, filename):
</span><span style="color: #008080;"> 19</span>         
<span style="color: #008080;"> 20</span>         torrent_file = open(filename, <span style="color: #800000;">'</span><span style="color: #800000;">rb</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 21</span>         data =<span style="color: #000000;"> torrent_file.read(_READ_MAX_LEN)
</span><span style="color: #008080;"> 22</span> <span style="color: #000000;">        torrent_file.close()
</span><span style="color: #008080;"> 23</span>         
<span style="color: #008080;"> 24</span>         <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 25</span>             metainfo, length =<span style="color: #000000;"> bcodec.bdecode(data)
</span><span style="color: #008080;"> 26</span>             self.<span style="color: #800080;">__file_name</span> =<span style="color: #000000;"> filename
</span><span style="color: #008080;"> 27</span>             self.<span style="color: #800080;">__metainfo</span> =<span style="color: #000000;"> metainfo
</span><span style="color: #008080;"> 28</span>             self.<span style="color: #800080;">__bencode_data</span> =<span style="color: #000000;"> data
</span><span style="color: #008080;"> 29</span>         <span style="color: #0000ff;">except</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 30</span>             <span style="color: #0000ff;">raise</span><span style="color: #000000;"> BTFormatError()
</span><span style="color: #008080;"> 31</span>         
<span style="color: #008080;"> 32</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__is_singlefile</span><span style="color: #000000;">(self):
</span><span style="color: #008080;"> 33</span>         
<span style="color: #008080;"> 34</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span>) !=<span style="color: #000000;"> None
</span><span style="color: #008080;"> 35</span>     
<span style="color: #008080;"> 36</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__decode_text</span><span style="color: #000000;">(self, text):
</span><span style="color: #008080;"> 37</span>         encoding = <span style="color: #800000;">'</span><span style="color: #800000;">utf-8</span><span style="color: #800000;">'</span>
<span style="color: #008080;"> 38</span>         resultstr = <span style="color: #800000;">''</span>
<span style="color: #008080;"> 39</span>         <span style="color: #0000ff;">if</span> self.get_encoding() !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 40</span>             encoding =<span style="color: #000000;"> self.get_encoding()
</span><span style="color: #008080;"> 41</span>         <span style="color: #0000ff;">elif</span> self.get_codepage() !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 42</span>             encoding = <span style="color: #800000;">'</span><span style="color: #800000;">cp</span><span style="color: #800000;">'</span> +<span style="color: #000000;"> str(self.get_codepage())
</span><span style="color: #008080;"> 43</span>         <span style="color: #0000ff;">if</span><span style="color: #000000;"> text:
</span><span style="color: #008080;"> 44</span>             <span style="color: #0000ff;">try</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 45</span>                 resultstr = text.decode(encoding=<span style="color: #000000;">encoding)
</span><span style="color: #008080;"> 46</span>             <span style="color: #0000ff;">except</span><span style="color: #000000;"> ValueError:
</span><span style="color: #008080;"> 47</span>                 <span style="color: #0000ff;">return</span><span style="color: #000000;"> text
</span><span style="color: #008080;"> 48</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 49</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;"> 50</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> resultstr
</span><span style="color: #008080;"> 51</span>     
<span style="color: #008080;"> 52</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__get_meta_top</span><span style="color: #000000;">(self, key):
</span><span style="color: #008080;"> 53</span>         <span style="color: #0000ff;">if</span> key <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__metainfo</span><span style="color: #000000;">.keys():
</span><span style="color: #008080;"> 54</span>             <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__metainfo</span><span style="color: #000000;">[key]
</span><span style="color: #008080;"> 55</span>         <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 56</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;"> 57</span>     <span style="color: #0000ff;">def</span> <span style="color: #800080;">__get_meta_info</span><span style="color: #000000;">(self,key):
</span><span style="color: #008080;"> 58</span>         meta_info = self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">info</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 59</span>         <span style="color: #0000ff;">if</span> meta_info != None <span style="color: #0000ff;">and</span> key <span style="color: #0000ff;">in</span><span style="color: #000000;"> meta_info.keys():
</span><span style="color: #008080;"> 60</span>                 <span style="color: #0000ff;">return</span><span style="color: #000000;"> meta_info[key]
</span><span style="color: #008080;"> 61</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;"> 62</span>     
<span style="color: #008080;"> 63</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_codepage(self):
</span><span style="color: #008080;"> 64</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">codepage</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 65</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_encoding(self):
</span><span style="color: #008080;"> 66</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">encoding</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 67</span>     
<span style="color: #008080;"> 68</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_announces(self):
</span><span style="color: #008080;"> 69</span>         announces = self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">announce-list</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 70</span>         <span style="color: #0000ff;">if</span> announces !=<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 71</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> announces
</span><span style="color: #008080;"> 72</span>         
<span style="color: #008080;"> 73</span>         announces =<span style="color: #000000;"> [[]]
</span><span style="color: #008080;"> 74</span>         ann = self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">announce</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 75</span>         <span style="color: #0000ff;">if</span><span style="color: #000000;"> ann:
</span><span style="color: #008080;"> 76</span> <span style="color: #000000;">            announces[0].append(ann)
</span><span style="color: #008080;"> 77</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> announces
</span><span style="color: #008080;"> 78</span>     
<span style="color: #008080;"> 79</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_publisher(self):
</span><span style="color: #008080;"> 80</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__decode_text</span>(self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">publisher</span><span style="color: #800000;">'</span><span style="color: #000000;">))
</span><span style="color: #008080;"> 81</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_publisher_url(self):
</span><span style="color: #008080;"> 82</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__decode_text</span>(self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">publisher-url</span><span style="color: #800000;">'</span><span style="color: #000000;">))
</span><span style="color: #008080;"> 83</span>     
<span style="color: #008080;"> 84</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_creater(self):
</span><span style="color: #008080;"> 85</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__decode_text</span>(self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">created by</span><span style="color: #800000;">'</span><span style="color: #000000;">))
</span><span style="color: #008080;"> 86</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_creation_date(self):
</span><span style="color: #008080;"> 87</span>         utc_date = self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">creation date</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 88</span>         <span style="color: #0000ff;">if</span> utc_date ==<span style="color: #000000;"> None:
</span><span style="color: #008080;"> 89</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> utc_date
</span><span style="color: #008080;"> 90</span>         creationdate =<span style="color: #000000;"> datetime.utcfromtimestamp(utc_date)
</span><span style="color: #008080;"> 91</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> creationdate
</span><span style="color: #008080;"> 92</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_comment(self):
</span><span style="color: #008080;"> 93</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">comment</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 94</span>           
<span style="color: #008080;"> 95</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_nodes(self):
</span><span style="color: #008080;"> 96</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__get_meta_top</span>(<span style="color: #800000;">'</span><span style="color: #800000;">nodes</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;"> 97</span>     
<span style="color: #008080;"> 98</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_piece_length(self):
</span><span style="color: #008080;"> 99</span>         <span style="color: #0000ff;">return</span> self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">piece length</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">100</span>     
<span style="color: #008080;">101</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_piece(self, index):
</span><span style="color: #008080;">102</span>         pieces = self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">pieces</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">103</span>         <span style="color: #0000ff;">if</span> pieces ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">104</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;">105</span>         
<span style="color: #008080;">106</span>         offset = index*20
<span style="color: #008080;">107</span>         <span style="color: #0000ff;">if</span> offset+20 &gt;<span style="color: #000000;"> len(pieces):
</span><span style="color: #008080;">108</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> None
</span><span style="color: #008080;">109</span>         <span style="color: #0000ff;">return</span> pieces[offset:offset+20<span style="color: #000000;">]
</span><span style="color: #008080;">110</span>     
<span style="color: #008080;">111</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_pieces_num(self):
</span><span style="color: #008080;">112</span>         <span style="color: #0000ff;">return</span> len(self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">pieces</span><span style="color: #800000;">'</span>))/20
<span style="color: #008080;">113</span>         
<span style="color: #008080;">114</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_files(self):
</span><span style="color: #008080;">115</span>         
<span style="color: #008080;">116</span>         files =<span style="color: #000000;"> []
</span><span style="color: #008080;">117</span>         name = self.<span style="color: #800080;">__decode_text</span>(self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">name</span><span style="color: #800000;">'</span><span style="color: #000000;">))
</span><span style="color: #008080;">118</span>         piece_length =<span style="color: #000000;"> self.get_piece_length()
</span><span style="color: #008080;">119</span>         <span style="color: #0000ff;">if</span> name ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">120</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> files
</span><span style="color: #008080;">121</span>         
<span style="color: #008080;">122</span>         <span style="color: #0000ff;">if</span> self.<span style="color: #800080;">__is_singlefile</span><span style="color: #000000;">():
</span><span style="color: #008080;">123</span>             file_name =<span style="color: #000000;"> name
</span><span style="color: #008080;">124</span>             file_length = self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">125</span>             <span style="color: #0000ff;">if</span> <span style="color: #0000ff;">not</span><span style="color: #000000;"> file_length:
</span><span style="color: #008080;">126</span>                 <span style="color: #0000ff;">return</span><span style="color: #000000;"> files
</span><span style="color: #008080;">127</span>             
<span style="color: #008080;">128</span>             pieces_num = file_length/<span style="color: #000000;">piece_length
</span><span style="color: #008080;">129</span>             last_piece_offset =  file_length %<span style="color: #000000;"> piece_length
</span><span style="color: #008080;">130</span>             <span style="color: #0000ff;">if</span> last_piece_offset !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">131</span>                 pieces_num = int(pieces_num) + 1
<span style="color: #008080;">132</span>                 last_piece_offset -= 1
<span style="color: #008080;">133</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">134</span>                 last_piece_offset = piece_length - 1
<span style="color: #008080;">135</span> 
<span style="color: #008080;">136</span>             first_piece_offset =<span style="color: #000000;"> 0
</span><span style="color: #008080;">137</span>             
<span style="color: #008080;">138</span>             files.append({<span style="color: #800000;">'</span><span style="color: #800000;">name</span><span style="color: #800000;">'</span>:[file_name], <span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span>:file_length, <span style="color: #800000;">'</span><span style="color: #800000;">first-piece</span><span style="color: #800000;">'</span>:(0, first_piece_offset), <span style="color: #800000;">'</span><span style="color: #800000;">last-piece</span><span style="color: #800000;">'</span>:(pieces_num-1<span style="color: #000000;">,last_piece_offset)})
</span><span style="color: #008080;">139</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> files
</span><span style="color: #008080;">140</span>         
<span style="color: #008080;">141</span>         folder =<span style="color: #000000;"> name
</span><span style="color: #008080;">142</span>         meta_files = self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">files</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">143</span>         <span style="color: #0000ff;">if</span> meta_files ==<span style="color: #000000;"> None:
</span><span style="color: #008080;">144</span>             <span style="color: #0000ff;">return</span><span style="color: #000000;"> files
</span><span style="color: #008080;">145</span>         
<span style="color: #008080;">146</span>         total_length =<span style="color: #000000;"> int(0)
</span><span style="color: #008080;">147</span>         <span style="color: #0000ff;">for</span> one_file <span style="color: #0000ff;">in</span> self.<span style="color: #800080;">__get_meta_info</span>(<span style="color: #800000;">'</span><span style="color: #800000;">files</span><span style="color: #800000;">'</span><span style="color: #000000;">):
</span><span style="color: #008080;">148</span>             
<span style="color: #008080;">149</span>             file_info =<span style="color: #000000;"> {}
</span><span style="color: #008080;">150</span>             path_list =<span style="color: #000000;"> []
</span><span style="color: #008080;">151</span> <span style="color: #000000;">            path_list.append(folder)
</span><span style="color: #008080;">152</span>                         
<span style="color: #008080;">153</span>             <span style="color: #0000ff;">if</span> <span style="color: #800000;">'</span><span style="color: #800000;">path</span><span style="color: #800000;">'</span> <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> one_file.keys():
</span><span style="color: #008080;">154</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">155</span>             <span style="color: #0000ff;">for</span> path <span style="color: #0000ff;">in</span> one_file[<span style="color: #800000;">'</span><span style="color: #800000;">path</span><span style="color: #800000;">'</span><span style="color: #000000;">]:
</span><span style="color: #008080;">156</span>                 path_list.append(self.<span style="color: #800080;">__decode_text</span><span style="color: #000000;">(path))
</span><span style="color: #008080;">157</span>             file_info[<span style="color: #800000;">'</span><span style="color: #800000;">name</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> path_list
</span><span style="color: #008080;">158</span>             
<span style="color: #008080;">159</span>             <span style="color: #0000ff;">if</span> <span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span> <span style="color: #0000ff;">not</span> <span style="color: #0000ff;">in</span><span style="color: #000000;"> one_file.keys():
</span><span style="color: #008080;">160</span>                 <span style="color: #0000ff;">break</span>
<span style="color: #008080;">161</span>             
<span style="color: #008080;">162</span>             file_info[<span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span>] =  one_file[<span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">163</span>             
<span style="color: #008080;">164</span>             piece_index = total_length /<span style="color: #000000;"> piece_length
</span><span style="color: #008080;">165</span>             first_piece_offset =  total_length %<span style="color: #000000;"> piece_length
</span><span style="color: #008080;">166</span>             
<span style="color: #008080;">167</span>             total_length += one_file[<span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">168</span>             pieces_num = total_length / piece_length -<span style="color: #000000;"> piece_index
</span><span style="color: #008080;">169</span>             last_piece_offset = total_length %<span style="color: #000000;"> piece_length
</span><span style="color: #008080;">170</span>             
<span style="color: #008080;">171</span>             <span style="color: #0000ff;">if</span> last_piece_offset !=<span style="color: #000000;"> 0:
</span><span style="color: #008080;">172</span>                 pieces_num += 1
<span style="color: #008080;">173</span>                 last_piece_offset -= 1
<span style="color: #008080;">174</span>             <span style="color: #0000ff;">else</span><span style="color: #000000;">:
</span><span style="color: #008080;">175</span>                 last_piece_offset = piece_length - 1
<span style="color: #008080;">176</span>             
<span style="color: #008080;">177</span>             file_info[<span style="color: #800000;">'</span><span style="color: #800000;">first-piece</span><span style="color: #800000;">'</span>] =<span style="color: #000000;"> (piece_index,first_piece_offset)
</span><span style="color: #008080;">178</span>             file_info[<span style="color: #800000;">'</span><span style="color: #800000;">last-piece</span><span style="color: #800000;">'</span>] = ((piece_index+pieces_num-1<span style="color: #000000;">),last_piece_offset)
</span><span style="color: #008080;">179</span> <span style="color: #000000;">            files.append(file_info)
</span><span style="color: #008080;">180</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> files
</span><span style="color: #008080;">181</span>     
<span style="color: #008080;">182</span>     <span style="color: #0000ff;">def</span><span style="color: #000000;"> get_info_hash(self):
</span><span style="color: #008080;">183</span>         info_index = self.<span style="color: #800080;">__bencode_data</span>.find(<span style="color: #800000;">'</span><span style="color: #800000;">4:info</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">184</span>         info_data_index = info_index+len(<span style="color: #800000;">'</span><span style="color: #800000;">4:info</span><span style="color: #800000;">'</span><span style="color: #000000;">)
</span><span style="color: #008080;">185</span>         
<span style="color: #008080;">186</span>         info_value, info_data_len = bcodec.bdecode(self.<span style="color: #800080;">__bencode_data</span><span style="color: #000000;">[info_data_index:])
</span><span style="color: #008080;">187</span>         info_data = self.<span style="color: #800080;">__bencode_data</span>[info_data_index:info_data_index+<span style="color: #000000;">info_data_len]
</span><span style="color: #008080;">188</span>         
<span style="color: #008080;">189</span>         info_hash =<span style="color: #000000;"> hashlib.sha1()
</span><span style="color: #008080;">190</span> <span style="color: #000000;">        info_hash.update(info_data)
</span><span style="color: #008080;">191</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> info_hash.digest()
</span><span style="color: #008080;">192</span> 
<span style="color: #008080;">193</span>     
<span style="color: #008080;">194</span> <span style="color: #0000ff;">if</span> <span style="color: #800080;">__name__</span> == <span style="color: #800000;">'</span><span style="color: #800000;">__main__</span><span style="color: #800000;">'</span><span style="color: #000000;">:
</span><span style="color: #008080;">195</span>     filename = r<span style="color: #800000;">"</span><span style="color: #800000;">.\narodo.torrent</span><span style="color: #800000;">"</span>
<span style="color: #008080;">196</span> 
<span style="color: #008080;">197</span>     torrent =<span style="color: #000000;"> TorrentFile()
</span><span style="color: #008080;">198</span> 
<span style="color: #008080;">199</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">begin to read file</span><span style="color: #800000;">"</span>
<span style="color: #008080;">200</span> <span style="color: #000000;">    torrent.read_file(filename)
</span><span style="color: #008080;">201</span> 
<span style="color: #008080;">202</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">end to read file</span><span style="color: #800000;">"</span>
<span style="color: #008080;">203</span> 
<span style="color: #008080;">204</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">announces: </span><span style="color: #800000;">"</span><span style="color: #000000;"> , torrent.get_announces() 
</span><span style="color: #008080;">205</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">info_hash: </span><span style="color: #800000;">"</span><span style="color: #000000;">, list(torrent.get_info_hash())
</span><span style="color: #008080;">206</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">peace length:</span><span style="color: #800000;">"</span><span style="color: #000000;">, torrent.get_piece_length()
</span><span style="color: #008080;">207</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">code page:</span><span style="color: #800000;">"</span><span style="color: #000000;"> , torrent.get_codepage()
</span><span style="color: #008080;">208</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">encoding:</span><span style="color: #800000;">"</span><span style="color: #000000;"> , torrent.get_encoding()
</span><span style="color: #008080;">209</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">publisher:</span><span style="color: #800000;">"</span><span style="color: #000000;"> ,torrent.get_publisher()
</span><span style="color: #008080;">210</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">publisher url:</span><span style="color: #800000;">"</span><span style="color: #000000;">, torrent.get_publisher_url()
</span><span style="color: #008080;">211</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">creater:</span><span style="color: #800000;">"</span><span style="color: #000000;"> , torrent.get_creater()
</span><span style="color: #008080;">212</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">creation date:</span><span style="color: #800000;">"</span><span style="color: #000000;">, torrent.get_creation_date()
</span><span style="color: #008080;">213</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">commnent:</span><span style="color: #800000;">"</span><span style="color: #000000;">, torrent.get_comment()
</span><span style="color: #008080;">214</span>     <span style="color: #0000ff;">print</span> <span style="color: #800000;">"</span><span style="color: #800000;">nodes:</span><span style="color: #800000;">"</span><span style="color: #000000;">, torrent.get_nodes()
</span><span style="color: #008080;">215</span> <span style="color: #000000;">    torrent.get_files()
</span><span style="color: #008080;">216</span>     <span style="color: #0000ff;">for</span> one_file <span style="color: #0000ff;">in</span><span style="color: #000000;"> torrent.get_files():
</span><span style="color: #008080;">217</span>         <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">name:</span><span style="color: #800000;">'</span>, <span style="color: #800000;">'</span><span style="color: #800000;">\\</span><span style="color: #800000;">'</span>.join(one_file[<span style="color: #800000;">'</span><span style="color: #800000;">name</span><span style="color: #800000;">'</span><span style="color: #000000;">])
</span><span style="color: #008080;">218</span>         <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">length:</span><span style="color: #800000;">'</span>, one_file[<span style="color: #800000;">'</span><span style="color: #800000;">length</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">219</span>         <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">first-piece:</span><span style="color: #800000;">'</span>, one_file[<span style="color: #800000;">'</span><span style="color: #800000;">first-piece</span><span style="color: #800000;">'</span><span style="color: #000000;">]
</span><span style="color: #008080;">220</span>         <span style="color: #0000ff;">print</span> <span style="color: #800000;">'</span><span style="color: #800000;">last-piece:</span><span style="color: #800000;">'</span>, one_file[<span style="color: #800000;">'</span><span style="color: #800000;">last-piece</span><span style="color: #800000;">'</span>]</pre>
</div>
</div>
<p>&nbsp;</p>
</div>
</div>



<pre>
referer:http://www.cnblogs.com/piaoliu/archive/2012/09/29/2708984.html
</pre>
