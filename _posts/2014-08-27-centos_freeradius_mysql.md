---
layout: post
title: "centos中应用freeradius+mysql进行认证"
categories: linux
tags: [linux, centos, freeradius]
date: 2014-08-27 15:26:22
---

在centos4.5系统中使用freeradius与mysql

（1）安装mysql
如果系统已连网，直接安装
{% highlight bash %}
# yum install mysql-server
{% endhighlight %}
否则要通过光盘安装。
（2）安装freeradius
{% highlight bash %}
# yum install freeradius
{% endhighlight %}
当然也可以从freeradius的ftp服务器上下载，我一开始就是从上面下的2.0.5版本，但编译一直不成功（本人的编程能力有限呀），所以只能依靠yum的强大功能了。

（3）测试freeradius是否已安装成功

　测试需要用户，因此先将/etc/raddb/users文件打开，创建新的用户名，如果不会创建（freeradius早已考虑到了这一点），就将steve前的#去掉,变成：
<pre>
  steve Cleartext-Password := "testing"
  Service-Type = Framed-User,
  Framed-Protocol = PPP,
  Framed-IP-Address = 172.16.3.33,
  Framed-IP-Netmask = 255.255.255.0,
  Framed-Routing = Broadcast-Listen,
  Framed-Filter-Id = "std.ppp",
  Framed-MTU = 1500,
  Framed-Compression = Van-Jacobsen-TCP-IP
</pre>
这样就有了用户steve及密码testing,可以进行测试了。

先启用radius:
{% highlight bash %}
# radiusd -X
如果程序正常运行，最后三行如下
Listening on authentication *:1812
Listening on accounting *:1813
Ready to process requests.

# radtest steve testing localhost 1812 testing123
{% endhighlight %}
最后的testing123是在/etc/raddb/clients.conf中定义的localhost的密码。

如果结果中出现Access-Accept，说明安装成功。

测试完成后将steve用户再恢复原样，即加上#注释。

（4）freeradius与mysql关连

本人一开始对这部分也不了解，全是从网上找的，经过N将的试验才通过。

   首先要启用mysql:
<pre>
   #/etc/rc.d/init.d/mysqld status 查看mysql是否已启动，如果没有
   #/etc/rc.d/init.d/mysql　start 　启动mysql,然后：　
</pre>

  （a)创建radius数据库
{% highlight bash %}
    # mysql -u root -p  //默认没有密码
    mysql>create database radius;
    mysql>exit;
{% endhighlight %}
    (b)将radius中的sql表导入到mysql的radius数据库中
{% highlight bash %}
　　# mysql -u root -p radius < /etc/raddb/sql/mysql/schema.sql
　　# mysql -u root -p radius < /etc/raddb/sql/mysql/nas.sql
　　# mysql -u root -p radius < /etc/raddb/sql/mysql/ippool.sql
{% endhighlight %}
　　注意：通过yum安装的freeradius由于版本太低，在/etc/raddb中没有sql目录，我是从freeradius2.0.5中将sql目录拷贝到/etc/raddb中的。
　　(c)授权
{% highlight bash %}
   mysql> GRANT SELECT ON radius.* TO 'radius'@'localhost' IDENTIFIED BY 'radpass';
   mysql> GRANT ALL on radius.radacct TO 'radius'@'localhost';
   mysql> GRANT ALL on radius.radpostauth TO 'radius'@'localhost';
{% endhighlight %}
   (d)加入一些组信息:
{% highlight bash %}
    mysql> insert into radgroupreply (groupname,attribute,op,value) values ('user','Auth-Type',':=','Local');
    mysql> insert into radgroupreply (groupname,attribute,op,value) values ('user','Service-Type','=','Framed-User');
    mysql> insert into radgroupreply (groupname,attribute,op,value) values ('user','Framed-IP-Netmask','=','255.255.255.255');
    mysql> insert into radgroupreply (groupname,attribute,op,value) values ('user','Framed-IP-Netmask',':=','255.255.255.0');
{% endhighlight %}

    (e)加入用户信息：
{% highlight bash %}
     mysql> INSERT INTO radcheck (UserName, Attribute, Value) VALUES ('azalea', 'Password', 'azalea');
　　mysql> INSERT INTO radcheck (UserName, Attribute, Value) VALUES ('support', 'Password', 'sup123');
{% endhighlight %}
    (f)然后把用户加到组里：
{% highlight bash %}
     mysql> insert into radusergroup(username,groupname) values('azalea','user');
     mysql> insert into radusergroup(username,groupname) values('support','user');
     使用命令：#mysql> select * from radcheck 查看已创建的用户名及密码
    mysql> select * from radcheck;
{% endhighlight %}
<pre>
+----+----------+-----------+----+---------+
| id | username | attribute | op | value   |
+----+----------+-----------+----+---------+
|  1 | azalea   | Password  | == | azalea  |
|  2 | support  | Password  | == | sup123  |
+----+----------+-----------+----+---------+
2 rows in set (0.00 sec)
</pre>

　　(g)修改mysql数据库的root用户密码为azalea
{% highlight bash %}
    # mysqladmin -u root -p password azalea
    Enter password:     //此处是旧密码，默认为空
{% endhighlight %}

(5)修改/etc/raddb中的相关文件

  (a)修改sql.conf
<pre>
    #Connect info
    server = "localhost"    //mysql服务器地址
    login = "root"　　　　　　//mysql登录用户名root
    password = "azalea"　　　　//mysql登录root用户的密码，已修改为azalea
    # Database table configuration
    radius_db = "radius"    //创建的数据库名
</pre>
   (b)修改radiusd.conf,包括：
<pre>
　　　proxy_requests = no
     authorize {
               ..
               ..
               sql   //去掉前面的注释#
              #files  //前面加上注释#,一定要加
               }


      preacct {
              ..
              # files  //前面加上注释#,一定要加
                 }

      accounting {
               ...
               sql  //去掉前面的注释#
                 }     
</pre>

   (c)修改users文件

      找到并加#号注释掉两行，如下
<pre>
     #   DEFAULT        Auth-Type = System
     #   Fall-Through = 1
</pre>
     保存退出

    (d)修改freeradius的配置文件eap.conf

          修改完毕后的内容如下  //只是将相应的注释去掉，我这里用的默认Eap类型为peap.
<pre>
     eap {
                default_eap_type = peap
                timer_expire     = 60
                ignore_unknown_eap_types = no
                cisco_accounting_username_bug = no
                md5 {
                }
                leap {
                }
                tls {
                        private_key_password = whatever
                        private_key_file = ${raddbdir}/certs/cert-srv.pem
                        certificate_file = ${raddbdir}/certs/cert-srv.pem
                        CA_file = ${raddbdir}/certs/demoCA/cacert.pem
                        dh_file = ${raddbdir}/certs/dh
                        random_file = ${raddbdir}/certs/random
                        fragment_size = 1024
                        include_length = yes
                        check_crl = yes
                       check_cert_issuer = "/C=GB/ST=Berkshire/L=Newbury/O=My Company Ltd"
                        check_cert_cn = %{User-Name}
                        cipher_list = "DEFAULT"
                }      
                ttls {
                        default_eap_type = md5
                        copy_request_to_tunnel = no
                        use_tunneled_reply = no
                }
                mschapv2 {
                }
        }
</pre>

      (e)修改clients.conf文件

　　　　　增加相应的NAS信息，我用的是webportal，地址是192.168.11.0/24网段的，因此增加为：
<pre>
   client 192.168.11.0/24 {            #无线路由器的IP，可以是网段
        secret    = azalea             #radius和NAS的通讯密码
        shortname = azalea.net         #shortname可以随便填写
                         }
</pre>
(6)测试修改是否正确。
　　先启用radius:
{% highlight bash %}
     # radiusd -X
{% endhighlight %}
   用配置过的帐号进行测试：
{% highlight bash %}
    #radtest azalea azalea localhost 1812 testing123
{% endhighlight %}
   出现Access-Accept，说明成功。
