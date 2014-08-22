---
layout: post
title: "Linux查看硬件信息dmidecode"
categories: linux
tags: [linux, dmidecode]
date: 2014-08-22 16:31:32
---

DMI ，即Desktop Management Interface。也有被称为SMBIOS，即System Management BIOS。
常用参数

较低版本的dmidecode命令不支持参数，因此要看信息的话，要用more/less/grep来配合才能更好些。

较高版本的dmidecode命令有如下参数：

-h 查看帮助信息。

-q  不显示未知设备。

-t type   查看指定类型的信息，比如bios,system,memory,processor等。

-s keyword   查看指定的关键字的信息，比如system-manufacturer, system-product-name, system-version, system-serial-number等。

1、查看设备品牌型号

 

{% highlight bash%}
    [root@ opt]# dmidecode -s system-manufacturer 
    IBM 
    [root@ opt]# dmidecode -s system-product-name 
    System x3550 M2 -[7946IWG]- 
{% endhighlight %}

 
2、查看内存槽数、那个槽位插了内存，大小是多少
 

{% highlight bash%}
    [root@ opt]# dmidecode|grep -P -A5 "Memory Device" |grep Size 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: No Module Installed 
            Size: 4096 MB 
            Size: No Module Installed 
            Size: No Module Installed 
{% endhighlight %}

 
3、查看最大支持内存数

{% highlight bash%}
    [root@ opt]# dmidecode -t memory |grep "Maximum Capacity" 
            Maximum Capacity: 192 GB 
{% endhighlight %}
