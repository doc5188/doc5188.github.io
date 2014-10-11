---
layout: post
title: "NetSnmp初步（二）：发送Notification"
categories: 网络
tags: [netsnmp, snmp]
date: 2014-10-11 09:00:09
---

前面提到了程序要主动上报异常状况，snmp提供了notification机制来实现此功能。大致步骤如下：

1.还是从MIB文件开始：

在文件"/usr/local/share/snmp/mibs/FIGURE-IT-MIB.txt"增加如下内容：

{% highlight bash %}
recordNotification NOTIFICATION-TYPE
    OBJECTS     { recordTrapsEntry }
    STATUS      current
    DESCRIPTION
        "Record's notifications "
::= { record 2 }

recordTrapsEntry OBJECT-TYPE
--    SYNTAX      SnmpAdminString
    SYNTAX  OCTET STRING (SIZE(1..512))
    MAX-ACCESS  accessible-for-notify
    STATUS      current
    DESCRIPTION
        "Record's notifications entery."
    ::= { recordNotification 1 }

{% endhighlight %}

通过snmptranslate -IR -Tp record命令检查mib文件是否添加正确。

2.使用mib2c生成代码：

{% highlight bash %}
# sudo mib2c -c mib2c.notify.conf FIGURE-IT-MIB::recordNotification
{% endhighlight %}

生成的代码照例有些小问题，改掉就Ok了。

其实就一个函数：send_recordNotification_trap(),我们通过它来发送trap消息。

我对它做了点小改造：添加了一个string参数，这样我们就可以发送不同的消息了。

3.将代码添加到工程中，在需要发送trap的时候调用send_recordNotification_trap().

4.【<span style="color: rgb(255, 0, 0);"><strong>重要提示！</strong></span>】

修改配置文件：/usr/local/share/snmp/Record.conf

确保包含类似如下的内容：
<pre>
trapsink localhost public
</pre>

否则即使调用了send_recordNotification_trap()函数，也不会发送任何trap的。我之前测试很久，一直都没有发送成功，添加这一行之后才Ok的。

SNMP的FAQ文档中对此有说明：

“ If this file contains 'trapsink', then the agent will send an SNMPv1 trap. If this file contains 'trap2sink', then the agent will send an SNMPv2c trap. And if this file contains both, then the agent will send *two* copies of this trap.”

5.接收trap消息：

(1)修改/usr/local/share/snmp/snmptrapd.conf为如下内容：
<pre>
authcommunity execute,log,net public #设置所有用户的访问权限：可 执行，记录，传递

#traphandle default log_it#接收到trap的处理动作，可以不设置
</pre>


(2)#sudo snmptrapd -d -f -Lo

如果有类似如下输出，就说名发送trap消息成功了：
<pre>
2012-03-29 16:52:54 192.168.110.68(via UDP: [127.0.0.1]:50370->[127.0.0.1]:162) TRAP, SNMP v1, community public
     FIGURE-IT-MIB::record Enterprise Specific Trap (2) Uptime: 0:00:00.17
     FIGURE-IT-MIB::recordTrapsEntry.0 = STRING: "[2012-03-29 16:52:51] NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNsnmp service is up and running."
</pre>

同时通过tcpdump也可以看到发送的trap消息：
{% highlight bash %}
# sudo tcpdump -i lo udp
{% endhighlight %}

6.网上有人报告bug说，发送trap时使用的send_v2trap()函数存在内存泄漏。待研究。





<pre>
referer: http://www.cnblogs.com/chutianyao/archive/2012/03/29/2423763.html
</pre>
