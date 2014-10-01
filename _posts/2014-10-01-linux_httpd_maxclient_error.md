---
layout: post
title: "Apache [error] server reached MaxClients setting, consider raising the MaxClients setting问题及解决办法 "
categories: linux
tags: [linux, Apache, httpd]
date: 2014-10-01 11:07:20
---

最近公司有个客户报了一个问题，就是运行一段时间后在apache的日志/var/log/httpd/error_log文件中有一条错误信息

[Fri Mar 04 10:48:20 2011] [error] server reached MaxClients setting, consider raising the MaxClients setting

检查了一下，这是由于并发链接数太多导致的，后来查了一下apache的文档，发现可以通过修改apache的配置文

/etc/httpd/conf/httpd.conf中的MaxClients参数来调整。

在调整之前首先要检查一下apache运行在哪一种模式下是prefork还是worker（具体prefork和worker有什么区别，可以google以下），如果不知道自己的apache是那种模式，可以使用“/usr/sbin/httpd -l”命令来检查，当检查出是哪一种模式之后，就可以找到/etc/httpd/conf/httpd.conf中对应的配置部分来修改。

这里我们首先先来重现一下上面的那个问题，先写一个php的测试程序test.php,并将其放在/var/www/html/test.php位置，文件内容比较简单，模拟一个简单的页面，内容如下：

{% highlight bash %}

    <?  
    sleep(1);  
    phpinfo();  
    ?>  
{% endhighlight %}

 

然后可以通过apache自带的测试工具ab来做一下测试，运行“ab -c 512 -n 100000  http://localhost/test.php”来做测试，其中“-n 100000”是指总共发十万个请求，“-c 512”是指并发512个请求，运行后可以发现成功的请求很少，并且很快在日志中就会出现上面那个错误，这是由于我的环境中的apache运行的prefork模式，其中MaxClients参数默认是256，所以当并发很高这里是512的时候就会出现这个错误。

下面我们来修改一下参数，将其中

{% highlight bash %}

    <IfModule prefork.c>  
    StartServers       8  
    MinSpareServers    5  
    MaxSpareServers   20  
    ServerLimit      256  
    MaxClients       256  
    MaxRequestsPerChild  4000  
    </IfModule>  
{% endhighlight %}

 

修改为

{% highlight bash %}

    <IfModule prefork.c>  
    StartServers     100  
    MinSpareServers  100  
    MaxSpareServers  100  
    ServerLimit     1024  
    MaxClients      1024  
    MaxRequestsPerChild  4000  
    </IfModule>  
{% endhighlight %}

 

注意这里我配置了MaxClients=1024，而测试只用了并发512个请求，留了一定的余地，这个可以在具体环境中再做调整。

然后重新启动apache“/etc/init.d/httpd restart”。

再次运行“ab -c 512 -n 100000  http://localhost/test.php”，可以发现所有的请求都正常完成，并且日志中也不再有上面那个错误。

 

 

关于参数的意义，在apache的配置中有详细说明，如下：

{% highlight bash %}

    # prefork MPM  
    # StartServers: number of server processes to start  
    # MinSpareServers: minimum number of server processes which are kept spare  
    # MaxSpareServers: maximum number of server processes which are kept spare  
    # ServerLimit: maximum value for MaxClients for the lifetime of the server  
    # MaxClients: maximum number of server processes allowed to start  
    # MaxRequestsPerChild: maximum number of requests a server process serves  
{% endhighlight %}

 

 

{% highlight bash %}

    # worker MPM  
    # StartServers: initial number of server processes to start  
    # MaxClients: maximum number of simultaneous client connections  
    # MinSpareThreads: minimum number of worker threads which are kept spare  
    # MaxSpareThreads: maximum number of worker threads which are kept spare  
    # ThreadsPerChild: constant number of worker threads in each server process  
    # MaxRequestsPerChild: maximum number of requests a server process serves  
{% endhighlight %}

 

 

 

<pre>
来源: http://blog.csdn.net/kongxx/article/details/6219734
</pre>
