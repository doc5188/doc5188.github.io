---
layout: post
title: "NetSnmp初步（三）：接收控制命令：实现SNMP的SET命令"
categories: 网络
tags: [netsnmp, snmp]
date: 2014-10-11 09:06:35
---

主要是接收并处理snmp客户端发送控制命令：启动/停止单个节目的录制。也就是实现snmp的SET命令。

1.还是从MIB开始。

由于只是一个简单的起停命令，前面定义的recordStatusTable中的Status字段完全满足要求，我们只需要给它设置一个不同的值就可以了。

之前在文件"/usr/local/share/snmp/mibs/FIGURE-IT-MIB.txt"中给它定义的访问属性是：“read-only”,将它改成“read-write”就OK了。

2.生成代码，与之前完全相同，就不多说了。

3.由于包含有“read-write”属性的IOD，生成的代码就多了些处理动作。我们在处理函数recordStatusTable_handler()的“case MODE_SET_ACTION”如下实现：

{% highlight bash %}
for (request = requests; request; request = request->next)
{
table_entry = (struct recordStatusTable_entry *)netsnmp_extract_iterator_context(request);
table_info = netsnmp_extract_table_info(request);
switch (table_info->colnum)
{
    case COLUMN_STATUS:
        memcpy(table_entry->old_Status,
               table_entry->Status,
               sizeof (table_entry->Status));
        table_entry->old_Status_len =
                table_entry->Status_len;
        memset(table_entry->Status, 0,
               sizeof (table_entry->Status));
        memcpy(table_entry->Status,
               request->requestvb->val.string,
               request->requestvb->val_len);
        table_entry->Status_len =
                request->requestvb->val_len;

        //在此响应设置命令
        LOG(LOG_TYPE_NOTICE, "RECV SNMP CMD[SET]: rule[%ld]:%s\n", table_entry->Index, table_entry->Status);
        if (g_pRecordCfg != NULL)
        {
            if(strcasecmp(table_entry->Status, "stop") == 0)
            {
                g_pRecordCfg->StartChannel(table_entry->Index);
            }
            else if(strcasecmp(table_entry->Status, "start") == 0)
            {
                g_pRecordCfg->StopChannel(table_entry->Index);
            }
        }
        break;
}
}
break;

{% endhighlight %}
 

4.修改配置文件，/usr/local/share/snmp/Record.conf,确保里面类似有如下一行：
<pre>
rwcommunity public
</pre>

这个“public”可以定义成自己想要的其他名称，但一定要是rwcommunity，表示赋予读写权限。

更多的，参见FAQ的“How do I configure access control?”

5.编译程序，使用snmpset发送测试命令：

{% highlight bash %}
# snmpset -v 1 -c public localhost FIGURE-IT-MIB::recordStatusTable.recordStatusEntry.Status.3 s stop
{% endhighlight %}

简单解释一下
<pre>
-v 1：表示使用snmp v1命令

-c public localhost ：表示"public"就是上面定义的名称。

FIGURE-IT-MIB::recordStatusTable.recordStatusEntry.Status 就是OID

3:表示设置index=3的行中的Status列

s：要设置值的类型

stop:就是具体的值了。
</pre>

可以看到程序输出：

<pre>
2012-03-30 14:32:26,826: NOTICE : RECV SNMP CMD[SET]: rule[3]:stop
</pre>

说明就Ok了。

6.snmp到此告一段落了。一点体会：snmp虽然叫简单网管协议，可协议本身真的不简单！ 




<pre>
referer: http://www.cnblogs.com/chutianyao/archive/2012/03/30/2425266.html
</pre>
