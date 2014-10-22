---
layout: post
title: "理解cpu load average"
categories: linux 
tags: [load average]
date: 2014-10-22 09:40:08
---

<p>要问我平常使用频率最高的命令，那必须是top，没有之一。虽然天天用，但有的参数还真不是很清楚。比如一直没弄明白cpu百分比和load average这两个参数哪个更“权威”一点。其实是因为对load average这个参数没什么概念，只知道大的时候就说明cpu负载比较高。为了以后不再糊涂，所以仔细研究了一下cpu load average。<br>
</p>
<h3>cpu百分比</h3>
<p>首先需要搞清楚的是，cpu的使用状态是一个离散的变量。就是说某一时刻cpu要么就是正在执行指令，要么就是处于空闲状态，cpu的利用百分比要不就是100%，要不就是0%。而绝不会说执行某条指令使用了50%的cpu。那为什么top里面有时候会显示除了0%和100%呢？其实top里面的的cpu百分比是时间上的概念:</p>
<blockquote><p>k: %CPU — CPU usage<br>
<strong>The task’s share of the elapsed CPU time since the last screen update, expressed as a percentage of total CPU time.</strong> In a true SMP environment, if ‘Irix mode’ is Off, top will operate in ‘Solaris mode’ where a task’s cpu usage will be divided by the total number of CPUs. You toggle ‘Irix/Solaris’ modes with the ‘I’ interactive command.</p></blockquote>
<p>以上内容出自top的manual。假设top里面更新一次的间隔是1s，进程a的cpu百分比为50%，那么说明在过去的一秒里面，cpu花了0.5秒来执行进程a的指令。如果总cpu百分比是70%，那么在过去的一秒中，总共有0.7秒cpu处于计算的状态，剩下的0.3秒处于空闲状态。这就是cpu百分比的真正含义。</p>
<h3>load average</h3>
<p>load average与cpu percentage主要有两点不同：第一，load average反映的不仅仅是某一瞬间的cpu利用情况，而是反映了一种趋势。第二，load average反映了系统对cpu的需求情况，而不只是cpu有多少时间处于活跃的状态。</p>
<p>为了更好的理解load average的概念，我们可以同交通流量做个类比。有一条单行道（cpu），最多只能容纳一定数量的车子在上面行驶（cpu执行任务）。车子在路上行驶可能有三种情况：</p>
<ol>
<li>路上很空旷，很可以容纳更多的车辆行驶。</li>
<li>路上很挤，有很多车辆在排队等待通过。</li>
<li>路上的车辆数量跟道路的容量刚好相等。</li>
</ol>
<p>以上3种情况，分别对应cpu load average小于1、大于1和刚好等于1。通过这样一个类比，load average的概念就清晰多了：</p>
<ol>
<li>load average小于1：任务数小于cpu的处理能力，cpu处于相对空闲的状态</li>
<li>load average大于1：任务数大于cpu的处理能力，cpu处理不过来，某些任务排队等候处理</li>
<li>load average等于1：任务数刚好等于cpu的处理能力，cpu既不繁忙也不空闲</li>
</ol>
<p>如果cpu是多核的呢？那么我们不应该用单行道来做类比，而是双行道、四行道等等。因此多核的cpu 要根据核的数量判断load average高低。如果是双核，那load average等于2的时候刚刚好，以此类推。核的数量可以通过读取proc文件系统中的信息判断：</p>
<div class="codecolorer-container bash dawn codecolorer-noborder" style="overflow: auto; white-space: nowrap;"><div class="bash codecolorer"><span class="kw2">grep</span> <span class="st_h">'model name'</span> <span class="sy0">/</span>proc<span class="sy0">/</span>cpuinfo <span class="sy0">|</span> <span class="kw2">wc</span> <span class="re5">-l</span></div></div>
<p><strong>参考：</strong></p>
<ol>
<li><a href="http://www.linuxjournal.com/article/9001">http://www.linuxjournal.com/article/9001</a></li>
<li><a href="http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages">http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages</a></li>
