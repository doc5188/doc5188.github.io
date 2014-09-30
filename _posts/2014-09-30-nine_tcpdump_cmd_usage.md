---
layout: post
title: "9个tcpdump使用实例"
categories: linux
tags: [linux, tcpdump]
date: 2014-09-30 14:30:22
---

tcpdump能帮助我们捕捉并保存网络包，保存下来的网络包可用于分析网络负载情况，包可通过tcpdump命令解析，也可以保存成后缀为pcap的文件，使用wireshark等软件进行查看。

 

以下将给出9个使用tcpdump的例子，以说明tcpdump的具体使用方法。

 

* 1.针对特定网口抓包(-i选项)

当我们不加任何选项执行tcpdump时，tcpdump将抓取通过所有网口的包；使用-i选项，我们可以在某个指定的网口抓包：
{% highlight bash %}

linux:/tmp/lx # tcpdump -i eth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 96 bytes
10:50:28.607429 IP 10.70.121.92.autodesk-lm > 10.71.171.140.ssh: . ack 116 win 64951
10:50:28.607436 IP 10.71.171.140.ssh > 10.70.121.92.autodesk-lm: P 116:232(116) ack 1 win 12864
10:50:30.384195 arp who-has 128.128.128.35 tell 128.128.128.35

{% endhighlight %}

以上例子中，tcpdump抓取所有通过eth0的包。

 

* 2.抓取指定数目的包(-c选项)

默认情况下tcpdump将一直抓包，直到按下”ctrl+c”中止，使用-c选项我们可以指定抓包的数量：
{% highlight bash %}

linux:/tmp/lx # tcpdump -c 2 -i eth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 96 bytes
10:58:05.656104 IP 10.71.171.140.ssh > 10.70.121.92.autodesk-lm: P 1210443473:1210443589(116) ack 2583117929 win 12864
10:58:05.657074 IP 10.70.121.92.autodesk-lm > 10.71.171.140.ssh: . ack 116 win 65211

2 packets captured
6 packets received by filter
0 packets dropped by kernel

{% endhighlight %}

以上例子中，只针对eth0网口抓2个包。

 

* 3.将抓到包写入文件中(-w选项)

使用-w选项，我们可将抓包记录到一个指定文件中，以供后续分析

{% highlight bash %}
linux:/tmp/lx # tcpdump -w 20120606.pcap -i eth0
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 96 bytes

75 packets captured
150 packets received by filter
0 packets dropped by kernel
{% endhighlight %}

应当保存为.pcap后缀的文件，方便我们使用wireshark等工具读取分析。

 

* 4.读取tcpdump保存文件(-r选项)

对于保存的抓包文件，我们可以使用-r选项进行读取：

{% highlight bash %}
linux:/tmp/lx # tcpdump -r 20120606.pcap
reading from file 20120606.pcap, link-type EN10MB (Ethernet)
11:01:57.392907 IP 10.71.171.140.ssh > 10.70.121.92.autodesk-lm: P 1210446405:1210446457(52) ack 2583119957 win 12864
11:01:57.392917 IP 10.71.171.140.ssh > 10.70.121.92.autodesk-lm: P 52:168(116) ack 1 win 12864
11:01:57.393649 IP 10.70.121.92.autodesk-lm > 10.71.171.140.ssh: . ack 52 win 65327
{% endhighlight %}

 

* 5.抓包时不进行域名解析(-n选项)

默认情况下，tcpdump抓包结果中将进行域名解析，显示的是域名地址而非ip地址，使用-n选项，可指定显示ip地址。

 

* 6.增加抓包时间戳(-tttt选项)

使用-tttt选项，抓包结果中将包含抓包日期：

{% highlight bash %}
linux:/tmp/lx # tcpdump -n -tttt -i eth0
2012-06-06 11:14:59.539736 IP 10.71.171.140.22 > 10.70.121.95.1787: P 1:53(52) ack 100 win 7504
2012-06-06 11:14:59.539754 IP 10.71.171.140.22 > 10.70.121.95.1787: P 53:105(52) ack 100 win 7504
2012-06-06 11:14:59.539770 IP 10.71.171.140.22 > 10.70.121.95.1787: P 105:157(52) ack 100 win 7504

{% endhighlight %}
 

* 7.指定抓包的协议类型

我们可以只抓某种协议的包，tcpdump支持指定以下协议：ip,ip6,arp,tcp,udp,wlan等。以下例子只抓取arp协议的包：
{% highlight bash %}

linux:/tmp/lx # tcpdump -i eth0 arp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 96 bytes
11:22:26.948656 arp who-has 10.10.1.30 tell 10.10.1.26
11:22:27.017406 arp who-has 10.10.1.30 tell 10.10.1.26
11:22:27.078803 arp who-has 10.10.1.30 tell 10.10.1.26

{% endhighlight %}

 

* 8.指定抓包端口

如果想要对某个特定的端口抓包，可以通过以下命令：
{% highlight bash %}
linux:/tmp/lx # tcpdump -i eth0 port 22
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 96 bytes
11:41:04.387547 IP 10.70.121.92.autodesk-lm > 10.71.171.140.ssh: . ack 1216136825 win 64751
11:41:04.387891 IP 10.71.171.140.ssh > 10.70.121.92.autodesk-lm: P 1:233(232) ack 0 win 16080
11:41:04.398973 IP 10.70.121.92.autodesk-lm > 10.71.171.140.ssh: P 0:52(52) ack 233 win 64519
{% endhighlight %}

如果想要过滤某个特定的端口抓包，可以通过以下命令：
{% highlight bash %}
linux:/tmp/lx # tcpdump -i eth0 port not 22 and port not 80
{% endhighlight %}

 

* 9.抓取特定目标ip和端口的包

网络包的内容中，包含了源ip地址、端口和目标ip、端口，我们可以根据目标ip和端口过滤tcpdump抓包结果，以下命令说明了此用法：

{% highlight bash %}
linux:/tmp/lx # tcpdump -i eth0 dst 10.70.121.92 and port 22
{% endhighlight %}

 

Reference: Packet Analyzer: 15 TCPDUMP Command Examples(http://www.thegeekstuff.com/2010/08/tcpdump-command-examples/)

 
