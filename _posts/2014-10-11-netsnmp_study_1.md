---
layout: post
title: "NetSnmp初步（一）：让我们的程序提供snmp服务"
categories: 网络
tags: [netsnmp, snmp]
date: 2014-10-11 08:52:40
---

录制程序要提供远程控制功能，大概需求为：

（1）可以查询程序当前的运行状态：录制了多少路节目，每路节目的状态，数据码率 等等；

（2）可以远程控制节目的起停，也就是发一个命令，就可以停掉某一路节目；

（3）异常情况，主动上报。 

上头决定使用snmp来实现。这几天研究了一下，做点笔记。 

 

闲话休叙，开工干活：

1.去netsnmp官网下载最新版本，我下的是5.7.1源码。

2.解压到任意目录，然后configure,make, sudo make install三步曲搞定。
（在我的ubuntu10.10上，需要安装libperl-dev，否则make时会连接失败。）

3.配置net-snmp，让它跑起来。

(1)关于net-snmp的详细配置，可以参看系统手册页。（强烈建议先看！！！了解一下snmp的配置）。
<pre>
#man snmp_config
#man snmp.conf
#man snmpd.conf
</pre>
(2)#sudo snmpd

(最好使用sudo启动snmpd，否则默认情况下没有权限，会启动失败退出，而又没有任何打印信息)

4.添加MIB文件

（1）写MIB文件（暂时使用已有的，文件名FIGURE-IT-MIB.txt）

（2）首先，将MIB文件拷到snmp的mibs目录下，有两种方式：
<pre>
#cp FIGURE-IT-MIB.txt /usr/local/share/snmp/mibs
(which makes it available to everyone on the system)
or
#mkdir $HOME/.snmp
#mkdir $HOME/.snmp/mibs
#cp MY-MIB.txt $HOME/.snmp/mibs
</pre>
(which makes it available to you only)

具体可参看：http://www.net-snmp.org/docs/FAQ.html#How_do_I_add_a_MIB_

（3）加载mib库:
{% highlight bash %}
# vi /usr/local/share/snmp/snmp.conf
{% endhighlight %}

（4）检查mib是否正常加载:
{% highlight bash %}
# snmptranslate -IR -Tp record
+--record(1)
|
+--recordStatusTable(1)
|
+--recordStatusEntry(1)
| Index: recordIndex
|
+-- -R-- INTEGER recordIndex(1)
| Range: 0..65535
+-- -R-- String recordChannelName(2)
| Size: 0..256
+-- -R-- String recordFileName(3)
| Size: 0..256
+-- -R-- IpAddr recordDeviceIp(4)
+-- -R-- String recordChannelStatus(5)
| Size: 1..256
+-- -RW- EnumVal recordChannelOp(6)
Textual Convention: RowStatus
Values: active(1), notInService(2), notReady(3), createAndGo(4), createAndWait(5), destroy(6)
{% endhighlight %}

4.使用mib2c生成代码：

{% highlight bash %}
# sudo mib2c -c mib2c.iterate.conf FIGURE-IT-MIB::recordStatusTable
{% endhighlight %}

（1）通过-c mib2c.iterate.conf 指定使用的模板名，模板位于：“/usr/local/share/snmp”下。

（2）由于我在FIGURE-IT-MIB.txt中使用的table类型的，所以在这里指定“mib2c.iterate.conf”，其实也可使用“mib2c.mfd.conf”模板，但我在编译时出现错误：

“ERROR: unknown node.decl: in_addr_t

exiting at conf file (/usr/local/share/snmp/mib2c-data/node-get.m2i:91) request”

在net-snmp的邮件列表中，有人说是Bug，修改一行代码就OK，我没试。

"http://sourceforge.net/mailarchive/forum.php?thread_name=20120227102423.5dcb9663%40freesnmp.com&forum_name=net-snmp-coders"

（3）mib2c提示生成的代码是否带数据缓存，缓存主要是减少snmp客户端频繁访问数据时真正获取数据的次数，提高性能用的。如果在很短的时间内获取相同的数据，就直接返回缓存的数据，而不需要每次去更新数据。这里我选择生成带缓存的代码。

（4）编译成功后，就会在当前目录下生成两个文件：

recordStatusTable.c和recordStatusTable.h

（5）生成的源文件是有语法错误的，一个个修改掉就ok了。

（6）在生成的代码中，大部分工作已近完成了，我们需要做的就是获取、维护返回给snmp客户端的数据。我们需要关注下面几个函数：

1）这数据是通过一个链表维护的，链表的插入、销毁分别是通过recordStatusTable_createEntry()、recordStatusTable_removeEntry()函数完成的（根据表名，实际的函数名会不一样，但是以_createEntry和_removeEntry结尾的函数，下同）。

2）recordStatusTable_load(),当接收到snmp请求时，如果缓存的数据已超时，就会调用该函数来更新数据；否则，将直接使用缓存数据。我们需要在该函数里给缓存数据赋值。

我的示例如下：

{% highlight bash %}
int recordStatusTable_load(netsnmp_cache *cache, void *vmagic)
{
    if(g_pRecordCfg == NULL)
    {
        return -1;
    }

    for(unsigned int i=0; i<g_pRecordCfg->m_pRecordModules.size(); i++)
    {
        CRecordRule* pRule = g_pRecordCfg->m_pRecordModules[i]->m_pRecordRule;
        IChannel* pChan = g_pRecordCfg->m_pRecordModules[i]->m_pChannel;
        IInput* pInput = g_pRecordCfg->m_pRecordModules[i]->m_pInput;
        IOutput* pOutput = g_pRecordCfg->m_pRecordModules[i]->m_pOutput;
        if((pRule == NULL) || (pChan == NULL) || (pInput == NULL) || (pOutput == NULL))
        {
            return -1;
        }

        string strChannelName = "[" + CSourceRule::GetSourceType(pChan->m_enmSourceType) + "]" + pChan->m_strName;
        string strFileName = pOutput->CurrentFile();
        string strInputRate = pInput->m_pStatistics->Info();
        string strOutputRate = pOutput->m_pStatistics->Info();
        string strStatus = g_pRecordCfg->m_pRecordModules[i]->Status();

        struct recordStatusTable_entry * pEntery = recordStatusTable_createEntry(pRule->m_nRuleID);
        strcpy(pEntery->ChannelName, strChannelName.c_str());
        pEntery->ChannelName_len = strlen(strChannelName.c_str());
        pEntery->DeviceIp = inet_addr(pChan->m_strDeviceIP.c_str());
        strcpy(pEntery->FileName, strFileName.c_str());
        pEntery->FileName_len = strlen(strFileName.c_str());
        strcpy(pEntery->InputRate, strInputRate.c_str());
        pEntery->InputRate_len = strlen(strInputRate.c_str());
        strcpy(pEntery->OutputRate, strOutputRate.c_str());
        pEntery->OutputRate_len = strlen(strOutputRate.c_str());
        strcpy(pEntery->Status, strStatus.c_str());
        pEntery->Status_len = strlen(strStatus.c_str());
    }

    return 0;
}
{% endhighlight %}



3）recordStatusTable_free()，当缓存的数据超时后，系统会自动调用该函数将缓存释放掉；但并不会主动调用recordStatusTable_load()来更新数据，除非收到新的snmp数据请求。可以不用关注。


5.将生成的recordStatusTable.c和recordStatusTable.h文件加入到工程中，修改Makefile，添加net-snmp头文件和库依赖。

net-snmp的头文件在源码目录下的include目录下，即<snmp-src>/include；
库文件一般在/usr/lib下。

{% highlight bash %}
# ls /usr/lib |grep libnetsn
libnetsnmpagent.so.15
libnetsnmpagent.so.15.1.2
libnetsnmphelpers.so.15
libnetsnmphelpers.so.15.1.2
libnetsnmpmibs.so.15
libnetsnmpmibs.so.15.1.2
libnetsnmp.so.15
libnetsnmp.so.15.1.2
libnetsnmptrapd.so.15
libnetsnmptrapd.so.15.1.2
{% endhighlight %}
在Makefile中添加“-lnetsnmp -lnetsnmpagent -lnetsnmphelpers -lnetsnmptrapd -lnetsnmpmibs”即可。

6.(1)在项目中开启一个线程，启动snmp服务。

{% highlight bash %}
void CSnmpThread::run()
{
    LOG(LOG_TYPE_NOTICE, "[Thread] CSnmpThread Start.");

    int agentx_subagent=0; /* change this if you want to be a SNMP master agent */
    int background = 0; /* change this if you want to run in the background */
    int syslog = 0; /* change this if you want to use syslog */

    //snmp_set_do_debugging(1);

    /* print log errors to syslog or stderr */
    if (syslog)
    {
        snmp_enable_calllog();
    }
    else
    {
        snmp_enable_stderrlog();
    }

    /* we're an agentx subagent? */
    if (agentx_subagent)
    {
        /* make us a agentx client. */
        netsnmp_ds_set_boolean(NETSNMP_DS_APPLICATION_ID, NETSNMP_DS_AGENT_ROLE, 1);
    }

    /* run in background, if requested */
    if (background && netsnmp_daemonize(1, !syslog))
    {
        LOG(LOG_TYPE_NOTICE, "netsnmp_daemonize() failed. [Thread] CSnmpThread exit!");
        return;
    }

    /* Initialize tcpip, if necessary */
    SOCK_STARTUP;

    /* Initialize the agent library */
    init_agent("Record");

    /* Initialize our mib code here */
    init_recordStatusTable(); // 加载节点信息

    /* initialize vacm/usm access control  */
//    if (!agentx_subagent)
//    {
//        void  init_vacm_vars();
//        void  init_usmUser();
//    }

    /* Example-demon will be used to read example-demon.conf files. */
    init_snmp("Record");// 配置文件名---->/usr/local/share/snmp/Record.conf

    /* If we're going to be a snmp master agent, initial the ports */
    if (!agentx_subagent)
    {
        init_master_agent();  /* open the port to listen on (defaults to udp:161) */
    }

    /* In case we recevie a request to stop (kill -TERM or kill -INT) */
    keep_running = 1;
    //signal(SIGTERM, stop_server);
//signal(SIGINT, stop_server);

    LOG(LOG_TYPE_INFO,"snmp service is up and running");

    /* your main loop here... */
    while(keep_running)
    {
        /* if you use select(), see snmp_select_info() in snmp_api(3) */
        /*     --- OR ---  */
        agent_check_and_process(1); /* 0 == don't block */
    }

    /* at shutdown time */
    snmp_shutdown("Record");
    SOCK_CLEANUP;
    return;
}

{% endhighlight %}

(2)编写配置文件Record.conf，放到vi /usr/local/share/snmp/下。

<pre>
###############################################################################
# Access Control
###############################################################################

#       sec.name  source          community
com2sec local     localhost       public
com2sec mynetwork 192.168.0.0/24      public

####
# Second, map the security names into group names:

#                 sec.model  sec.name
group MyRWGroup    v1         local
group MyRWGroup    v2c        local
group MyRWGroup    usm        local
group MyROGroup v1         mynetwork
group MyROGroup v2c        mynetwork
group MyROGroup usm        mynetwork

####
# Third, create a view for us to let the groups have rights to:

#           incl/excl subtree                          mask
view all    included  .1                               80

####
# Finally, grant the 2 groups access to the 1 view with different
# write permissions:

#              context sec.model sec.level match  read   write  notif
access MyROGroup ""      any       noauth    exact  all    none   none
access MyRWGroup ""      any       noauth    exact  all    all    none

agentaddress 161

</pre>

配置文件是从别处拷来的，具体待研究。

7.测试snmp.

(1)编译程序，sudo后以root权限运行。

否则会报错：
“Error opening specified endpoint "161"”

(2)snmpwalk -v1 -c public localhost recordStatusTable

如果看到类似如下信息，就说明成功了：
<pre>
FIGURE-IT-MIB::Index.1 = INTEGER: 1
FIGURE-IT-MIB::Index.3 = INTEGER: 3
FIGURE-IT-MIB::Index.4 = INTEGER: 4
FIGURE-IT-MIB::ChannelName.1 = Hex-STRING: 5B 53 74 72 65 61 6D 54 53 5D E7 A0 81 E6 B5 81 
5F E9 AD 85 E5 8A 9B E9 9F B3 20 E4 B9 90 E4 B8 
BB E8 B7 AF 
FIGURE-IT-MIB::ChannelName.3 = Hex-STRING: 5B 41 75 64 69 6F 50 61 72 61 6D 5D E9 9F B3 E9 
A2 91 E5 8F 82 E6 95 B0 5F E8 8A 82 E7 9B AE 31 
FIGURE-IT-MIB::ChannelName.4 = Hex-STRING: 5B 54 65 6D 70 48 75 6D 69 5D E6 B8 A9 E6 B9 BF 
E5 BA A6 5F E9 80 9A E9 81 93 31 
FIGURE-IT-MIB::DeviceIp.1 = IpAddress: 10.0.60.2
FIGURE-IT-MIB::DeviceIp.3 = IpAddress: 10.0.60.2
FIGURE-IT-MIB::DeviceIp.4 = IpAddress: 10.0.60.2
FIGURE-IT-MIB::Status.1 = STRING: "[Input]:No Input Data. [Output]:No Input Data."
FIGURE-IT-MIB::Status.3 = STRING: "[Input]:No Input Data. [Output]:No Input Data."
FIGURE-IT-MIB::Status.4 = STRING: "[Input]:No Input Data. [Output]:No Input Data."
FIGURE-IT-MIB::InputRate.1 = STRING: "0(bytes) "
FIGURE-IT-MIB::InputRate.3 = STRING: "0"
FIGURE-IT-MIB::InputRate.4 = STRING: "0"
FIGURE-IT-MIB::OutputRate.1 = STRING: "0(bytes) "
FIGURE-IT-MIB::OutputRate.3 = STRING: "0"
FIGURE-IT-MIB::OutputRate.4 = STRING: "0"
FIGURE-IT-MIB::FileName.1 = Hex-STRING: 2F 66 69 67 75 72 65 2F 52 65 63 6F 72 64 2F 53 
74 72 65 61 6D 54 53 2F 31 2D 31 2D E7 A0 81 E6 
B5 81 5F E9 AD 85 E5 8A 9B E9 9F B3 20 E4 B9 90 
E4 B8 BB E8 B7 AF 2F 32 30 31 32 2D 30 33 2D 32 
38 2F 32 30 31 32 30 33 32 38 31 36 31 38 30 30 
2E 74 73 
FIGURE-IT-MIB::FileName.3 = Hex-STRING: 2F 66 69 67 75 72 65 2F 52 65 63 6F 72 64 2F 41 
75 64 69 6F 50 61 72 61 6D 2F 35 2D 33 2D E9 9F 
B3 E9 A2 91 E5 8F 82 E6 95 B0 5F E8 8A 82 E7 9B 
AE 31 2F 32 30 31 32 2D 30 33 2D 32 38 2F 32 30 
31 32 30 33 32 38 31 36 31 37 34 31 2E 70 61 72 
61 6D 
FIGURE-IT-MIB::FileName.4 = ""
End of MIB

</pre>

(3)有一个问题，snmpwalk似乎不支持中文？都是以ascii码输出中文？以后再研究。

8.经实际测试，我们的程序作为agent，可以单独提供snmp服务，并不需要再启动snmpd服务。

9.程序出现异常情况需要主动上报，接下来研究Notifications看看（初步看下来，In SNMPv1的TRAPs 似乎足够了，因为我们不需要receiver的响应，“http://www.net-snmp.org/wiki/index.php/TUT:Configuring_snmptrapd_to_receive_SNMPv3_notifications”）。

<pre>
原文：　http://www.cnblogs.com/chutianyao/archive/2012/03/28/2421576.html
</pre>
