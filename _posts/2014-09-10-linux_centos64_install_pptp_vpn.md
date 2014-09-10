---
layout: post
title: "centos6.4安装搭建pptp vpn服务(附pptp vpn 一键安装包)"
categories: linux
tags: [vpn, linux, centos, pptp]
date: 2014-09-10 15:52:22
---

<div class="article_content" id="article_content">

<div style="color:rgb(68,68,68); font-size:16px; line-height:24px" class="left">
<h2><a name="t0"></a>centos6.4安装搭建pptp vpn服务(附pptp vpn 一键安装包)</h2>
<div class="post_date"><span class="date_m">Mar</span><span class="date_d">25</span><span class="date_y">2013</span></div>
<div class="article">
<div class="article_info">作者：大步 &nbsp; 发布：2013-03-25 21:27 &nbsp; 分类：<a style="color:rgb(61,107,167); text-decoration:none" rel="category tag" title="View all posts in Linux运维" href="http://www.ksharpdabu.info/category/linux-server" target="_blank">Linux运维</a>,&nbsp;<a style="color:rgb(61,107,167); text-decoration:none" rel="category tag" title="View all posts in vpn" href="http://www.ksharpdabu.info/category/linux-server/linux_software/vpn" target="_blank">vpn</a>&nbsp;&nbsp;
 阅读：5,020 &nbsp;&nbsp;<a style="color:rgb(61,107,167); text-decoration:none" title="Comment on centos6.4安装搭建pptp vpn服务(附pptp vpn 一键安装包)" class="ds-thread-count" href="http://www.ksharpdabu.info/centos6-4-structures-pptp-vpn.html#comments" target="_blank">44条评论</a>&nbsp;&nbsp;</div>
<div class="clear"></div>
<div class="context">
<div>
<center>
<div id="nuffnang_bn"></div>
</center>
</div>
<p>今天在vps上装pptp ，和以往一样，只不过不是在自己的vps上，上次ssh代理被封ip，对我的身心造成了深深的影响，所以，这次拿网友放我这的vps来搭建vpn环境。pptp的搭建比openvpn容易多了。以下是我的配置过程，其实和网上差不多，<span style="color:rgb(136,136,136); background-color:rgb(136,136,136)">centos6.4 搭建 centos 6.4 搭建pptp vpn</span><span style="color:rgb(0,128,0); background-color:rgb(0,128,0)">ppp
 = 2.4.4 is needed by pptpd-1.3.4-2.rhel5.x86_64</span></p>
<p><span style="color:rgb(255,0,0)"><span style="font-size:18px"><span style="font-size:14px; color:rgb(0,0,0)">centos6.4安装搭建pptp vpn服务的</span></span><strong><span style="font-size:18px">大致步骤简介，下面会有详细的步骤</span></strong><span style="font-size:18px"><span style="font-size:14px; color:rgb(0,0,0)">(我不喜欢写大纲，决定麻烦，但是有人还</span></span><span style="font-size:18px"><span style="font-size:14px; color:rgb(0,0,0)">是看不懂，所以勉为其难的</span></span><span style="font-size:18px"><span style="color:rgb(0,0,0)">写了个，实在不会的，我在文章的后面提供一些网上的<span style="color:rgb(255,0,0)">centos
 pptp vpn 一键安装包</span>，有人写了就不必再写一遍了，一键安装包<span style="font-size:14px">要是有问题，也别找我，新手</span>想享受自己亲手一步步具</span></span><span style="font-size:18px"><span style="color:rgb(0,0,0)">体搭建过程的乐趣，就接着看看吧)<strong><span style="color:rgb(255,0,0)">：</span></strong></span></span></span></p>
<blockquote>
<p>1.先检查vps是否满足配置pptp vpn的环境。因为有的openvz的vps被母鸡给禁用了。其实，你在配置前最好向vps的客服发TK，可能客服会帮你开通vpn或者客服那里会给你他们自己定制的vpn一键安装包也有可能。<br>
2.接着是安装配置pptp vpn的相关软件，<strong>安装ppp和iptables</strong>。<br>
配置安装好后的pptp软件，这个不像windows那样，安装的过程就是配置的过程。linux的要安装完之后，修改配置文件，才算是完成配置。<br>
3.启动pptp vpn 服务。<span style="background-color:rgb(255,255,0)">此时，就是检验你能够vpn拨号成功，如果你拨号成功了，说明你的pptp vpn的安装配置就算真正的完成了。但是此时只能登录vpn，却不能用来上网。</span><br>
4.开启内核和iptables的转发功能。这个步骤是为了让你连上vpn之后，能够上网，上那些yourporn，youtube之类的。<span style="background-color:rgb(255,255,0)">这步是最关键的，很多人能成功拨号，登录vpn，但是却不能上网就是因为这个步骤没做好。这步骤完成了，你就可以尽情去国外的网站访问了</span>。</p>
</blockquote>
<p>#########################################手动搭建配置pptp vpn 详细方法如下########</p>
<p><strong><span style="font-size:18px">第一步</span></strong>：检测是否符合pptp的搭建环境的要求</p>
<div>服务器版本：CentOs 6.4&nbsp;<span style="color:rgb(255,0,0); font-size:18px">xen vps</span></div>
<div>
<div>如果检查结果没有这些支持的话，是不能安装pptp的。执行指令：</div>
<blockquote>#modprobe ppp-compress-18 &amp;&amp; echo ok</blockquote>
<div>这条执行执行后，显示“ok”则表明通过。不过接下来还需要做另一个检查，输入指令：</div>
<blockquote>#cat /dev/net/tun</blockquote>
<div>如果这条指令显示结果为下面的文本，则表明通过：</div>
<div>cat: /dev/net/tun: File descriptor in bad state</div>
<div>上述两条均通过，才能安装pptp。否则就只能考虑openvpn，或者请vps空间商的技术客服为你的VPS打开TUN/TAP/PPP功能了，貌似有部分vps控制面板上提供打开TUN/TAP/PPP功能的按钮。</div>
<div>
<div><strong><span style="color:rgb(255,0,0)">Cent os 6.4内核版本在2.6.15以上，都默认集成了MPPE和PPP，因此下面<span style="font-size:18px">检查可以忽略</span>：</span></strong></div>
<div><span style="color:rgb(255,255,255)"><strong>http://www.ksharpdabu.info/?p=2178</strong></span></div>
<blockquote>#rpm -q ppp //查询当前系统的ppp是否默认集成了，以及ppp的版本</blockquote>
<div></div>
<div>检查PPP是否支持MPPE</div>
<div>用以下命令检查PPP是否支持MPPE：</div>
<blockquote>#strings '/usr/sbin/pppd' |grep -i mppe | wc --lines</blockquote>
<div><span style="color:rgb(255,255,255)"><strong>http://www.ksharpdabu.info/?p=2178</strong></span></div>
<div>如果以上命令输出为“0”则表示不支持；输出为“30”或更大的数字就表示支持，MPPE（Microsoft Point to Point Encryption，微软点对点加密）。</div>
</div>
</div>
<div></div>
<div><strong><span style="font-size:18px">第二步</span></strong>：</div>
<div><strong><span style="font-size:14px">1.安装ppp和iptables</span></strong></div>
<div></div>
<div>PPTPD要求Linux内核支持mppe，一般来说CentOS安装时已经包含了</div>
<div><span style="color:rgb(255,255,255)"><strong>http://www.ksharpdabu.info/?p=2178</strong></span></div>
<blockquote>
<div>#yum install -y perl ppp iptables //centos默认安装了iptables和ppp</div>
<div></div>
</blockquote>
<div></div>
<div></div>
<div><strong><span style="font-size:14px">2.安装pptpd</span></strong></div>
<div>
<p>刚才用了yum安装了ppp,但是这里有个问题，几乎大部分的人都会在这里遇到ppp和pptpd不兼容的错误。因为yum安装ppp，总是安装最新版本的ppp，而由于安装的ppp的版本不同，那么就需要安装对应版本的pptpd才行。(参考我的文章《<a style="color:rgb(61,107,167); text-decoration:none" href="http://www.ksharpdabu.info/ppp-2-4-4-is-needed-by-pptpd-1-3-4-2-rhel5-x86_64-solutions-and-reasons.html" target="_blank">ppp
 = 2.4.4 is needed by pptpd-1.3.4-2.rhel5.x86_64的解决办法及原因</a>|<a style="color:rgb(61,107,167); text-decoration:none" href="http://www.ksharpdabu.info/" target="_blank">大步's blog</a>》)</p>
<p>我们要先查看已经安装的ppp的版本，在去找对应的pptpd版本。我手头刚好有两个vps，一个是前年装的pptp vpn，一个是一年后装的pptp vpn，所以，装的yum install ppp的版本不同。</p>
<p>使用下面的命令查看ppp的版本，前提你是yum安装的ppp。</p>
<p>旧的vps上的ppp版本显示：</p>
<p>#yum list installed ppp</p>
<p>显示：</p>
<blockquote>
<p>ppp.i386&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong><span style="color:rgb(255,0,0)">&nbsp;2.4.4-2.el5&nbsp;&nbsp;</span></strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; installed</p>
</blockquote>
<p>新的vps上的ppp版本显示；</p>
<p>#yum list installed ppp</p>
<p>显示：</p>
<blockquote>
<p>ppp.i686&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong><span style="color:rgb(255,0,0)">&nbsp;2.4.5-5.el6&nbsp;</span></strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; @base</p>
</blockquote>
<p>所以，要对根据ppp版本选择对应的pptpd版本。这里我主要列出常用的。</p>
<blockquote>
<p><strong><span style="color:rgb(255,0,0)">ppp 2.4.4&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&gt;pptpd 1.3.4</span></strong></p>
<p><strong><span style="color:rgb(255,0,0)">ppp 2.5.0&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&gt;pptpd 1.4.0</span></strong></p>
</blockquote>
<p>贴个ppp和pptpd各个版本的下载地址；<a style="color:rgb(61,107,167); text-decoration:none" rel="nofollow" href="http://poptop.sourceforge.net/yum/stable/packages/" target="_blank"><strong><span style="color:rgb(0,128,0)">http://poptop.sourceforge.net/yum/stable/packages/</span></strong></a></p>
<p>大家下载的时候注意，分清楚你系统的版本是64位的还是32位的。<span style="color:rgb(0,0,255)"><u><strong>我个人建议ppp用yum安装，pptpd用rpm的安装，因为如果全都rpm或者源码安装，依赖关系很是烦人。文件名含有数字64的就是64位版本，没有的就是32位版本。可以用下面的命令查看自己的系统是32位还是64位的。</strong></u></span></p>
<blockquote>
<p>#getconf LONG_BIT</p>
</blockquote>
<p>下面假设我这里的ppp是2.4.4版本，然后安装pptpd</p>
<p><span style="font-size:18px"><strong><span style="color:rgb(255,0,0)">第一种</span></strong></span>安装pptpd的方法是直接用yum安装，让电脑自动选择对应的版本：</p>
<p>先<strong><span style="color:rgb(255,0,0)">加入yum源</span></strong>：</p>
<blockquote>
<p>#rpm -Uvh http://poptop.sourceforge.net/yum/stable/rhel6/pptp-release-current.noarch.rpm</p>
</blockquote>
<p>然后用yum安装pptpd：</p>
<blockquote>
<p>#yum install pptpd</p>
</blockquote>
<p><span style="color:rgb(0,128,0)"><strong>这是最省时间和力气的。余下的和手动安装没什么区别了。</strong></span></p>
<p>&nbsp;</p>
<p><span style="color:rgb(255,0,0)"><strong><span style="font-size:18px">第二种</span></strong></span>是手动安装pptpd包：</p>
<blockquote>
<p>对于32位CentOS，执行</p>
<p>wget http://acelnmp.googlecode.com/files/pptpd-1.3.4-1.rhel5.1.i386.rpm</p>
<p>rpm -ivh pptpd-1.3.4-1.rhel5.1.i386.rpm</p>
<p>对于64位CentOS，执行</p>
<p>wget http://acelnmp.googlecode.com/files/pptpd-1.3.4-1.rhel5.1.x86_64.rpm</p>
<p>rpm -ivh pptpd-1.3.4-1.rhel5.1.x86_64.rpm</p>
<p>这里贴上32位的pptpd的rpm的下载地址：</p>
<p><a style="color:rgb(61,107,167); text-decoration:none" rel="nofollow" href="http://www.400gb.com/file/34722122" target="_blank">http://www.400gb.com/file/34722122</a></p>
</blockquote>
<h3><a name="t1"></a>64位安装的时候如果出现：<span style="color:rgb(255,255,255)">http://www.ksharpdabu.info/?p=2178</span></h3>
<blockquote>
<p>warning: pptpd-1.3.4-2.rhel5.x86_64.rpm: Header V3 DSA/SHA1 Signature, key ID 862acc42: NOKEY<br>
error: Failed dependencies:<br>
<strong><span style="text-decoration:underline"><span style="color:rgb(51,153,102)">ppp = 2.4.4 is needed by pptpd-1.3.4-2.rhel5.x86_64</span></span></strong></p>
<p><span style="color:rgb(255,0,0)">原因是pptpd与PPP不兼容，那么，此时用#yum list installed ppp&nbsp;&nbsp; 命令查看ppp版本，极有可能ppp是2.4.5版本的。所以，我们要下载pptp&nbsp; 1.4.0版本才行，而且这里是64位的系统。下载<span style="color:rgb(0,0,255)">pptpd-1.4.0-1.el6.x86_64.rpm</span>安装即可。这就是我说的出现版本不兼容的问题，当ppp版本和pptpd版本不兼容时候，就会出现类似的错误。</span></p>
<p>这里我分享下pptpd 下载地址；</p>
<p>64位<span style="color:rgb(0,0,255)"><strong>pptpd-1.4.0-1.el6.x86_64.rpm</strong></span>的下载地址：<a style="color:rgb(61,107,167); text-decoration:none" rel="nofollow" href="http://www.400gb.com/file/54124122" target="_blank">http://www.pipipan.com/file/18457333</a></p>
<p><span style="color:rgb(0,0,0)">32位<strong><span style="color:rgb(0,0,255)">pptpd-1.4.0-1.el6.i686.rpm</span></strong>版本下载地址：<a style="color:rgb(61,107,167); text-decoration:none" rel="nofollow" href="http://www.400gb.com/file/54124192" target="_blank">http://www.400gb.com/file/54124192</a></span></p>
<p>看到有人建议用--nodeps --force 这个参数，我个人不建议，这个参数可能以后会出现奇怪的问题，但是如果实在不行，你就用吧</p>
</blockquote>
<p>&nbsp;</p>
<p><strong><span style="font-size:18px">第三步：修改配置文件</span></strong></p>
<p>1.<strong>配置文件/etc/ppp/options.pptpd</strong></p>
<blockquote>
<p>#mv /etc/ppp/options.pptpd /etc/ppp/options.pptpd.bak<br>
#vi /etc/ppp/options.pptpd</p>
</blockquote>
<p><strong>options.pptpd</strong>内容如下：</p>
<blockquote>
<p>name pptpd<br>
refuse-pap<br>
refuse-chap<br>
refuse-mschap<br>
require-mschap-v2<br>
require-mppe-128<br>
proxyarp<br>
lock<br>
nobsdcomp<br>
novj<br>
novjccomp<br>
nologfd<br>
idle 2592000<br>
<span style="color:rgb(255,0,0); background-color:rgb(255,255,0)">ms-dns 8.8.8.8</span><br>
<span style="color:rgb(255,0,0); background-color:rgb(255,255,0)">ms-dns 8.8.4.4</span></p>
</blockquote>
<p>解析：ms-dns 8.8.8.8， ms-dns 8.8.4.4是使用google的dns服务器。</p>
<p>2.<strong>配置文件/etc/ppp/chap-secrets</strong></p>
<blockquote>
<p>#cp &nbsp; /etc/ppp/chap-secrets /etc/ppp/chap-secrets.bak<br>
#vi&nbsp; /etc/ppp/chap-secrets</p>
</blockquote>
<p><strong>chap-secrets</strong>内容如下：</p>
<blockquote>
<p># Secrets for authentication using CHAP<br>
# client server secret IP addresses<br>
myusername &nbsp; &nbsp;&nbsp;&nbsp;<span style="color:rgb(255,0,0)">pptpd&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>mypassword&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:rgb(255,0,0)">*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
<p>//myusername是你的vpn帐号，mypassword是你的vpn的密码，<span style="color:rgb(255,0,0)">*</span>表示对任何ip，记得不要丢了这个<span style="color:rgb(255,0,0)">星号</span>。我这里根据这个格式，假设我的vpn的帐号是<span style="color:rgb(255,0,0)">ksharpdabu</span>，密码是&nbsp;<span style="color:rgb(255,0,0)">sky</span>。那么，应该如下：</p>
<p><span style="color:rgb(51,153,102)"><span style="background-color:rgb(255,255,0)">ksharpdabu pptpd sky *</span></span></p>
</blockquote>
<p>&nbsp;</p>
<p>3.<strong>配置文件/etc/pptpd.conf</strong></p>
<p>#cp &nbsp; /etc/pptpd.conf /etc/pptpd.conf.bak<br>
#vi /etc/pptpd.conf</p>
<p><strong>pptpd.conf</strong>内容如下：</p>
<blockquote>
<p><span style="color:rgb(255,0,0)"><strong>option /etc/ppp/options.pptpd</strong></span><br>
logwtmp<br>
localip 192.168.9.1<br>
remoteip 192.168.9.11-30 //表示vpn客户端获得ip的范围</p>
</blockquote>
<p>&nbsp;</p>
<p><strong><span style="color:rgb(255,0,0); font-size:18px">关键点：<span style="color:rgb(0,0,0); font-size:14px"><strong>pptpd.conf这个配置文件必须保证最后是以空行结尾才行，否则会导致启动pptpd服务时，出现“Starting pptpd:”，一直卡着不动的问题，无法启动服务，切记呀！（相关文档可以查看：<a style="color:rgb(61,107,167); text-decoration:none" rel="bookmark" href="http://www.ksharpdabu.info/starting-pptpd-does-not-run-down-turn.html" title="Starting pptpd: 运行不下去的原因(转)" target="_blank">Starting
 pptpd: 运行不下去的原因</a>）</strong></span></span></strong></p>
<p><span style="color:rgb(0,128,0); background-color:rgb(0,128,0)">ppp = 2.4.4 is needed by pptpd-1.3.4-2.rhel5.x86_64</span></p>
<p>&nbsp;</p>
<p>4.<strong>配置文件/etc/sysctl.conf</strong></p>
<blockquote>
<p>#vi /etc/sysctl.conf&nbsp;//修改内核设置，使其支持转发</p>
</blockquote>
<p>将<span style="color:rgb(0,128,0)">net.ipv4.ip_forward = 0&nbsp;</span>改成&nbsp;<span style="color:rgb(0,128,0)">net.ipv4.ip_forward = 1</span></p>
<p>保存修改后的文件</p>
<blockquote>
<p>#/sbin/sysctl -p</p>
</blockquote>
<p>&nbsp;</p>
<p><strong><span style="font-size:18px">第四步</span><span style="font-size:18px">：启动pptp vpn服务和iptables</span></strong></p>
<blockquote>
<p>#/sbin/service pptpd start 或者 #service pptpd start</p>
</blockquote>
<p>经过前面步骤，我们的VPN已经<strong><span style="background-color:rgb(255,255,0); font-size:18px">可以拨号登录</span></strong>了，但<span style="background-color:rgb(255,204,0); font-size:18px">是<span style="background-color:rgb(255,255,0)">还不能访问任何网页</span></span>。最后一步就是添加iptables转发规则了，输入下面的指令：</p>
<p><span style="color:rgb(255,0,0)">启动iptables和nat转发功能，很关键的呀</span>：</p>
<p>#/sbin/service iptables start //启动iptables</p>
<p>#/sbin/iptables -t nat -A POSTROUTING -o eth0 -s<span style="background-color:rgb(255,255,0)">&nbsp;192.168.<span style="color:rgb(255,0,0)">9</span>.0/24</span>&nbsp;-j MASQUERADE&nbsp;<strong><span style="color:rgb(255,0,0); font-size:18px">或者</span></strong>使用下面的一种：</p>
<p>#iptables -t nat -A POSTROUTING -o eth0 -s&nbsp;<span style="background-color:rgb(255,255,0)">192.168.<span style="color:rgb(255,0,0)">9</span>.0/24</span>&nbsp;-j SNAT&nbsp;<span style="color:rgb(0,0,0)"><span style="color:rgb(255,0,0)">-<span style="color:rgb(51,153,102)">-</span><strong></strong></span></span>to-source<span style="color:rgb(255,0,0)">207.210.83.140&nbsp;</span>//你需要将207.210.83.140替换成你的<span style="font-size:14px"><span style="font-weight:bold"><span style="color:rgb(255,0,0)">vps的公网ip地址，因为这里我写的是我的。<span style="color:rgb(0,0,0)">还有就是有人说我这--to-source前只有一个横杠，其实是有两个横杠的。文章在编辑模式下显示是<span style="color:rgb(255,0,0); font-size:18px">两个横杠</span>，因为用的是英文输入法，所以，发表后就变成了一个横杆，而且在源码下复制粘贴也是一横，只有在编辑模式下才能看清楚是两横。但是可以明显看到to前面的那一横比source前的那横长一些，这些都是我操作记录下的命令，不会有错的。为了防止你们出错，我还是用不同的颜色标记吧。</span></span></span></span></p>
<p>这里我先前写的不是很详细，现在补上：</p>
<ul style="list-style-type:none; padding:0px; margin:0px">
<li style="padding:0px; margin:0px">需要注意的是，这个指令中的“192.168.9.0/24”是根据之前的配置文件中的“localip”网段来改变的(网上有的教程是<span style="background-color:rgb(255,255,0)">192.168.<span style="color:rgb(255,0,0)">0</span>.0/24&nbsp;</span>)，比如你设置的 “10.0.0.1”网段，则应该改为“10.0.0.0/24”。此外还有一点需要注意的是eth0，如果你的外网网卡不是eth0，而是eth1（比
 如SoftLayer的服务器就是这样的情况），那么请记得将eth0也更改为对应的网卡编号，不然是上不了网的！</li><li style="padding:0px; margin:0px">如果你的linux vps是ppp或者ADSL这种由DHCP动态分配获取ip的方式<span style="font-size:18px; color:rgb(0,128,128)">（当然vps的ip基本都是是固定的。如果你是<span style="color:rgb(255,0,0)">XEN的vps</span>，那么这个转发规则其实<span style="color:rgb(255,0,0)"><strong>也是适用</strong></span></span>的，就是让vps自己判断自己的ip，省去了我们指定。），那么就需要用<span style="color:rgb(255,0,0)">-j
 MASQUERADE</span>这种写法，就是ip伪装。当然如果使用<span style="background-color:rgb(255,255,0)">iptables -t nat -A POSTROUTING -o eth0 -s 192.168.<span style="color:rgb(255,0,0)">9</span>.0/24 -j SNAT&nbsp;<span style="color:rgb(255,0,0)">-</span><span style="color:rgb(51,153,102)">-</span>to-source&nbsp;</span><span style="color:rgb(255,0,0)"><span style="background-color:rgb(255,255,0)">XXX.XXX.XXX.XXX</span>&nbsp;</span>这种转发规则其实也是可以的，这样亲自指定自己的vps的ip地址。以后你通过vpn访问网站，显示的就是这个ip了。</li></ul>
<p>#/etc/init.d/iptables save //保存iptables的转发规则</p>
<p>#/sbin/service iptables restart&nbsp;//重新启动iptables</p>
<p>&nbsp;</p>
<p><strong><span style="font-size:18px">最后一步：重启pptp vpn</span></strong></p>
<blockquote>
<p>#/sbin/service pptpd retart&nbsp;或者 #service pptpd restart</p>
</blockquote>
<p>#############################################3</p>
<p>客户端如何拨号登陆vpn，我就不写了，大家可以自行google，因为系统那么多，我不可能xp，win7，centos，mac之类的每个都写，何况网上一大堆，只要你pptp vpn服务器搭建好了，客户端登陆的选择就是简单的事。如果这个也不知道，那我就没法了，自己动手吧。</p>
<p>&nbsp;</p>
<p><strong><span style="font-size:18px">多余的步骤</span></strong>：设置pptp vpn 开机启动</p>
<p>有的人懒的重启后手动开启服务，所以下面我再补上开机自动启动pptp vpn 和 iptables的命令</p>
<p>#chkconfig pptpd on&nbsp;//开机启动pptp vpn服务</p>
<p>#chkconfig iptables on //开机启动iptables</p>
<p>&nbsp;</p>
<p>有问题请先看log，查google，百度，论坛，有的人连软件下载都不自己去搜索，对于这样的人，我也懒得理睬。</p>
<p>&nbsp;</p>
<p>##############################华丽分隔线############################3</p>
<p>下面贴出网上的别人写的pptp vpn 一键安装包使用方法：</p>
<p><strong><span style="color:rgb(255,0,0); font-size:18px">第一篇：</span></strong></p>
<blockquote>
<p>本教程仅仅适用于Xen或KVM VPS,不适用于Openvz VPS，安装之前请确定自己是否是符合标准！</p>
<p>1. 下载vpn(CentOS6专用)一键安装包<br>
#wget http://www.hi-vps.com/shell/vpn_centos6.sh<br>
#chmod a+x vpn_centos6.sh<br>
2. 运行一键安装包<br>
#bash vpn_centos6.sh</p>
<p>会有三个选择:</p>
<p>1. 安装VPN服务<br>
2. 修复VPN<br>
3. 添加VPN用户首先输入1，回车,VPS开始安装VPN服务. VPN服务安装完毕后会默认生成一个用户名为vpn，密码为随机数的用户来。</p>
<p>3. 添加VPN用户<br>
#bash vpn_centos6.sh选择3，然后输入用户名和密码,OK</p>
<p>4. 修复VPN服务<br>
如果VPN拨号发生错误,可以试着修复VPN,然后重启VPS<br>
#bash vpn_centos6.sh<br>
选择2，然后reboot</p>
<p>下面是具体的脚本：<br>
#!/bin/bash</p>
<p>function installVPN(){<br>
echo “begin to install VPN services”;<br>
#check wether vps suppot ppp and tun</p>
<p>yum remove -y pptpd ppp<br>
iptables &ndash;flush POSTROUTING &ndash;table nat<br>
iptables &ndash;flush FORWARD<br>
rm -rf /etc/pptpd.conf<br>
rm -rf /etc/ppp</p>
<p>arch=`uname -m`</p>
<p>wget http://www.hi-vps.com/downloads/dkms-2.0.17.5-1.noarch.rpm<br>
wget http://wty.name/linux/sources/kernel_ppp_mppe-1.0.2-3dkms.noarch.rpm<br>
wget http://www.hi-vps.com/downloads/kernel_ppp_mppe-1.0.2-3dkms.noarch.rpm<br>
wget http://www.hi-vps.com/downloads/pptpd-1.3.4-2.el6.$arch.rpm<br>
wget http://www.hi-vps.com/downloads/ppp-2.4.5-17.0.rhel6.$arch.rpm</p>
<p>yum -y install make libpcap iptables gcc-c++ logrotate tar cpio perl pam tcp_wrappers<br>
rpm -ivh dkms-2.0.17.5-1.noarch.rpm<br>
rpm -ivh kernel_ppp_mppe-1.0.2-3dkms.noarch.rpm<br>
rpm -qa kernel_ppp_mppe<br>
rpm -Uvh ppp-2.4.5-17.0.rhel6.$arch.rpm<br>
rpm -ivh pptpd-1.3.4-2.el6.$arch.rpm</p>
<p>mknod /dev/ppp c 108 0<br>
echo 1 &gt; /proc/sys/net/ipv4/ip_forward<br>
echo “mknod /dev/ppp c 108 0″ &gt;&gt; /etc/rc.local<br>
echo “echo 1 &gt; /proc/sys/net/ipv4/ip_forward” &gt;&gt; /etc/rc.local<br>
echo “localip 172.16.36.1″ &gt;&gt; /etc/pptpd.conf<br>
echo “remoteip 172.16.36.2-254″ &gt;&gt; /etc/pptpd.conf<br>
echo “ms-dns 8.8.8.8″ &gt;&gt; /etc/ppp/options.pptpd<br>
echo “ms-dns 8.8.4.4″ &gt;&gt; /etc/ppp/options.pptpd</p>
<p>pass=`openssl rand 6 -base64`<br>
if [ "$1" != "" ]<br>
then pass=$1<br>
fi</p>
<p>echo “vpn pptpd ${pass} *” &gt;&gt; /etc/ppp/chap-secrets</p>
<p>iptables -t nat -A POSTROUTING -s 172.16.36.0/24 -j SNAT &ndash;to-source `ifconfig | grep ‘inet addr:’| grep -v ’127.0.0.1′ | cut -d: -f2 | awk ‘NR==1 { print $1}’`<br>
iptables -A FORWARD -p tcp &ndash;syn -s 172.16.36.0/24 -j TCPMSS &ndash;set-mss 1356<br>
service iptables save</p>
<p>chkconfig iptables on<br>
chkconfig pptpd on</p>
<p>service iptables start<br>
service pptpd start</p>
<p>echo “VPN service is installed, your VPN username is vpn, VPN password is ${pass}”</p>
<p>}</p>
<p>function repaireVPN(){<br>
echo “begin to repaire VPN”;<br>
mknod /dev/ppp c 108 0<br>
service iptables restart<br>
service pptpd start<br>
}</p>
<p>function addVPNuser(){<br>
echo “input user name:”<br>
read username<br>
echo “input password:”<br>
read userpassword<br>
echo “${username} pptpd ${userpassword} *” &gt;&gt; /etc/ppp/chap-secrets<br>
service iptables restart<br>
service pptpd start<br>
}</p>
<p>echo “which do you want to?input the number.”<br>
echo “1. install VPN service”<br>
echo “2. repaire VPN service”<br>
echo “3. add VPN user”<br>
read num</p>
<p>case “$num” in<br>
[1] ) (installVPN);;<br>
[2] ) (repaireVPN);;<br>
[3] ) (addVPNuser);;<br>
*) echo “nothing,exit”;;<br>
esac</p>
</blockquote>
<p><strong><span style="color:rgb(255,0,0); font-size:18px">第二篇：</span></strong></p>
<blockquote>
<h2><a name="t2"></a><a style="color:rgb(61,107,167); text-decoration:none" rel="nofollow" href="http://www.centoscn.com/image-text/2013/0413/307.html" target="_blank">PPTP VPN 一键安装包（OpenVZ适用）</a></h2>
<h3 style="padding:0px; margin:0px; font-weight:normal; font-size:16px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif"><a name="t3"></a>
1、<span style="padding:0px; margin:0px; color:rgb(0,0,0)">检测</span><span style="padding:0px; margin:0px" class="entry"><span style="padding:0px; margin:0px; color:rgb(0,0,0)">虚拟网卡支持</span></span></h3>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:15px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif; line-height:20px">
<span style="padding:0px; margin:0px; color:rgb(0,0,0)">OpenVZ的VPS客户需要检测</span><span style="padding:0px; margin:0px" class="entry"><span style="padding:0px; margin:0px; color:rgb(0,0,0)">虚拟网卡ppp模块支持，</span></span><span style="padding:0px; margin:0px" class="entry"><span style="padding:0px; margin:0px; color:rgb(0,0,0)">如果不支持即使安装成功也没用。</span><span style="padding:0px; margin:0px; color:rgb(0,0,255)">（Xen等可跳过此步）</span></span></p>
<h4 style="padding:0px; margin:0px; font-weight:normal; font-size:15px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif"><a name="t4"></a>
检测是否支持ppp模块</h4>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:15px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif; line-height:20px">
执行命令：</p>
<pre lang="bash">cat /dev/ppp</pre>
<p>如果返回信息为：cat: /dev/ppp: No such device or address 说明正常</p>
<h3 style="padding:0px; margin:0px; font-weight:normal; font-size:16px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif"><a name="t5"></a>
2、使用管理员帐号密码登陆SSH，并输入以下指令</h3>
<p>wget http://soft.kwx.gd/vpn/pptpd.sh //下载centos pptp vpn一键安装包的脚本</p>
<h3 style="padding:0px; margin:0px; font-weight:normal; font-size:16px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif"><a name="t6"></a>
<span style="padding:0px; margin:0px" class="entry">3、以上操作是下载安装脚本，下载完毕后请直接执行：</span></h3>
<p>sh pptpd.sh</p>
<h3><a name="t7"></a>安装完成后，默认账户是vpn ，密码:vpn 如果要添加修改密码，参考我上面的教程<span style="padding:0px; margin:0px" class="entry">输入命令 vi /etc/ppp/chap-secrets 编辑文件，按照相同格式添加用户名和密码即可。</span><span style="padding:0px; margin:0px" class="entry">：</span></h3>
<p><strong>chap-secrets</strong>内容如下：</p>
<p># Secrets for authentication using CHAP<br>
# client server secret IP addresses<br>
myusername pptpd mypassword *</p>
<p>//myusername是你的vpn帐号，mypassword是你的vpn的密码，*表示对任何ip，记得不要丢了这个星号。我这里根据这个格式，假设我的vpn的帐号是ksharpdabu，密码是 sky。那么，应该如下：</p>
<p>ksharpdabu pptpd sky *</p>
</blockquote>
</div>
<div></div>
<div>############################完#############################</div>
<div>如果一件安装包都不知道用，那就真的没法子了</div>
<div>
<p><span style="background-color:rgb(255,255,0)"><strong><span style="font-size:18px">FAQ：</span></strong></span></p>
<p>1.报错：重启时候提示</p>
<p># service pptpd restart<br>
Shutting down pptpd: [失败]<br>
Starting pptpd: [失败]<br>
Warning: a pptpd restart does not terminate existing<br>
connections, so new connections may be assigned the same IP<br>
address and cause unexpected results. Use restart-kill to<br>
destroy existing connections during a restart.</p>
<p><span style="color:rgb(255,0,0); font-size:14px">解决办法：</span>根据提示，可能是你重启pptpd服务的时候，没有切断已经存在的连接，所以新的连接会被分配为相同的ip地址，导致一些不可预料的问题。所以你重启 pptpd服务前，先用下面的命令断开当前存在的连接：#service pptpd restart-kill，然后再#service pptpd start</p>
<p>2.有的vps不支持加密连接，导致不能拨号成功登陆vpn。</p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:15px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif; line-height:20px">
解决办法：是<span style="padding:0px; margin:0px" class="entry">编辑/etc/ppp/options.pptpd（vim /etc/ppp/options.pptpd），在require-mppe-128前面加个#（# require-mppe-128）；</span></p>
<p style="padding-top:0px; padding-bottom:0px; margin-top:0px; margin-bottom:15px; font-family:微软雅黑,宋体,Tahoma,Georgia,Times,'Times New Roman',serif; line-height:20px">
<span style="padding:0px; margin:0px" class="entry">在windows的VPN连接属性里，加密方式选择为可选加密，并允许未加密的密码。</span></p>
<p>&nbsp;</p>
<p>3.能够直接用域名作为vpn的拨号地址，而不用vps的ip。因为ip不方便记忆，我自己也记不住自己的服务器的ip。</p>
<p><span style="color:rgb(255,0,0); font-size:18px">解决办法：</span>去dns里面设置，将<span style="color:rgb(255,0,0); font-size:18px">域名设置为A记录</span>，这样就可以直接用域名作为vpn的服务器的地址了。</p>
<p>4.有的链接 pptp vpn时候失败，提示619.</p>
<p>解决办法：执行下面的命令：</p>
<p># rm -r /dev/ppp</p>
<p># mknod /dev/ppp c 108 0 然后重启VPS即可。</p>
<p>也可以参考这片文章《<a style="color:rgb(61,107,167); text-decoration:none" href="http://www.hkcdn.net/23.html" target="_blank">VPN连接时提示619错误处理办法及vpn连接成功后无法上网解决办法</a>》</p>
<p><span style="color:rgb(0,128,0); background-color:rgb(0,128,0)">centos6.4 安装 搭建 pptp vpn ppp = 2.4.4 is needed by pptpd-1.3.4-2.rhel5.x86_64</span></p>
</div>
<p>本文固定链接:&nbsp;<a style="color:rgb(61,107,167); text-decoration:none" title="centos6.4安装搭建pptp vpn服务(附pptp vpn 一键安装包)" rel="bookmark" href="http://www.ksharpdabu.info/centos6-4-structures-pptp-vpn.html" target="_blank">http://www.ksharpdabu.info/centos6-4-structures-pptp-vpn.html
 | 大步's Blog</a></p>
</div>
</div>
</div>

</div>
