---
layout: post
title: "iptables基础知识.详解"
categories: linux
tags: [linux, iptables]
date: 2014-08-19 09:40:21
---

<p>&nbsp;</p>
<div>iptables防火墙可以用于创建过滤(filter)与NAT规则。所有Linux发行版都能使用iptables，因此理解如何配置iptables将会帮助你更有效地管理Linux防火墙。如果你是第一次接触iptables，你会觉得它很复杂，但是一旦你理解iptables的工作原理，你会发现其实它很简单。</div>
<div>首先介绍iptables的结构：iptables -&gt; Tables -&gt; Chains -&gt; Rules. 简单地讲，tables由chains组成，而chains又由rules组成。如下图所示。<a href="/upload/images/iptables-table-chain-rule-structure.png" rel="prettyPhoto[207]"><img class="aligncenter size-full wp-image-208" alt="iptables-table-chain-rule-structure" src="/upload/images/iptables-table-chain-rule-structure.png" width="540" height="400" /></a></div>
<div></div>
<div>
<div style="text-align: center;">图: IPTables Table, Chain, and Rule Structure</div>
<div></div>
<div><strong>一、iptables的表与链</strong></div>
<div></div>
<div>iptables具有Filter, NAT, Mangle, Raw四种内建表：</div>
<div></div>
<div><strong>1. Filter表</strong></div>
<div>Filter表示iptables的默认表，因此如果你没有自定义表，那么就默认使用filter表，它具有以下三种内建链：</div>
<ul>
<li><strong>INPUT链</strong> – 处理来自外部的数据。</li>
<li><strong>OUTPUT链</strong> – 处理向外发送的数据。</li>
<li><strong>FORWARD链</strong> – 将数据转发到本机的其他网卡设备上。</li>
</ul>
<div><strong>2. NAT表</strong></div>
<div>NAT表有三种内建链：</div>
<ul>
<li><strong>PREROUTING链</strong> – 处理刚到达本机并在路由转发前的数据包。它会转换数据包中的目标IP地址（destination ip address），通常用于DNAT(destination NAT)。</li>
<li><strong>POSTROUTING链</strong> – 处理即将离开本机的数据包。它会转换数据包中的源IP地址（source ip address），通常用于SNAT（source NAT）。</li>
<li><strong>OUTPUT链</strong> – 处理本机产生的数据包。</li>
</ul>
<div><strong>3. Mangle表</strong></div>
<div>Mangle表用于指定如何处理数据包。它能改变TCP头中的QoS位。Mangle表具有5个内建链：</div>
<ul>
<li>PREROUTING</li>
<li>OUTPUT</li>
<li>FORWARD</li>
<li>INPUT</li>
<li>POSTROUTING</li>
</ul>
<div><strong>4. Raw表</strong></div>
<div>Raw表用于处理异常，它具有2个内建链：</div>
<ul>
<li>PREROUTING chain</li>
<li>OUTPUT chain</li>
</ul>
<div><strong>5.小结</strong></div>
<div>下图展示了iptables的三个内建表：</div>
<div><a href="/upload/images/iptables-filter-nat-mangle-tables.png" rel="prettyPhoto[207]"><img class="aligncenter size-full wp-image-220" alt="iptables-filter-nat-mangle-tables" src="/upload/images/iptables-filter-nat-mangle-tables.png" width="540" height="279" /></a></div>
<div style="text-align: center;">图: IPTables 内建表</div>
<div></div>
<div><strong>二、IPTABLES 规则(Rules)</strong></div>
<div></div>
<div>牢记以下三点式理解iptables规则的关键：</div>
<ul>
<li>Rules包括一个条件和一个目标(target)</li>
<li>如果满足条件，就执行目标(target)中的规则或者特定值。</li>
<li>如果不满足条件，就判断下一条Rules。</li>
</ul>
<div><strong>目标值（Target Values）</strong></div>
<div>下面是你可以在target里指定的特殊值：</div>
<ul>
<li><strong>ACCEPT</strong> – 允许防火墙接收数据包</li>
<li><strong>DROP</strong> – 防火墙丢弃包</li>
<li><strong>QUEUE</strong> – 防火墙将数据包移交到用户空间</li>
<li><strong>RETURN</strong> – 防火墙停止执行当前链中的后续Rules，并返回到调用链(the calling chain)中。</li>
</ul>
<div>如果你执行iptables &#8211;list你将看到防火墙上的可用规则。下例说明当前系统没有定义防火墙，你可以看到，它显示了默认的filter表，以及表内默认的input链, forward链, output链。</div>
<div></div>
<div># iptables -t filter &#8211;list<br />
Chain INPUT (policy ACCEPT)<br />
target    prot opt source              destination&nbsp;</p>
<p>Chain FORWARD (policy ACCEPT)<br />
target    prot opt source              destination</p>
<p>Chain OUTPUT (policy ACCEPT)<br />
target    prot opt source              destination</p>
</div>
<div></div>
<div>查看mangle表：</div>
<div></div>
<div># iptables -t mangle &#8211;list</div>
<div></div>
<div>查看NAT表：</div>
<div></div>
<div># iptables -t nat &#8211;list</div>
<div></div>
<div>查看RAW表：</div>
<div></div>
<div># iptables -t raw &#8211;list</div>
<div></div>
<div>!注意：如果不指定<strong>-t</strong>选项，就只会显示默认的<strong>filter</strong>表。因此，以下两种命令形式是一个意思：</div>
<div></div>
<div># iptables -t filter &#8211;list<br />
(or)<br />
# iptables &#8211;list</div>
<div></div>
<div>以下例子表明在filter表的input链, forward链, output链中存在规则：</div>
<div></div>
<div># iptables &#8211;list<br />
Chain INPUT (policy ACCEPT)<br />
num        target                 prot    opt        source            destination<br />
1    RH-Firewall-1-INPUT     all       &#8212;         0.0.0.0/0         0.0.0.0/0&nbsp;</p>
<p>Chain FORWARD (policy ACCEPT)<br />
num        target                 prot    opt        source            destination<br />
1      RH-Firewall-1-INPUT   all        &#8211;      0.0.0.0/0           0.0.0.0/0</p>
<p>Chain OUTPUT (policy ACCEPT)<br />
num  target    prot opt source              destination</p>
<p>Chain RH-Firewall-1-INPUT (2 references)<br />
num  target    prot opt source              destination<br />
1    ACCEPT    all  &#8211;  0.0.0.0/0            0.0.0.0/0<br />
2    ACCEPT    icmp &#8211;  0.0.0.0/0            0.0.0.0/0          icmp type 255<br />
3    ACCEPT    esp  &#8211;  0.0.0.0/0            0.0.0.0/0<br />
4    ACCEPT    ah  &#8211;  0.0.0.0/0            0.0.0.0/0<br />
5    ACCEPT    udp  &#8211;  0.0.0.0/0            224.0.0.251        udp dpt:5353<br />
6    ACCEPT    udp  &#8211;  0.0.0.0/0            0.0.0.0/0          udp dpt:631<br />
7    ACCEPT    tcp  &#8211;  0.0.0.0/0            0.0.0.0/0          tcp dpt:631<br />
8    ACCEPT    all  &#8211;  0.0.0.0/0            0.0.0.0/0          state RELATED,ESTABLISHED<br />
9    ACCEPT    tcp  &#8211;  0.0.0.0/0            0.0.0.0/0          state NEW tcp dpt:22<br />
10  REJECT    all  &#8211;  0.0.0.0/0            0.0.0.0/0          reject-with icmp-host-prohibited</p>
</div>
<div></div>
<div>以上输出包含下列字段：</div>
<ul>
<li>num – 指定链中的规则编号<br />
target – 前面提到的target的特殊值<br />
prot – 协议：tcp, udp, icmp等<br />
source – 数据包的源IP地址<br />
destination – 数据包的目标IP地址</li>
</ul>
<div><strong>三、清空所有iptables规则</strong></div>
<div></div>
<div>在配置iptables之前，你通常需要用iptables &#8211;list命令或者iptables-save命令查看有无现存规则，因为有时需要删除现有的iptables规则：</div>
<div></div>
<div>iptables &#8211;flush<br />
或者<br />
iptables -F</div>
<div></div>
<div>这两条命令是等效的。但是并非执行后就万事大吉了。你仍然需要检查规则是不是真的清空了，因为有的linux发行版上这个命令不会清除NAT表中的规则，此时只能手动清除：</div>
<div></div>
<div>iptables -t NAT -F</div>
<div></div>
<div><strong>四、永久生效</strong></div>
<div></div>
<div>当你删除、添加规则后，这些更改并不能永久生效，这些规则很有可能在系统重启后恢复原样。为了让配置永久生效，根据平台的不同，具体操作也不同。下面进行简单介绍：</div>
<div></div>
<div><strong>1.Ubuntu</strong></div>
<div>首先，保存现有的规则：</div>
<div></div>
<div>iptables-save &gt; /etc/iptables.rules</div>
<div></div>
<div>然后新建一个bash脚本，并保存到<em>/etc/network/if-pre-up.d/</em>目录下：</div>
<div></div>
<div>#!/bin/bash<br />
iptables-restore &lt; /etc/iptables.rules</div>
<div></div>
<div>这样，每次系统重启后iptables规则都会被自动加载。</div>
<div><span style="color: #ff0000;"><strong>！注意：不要尝试在.bashrc或者.profile中执行以上命令，因为用户通常不是root，而且这只能在登录时加载iptables规则。</strong></span></div>
<div></div>
<div><strong>2.CentOS, RedHat</strong></div>
<div># 保存iptables规则<br />
service iptables save&nbsp;</p>
<p># 重启iptables服务<br />
service iptables stop<br />
service iptables start</p>
</div>
<div></div>
<div>查看当前规则：</div>
<div></div>
<div>cat  /etc/sysconfig/iptables</div>
<div></div>
<div><strong>五、追加iptables规则</strong></div>
<div></div>
<div>可以使用iptables -A命令追加新规则，其中<strong>-A</strong>表示<strong>Append</strong>。因此，<strong>新的规则将追加到链尾。</strong></div>
<div>一般而言，最后一条规则用于丢弃(DROP)所有数据包。如果你已经有这样的规则了，并且使用<strong>-A</strong>参数添加新规则，那么就是无用功。</div>
<div></div>
<div><strong>1.语法</strong></div>
<div>iptables -A chain firewall-rule</div>
<ul>
<li>-A chain – 指定要追加规则的链</li>
<li>firewall-rule – 具体的规则参数</li>
</ul>
<div><strong>2.描述规则的基本参数</strong></div>
<div>以下这些规则参数用于描述数据包的协议、源地址、目的地址、允许经过的网络接口，以及如何处理这些数据包。这些描述是对规则的基本描述。</div>
<div></div>
<div><strong>-p 协议（protocol）</strong></div>
<ul>
<li>指定规则的协议，如tcp, udp, icmp等，可以使用<strong>all</strong>来指定所有协议。</li>
<li>如果不指定<strong>-p</strong>参数，则默认是<strong>all</strong>值。这并不明智，请总是明确指定协议名称。</li>
<li>可以使用协议名(如tcp)，或者是协议值（比如6代表tcp）来指定协议。映射关系请查看<em>/etc/protocols</em></li>
<li>还可以使用<strong>–protocol</strong>参数代替<strong>-p</strong>参数</li>
</ul>
<div><strong>-s 源地址（source）</strong></div>
<ul>
<li>指定数据包的源地址</li>
<li>参数可以使IP地址、网络地址、主机名</li>
<li>例如：-s 192.168.1.101指定IP地址</li>
<li>例如：-s 192.168.1.10/24指定网络地址</li>
<li>如果不指定-s参数，就代表所有地址</li>
<li>还可以使用<strong>–src</strong>或者<strong>–source</strong></li>
</ul>
<div><strong>-d 目的地址（destination）</strong></div>
<ul>
<li>指定目的地址</li>
<li>参数和<strong>-s</strong>相同</li>
<li>还可以使用<strong>–dst</strong>或者<strong>–destination</strong></li>
</ul>
<div><strong>-j 执行目标（jump to target）</strong></div>
<ul>
<li><strong>-j</strong>代表”jump to target”</li>
<li><strong>-j</strong>指定了当与规则(Rule)匹配时如何处理数据包</li>
<li>可能的值是ACCEPT, DROP, QUEUE, RETURN</li>
<li>还可以指定其他链（Chain）作为目标</li>
</ul>
<div><strong>-i 输入接口（input interface）</strong></div>
<ul>
<li><strong>-i</strong>代表输入接口(input interface)</li>
<li><strong>-i</strong>指定了要处理来自哪个接口的数据包</li>
<li>这些数据包即将进入INPUT, FORWARD, PREROUTE链</li>
<li>例如：<strong>-i eth0</strong>指定了要处理经由eth0进入的数据包</li>
<li>如果不指定<strong>-i</strong>参数，那么将处理进入所有接口的数据包</li>
<li>如果出现<strong>!</strong> -i eth0，那么将处理所有经由<strong>eth0以外的接口</strong>进入的数据包</li>
<li>如果出现-i eth<strong>+</strong>，那么将处理所有经由<strong>eth开头的接口</strong>进入的数据包</li>
<li>还可以使用<strong>–in-interface</strong>参数</li>
</ul>
<div><strong>-o 输出（out interface）</strong></div>
<ul>
<li><strong>-o</strong>代表”output interface”</li>
<li><strong>-o</strong>指定了数据包由哪个接口输出</li>
<li>这些数据包即将进入FORWARD, OUTPUT, POSTROUTING链</li>
<li>如果不指定<strong>-o</strong>选项，那么系统上的所有接口都可以作为输出接口</li>
<li>如果出现<strong>!</strong> -o eth0，那么将从<strong>eth0以外的接口</strong>输出</li>
<li>如果出现-i eth<strong>+</strong>，那么将仅从<strong>eth开头的接口</strong>输出</li>
<li>还可以使用<strong>–out-interface</strong>参数</li>
</ul>
<div><strong>3.描述规则的扩展参数</strong></div>
<div>对规则有了一个基本描述之后，有时候我们还希望指定端口、TCP标志、ICMP类型等内容。</div>
<div></div>
<div><strong>–sport 源端口（source port）针对 -p tcp 或者 -p udp</strong></div>
<ul>
<li>缺省情况下，将匹配所有端口</li>
<li>可以指定端口号或者端口名称，例如”–sport 22″与”–sport ssh”。</li>
<li><em>/etc/services</em>文件描述了上述映射关系。</li>
<li>从性能上讲，使用端口号更好</li>
<li>使用冒号可以匹配端口范围，如”–sport 22:100″</li>
<li>还可以使用”–source-port”</li>
</ul>
<div><strong>–-dport 目的端口（destination port）针对-p tcp 或者 -p udp</strong></div>
<ul>
<li>参数和–sport类似</li>
<li>还可以使用”–destination-port”</li>
</ul>
<div><strong>-–tcp-flags TCP标志 针对-p tcp</strong></div>
<ul>
<li>可以指定由逗号分隔的多个参数</li>
<li>有效值可以是：SYN, ACK, FIN, RST, URG, PSH</li>
<li>可以使用<strong>ALL</strong>或者<strong>NONE</strong></li>
</ul>
<div><strong>-–icmp-type ICMP类型 针对-p icmp</strong></div>
<ul>
<li>–icmp-type 0 表示Echo Reply</li>
<li>–icmp-type 8 表示Echo</li>
</ul>
<div><strong>4.追加规则的完整实例：仅允许SSH服务</strong></div>
<div>本例实现的规则将仅允许SSH数据包通过本地计算机，其他一切连接（包括ping）都将被拒绝。</div>
<div></div>
<div># 1.清空所有iptables规则<br />
iptables -F&nbsp;</p>
<p># 2.接收目标端口为22的数据包<br />
iptables -A INPUT -i eth0 -p tcp &#8211;dport 22 -j ACCEPT</p>
<p># 3.拒绝所有其他数据包<br />
iptables -A INPUT -j DROP</p>
</div>
<div></div>
<div><strong>六、更改默认策略</strong></div>
<div></div>
<div>上例的例子仅对接收的数据包过滤，而对于要发送出去的数据包却没有任何限制。本节主要介绍如何更改链策略，以改变链的行为。</div>
<div></div>
<div><strong>1. 默认链策略</strong></div>
<div><strong>/!\警告</strong>：请勿在远程连接的服务器、虚拟机上测试！</div>
<div>当我们使用-L选项验证当前规则是发现，所有的链旁边都有<strong>policy ACCEPT</strong>标注，这表明当前链的默认策略为ACCEPT：</div>
<div></div>
<div># iptables -L<br />
Chain INPUT (policy ACCEPT)<br />
target    prot opt source              destination<br />
ACCEPT    tcp  &#8211;  anywhere            anywhere            tcp dpt:ssh<br />
DROP      all  &#8211;  anywhere            anywhere&nbsp;</p>
<p>Chain FORWARD (policy ACCEPT)<br />
target    prot opt source              destination</p>
<p>Chain OUTPUT (policy ACCEPT)<br />
target    prot opt source              destination</p>
</div>
<div></div>
<div>这种情况下，如果没有明确添加DROP规则，那么默认情况下将采用ACCEPT策略进行过滤。除非：</div>
<div><strong>a)为以上三个链单独添加DROP规则：</strong></div>
<div></div>
<div>iptables -A INPUT -j DROP<br />
iptables -A OUTPUT -j DROP<br />
iptables -A FORWARD -j DROP</div>
<div></div>
<div><strong>b)更改默认策略：</strong></div>
<div></div>
<div>iptables -P INPUT DROP<br />
iptables -P OUTPUT DROP<br />
iptables -P FORWARD DROP</div>
<div></div>
<div>糟糕！！如果你严格按照上一节的例子配置了iptables，并且现在使用的是SSH进行连接的，那么会话恐怕已经被迫终止了！</div>
<div>为什么呢？因为我们已经把OUTPUT链策略更改为DROP了。此时虽然服务器能接收数据，但是无法发送数据：</div>
<div></div>
<div># iptables -L<br />
Chain INPUT <strong>(policy DROP)</strong><br />
target    prot opt source              destination<br />
ACCEPT    tcp  &#8211;  anywhere            anywhere            tcp dpt:ssh<br />
DROP      all  &#8211;  anywhere            anywhere&nbsp;</p>
<p>Chain FORWARD <strong>(policy DROP)</strong><br />
target    prot opt source              destination</p>
<p>Chain OUTPUT <strong>(policy DROP)</strong><br />
target    prot opt source              destination</p>
</div>
<div></div>
<div><strong>七、配置应用程序规则</strong></div>
<div></div>
<div>尽管5.4节已经介绍了如何初步限制除SSH以外的其他连接，但是那是在链默认策略为ACCEPT的情况下实现的，并且没有对输出数据包进行限制。本节在上一节基础上，以SSH和HTTP所使用的端口为例，教大家如何在默认链策略为DROP的情况下，进行防火墙设置。在这里，我们将引进一种新的参数-m state，并检查数据包的状态字段。</div>
<div></div>
<div><strong>1.SSH</strong></div>
<div># 1.允许接收远程主机的SSH请求<br />
iptables -A INPUT -i eth0 -p tcp &#8211;dport 22 -m state &#8211;state NEW,ESTABLISHED -j ACCEPT&nbsp;</p>
<p># 2.允许发送本地主机的SSH响应<br />
iptables -A OUTPUT -o eth0 -p tcp &#8211;sport 22 -m state &#8211;state ESTABLISHED -j ACCEPT</p>
</div>
<ul>
<li><strong>-m state:</strong> 启用状态匹配模块（state matching module）</li>
<li><strong>–-state:</strong> 状态匹配模块的参数。当SSH客户端第一个数据包到达服务器时，状态字段为NEW；建立连接后数据包的状态字段都是ESTABLISHED</li>
<li><strong>–sport 22:</strong> sshd监听22端口，同时也通过该端口和客户端建立连接、传送数据。因此对于SSH服务器而言，源端口就是22</li>
<li><strong>–dport 22:</strong> ssh客户端程序可以从本机的随机端口与SSH服务器的22端口建立连接。因此对于SSH客户端而言，目的端口就是22</li>
</ul>
<div>如果服务器也需要使用SSH连接其他远程主机，则还需要增加以下配置：</div>
<div></div>
<div># 1.送出的数据包目的端口为22<br />
iptables -A OUTPUT -o eth0 -p tcp &#8211;dport 22 -m state &#8211;state NEW,ESTABLISHED -j ACCEPT&nbsp;</p>
<p># 2.接收的数据包源端口为22<br />
iptables -A INPUT -i eth0 -p tcp &#8211;sport 22 -m state &#8211;state ESTABLISHED -j ACCEPT</p>
</div>
<div></div>
<div><strong>2.HTTP</strong></div>
<div>HTTP的配置与SSH类似：</div>
<div></div>
<div># 1.允许接收远程主机的HTTP请求<br />
iptables -A INPUT -i eth0 -p tcp &#8211;dport 80 -m state &#8211;state NEW,ESTABLISHED -j ACCEPT&nbsp;</p>
<p># 1.允许发送本地主机的HTTP响应<br />
iptables -A OUTPUT -o eth0 -p tcp &#8211;sport 80 -m state &#8211;state ESTABLISHED -j ACCEPT</p>
</div>
<div></div>
<div><strong>3.完整的配置</strong></div>
<div># 1.删除现有规则<br />
iptables -F&nbsp;</p>
<p># 2.配置默认链策略<br />
iptables -P INPUT DROP<br />
iptables -P FORWARD DROP<br />
iptables -P OUTPUT DROP</p>
<p># 3.允许远程主机进行SSH连接<br />
iptables -A INPUT -i eth0 -p tcp &#8211;dport 22 -m state &#8211;state NEW,ESTABLISHED -j ACCEPT<br />
iptables -A OUTPUT -o eth0 -p tcp &#8211;sport 22 -m state &#8211;state ESTABLISHED -j ACCEPT</p>
<p># 4.允许本地主机进行SSH连接<br />
iptables -A OUTPUT -o eth0 -p tcp &#8211;dport 22 -m state &#8211;state NEW,ESTABLISHED -j ACCEPT<br />
iptables -A INPUT -i eth0 -p tcp &#8211;sport 22 -m state &#8211;state ESTABLISHED -j ACCEPT</p>
<p># 5.允许HTTP请求<br />
iptables -A INPUT -i eth0 -p tcp &#8211;dport 80 -m state &#8211;state NEW,ESTABLISHED -j ACCEPT<br />
iptables -A OUTPUT -o eth0 -p tcp &#8211;sport 80 -m state &#8211;state ESTABLISHED -j ACCEPT</p>
</div>
<div></div>
<div><strong>References</strong></div>
<div></div>
<div>[1] <a href="http://www.thegeekstuff.com/2011/01/iptables-fundamentals/">Linux Firewall Tutorial: IPTables Tables, Chains, Rules Fundamentals</a></div>
<div>[2] <a href="http://www.thegeekstuff.com/2011/01/redhat-iptables-flush/">IPTables Flush: Delete / Remove All Rules On RedHat and CentOS Linux</a></div>
<div>[3] <a href="http://www.thegeekstuff.com/2011/02/iptables-add-rule/">Linux IPTables: How to Add Firewall Rules (With Allow SSH Example)</a></div>
<div>[4] <a href="http://www.thegeekstuff.com/2011/03/iptables-inbound-and-outbound-rules/">Linux IPTables: Incoming and Outgoing Rule Examples (SSH and HTTP)</a></div>
<div>[5] <a href="http://www.thegeekstuff.com/2011/06/iptables-rules-examples/">25 Most Frequently Used Linux IPTables Rules Examples</a></div>
<div>[6] man 8 iptables</div>
</div>
