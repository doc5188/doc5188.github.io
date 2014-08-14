---
layout: post
title: "虚拟化实战：Cluster设计之一资源池"
categories: 虚拟化 
tags: [virtual, cluster, 虚拟化]
date: 2014-08-13 10:18:20
---

　　资源池是Cluster设计中的一个重要概念，本文介绍了为什么用资源池，怎么用好资源池，以及澄清了一些常见的误区。

　　一概念

　　每个ESXi主机和Cluster缺省都有一个Root资源池。如果没有新的自由池创建的话，整个系统仅仅有一个资源池。

<img src="/upload/images/31820031548.png">

　　图中所示RP-Marketing和RP-QA是在Root资源池内新创建的资源池，他们和root资源池是父子关系，他们之间是兄弟关系。

　　RP-QA-UI是RP-QA下的子资源池。

　　为了简化管理，通常不建议在资源池内建好几级子资源池，2级资源池应该可以满足绝大多数的情况。

　　二 为什么使用资源池

　　授权管理

　　vCenter管理员可以为每个部门建立资源池，授权特定用户管理该部门的资源池。这样vCenter管理员就无需过多介入对各部门内部资源的控制。

　　统一策略：

　　对每个VM进行资源控制费时费力，把有共同需要的VM分配到相应的资源池，可以很便捷的实现资源控制。

　　资源分离：

　　对一个资源池的设置改变不会影响到其他资源池，

　　三基本设计原则

　　不要仅仅因为逻辑区分或者访问控制的原因，来使用资源池。其实文件夹可以更好的实现该目的。

　　为了简化管理和减少资源开销，建议资源池的深度不要超过2

　　不要把虚拟机和资源池分在同一级

　　不要过度分配资源。在建议资源池之前，检查上一级资源池可供分配的资源。

　　四 SeparateESXi Cluster vs Resource Pool

　　如果仅仅从资源分离的角度考虑，需要斟酌是建一个单独的Cluster，还是在Cluster内建资源池。

　　建议考虑下面的因素：

　　Cluster内的主机数目

　　如果一个Cluster有8个以上主机，可以考虑为管理功能的VM设置单独的Cluster。比如vcenter，vCloud，Database等等。 如果主机个数很少，而希望能充分利用资源，在Cluster内建立资源池是更好的选择。

　　安全

　　有的公司有非常严格的安全策略，某些特定应用不可以和其他应用共享硬件。为此需要单独设置Cluster，设置为该Cluster分配专属的存储资源。

　　性能

　　为了最大化性能的保障，考虑单独的Cluster，能保证充足资源的供给。毕竟资源池还是要共享资源的，在资源竞争很厉害的情况下，资源池的份额设置为High，仅仅是有优势抢到资源，但并不意味着就能满足应用的需要。

　　五 实例

<img src="/upload/images/31823031548.png">

　　假设一台主机由几台虚拟机，分别属于QA和Marketing部门。QA部分需要更多的资源。

　　设置如下

　　资源池ShareResource Allocation

　　RP-QAHigh4GHz, 2GB

　　RP-MarketingNormal2GHz, 1GB

　　这时候RP-QA内的两个虚拟机，一定比RP-Marketing内的虚拟机更容易在有竞争的情况下抢占到资源。

　　假如我们在RP-QA内再创建5个VM，那么情况就不一定了。即使RP-QA的share设置为High，但每个VM能抢占到的很有限。

　　虽然RP-Marketing的RP-Marketing的share设置为Normal，但仅有3个VM，可能每个VM可以抢占的资源比RP-QA内的VM要多。

　　所以资源池的设置不是一劳永逸，需要密切注意池内的VM数量，可以写一个脚本来根据优先级和VM的数量，自动计算该资源池应该设置的Share数值。
<pre>
来源： http://www.educity.cn/wulianwang/1445944.html
</pre>

