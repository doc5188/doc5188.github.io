---
layout: post
title: "linux 本地通信实例 AF_UNIX"
categories: 网络
tags: [linux, unixsocket, AF_UNIX, linux通信]
date: 2014-10-08 17:08:33
---

程序说明：

程序里包含服务端和客户端两个程序，它们之间使用 AF_UNIX 实现本机数据流通信。使用 AF_UNIX 域实际上是使用本地 socket 文件来通信。

* 服务器端代码：
 
{% highlight c %}
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <stdio.h>
    #include <sys/un.h>
    #include <unistd.h>
    #include <stdlib.h>
    int main (int argc, char *argv[])
    {
            int server_sockfd, client_sockfd;
            int server_len, client_len;
            struct sockaddr_un server_address;      /*声明一个UNIX域套接字结构*/
            struct sockaddr_un client_address;
            int i, bytes;
            char ch_send, ch_recv;
            unlink ("server_socket");       /*删除原有server_socket对象*/
            /*创建 socket, 通信协议为AF_UNIX, SCK_STREAM 数据方式*/
            server_sockfd = socket (AF_UNIX, SOCK_STREAM, 0);
            /*配置服务器信息(通信协议)*/
            server_address.sun_family = AF_UNIX;
            /*配置服务器信息(socket 对象)*/
            strcpy (server_address.sun_path, "server_socket");
            /*配置服务器信息(服务器地址长度)*/
            server_len = sizeof (server_address);
            /*绑定 socket 对象*/
            bind (server_sockfd, (struct sockaddr *)&server_address, server_len);
            /*监听网络,队列数为5*/
            listen (server_sockfd, 5);
            printf ("Server is waiting for client connect...\n");
            client_len = sizeof (client_address);
            /*接受客户端请求; 第2个参数用来存储客户端地址; 第3个参数用来存储客户端地址的大小*/
            /*建立(返回)一个到客户端的文件描述符,用以对客户端的读写操作*/
            client_sockfd = accept (server_sockfd, (struct sockaddr *)&server_address, (socklen_t *)&client_len);
            if (client_sockfd == -1) {
                    perror ("accept");
                    exit (EXIT_FAILURE);
            }
            printf ("The server is waiting for client data...\n");
            for (i = 0, ch_send = '1'; i < 5; i++, ch_send++) {
                    if ((bytes = read (client_sockfd, &ch_recv, 1)) == -1) {
                            perror ("read");
                            exit (EXIT_FAILURE);
                    }
                    printf ("The character receiver from client is %c\n", ch_recv);
                    sleep (1);
                    if ((bytes = write (client_sockfd, &ch_send, 1)) == -1) {
                            perror ("read");
                            exit (EXIT_FAILURE);
                    }
            }
                    close (client_sockfd);
                    unlink ("server socket");
    }
{% endhighlight %}


客户端代码：
 
{% highlight c %}
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <stdio.h>
    #include <sys/un.h>
    #include <unistd.h>
    #include <stdlib.h>

    int main (int argc, char *argv[])
    {
        struct sockaddr_un address;
        int sockfd;
        int len;
        int i, bytes;
        int result;
        char ch_recv, ch_send;

        /*创建socket,AF_UNIX通信协议,SOCK_STREAM数据方式*/
        if ((sockfd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
                perror ("socket");
                exit (EXIT_FAILURE);
        }

        address.sun_family = AF_UNIX;
        strcpy (address.sun_path, "server_socket");
        len = sizeof (address);

        /*向服务器发送连接请求*/
        result = connect (sockfd, (struct sockaddr *)&address, len);
        if (result == -1) {
            printf ("ensure the server is up\n");
            perror ("connect");
            exit (EXIT_FAILURE);
        }

        for (i = 0, ch_send = 'A'; i < 5; i++, ch_send++) {
            if ((bytes = write(sockfd, &ch_send, 1)) == -1) { /*发消息给服务器*/
                perror ("write");
                exit (EXIT_FAILURE);
            }

            sleep (2);    /*休息二秒钟再发一次*/

            if ((bytes = read (sockfd, &ch_recv, 1)) == -1) { /*接收消息*/
                perror ("read");
                exit (EXIT_FAILURE);
            }

            printf ("receive from server data is %c\n", ch_recv);
        }
        close (sockfd);

        return (0);
    }

{% endhighlight %}


程序说明：

先运行服务器端，然后再运行客户端可以在两边同时看到输出。服务器端先运行后会出现如下提示：
 
<pre>
     ./sock_local_server
    Server is waiting for client connect...
</pre>

这表示，服务器端已经被阻塞到到 accept() 这里，服务器就在此等候客户端的连接。

如果不是先运行服务器端，而直接运行客户端，那么客户端会提示：
 
<pre>
     ./sock_local_client
    ensure the server is up
    connect: Connection refused
</pre>

提示服务器没有准备好，连接被拒绝，从而直接退出程序。

如果服务器和客户端依次运行，可以在两边看到输出：

服务器端：
 
<pre>
     ./sock_local_server
    Server is waiting for client connect...
    The server is waiting for client data...
    The character receiver from client is A
    The character receiver from client is B
    The character receiver from client is C
    The character receiver from client is D
    The character receiver from client is E
</pre>

客户端：
 
<pre>
    ./sock_local_client
    receive from server data is 1
    receive from server data is 2
    receive from server data is 3
    receive from server data is 4
    receive from server data is 5
</pre>
