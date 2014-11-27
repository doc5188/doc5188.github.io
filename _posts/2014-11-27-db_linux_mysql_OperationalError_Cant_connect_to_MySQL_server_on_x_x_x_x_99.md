---
layout: post
title: "关于大并发mysql连接引起数据库错误OperationalError: (2003, \"Can't connect to MySQL server on 'x.x.x.x (99)\")分析"
categories: 数据库
tags: [mysql, OperationalError, linux]
date: 2014-11-27 12:56:36
---

<p>之前线上一个服务偶尔会产生数据库连接失败的错误，类&#20284;这种</p>
<p></p>
<pre name="code" class="plain">OperationalError: (2003, &quot;Can't connect to MySQL server on '127.0.0.1' (99)&quot;)
</pre><br>
通过分析业务逻辑，分析出引起这个问题的原因是因为当时短时间内产生了大量的数据库连接。
<p></p>
<p>接着我在本地测试环境写了下面的python脚本</p>
<p></p>
<pre name="code" class="plain">import MySQLdb
def test(self):
    while True:          
        db = MySQLdb.connect(host='127.0.0.1', user='me',passwd='mypassword')
        c = db.cursor()
        c.close()
        db.close()
        print i
        i = i + 1
</pre>执行之后，在12秒之后报相同的错误退出，整个过程中开启了28287个连接。
<p><br>
</p>
<p>在这12秒过程中监控数据库发现当时的数据库连接数在15以下，是正常状态。因此基本可以断定这个bug和数据库本身没有主要关系。</p>
<p>通过下面命令可以统计当前各种状态的连接的数量</p>
<p></p>
<pre name="code" class="plain"># netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
TIME_WAIT 28417
ESTABLISHED 49
</pre>可能出现的情况以及解释
<p></p>
<p></p>
<pre name="code" class="plain">CLOSED：无连接是活动的或正在进行
LISTEN：服务器在等待进入呼叫
SYN_RECV：一个连接请求已经到达，等待确认
SYN_SENT：应用已经开始，打开一个连接
ESTABLISHED：正常数据传输状态
FIN_WAIT1：应用说它已经完成
FIN_WAIT2：另一边已同意释放
ITMED_WAIT：等待所有分组死掉
CLOSING：两边同时尝试关闭
TIME_WAIT：另一边已初始化一个释放
LAST_ACK：等待所有分组死掉</pre><br>
<p>可以看到连接数据库失败的时候，存在大量的time_wait状态的连接。基本可以断定造成此Bug的原因是因为time_wait积累导致端口耗尽。</p>
<p>产生time_wait的原因：</p>
<p>当某个tcp端点关闭tcp连接时，会在内存中维护一个小的控制块，用来记录最近关闭链接的ip地址和端口号，这类信息只会维持一小段时间，通常是所估计的最大分段使用期的两倍（成为2MSL,通常为2分钟），在这段时间内无法重新创建两个具有相同ip地址和端口号的连接。</p>
<p>在本场景下构建一条tcp连接的4个&#20540;</p>
<p></p>
<pre name="code" class="plain">&lt;source-IP-address,source-port,destination-address,desctnation-port&gt;</pre>中只有源端口号是可以改变的，客户端（python脚本所在机器）每次连接到服务器（数据库）上去时，都会获得一个新的原端口，以实现链接惟一性，
<p></p>
<p>但是由于可用端口的数量有限（比如60000）个，而在2MSL秒（比如120秒）内连接是无法重用的，连接率被限制在60000/120=500秒/次。</p>
<p>当前场景就是因为连接率过高导致time_wait端口耗尽的问题，端口耗尽后由于没有可用端口自然遇到连接数据库失败.</p>
<p><br>
</p>
<p>知道问题的原因我们可以从两方面解决问题:</p>
<p>1.减少time_wait连接等待时间</p>
<p>通过修改内核参数解决</p>
<p>主要修改两个参数</p>
<p></p>
<pre name="code" class="plain">tcp_tw_recycle - BOOLEAN
	Enable fast recycling TIME-WAIT sockets. Default value is 0.
	It should not be changed without advice/request of technical
	experts.

tcp_tw_reuse - BOOLEAN
	Allow to reuse TIME-WAIT sockets for new connections when it is
	safe from protocol viewpoint. Default value is 0.
	It should not be changed without advice/request of technical
	experts.</pre><a target="_blank" target="_blank" href="https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt">参考自</a>
<p></p>
<p>修改方法如下</p>
<p></p>
<pre name="code" class="plain">[root@aaa1 ~]# sysctl -a|grep net.ipv4.tcp_tw
net.ipv4.tcp_tw_reuse = 0
net.ipv4.tcp_tw_recycle = 0
[root@aaa1 ~]#

vim /etc/sysctl.conf
增加或修改net.ipv4.tcp_tw值：
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1

使内核参数生效：
[root@aaa1 ~]# sysctl -p

[root@aaa1 ~]# sysctl -a|grep net.ipv4.tcp_tw
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1</pre><br>
2.增加客户端负载生成机器的数量,或这个确保客户端和服务器在循环使用几个虚拟ip地址已增加更多的连接组合,
<p></p>
<p>在本场景中因为是主要和数据库的交互,可以通过创建数据库连接池复用myslq连接较少新连接的生成.</p>
<p><br>
</p>
<p>参考资料</p>
<p>http://elf8848.iteye.com/blog/1739571<br>
</p>
<p>http://blog.csdn.net/sungblog/article/details/1385345<br>
</p>
<p>&lt;&lt;http权威指南&gt;&gt; 4.2.7 TIME_WAIT累积与端口耗尽</p>


<pre>
referer:http://blog.csdn.net/a657941877/article/details/23350133
</pre>
