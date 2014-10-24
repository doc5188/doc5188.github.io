---
layout: post
title: "SNMP Cache机制"
categories: 网络 
tags: [snmp cache]
date: 2014-10-24 09:44:03
---

SNMP Cache机制

使用mib文件生成c代码时，模板用mib2c.iterate.conf才会生成Cache相关的代码，这时候才会有Cache机制。

Cache最主要的相关代码，下面是从SNMPManager中找到的icTable里面的代码：

<pre>
netsnmp_inject_handler( reg,
netsnmp_get_cache_handler(AGENT_TIMEOUT,
                               icTable_load, icTable_free,
                               icTable_oid, icTable_oid_len));
</pre>

这段代码的作用： 
<pre>
1  告诉Agent的超时时间是多少?
2  告诉Agent Load Cache和Free Cache的函数指针
3         Oid
</pre>

告诉Agent这些参数后，大致的过程如下：

当NMS向AgentX发送一个请求时，AgentX会先在Cache里面找，如果Cache 已经Timeout,那么会先Free Cache再Load Cache,如果Cache没有TimeOut那么直接在Cache里面去找，这样对于请求很频繁的需求，会节省很多的时间。

Cache机制主要实现集中在cache_handler.c和cache_handler.h文件中，里面有一个非常重要的结构体：

<pre>
struct netsnmp_cache_s {
        /* For operation of the data caches */
        int      flags;
        int      enabled;
        int      valid;
                      // 判断cache是否是有效的，如果无效会先free后load.
        char     expired;
                     //  判断cache是否超时,主要是根据我们传入的timeout值去判断是否超时
        int      timeout;      /* Length of time the cache is valid (in s) */
                     //  我们传入的timeout值,如果传入-1代表不使用cache机制
        marker_t timestamp;          /* When the cache was last loaded */
        u_long   timer_id;      /* periodic timer id */
        NetsnmpCacheLoad *load_cache;
                     //        返回值大于等于0,代表成功
        NetsnmpCacheFree *free_cache;
       /*
        * void pointer for the user that created the cache.
        * You never know when it might not come in useful ....
        */
        void             *magic;
       /*
        * hint from the cache helper. contains the standard
        * handler arguments.
        */
       netsnmp_handler_args          *cache_hint;
        /*
            * For SNMP-management of the data caches
            */
           netsnmp_cache *next, *prev;
        oid *rootoid;
        int  rootoid_len;
    };
</pre>

其中flags这个标志位非常重要，决定了cache的运行机制，如何对Cache进行Load和Free，缺省的是当超时时会free+load, 做set操作时会free+load,下面是对flags的详细解释：

If NETSNMP_CACHE_DONT_INVALIDATE_ON_SET is set, the free_cache method will not be called after a set request has processed. It is assumed that the lower mib handler using the cache has maintained cache consistency.

If NETSNMP_CACHE_DONT_FREE_BEFORE_LOAD is set, the free_cache method will not be called before the load_cache method is called. It is assumed that the load_cache routine will properly deal with being called with a valid cache.

If NETSNMP_CACHE_DONT_FREE_EXPIRED is set, the free_cache method will not be called with the cache expires. The expired flag will be set, but the valid flag will not be cleared. It is assumed that the load_cache routine will properly deal with being called with a valid cache.

If NETSNMP_CACHE_PRELOAD is set when a the cache handler is created, the cache load routine will be called immediately.

If NETSNMP_CACHE_DONT_AUTO_RELEASE is set, the periodic callback that checks for expired caches will skip the cache. The cache will only be checked for expiration when a request triggers the cache handler. This is useful if the cache has it's own periodic callback to keep the cache fresh.

If NETSNMP_CACHE_AUTO_RELOAD is set, a timer will be set up to reload the cache when it expires. This is useful for keeping the cache fresh, even in the absence of incoming snmp requests.

由于flags default值为0，实际上在我们项目中没有用到以上任何的设置。

可以通过如下方式设置我们所需要的flags值：

Sample:
<pre>
netsnmp_cache* netsnmp_cache_find_by_oid (const oid * rootoid, int rootoid_len)
</pre>

可以通过这个API得到netsnmp_cach指针，然后修改flag值

或者：

<pre>
int managerTable_load(netsnmp_cache *cache, void *vmagic)
{
           cache->flags &= NETSNMP_CACHE_AUTO_RELOAD;
           // 这里可以通过逻辑操作符来设置标记位
           g_log.dcLog(CommonLog::INFO, "load managerTable");
   /*return*/ getManagerStatus(0);
    for(struct managerTable_entry* e =  managerTable_head; e ; e = e->next)
    {
                     if(1 == e->managerStatus)
                                getManagerVersion(e);
    }
           return 0;
}

void managerTable_free(netsnmp_cache *cache, void *magic)
{
           cache->flags = NETSNMP_CACHE_AUTO_RELOAD;
// 这里可以通过逻辑操作符来设置标记位
           g_log.dcLog(CommonLog::INFO, "free managerTable");
           managerTable_cleanMem(managerTable_head);
           managerTable_head = NULL;
}
</pre>

<pre>
referer: http://blog.csdn.net/hbhhww/article/details/7026321
</pre>
