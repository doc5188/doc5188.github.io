---
layout: post
title: "用Python教你如何“养”一只DHT爬虫"
categories: python
tags: [python, dht]
date: 2014-10-29 17:09:49
---

废话少说, 直接上菜.

我假设你了解:
<pre>
1, DHT协议
2, 网络字节序/主机字节序
3, bencode
4, UDP
5, 种子文件构造
</pre>

不懂的赶紧去google, 要是缺一个, 我会一口盐汽水喷死你的!

最重要的是, 你必须会编程!!!!!!! 必须会!!!!!!!!!!!

ok, DHT原理是什么我在这就不写了, 毕竟会看我这文章的人都是已经知道了的.

本文贴的代码均为Python, 使用其他编程语言的人可以看注释. 为了简单, 只会说大概思路和关键性代码, 细节自行搞定.

本文讲的是要实现一个爬虫, 所以不会跟协议文档那么严格. 只要保证你能正确请求,回应即可. 用软件开发的一句话来说: 只要接口一致, 管你内部细节代码是怎么写的.

* 第一步, 构建自己的路由表, 这里涉及到大量Python代码, 请深呼吸:

在构建自己的路由表之前, 得写两个辅助函数, 后面会用到:

{% highlight bash %}
    from hashlib import sha1  
    from random import randint  
    def node_id():  
        """  
        把爬虫"伪装"成正常node, 一个正常的node有ip, port, node ID三个属性, 因为是基于UDP协议,   
        所以向对方发送信息时, 即使没"明确"说明自己的ip和port时, 对方自然会知道你的ip和port,   
        反之亦然. 那么我们自身node就只需要生成一个node ID就行, 协议里说到node ID用sha1算法生成,   
        sha1算法生成的值是长度是20 byte, 也就是20 * 8 = 160 bit, 正好如DHT协议里说的那范围: 0 至 2的160次方,   
        也就是总共能生成1461501637330902918203684832716283019655932542976个独一无二的node.   
        ok, 由于sha1总是生成20 byte的值, 所以哪怕你写SHA1(20)或SHA1(19)或SHA1("I am a 2B")都可以,   
        只要保证大大降低与别人重复几率就行. 注意, node ID非十六进制,   
        也就是说非FF5C85FE1FDB933503999F9EB2EF59E4B0F51ECA这个样子, 即非hash.hexdigest().  
        """ 
        hash = sha1()  
        s = ""  
        for i in range(20):  
            s += chr(randint(0, 255))  
        hash.update(s)  
        return hash.digest()  
     
    def intify(nid):  
        """这是一个小工具, 把一个node ID转换为数字. 后面会频繁用到.""" 
        assert len(nid) == 20 
        return long(nid.encode('hex'), 16) #先转换成16进制, 再变成数字 
{% endhighlight %}

协议里说道, table里有bucket, bucket里有node, 每个bucket有K个node, 目前K=8, 即每个bucket有8个node. 由于table范围是0到2的160次方, 那么一个table最多能有(2的160次方)/K那么多的bucket.

OK, 按照OOP编程思想来说, 那么肯定会有table, bucket, node这3个类, 无OOP的, 自己看着办.

由于是基于Kademila而写, 所以我习惯上把这三个类名变为KTable, KBucket, KNode:

{% highlight bash %}
    class KNode:  
        def __init__(self, nid, ip, port):  
            """  
            nid就是node ID的简写, 就不取id这么模糊的变量名了. __init__方法相当于别的OOP语言中的构造方法,   
            在python严格来说不是构造方法, 它是初始化, 不过, 功能差不多就行.  
            """ 
            self.nid = nid #node ID  
            self.ip = ip  
            self.port = port  
     
        #以下两个方法非Python程序员不需关心  
        def __eq__(self, other):  
            return self.nid == other.nid  
        def __ne__(self, other):  
            return self.nid != other.nid  
     
     
    class KBucket:  
        def __init__(self, min, max):  
            """  
            min和max就是该bucket负责的范围, 比如该bucket的min:0, max:16的话,   
            那么存储的node的intify(nid)值均为: 0到15, 那16就不负责, 这16将会是该bucket后面的bucket的min值.   
            nodes属性就是个列表, 存储node. last_accessed代表最后访问时间, 因为协议里说到,   
            当该bucket负责的node有请求, 回应操作; 删除node; 添加node; 更新node; 等这些操作时,   
            那么就要更新该bucket, 所以设置个last_accessed属性, 该属性标志着这个bucket的"新鲜程度". 用linux话来说, touch一下.  
            这个用来便于后面说的定时刷新路由表.  
            """ 
            self.min = min #最小node ID数字值  
            self.max = max #最大node ID数字值  
            self.nodes = [] #node列表  
            self.last_accessed = time() #最后访问时间  
     
        def nid_in_range(self, nid):  
            """判断指定的node ID是否属于该bucket的范围里""" 
            return self.min <= intify(nid) < self.max  
     
        def append(self, node):  
            """  
            添加node, 参数node是KNode实例.  
     
            如果新插入的node的nid属性长度不等于20, 终止.  
            如果满了, 抛出bucket已满的错误, 终止. 通知上层代码进行拆表.  
            如果未满, 先看看新插入的node是否已存在, 如果存在, 就替换掉, 不存在, 就添加,  
            添加/替换时, 更新该bucket的"新鲜程度".  
            """ 
            if len(node.nid) != 20: return 
            if len(self.nodes) < 8:  
                if node in self.nodes:  
                    self.nodes.remove(node)  
                    self.nodes.append(node)  
                else:  
                    self.nodes.append(node)  
                self.last_accessed = time()  
            else:  
                raise BucketFull  
     
     
    class KTable:  
        """  
        该类只实例化一次.  
        """ 
        def __init__(self, nid):  
            """  
            这里的nid就是通过node_id()函数生成的自身node ID. 协议里说道, 每个路由表至少有一个bucket,   
            还规定第一个bucket的min=0, max=2的160次方, 所以这里就给予了一个buckets属性来存储bucket, 这个是列表.  
            """ 
            self.nid = nid #自身node ID  
            self.buckets = [KBucket(0, 2 ** 160)] #存储bucket的例表  
     
        def append(self, node):  
            """添加node, 参数node是KNode实例""" 
     
            #如果待插入的node的ID与自身一样, 那么就忽略, 终止接下来的操作.  
            if node.nid == self.nid: return   
     
            #定位出待插入的node应该属于哪个bucket.  
            index = self.bucket_index(node.nid)  
            bucket = self.buckets[index]  
     
            #协议里说道, 插入新节点时, 如果所归属的bucket是满的, 又都是活跃节点,   
            #那么先看看自身的node ID是否在该bucket的范围里, 如果不在该范围里, 那么就把  
            #该node忽略掉, 程序终止; 如果在该范围里, 就要把该bucket拆分成两个bucket, 按范围"公平平分"node.  
            try:  
                bucket.append(node)  
            except BucketFull:  
                if not bucket.nid_in_range(self.nid): return #这个步骤很重要, 不然递归循环很狂暴, 导致程序死翘翘.  
                self.split_bucket(index)   
                self.append(node)  
     
        def bucket_index(self, nid):  
            """  
            定位bucket的所在索引  
     
            传一个node的ID, 从buckets属性里循环, 定位该nid属于哪个bucket, 找到后, 返回对应的bucket的索引;   
            没有找到, 说明就是要创建新的bucket了, 那么索引值就是最大索引值+1.  
            注意: 为了简单, 就采用循环方式. 这个恐怕不是最有效率的方式.  
            """ 
            for index, bucket in enumerate(self.buckets):  
                if bucket.nid_in_range(nid):  
                    return index  
            return index          
     
        def split_bucket(self, index):  
            """  
            拆表  
     
            index是待拆分的bucket(old bucket)的所在索引值.   
            假设这个old bucket的min:0, max:16. 拆分该old bucket的话, 分界点是8, 然后把old bucket的max改为8, min还是0.   
            创建一个新的bucket, new bucket的min=8, max=16.  
            然后根据的old bucket中的各个node的nid, 看看是属于哪个bucket的范围里, 就装到对应的bucket里.   
            各回各家,各找各妈.  
            new bucket的所在索引值就在old bucket后面, 即index+1, 把新的bucket插入到路由表里.  
            """ 
            old = self.buckets[index]  
            point = old.max - (old.max - old.min)/2 
            new = KBucket(point, old.max)  
            old.max = point  
            self.buckets.insert(index + 1, new)  
            for node in old:  
                if new.nid_in_range(node.nid):  
                    new.append(node)  
            for node in new:  
                old.remove(node)          
     
        def find_close_nodes(self, target):  
            """  
            返回与目标node ID或infohash的最近K个node.  
     
            定位出与目标node ID或infohash所在的bucket, 如果该bucuck有K个节点, 返回.   
            如果不够到K个节点的话, 把该bucket前面的bucket和该bucket后面的bucket加起来, 只返回前K个节点.  
            还是不到K个话, 再重复这个动作. 要注意不要超出最小和最大索引范围.  
            总之, 不管你用什么算法, 想尽办法找出最近的K个节点.  
            """ 
            nodes = []  
            if len(self.buckets) == 0: return nodes  
            index = self.bucket_index(target)  
            nodes = self.buckets[index].nodes  
            min = index - 1 
            max = index + 1 
            while len(nodes) < K and (min >= 0 or max < len(self.buckets)):  
                if min >= 0:  
                    nodes.extend(self.buckets[min].nodes)  
                if max < len(self.buckets):  
                    nodes.extend(self.buckets[max].nodes)  
                min -= 1 
                max += 1 
     
            num = intify(target)  
            nodes.sort(lambda a, b, num=num: cmp(num^intify(a.nid), num^intify(b.nid)))  
            return nodes[:K] #K是个常量, K=8 
{% endhighlight %}

ok, 路由表这个玩意儿比较有技术含量, 又难以描述, 所以会贴代码演示. 接下来的DHT客户端/服务端就不再贴那么多的代码了, 毕竟处理网络的代码太多太复杂, 技术含量不高, 按照DHT协议描述的那样操作就行了.

 

* 第二步, 实现DHT客户端

实现一个DHT客户端, 不用都要实现ping, find_node, get_peers, announce_peer操作了, 做一个爬虫, 仅仅只需要实现find_node功能就能达到目的了. 因为我们只想不停地交朋友而已.

要想加入DHT网络, 首先得认识第一个已知的node, 这个node最好是长期在线的, 又稳定的. 我这里就认识一个, dht.transmissionbt.com:6881, 由于UDP的原因, 只能接受ip, 所以请提前解析出ip地址.

然后使用DHT协议说的那个find_node操作, 现在解释一下某些key的潜在意义吧

t: transaction ID的简称, 传输ID. 起什么作用呢? 由于UDP无3次握手这个机制, 所以任何人都可随便发送信息给你, 根本就不需与你提前进行连接. 想想这么个情况, 你发送了一请求数据给某node, 然后收到DHT说的回复类型的数据, 即y=r, 但是, 你怎么知道回应的是你之前的哪个请求呢? 所以就要靠t了, 当你发送时, t=aa的话, 对方回应这个请求时, 回应消息的t绝对是aa, 这样你就能区分了. 在发送之前, 要为该t值注册一个处理函数, 当收到回应时, 调用该函数进行处理. 记得设置一个定时器, 时间一到, 立马删除该函数, 不然你内存飙升. 如果超时后才收到信息的话, 很遗憾, 没了处理函数, 直接忽略. 我建议定时器设定到5秒. 当然, 随便你. 一定要保证成功收到第一个node的find_node回复, 不然失败, 就没法继续find_node了.即: 认识不到第一个朋友, 就别想认识第二个朋友.

id: 就是自身node ID了, 是node_id()函数生成的哈, 样子绝不是DHT协议例子中的样子, 这主要是为了方便演示而已

target: 这个也是自身的node ID, 作用是问某node离我最近的都有哪些node.

收到对方回复后, 把那key为nodes给解析出来, 按DHT协议说的, 每个node是以4字节ip+2字节port+20字节node ID组成, 那么nodes的字节数就会是26的倍数. "解码"node和"编码"node的Python代码如下:

{% highlight bash %}
    from struct import unpack  
     
    def num_to_dotted(n):  
        d = 256 * 256 * 256 
        q = []  
        while d > 0:  
            m, n = divmod(n, d)  
            q.append(str(m))  
            d /= 256 
        return '.'.join(q)  
     
    def decode_nodes(nodes):  
        n = []  
        nrnodes = len(nodes) / 26 
        nodes = unpack("!" + "20sIH" * nrnodes, nodes)  
        for i in range(nrnodes):  
            nid, ip, port = nodes[i * 3], num_to_dotted(nodes[i * 3 + 1]), nodes[i * 3 + 2]  
            n.append((nid, ip, port))  
        return n  
     
    decode_nodes函数的反作用函数如下:  
    def dotted_to_num(ip):  
        hexn = ''.join(["%02X" % long(i) for i in ip.split('.')])  
        return long(hexn, 16)  
     
    def encode_nodes(nodes):  
        n = []  
        for node in nodes:  
            n.extend([node.nid, dotted_to_num(node.ip), node.port])  
        return pack("!" + "20sIH" * len(nodes), *n) 
{% endhighlight %}

解析出来后, 插入到路由表里, 然后使用find_node继续向刚解析出来的node进行请求, target还是自身node ID, 以此循环. 这样就能认识很多很多的node啦. 细节就不说了, 自己看着办.

 

* 第三步, 实现DHT服务器端, 协议文档说得很清楚了, 我只列出几个需要注意的问题:

1, 服务器端得实现处理node发来的ping, find_node, get_peers, announce_peer请求.

2, 回应信息里的t的值是对方的t值, 不是自己随便写的.

3, 最好要实现那个token机制, 这样就减少被捣乱的几率, 此token就按协议那种方式就行, 每5分钟变换一次, 10分钟内的有效.

4, 一定要记得前面说的那句"当该bucket负责的node有请求, 回应操作; 删除node; 添加node; 更新node; 等这些操作时, 那么就刷新该bucket".

5, 由于是做DHT爬虫, 所以处理get_peers请求和find_node请求差不多一样, 都是返回最近的node. 当然, 你闲得蛋疼的话, 可以来得标准点, 做能返回peers那种, 不过, 没必要.

6, announce_peer请求里的port就是对方提供下载种子的端口, 监听于TCP, 不是DHT连接的端口. 还有请求消息里的id就仅仅指的是对方的node ID, 我看博客园某人写的文章说是对方的peer ID, 我表示很不解.

 

* 第四步, 定时刷新路由表

按协议所说, 过一段时间后, 路由表里的node不全都是活跃了, 所以要定时刷新路由表. 说下大概思路, 遍历路由表中的bucket列表, 看看bucket的last_accessed是不是超过了比如说15分钟, 如果超过了, 说明有可能不"新鲜"了, 那么从该bucket随机选择一个node, 向该node发送find_node操作, 接着就不管了. 笔者为了简单, 就采用这么简单的方式了, 没有去确认可疑node是否还"活"着. 你可以严格按照协议文档那么写.

 

你可能会问的问题:

1, 怎么知道一个资源的下载速度?

答: 有句话这么说: 下载人数越多, 下载速度越快. 那么, 如果某一个资源的infohash出现的announce_peer次数越高, 那么就说明下载人数就越多, 人数越多就越快. 这个下载速度就没法用绝对速度表示, 不过可以使用相对速度.

2, 怎么在众多的资源中过滤出影视资源?

答: 得到种子, 如果有files字段话, 遍历它进行正则匹配, 看看有木有后缀名是rmvb, avi, mp4等什么的, 如果有, 那它大部分情况就是影视了. 如果没有files字段, 就对name字段进行正则匹配吧.

3, 为什么那些影视资源总是些"很黄很暴力"?

答: 这个就不是很清楚了, 我想, 使用BT的人大多数都是些撸管男吧.

4, infohash这个词是根据什么而来的?

答: 种子文件中info字段的hash值

5, 如何认识更多的node?

答: 多开启几个node实例.

6, 什么情况下, 对方把我给加入到对方的路由表里?

答: 当你向对方find_node时. 也许你的ping, get_peers也能让对方把你添加到路由表里. 同理, 当你接到ping, find_node, get_peers时, 就把对方给添加到路由表里, 至少收到find_node请求时, 就要把对方给添加到路由表里.

7, 如何长期保存node?

答: 数据库, 文件都行, 我不建议长期保存node, 你只要一直在线, 使用内存存储最好不过了, 速度快, 代码简单.






















<pre>
原文链接：http://www.cnblogs.com/52web/p/How-to-write-a-DHT-crawler.html
</pre>
