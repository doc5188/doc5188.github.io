---
layout: post
title: "Linux Centos 系统上安装BT客户端 Transmission"
categories: linux
tags: [linux, transmission]
date: 2014-10-30 23:40:07
---

<p><span style="font-size: xx-large; float: left; font-weight: bolder; padding: 10px;">T</span>ransmission是一种BitTorrent客户端，特点是一个跨平台的后端和其上的简洁的用户界面，以MIT许可证和GNU通用公共许可证双许可证授权，因此是一款自由软件，还被众多linux发行版，包括Ubuntu、Mandriva、Mint、Fedora、Puppy、openSUSE 选作默认BT下载工具；Imageshack的服务使用其技术。</p>
<p>上面已经提到了很多种Linux系统都内置了这软件，可是使用最广的<span style="color: #ff0000;">Centos</span>居然无视掉了，情何以堪，只能靠自己了。</p>
<p>首先这个教程极其简单，如果已经是熟悉Linux的，建议编译源码安装，自由度更高，毕竟Linux追求的就是自由度。</p>
<p>在Linux Centos系统上编译源码安装Transmission的教程推荐<a href="http://520.be/1452-%E5%9C%A8vps%E4%B8%8A%E5%AE%89%E8%A3%9Dbt%E8%BB%9F%E9%AB%94transmission.html" target="_blank">这篇</a>。</p>
<p>文中一些基础命令不会详细写出，如果有问题的留言吧。好了，正式开始：</p>
<hr />
<p><strong>更新历史：</strong></p>
<p>2011/05/02 - 初次发布<br />
2011/05/30 - 更新至版本2.31（<a href="https://trac.transmissionbt.com/wiki/Changes" target="_blank">官方更新说明</a>），安装过程无改动。<br />
<span style="color: #ff0000;">暂停更新</span></p>
<hr />
<p><span id="more-275"></span></p>
<h2>前期准备</h2>
<ul>
<li>可选，<span style="color: #ff0000;">yum -y remove libevent libevent-devel</span> 先删掉这两个组件，因为有可能安装的时候发生冲突。</li>
<li>从<a href="http://geekery.blog.com/2011/03/09/transmission-2-22-daemon-cli/" target="_blank">这里</a>上对应版本下载全部的一套rpm包到一个目录中，如<span style="color: #ff0000;">/tmp</span>。教程使用的是2.22版和32位系统，更多更新可以关注这个<a href="http://geekery.blog.com/" target="_blank">博客</a>，<span style="color: #ff0000;">也可以从我的</span><a href="http://code.google.com/p/linux-trip/downloads/list" target="_blank">GoogleCode</a><span style="color: #ff0000;">里拿，包含最新的软件，已经打包成zip格式，使用时候先解压</span>。</li>
<li>导入证书
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">rpm <span class="re5">--import</span> http:<span class="sy0">//</span>geekery.altervista.org<span class="sy0">/</span>download.php?<span class="re2">filename</span>=GEEKERY-GPG-KEY</div></div>
</li>
</ul>
<h2>安装（注意顺序）</h2>
<h3>1、安装<span style="color: #ff0000;">libevent</span>的rpm包</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">rpm <span class="re5">-ivh</span> libevent-2.0.10-1geekery.i386.rpm<br />
Preparing... <span class="co0">########################################### [100%]</span><br />
<span class="nu0">1</span>:libevent <span class="co0">########################################### [100%]</span></div></div>
<h3>2、安装<span style="color: #ff0000;">transmission-common</span>的rpm包</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">rpm <span class="re5">-ivh</span> transmission-common-<span class="nu0">2.22</span>-1geekery.i386.rpm<br />
Preparing... <span class="co0">########################################### [100%]</span><br />
<span class="nu0">1</span>:transmission-common <span class="co0">########################################### [100%]</span></div></div>
<h3>3、安装<span style="color: #ff0000;">transmission-daemon</span>的rpm包</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">rpm <span class="re5">-ivh</span> transmission-daemon-<span class="nu0">2.22</span>-1geekery.i386.rpm<br />
Preparing... <span class="co0">########################################### [100%]</span><br />
<span class="nu0">1</span>:transmission-daemon <span class="co0">########################################### [100%]</span></div></div>
<h3>4、安装<span style="color: #ff0000;">transmission-cli</span>的rpm包</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">rpm <span class="re5">-ivh</span> transmission-cli-<span class="nu0">2.22</span>-1geekery.i386.rpm<br />
Preparing... <span class="co0">########################################### [100%]</span><br />
<span class="nu0">1</span>:transmission-cli <span class="co0">########################################### [100%]</span></div></div>
<h3>5、最后安装<span style="color: #ff0000;">transmission</span>的rpm包</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">rpm <span class="re5">-ivh</span> transmission-<span class="nu0">2.22</span>-1geekery.i386.rpm<br />
Preparing... <span class="co0">########################################### [100%]</span><br />
<span class="nu0">1</span>:transmission <span class="co0">########################################### [100%]</span></div></div>
<h2>配置</h2>
<h3>1、启动软件，以自动生成默认配置文件。</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">service transmission-daemon start<br />
Starting transmission-daemon: <span class="br0">&#91;</span> OK <span class="br0">&#93;</span></div></div>
<h3>2、然后关掉软件，或强行关闭掉，查看进程确保软件完全关闭。</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">service transmission-daemon stop<br />
<span class="kw2">killall</span> transmission-daemon</div></div>
<h3>3、编辑配置文件，有时候位置可能不同，请先用<span style="color: #ff0000;">locate</span>命令找下<span style="color: #ff0000;">transmission</span>文件夹的位置。</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer"><span class="kw2">vi</span> <span class="sy0">/</span>var<span class="sy0">/</span>lib<span class="sy0">/</span>transmission<span class="sy0">/</span>settings.json</div></div>
<blockquote><p>下面只标出主要参数的说明，详情可以参考<a href="https://trac.transmissionbt.com/wiki/EditConfigFiles" target="_blank">这里</a></p></blockquote>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer"><span class="br0">&#123;</span><br />
<span class="st0">&quot;alt-speed-down&quot;</span>: <span class="nu0">50</span>,<br />
<span class="st0">&quot;alt-speed-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;alt-speed-time-begin&quot;</span>: <span class="nu0">540</span>,<br />
<span class="st0">&quot;alt-speed-time-day&quot;</span>: <span class="nu0">127</span>,<br />
<span class="st0">&quot;alt-speed-time-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;alt-speed-time-end&quot;</span>: <span class="nu0">1020</span>,<br />
<span class="st0">&quot;alt-speed-up&quot;</span>: <span class="nu0">50</span>,<br />
<span class="st0">&quot;bind-address-ipv4&quot;</span>: <span class="st0">&quot;0.0.0.0&quot;</span>,<br />
<span class="st0">&quot;bind-address-ipv6&quot;</span>: <span class="st0">&quot;::&quot;</span>,<br />
<span class="st0">&quot;blocklist-enabled&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;blocklist-url&quot;</span>: <span class="st0">&quot;http://www.example.com/blocklist&quot;</span>,<br />
<span class="st0">&quot;cache-size-mb&quot;</span>: <span class="nu0">4</span>,<br />
<span class="st0">&quot;dht-enabled&quot;</span>: <span class="kw2">true</span>,   <span class="sy0">//</span>DHT支持<br />
<span class="st0">&quot;download-dir&quot;</span>: <span class="st0">&quot;/var/lib/transmission/Downloads&quot;</span>,   <span class="sy0">//</span>下载完成的保存路径<br />
<span class="st0">&quot;encryption&quot;</span>: <span class="nu0">1</span>,<br />
<span class="st0">&quot;idle-seeding-limit&quot;</span>: <span class="nu0">30</span>,<br />
<span class="st0">&quot;idle-seeding-limit-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;incomplete-dir&quot;</span>: <span class="st0">&quot;/var/lib/transmission/Downloads&quot;</span>,   <span class="sy0">//</span>未下载完成的保存路径<br />
<span class="st0">&quot;incomplete-dir-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;lazy-bitfield-enabled&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;lpd-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;message-level&quot;</span>: <span class="nu0">2</span>,<br />
<span class="st0">&quot;open-file-limit&quot;</span>: <span class="nu0">32</span>,<br />
<span class="st0">&quot;peer-congestion-algorithm&quot;</span>: <span class="st0">&quot;&quot;</span>,<br />
<span class="st0">&quot;peer-limit-global&quot;</span>: <span class="nu0">240</span>,   <span class="sy0">//</span>全局种子最大连接数<br />
<span class="st0">&quot;peer-limit-per-torrent&quot;</span>: <span class="nu0">60</span>,   <span class="sy0">//</span>单一种子最大连接数<br />
<span class="st0">&quot;peer-port&quot;</span>: <span class="nu0">51413</span>,<br />
<span class="st0">&quot;peer-port-random-high&quot;</span>: <span class="nu0">65535</span>,<br />
<span class="st0">&quot;peer-port-random-low&quot;</span>: <span class="nu0">49152</span>,<br />
<span class="st0">&quot;peer-port-random-on-start&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;peer-socket-tos&quot;</span>: <span class="st0">&quot;default&quot;</span>,<br />
<span class="st0">&quot;pex-enabled&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;port-forwarding-enabled&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;preallocation&quot;</span>: <span class="nu0">1</span>,<br />
<span class="st0">&quot;prefetch-enabled&quot;</span>: <span class="nu0">1</span>,<br />
<span class="st0">&quot;ratio-limit&quot;</span>: <span class="nu0">2</span>,<br />
<span class="st0">&quot;ratio-limit-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;rename-partial-files&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;rpc-authentication-required&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;rpc-bind-address&quot;</span>: <span class="st0">&quot;0.0.0.0&quot;</span>,<br />
<span class="st0">&quot;rpc-enabled&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;rpc-password&quot;</span>: <span class="st0">&quot;{096110376f678fa59ac93b4ba2ef383fba6a9edcBELB4tYF&quot;</span>,   <span class="sy0">//</span>密码<br />
<span class="st0">&quot;rpc-port&quot;</span>: <span class="nu0">9091</span>,   <span class="sy0">//</span>网页GUI使用的端口<br />
<span class="st0">&quot;rpc-url&quot;</span>: <span class="st0">&quot;/transmission/&quot;</span>,<br />
<span class="st0">&quot;rpc-username&quot;</span>: <span class="st0">&quot;&quot;</span>,   <span class="sy0">//</span>用户名<br />
<span class="st0">&quot;rpc-whitelist&quot;</span>: <span class="st0">&quot;*.*.*.*&quot;</span>,<br />
<span class="st0">&quot;rpc-whitelist-enabled&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;script-torrent-done-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;script-torrent-done-filename&quot;</span>: <span class="st0">&quot;&quot;</span>,<br />
<span class="st0">&quot;speed-limit-down&quot;</span>: <span class="nu0">100</span>,<br />
<span class="st0">&quot;speed-limit-down-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;speed-limit-up&quot;</span>: <span class="nu0">100</span>,<br />
<span class="st0">&quot;speed-limit-up-enabled&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;start-added-torrents&quot;</span>: <span class="kw2">true</span>,<br />
<span class="st0">&quot;trash-original-torrent-files&quot;</span>: <span class="kw2">false</span>,<br />
<span class="st0">&quot;umask&quot;</span>: <span class="nu0">18</span>,   <span class="sy0">//</span>这里改为<span class="nu0">0</span>，可以控制默认下载文件权限为<span class="nu0">777</span><br />
<span class="st0">&quot;upload-slots-per-torrent&quot;</span>: <span class="nu0">14</span>   <span class="sy0">//</span>每个种子上传连接数<br />
<span class="br0">&#125;</span></div></div>
<h3>4、给予下载目录的所有者为<span style="color: #ff0000;">transmission:transmission</span>，并启动软件</h3>
<div class="codecolorer-container bash vibrant" style="overflow:auto;white-space:nowrap;"><div class="bash codecolorer">service transmission-daemon start<br />
Starting transmission-daemon: <span class="br0">&#91;</span> OK <span class="br0">&#93;</span></div></div>
<h3>5、大功告成，现在可以通过浏览器访问<span style="color: #ff0000;">IP或域名:端口</span>来使用网页GUI了，有个GUI，其它没什么好说的了。另外嫌网页GUI不够用，还可以用一些远控软件爱你来管理，主要有<a href="http://code.google.com/p/transmission-remote-dotnet/" target="_blank">transmission-remote-dotnet</a>和<a href="http://code.google.com/p/transmisson-remote-gui/" target="_blank">transmisson-remote-gui</a>。</h3>
