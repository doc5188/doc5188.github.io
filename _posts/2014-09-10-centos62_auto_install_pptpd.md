---
layout: post
categories: linux
tags: [linux, pptp, vpn]
date: 2014-09-10 09:07:21
title: "Centos6.2一键搭建PPTP VPN脚本"
---

<div id="a1275" class="con">
			        <div class="jianjie"> <font color="436206"><b>摘要</b></font>：本文介绍Centos6.2一键搭建PPTP VPN脚本以及安装方法。</div>						<p>转载注明出处：<a href="http://www.maer1001.com/soso/1275.html">http://www.maer1001.com/soso/1275.html</a></p>
					
<div id="mulu">
                <strong>文章目录</strong>
                <ul id="index-ul">
<li><a title="下载Centos6.2一键搭建PPTP VPN脚本" href="#title-0">下载Centos6.2一键搭建PPTP VPN脚本</a></li>
<li><a title="安装Centos6.2PPTPVPN脚本" href="#title-1">安装Centos6.2PPTPVPN脚本</a></li>
</ul>
            </div>
<p>以前是Centos5，按照网上的一键安装包可以安装PPTP VPN，但是换成Centos6.2后，死活不行，说文件不存在。下面是Centos6.2一键搭建PPTP VPN脚本以及安装方法。</p>
<h2 id="title-0">下载Centos6.2一键搭建PPTP VPN脚本</h2>
<blockquote><p>#wget http://www.hi-vps.com/shell/vpn_centos6.sh<br>
#chmod a+x vpn_centos6.sh</p></blockquote>
<h2 id="title-1">安装Centos6.2PPTPVPN脚本</h2>
<blockquote><p>#bash vpn_centos6.sh</p></blockquote>
<p>执行完后有1、2、3种英文，对应如下中文意思。</p>
<blockquote><p>1. 安装VPN服务<br>
2. 修复VPN<br>
3. 添加VPN用户</p></blockquote>
<p>我们要安装PPTP vpn，当然输入1，然后enter键了。等待安装完成，就会出现账号和密码啦，默认账号是vpn，密码是一串随机数字，自己用的话就不用加账号和密码了，复制下来备用吧。</p>
					<div class="clear"></div>
				</div>

