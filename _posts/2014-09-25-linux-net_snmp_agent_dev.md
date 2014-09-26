---
layout: post
categories: 网络
tags: [linux, net-snmp, snmp, snmp agent]
date: 2014-09-25 17:53:32
title: "基于net-snmp的代理agent开发详解"
---

花了一两天时间测试和整理一下。

用net-snmp扩展MIB库，实现方法可归结为四种：

1）一是静态库方式，通过修改配置头文件，在相应地方包含新引入的mib模块的.c和.h文件，然后重新编译库文件和扩展代码；这种方式不够灵活，每次修改扩展的MIB后，都需要重新编译snmpd和扩展的代码，再重新安装snmpd到系统中。

2）二是编译动态共享库，只需把新引入的MIB模块的.c和.h文件编译成动态库，通过设置能够让代理程序载入。

对于第二种方式，一需要编译成.so动态共享库，二需要原代理程序是否包含dlmod或load命令，三还要看系统是否支持。一般情况下仅支持Unix平台。

3）三是扩展一个子代理，让SNMPD以主代理的模式运行，对于SNMPD我们只要让它启动就可以，不需要任何的更改和配置，把子代理编译生成的程序运行起来就可以扩展自定义的MIB库。

4）用shell脚本来扩展

本文我们以第三种方法在linux上开发和测试


一、安装snmpd

既然要测试，而且我们用的也是net-snmp工具，当然要先安装snmpd，本文采用5.7.2版本的snmpd，需安装net-snmp-5.7.2-1, net-snmp-devel-5.7.2-1,net-snmp-perlmods-5.7.2-1，安装可以是编译net-snmp的源码，也可以下载rpm包安装，这里略过。

安装好后测试一下service snmpd status，如果没有反应，可能是没有配置文件，可以手动建立/etc/snmp目录，在snmp目录下建立snmpd.conf文件，填入一些基本的配置信息(或者通过snmpconf程序一步一步生成,snmpconf程序比较容易懂，适合童鞋们，snmpconf会提示你创建什么配置文件，需不需要把snmpd作为主代理等等强大的提示)：

<pre>
    master agentx  
    rocommunity public  
    rwcommunity public  
</pre>

master 是说该snmpd以主代理方式运行，目前主代理snmpd只支持agentx类型，而我们要开发的程序是一种子代理（subagent），是需要连snmpd的master agent的。rocommunity （只读对象）和rwcommunity（读写对象）的密码都是public.（这个密码就是客户端访问OID时需要提供的密码，比如在任一一个装有snmpd的linux机器上，执行snmpwalk -v2c -c public localhost 1.3.6.1.2.1.1, 这里的public就是密码，分别有只读OID密码，和读写OID密码），本文测试就以public作为默认的密码吧。

现在测试一下snmpd是否正常，启动service snmpd restart，执行snmpwalk -v2c -c public localhost 1.3.6.1.2.1.1, 如果有SNMPv2-MIB:xxxx之类的输出就表示我们的主代理已经工作了。


二、自己的MIB库

首先MIB库有什么用？其实作为子代理来说，在server机器上，可以不用MIB库，MIB库只为了让用户访问时方便，有了MIB库，用户就不用记那么多和长的OID，比如把MIB放在windows机器上，在windows机器装一个支持MIB的软件，用该软件打开MIB库，只要点击相应的对象就可以自动发送snmp请求到server端，所以server端是可以不要MIB库的。如果把MIB库放在linux客户端机器上，以下面自定义的MIB库为例，那么就可以直接执行snmpget -v2c -c public Test-MIB::GetTime.0，当然需要linux客户端装有snmp，而且自定义的MIB库必须能让snmpd程序找到。 

这里用就一个OID建一个MIB库来简化，命名Test-MIB.my,放在/usr/local/share/snmp/mibs目录下，因为这个目录是snmpd的默认目录，只要把MIB库放入该目录就可以自动加载MIB库，否则需要修改/etc/snmp/snmp.conf文件，添加mibs +/path/to/Test-MIB.my 并重启snmpd。

自定义MIB库，如下：
<pre>
    -- Test-MIB.my  
        Test-MIB DEFINITIONS ::= BEGIN  
       
            IMPORTS  
                OBJECT-GROUP, MODULE-COMPLIANCE, NOTIFICATION-GROUP      
                    FROM SNMPv2-CONF      
                enterprises, Integer32, Unsigned32, OBJECT-TYPE, MODULE-IDENTITY,   
                NOTIFICATION-TYPE      
                    FROM SNMPv2-SMI      
                DisplayString      
                    FROM SNMPv2-TC;  
          
    -- October 09, 2002 at 14:50 GMT  
            -- 1.3.6.1.4.1.16535  
            Test MODULE-IDENTITY   
                LAST-UPDATED "200210091450Z"        -- October 09, 2002 at 14:50 GMT  
                ORGANIZATION   
                    ""    
                CONTACT-INFO   
                    ""    
                DESCRIPTION   
                    "Video's Server MIB."  
                ::= { enterprises 16535 }  
          
    --  Node definitions  
    -- This part will include all details about the Test.  
            -- 1.3.6.1.4.1.16535.1  
            Time OBJECT IDENTIFIER ::= { Test 1 }   
      
          
            -- 1.3.6.1.4.1.16535.1.1  
            GetTime OBJECT-TYPE  
                SYNTAX DisplayString (SIZE (0..100))  
                MAX-ACCESS read-only  
                STATUS current  
                DESCRIPTION  
                    "Example : 2013/4/11"  
                ::= { Time 1 }  
        END  
      
    -- Test-MIB.my  
</pre>
很简单，该MIB库只有一个OID，即：1.3.6.1.4.1.16535.1.1，写完后我们测一个MIB库有没有问题，在linux机器上用snmptranslate -Tp -IR Test-MIB::Test显示结果如下：

<pre>
[plain] view plaincopy

    +--Test(16535)  
       |  
       +--Time(1)  
          |  
          +-- -R-- String    GetTime(1)  
                   Textual Convention: DisplayString  
                   Size: 0..100  
</pre>

OK, snmp自动发现了这个MIB库， 有了自定义的OID，但是还没有处理程序（子代理）

三、生成源代码

mib2c可以根据mib库生成对应的源代码，有多种模板，这里我们要生成子代理的代码，所以选择是固定的，执行env MIBS"+/usr/local/share/snmp/mibs/Test-MIB.my" mib2c Test，会引导你逐渐生成Test.h和Test.c, 先选2再选1，过程如下：
{% highlight bash %}
[root@localhost mibs]# env MIBS="+/etc/snmp/mibs/Test-MIB.my" mib2c Test  
writing to -  
mib2c has multiple configuration files depending on the type of  
code you need to write.  You must pick one depending on your need.  
  
You requested mib2c to be run on the following part of the MIB tree:  
  OID:                              Test  
  numeric translation:              .1.3.6.1.4.1.16535  
  number of scalars within:         1     
  number of tables within:          0     
  number of notifications within:   0     
  
First, do you want to generate code that is compatible with the   
ucd-snmp 4.X line of code, or code for the newer Net-SNMP 5.X code  
base (which provides a much greater choice of APIs to pick from):  
  
  1) ucd-snmp style code  
  2) Net-SNMP style code  
  
Select your choice : 2   
  
**********************************************************************  
         GENERATING CODE FOR SCALAR OBJECTS:  
**********************************************************************  
  
  It looks like you have some scalars in the mib you requested, so I  
  will now generate code for them if you wish.  You have two choices  
  for scalar API styles currently.  Pick between them, or choose not   
  to generate any code for the scalars:  
  
  1) If you're writing code for some generic scalars  
     (by hand use: "mib2c -c mib2c.scalar.conf Test")  
  
  2) If you want to magically "tie" integer variables to integer  
     scalars  
     (by hand use: "mib2c -c mib2c.int_watch.conf Test")  
  
  3) Don't generate any code for the scalars  
  
Select your choice: 1  
    using the mib2c.scalar.conf configuration file to generate your code.  
writing to Test.h  
writing to Test.c  
  
  
  
**********************************************************************  
* NOTE WELL: The code generated by mib2c is only a template.  *YOU*  *  
* must fill in the code before it'll work most of the time.  In many *  
* cases, spots that MUST be edited within the files are marked with  *  
* /* XXX */ or /* TODO */ comments.                                  *  
**********************************************************************  
running indent on Test.h  
running indent on Test.c 
{% endhighlight %}
mib2c已经统计出我们的mib库包含1个scalar变量，0个table变量，0个通知变量，Scalar就是包含我们常用的整型，字符串，时间等等数据类型。table就是scalar的一种集合，有一个和多个列组成，类似于数据库中的表。它必须具有索引项，用来按一定顺序检索表项，当然我们只写了一个标量的OID，不是表结构也不是通知结构

生成的Test.h如下：


{% highlight c %}
    /* 
     * Note: this file originally auto-generated by mib2c using 
     *        $ 
     */  
    #ifndef TEST_H  
    #define TEST_H  
      
    /* 
     * function declarations  
     */  
    void            init_Test(void);  
    Netsnmp_Node_Handler handle_GetTime;  
      
    #endif                          /* TEST_H */  
{% endhighlight %}


生成的Test.c文件如下：

{% highlight c %}
    /* 
     * Note: this file originally auto-generated by mib2c using 
     *        $ 
     */  
      
    #include <net-snmp/net-snmp-config.h>  
    #include <net-snmp/net-snmp-includes.h>  
    #include <net-snmp/agent/net-snmp-agent-includes.h>  
    #include "Test.h"  
      
    /** Initializes the Test module */  
    void  
    init_Test(void)  
    {  
        const oid       GetTime_oid[] = { 1, 3, 6, 1, 4, 1, 16535, 1, 1 };  
      
        DEBUGMSGTL(("Test", "Initializing\n"));  
      
        netsnmp_register_scalar(netsnmp_create_handler_registration  
                                ("GetTime", handle_GetTime, GetTime_oid,  
                                 OID_LENGTH(GetTime_oid), HANDLER_CAN_RONLY));  
    }  
      
    int  
    handle_GetTime(netsnmp_mib_handler *handler,  
                   netsnmp_handler_registration *reginfo,  
                   netsnmp_agent_request_info *reqinfo,  
                   netsnmp_request_info *requests)  
    {  
        /*   
         * We are never called for a GETNEXT if it's registered as a 
         * "instance", as it's "magically" handled for us.   
         */  
      
        /*   
         * a instance handler also only hands us one request at a time, so 
         * we don't need to loop over a list of requests; we'll only get one.  
         */  
      
        switch (reqinfo->mode) {  
      
        case MODE_GET:  
            snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,  
                                     /* 
                                      * XXX: a pointer to the scalar's data  
                                      */ ,  
                                     /* 
                                      * XXX: the length of the data in bytes  
                                      */ );  
            break;  
      
      
        default:  
            /* 
             * we should never get here, so this is a really bad error  
             */  
            snmp_log(LOG_ERR, "unknown mode (%d) in handle_GetTime\n",  
                     reqinfo->mode);  
            return SNMP_ERR_GENERR;  
        }  
      
        return SNMP_ERR_NOERROR;  
    }  
{% endhighlight %}


以上的代码都是自动生成的，我们没有写一行代码，到了这一步，我们需要把Test.c里面的 XXX改成自己的值，也就两行，修改后Test.c文件代码如下：

{% highlight c %}
    /* 
     * Note: this file originally auto-generated by mib2c using 
     *        $ 
     */  
      
    #include <net-snmp/net-snmp-config.h>  
    #include <net-snmp/net-snmp-includes.h>  
    #include <net-snmp/agent/net-snmp-agent-includes.h>  
    #include "Test.h"  
    #include <time.h>  
      
    /** Initializes the Test module */  
    void  
    init_Test(void)  
    {  
        const oid       GetTime_oid[] = { 1, 3, 6, 1, 4, 1, 16535, 1, 1 };  
      
        DEBUGMSGTL(("Test", "Initializing\n"));  
      
        netsnmp_register_scalar(netsnmp_create_handler_registration  
                                ("GetTime", handle_GetTime, GetTime_oid,  
                                 OID_LENGTH(GetTime_oid), HANDLER_CAN_RONLY));  
    }  
      
    int  
    handle_GetTime(netsnmp_mib_handler *handler,  
                   netsnmp_handler_registration *reginfo,  
                   netsnmp_agent_request_info *reqinfo,  
                   netsnmp_request_info *requests)  
    {  
        /*   
         * We are never called for a GETNEXT if it's registered as a 
         * "instance", as it's "magically" handled for us.   
         */  
         /* 
         * a instance handler also only hands us one request at a time, so 
         * we don't need to loop over a list of requests; we'll only get one.  
         */  
      
        time_t t;  
        switch (reqinfo->mode) {  
        case MODE_GET:  
            time(&t);  
            char szTime[100];  
            snprintf(szTime,100,"%s",ctime(&t));  
            snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,  
                                     /* 
                                      * XXX: a pointer to the scalar's data  
                                      */ szTime,  
                                     /* 
                                      * XXX: the length of the data in bytes  
                                      */ strlen(szTime));  
            break;  
      
      
        default:  
            /* 
             * we should never get here, so this is a really bad error  
             */  
            snmp_log(LOG_ERR, "unknown mode (%d) in handle_GetTime\n",  
                     reqinfo->mode);  
            return SNMP_ERR_GENERR;  
        }  
      
        return SNMP_ERR_NOERROR;  
    }  
{% endhighlight %}

简单吧，现在子代理程序基本就写完了，我们执行命令让我们的子代理生成可执行程序，执行

{% highlight bash %}
# net-snmp-config --compile-subagent Test Test.c
{% endhighlight %}
生成了Test程序， 执行过程如下：



可以看出来，net-snmp-config程序生成了一个临时的C文件，netsnmptmp.12373.c 并与Test.c一起编译，生成了Test程序后又删除了该临时文件。我们会在最后研究netsnmptmp.12373.c文件。


四、测试一下

现在Test程序已经生成了，我们先执行主代理（service snmpd start）,再执行子代理./Test,再ps -ef | grep Test，看一下，可以看到Test程序自动在后台启动了，如下：

{% highlight bash %}
    [root@localhost hepeng]# ps -ef| grep Test   
    root     27526     1  0 13:29 ?        00:00:00 ./Test  
    root     27531 27448  0 13:29 pts/2    00:00:00 grep Test  
{% endhighlight %}

到这里我们可以想象到,Test.c文件中是没有main函数的，那么main函数肯定是在netsnmptmp.12373.c 中，net-snmp-config让Test程序变成了守护进程在后台运行。

到此我们的service端就已经布置完成了，子代理理论上可以回复自定义的GetTime OID的请求。

本文在一台装有snmpd和子代理的linux server机器上直接测试。执行命令如下：

{% highlight bash %}
    [root@localhost hepeng]# snmpget -v2c -c public localhost 1.3.6.1.4.1.16535.1.1.0  
    SNMPv2-SMI::enterprises.16535.1.1.0 = STRING: "Thu Apr 11 13:40:20 2013  
    "  
{% endhighlight%}

可以看到，我们开发的子代理成功工作了。如果自定义的MIB库已经加入到snmpd指定的目录中，我们可以执行


{% highlight bash %}
    [hepeng@localhost ~]$ snmpget -v2c -c public localhost Test-MIB:GetTime.0  
    Test-MIB::GetTime.0 = STRING: Thu Apr 11 13:46:42 2013  
{% endhighlight %}

snmpget会自动在所有的MIB库中查找Test-MIB库，并把Test-MIB:GetTime.0转换成1.3.6.1.4.1.16535.1.1.0并发送get请求。

现在子代理是已经开发成功了，我们实际上只写了两三行代码就开发了net-snmp子代理，是不是很简单呢？

现在有个问题，怎么加入到我们自己的项目中呢？因为Test.c中并没有main函数，在一个项目中直接调用init_Test()能不能让子代理work呢？那就要研究一下netsnmptmp.12373.c。


五、加入项目中

我们再次执行net-snmp-config --compile-subagent Test Test.c，然后立刻Ctrl+c,时间要控制好，让net-snmp-config程序产生了临时的C文件，却没有删除它。打开netsnmptmp.12373.c，我们来看一下代码，200多行，本文只贴上main函数的重要部分，代码中都添加了注释，不难理解：

{% highlight c %}
    int main (int argc, char **argv)  
    {  
      int arg;  
      char* cp = NULL;  
      int dont_fork = 0, do_help = 0;  
      
      while ((arg = getopt(argc, argv, "dD:fhHL:"  
    #ifndef DISABLE_MIB_LOADING  
                           "m:M:"  
    #endif /* DISABLE_MIB_LOADING */  
                           "n:"  
    #ifndef DISABLE_MIB_LOADING  
                           "P:"  
    #endif /* DISABLE_MIB_LOADING */  
                           "vx:")) != EOF) {  
        switch (arg) {  
        case 'D':/*这里省略多个case break,只是一些选项，没必要研究/ 
          break; 
     
        default: 
          fprintf(stderr, "invalid option: -%c\n", arg); 
          usage(argv[0]); 
          break; 
        } 
      } 
     
      if (do_help) { 
        netsnmp_ds_set_boolean(NETSNMP_DS_APPLICATION_ID, 
                               NETSNMP_DS_AGENT_NO_ROOT_ACCESS, 1); 
      } else { 
        /* we are a subagent  第一步：这里是告诉snmpd我们这个Test作为子代理*/  
        netsnmp_ds_set_boolean(NETSNMP_DS_APPLICATION_ID,  
                               NETSNMP_DS_AGENT_ROLE, 1);  
      
        if (!dont_fork) {/* 这里是让Test程序变成守护进程，执行Test后可以在后台运行不会退出 */  
          if (netsnmp_daemonize(1, snmp_stderrlog_status()) != 0)  
            exit(1);  
        }  
      
        /* initialize tcpip, if necessary */  
        SOCK_STARTUP;  
      }  
      
      /* initialize the agent library 第二步*/  
      init_agent(app_name);  
      
      /* initialize your mib code here 第三步*/  
      init_Test();  
      
      /* Test will be used to read Test.conf files. 第四步 */  
      init_snmp("Test");  
      
      if (do_help) {  
        fprintf(stderr, "Configuration directives understood:\n");  
        read_config_print_usage("  ");  
        exit(0);  
      }  
      
      /* In case we received a request to stop (kill -TERM or kill -INT) */  
      netsnmp_running = 1;  
    #ifdef SIGTERM  
      signal(SIGTERM, stop_server);  
    #endif  
    #ifdef SIGINT  
      signal(SIGINT, stop_server);  
    #endif  
    #ifdef SIGHUP  
      signal(SIGHUP, hup_handler);  
    #endif  
      
      /* main loop here... */  
      while(netsnmp_running) {  
        if (reconfig) {  
          free_config();  
          read_configs();  
          reconfig = 0;  
        }  
        agent_check_and_process(1);  
      }  
      
      /* at shutdown time */  
      snmp_shutdown(app_name);  
      
      /* deinitialize your mib code here */  
      
      /* shutdown the agent library */  
      shutdown_agent();  
      SOCK_CLEANUP;  
      exit(0);  
    }  
{% endhighlight %}


我们不管上面代码那些看不懂的函数，知道大概意思就行，现在我们来加入到自己的项目中，找到项目中的main函数，在main函数中添加初始化Test子代理的代码，本文为了方便理解，就在Test.c中添加main函数，就地取材，写个超简单函数，不考虑传入参数。修改后的Test.c文件如下：

{% highlight c %}
    /* 
     * Note: this file originally auto-generated by mib2c using 
     *        $ 
     */  
      
    #include <net-snmp/net-snmp-config.h>  
    #include <net-snmp/net-snmp-includes.h>  
    #include <net-snmp/agent/net-snmp-agent-includes.h>  
    #include "Test.h"  
    #include <time.h>  
      
    /** Initializes the Test module */  
    void  
    init_Test(void)  
    {  
        const oid       GetTime_oid[] = { 1, 3, 6, 1, 4, 1, 16535, 1, 1 };  
      
        DEBUGMSGTL(("Test", "Initializing\n"));  
      
        netsnmp_register_scalar(netsnmp_create_handler_registration  
                                ("GetTime", handle_GetTime, GetTime_oid,  
                                 OID_LENGTH(GetTime_oid), HANDLER_CAN_RONLY));  
    }  
      
    int  
    handle_GetTime(netsnmp_mib_handler *handler,  
                   netsnmp_handler_registration *reginfo,  
                   netsnmp_agent_request_info *reqinfo,  
                   netsnmp_request_info *requests)  
    {  
        /* 
         * We are never called for a GETNEXT if it's registered as a 
         * "instance", as it's "magically" handled for us.   
         */  
        /* 
         * a instance handler also only hands us one request at a time, so 
         * we don't need to loop over a list of requests; we'll only get one.  
         */  
      
        time_t t;  
        switch (reqinfo->mode) {  
        case MODE_GET:  
        time(&t);  
        char szTime[100];  
        snprintf(szTime,100,"%s",ctime(&t));  
            snmp_set_var_typed_value(requests->requestvb, ASN_OCTET_STR,  
                                     /* 
                                      * XXX: a pointer to the scalar's data  
                                      */ szTime,  
                                     /* 
                                      * XXX: the length of the data in bytes  
                                      */ strlen(szTime));  
            break;  
      
      
        default:  
            /* 
             * we should never get here, so this is a really bad error  
             */  
            snmp_log(LOG_ERR, "unknown mode (%d) in handle_GetTime\n",  
                     reqinfo->mode);  
            return SNMP_ERR_GENERR;  
        }  
      
        return SNMP_ERR_NOERROR;  
    }  
      
    static int keep_running;  
    RETSIGTYPE stop_server(int __attribute__((unused)) a) {  
            keep_running = 0;  
    }  
      
    int main()  
    {  
       const char *app_name = "Test";  
       /* we are a subagent */  
       netsnmp_ds_set_boolean(NETSNMP_DS_APPLICATION_ID, NETSNMP_DS_AGENT_ROLE, 1);  
      
       /* initialize the agent library */  
       init_agent(app_name);  
      
       /* initialize your mib code here */  
       init_Test();  
      
       /* Test will be used to read Test.conf files. */  
       init_snmp("Test");  
       keep_running = 1;  
       while(keep_running)  
       {  
            agent_check_and_process(1);/* block every 1 second */  
       }  
       /* at shutdown time */  
       snmp_shutdown(app_name);  
      
       /* deinitialize your mib code here */  
      
       /* shutdown the agent library */  
       shutdown_agent();  
       return 0;  
    }  
{% endhighlight %}


这个main函数是不是很简单呢？当snmpd stop的时候会调用stop_server,也就会注销我们的子代理。编译一下，这里我们不用net-snmp-config编译，因为是要加入到自己的项目中，所以推荐写入到Makefile中，本文就不写Makefile了，直接调用gcc命令生成（直接用net-snmp-config的参数就可以），如下：

{% highlight bash %}
    [root@localhost hepeng]# gcc  -fno-strict-aliasing -g -O2 -Ulinux -Dlinux=linux  -D_REENTRANT -D_GNU_SOURCE -fno-strict-aliasing -pipe -Wdeclaration-after-statement -I/usr/local/include -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -I/usr/include/gdbm  -I/usr/lib64/perl5/5.8.8/x86_64-linux-thread-multi/CORE   -I. -I/usr/local/include -o Test Test.c  -L/usr/local/lib -lnetsnmpmibs -lnetsnmpagent -lnetsnmp -lnetsnmpmibs -lpci -lrpm -lrpmdb -lrpmio   -lnetsnmpagent  -Wl,-E -Wl,-rpath,/usr/lib64/perl5/5.8.8/x86_64-linux-thread-multi/CORE -lnetsnmp  -lcrypto  
    Test.c: In function ‘handle_GetTime’:  
    Test.c:45: warning: ISO C90 forbids mixed declarations and code  
{% endhighlight %}


然后我们启动snmpd，再执行Test程序，程序会block住，因为不是守护进程嘛，而且main有循环，如下：


{% highlight bash %}
    [root@video6 ~]# ./Test   
    NET-SNMP version 5.7.2 AgentX subagent connected  
{% endhighlight %}

我们再调用snmpget来测试结果：

{% highlight bash %}
    [root@localhost hepeng]# snmpget -v2c -c public localhost 1.3.6.1.4.1.16535.1.1.0  
    SNMPv2-SMI::enterprises.16535.1.1.0 = STRING: "Thu Apr 11 02:39:17 2013  
    "  
{% endhighlight %}


六、总结

子代理看起来非常好写，我们实际上就写了两三行，其它的函数看不懂也没关系， 不用深入了解，拷贝过来直接用，能编译过就行，一般看函数名字就知道怎么用。

子代理官方参考：http://www.net-snmp.org/wiki/index.php/TUT:Writing_a_Subagent

动态库扩展MIB库方法：http://www.net-snmp.org/wiki/index.php/TUT:Writing_a_Dynamically_Loadable_Object

shell脚本扩展MIB库方法：http://www.net-snmp.org/wiki/index.php/Tut:Extending_snmpd_using_shell_scripts

<pre>
原文地址：http://blog.csdn.net/hepeng597/article/details/8782868
</pre>
