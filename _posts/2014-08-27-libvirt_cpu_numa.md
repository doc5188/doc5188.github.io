---
layout: post
title: "libvirt 中cpu, numa 的配置"
categories: 虚拟化
tags: [libvirt, 虚拟化]
date: 2014-08-27 17:37:08
---

1. cpu nodes
{% highlight bash %}
<cpu>
    <topology sockets='1' cores='8' threads='1'/>
    <numa>
      <cell cpus='0-3' memory='1024000'/>
      <cell cpus='4-7' memory='1024000'/>
     </numa>
  </cpu>
{% endhighlight %}

这里创建了两个nodes，每个node的memory大都是 1024000KB, vcpu0-3绑定在node0, vcpu4-7绑定在node1.

2. guest binding
{% highlight bash %}
<vcpu cpuset='1-2'>4</vcpu>
{% endhighlight %}

这里将guest绑定在某几个物理cpu上。1-2上。如果在同一个physical node上，那么就可以将不同的guest绑定在
不同的nodes上，可以提高系统性能。

{% highlight bash %}
# grep pid /usr/local/var/run/libvirt/qemu/cputune.xml
 <domstatus state='running' reason='booted' pid='28863'>
    <vcpu pid='28864'/>
    <vcpu pid='28865'/>
    <vcpu pid='28866'/>
    <vcpu pid='28867'/>

# grep Cpus_allowed_list /proc/28863/task/*/status
/proc/28863/task/28863/status:Cpus_allowed_list:    1-2
/proc/28863/task/28864/status:Cpus_allowed_list:    1-2
/proc/28863/task/28865/status:Cpus_allowed_list:    1-2
/proc/28863/task/28866/status:Cpus_allowed_list:    1-2
/proc/28863/task/28867/status:Cpus_allowed_list:    1-2
{% endhighlight %}

3. cputune:
{% highlight bash %}
 <vcpu placement='static'>4</vcpu>
  <cputune>
    <shares>2048</shares>
    <period>1000000</period>
    <quota>-1</quota>
    <vcpupin vcpu='0' cpuset='8'/>
    <vcpupin vcpu='1' cpuset='16'/>
    <emulatorpin cpuset='16'/>
  </cputune>
{% endhighlight %}

4. numatune:
{% highlight bash %}
<numatune>
    <memory mode="strict" nodeset="1"/>
  </numatune>
{% endhighlight %}
  设置memory在某个node上。

{% highlight bash %}
# grep pid /usr/local/var/run/libvirt/qemu/numatune.xml
<domstatus state='running' reason='booted' pid='18104'>
    <vcpu pid='18105'/>
    <vcpu pid='18106'/>

# grep Mems_allowed_list /proc/18104/task/*/status
/proc/18104/task/18104/status:Mems_allowed_list:    1
/proc/18104/task/18105/status:Mems_allowed_list:    1
/proc/18104/task/18106/status:Mems_allowed_list:    1
/proc/18104/task/18114/status:Mems_allowed_list:    1
{% endhighlight %}

<pre>
引用：http://blog.chinaunix.net/uid-20663421-id-4081986.html
</pre>
