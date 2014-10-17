---
layout: post
title: "centos6.5直接yum安装nginx，并且支持php访问的配置"
categories: linux
tags: [yum安装nginx]
date: 2014-10-17 17:17:48
---



<p>但是今天装了CentOS6.5，直接yum install nginx不行，要先处理下源，下面是安装完整流程，也十分简单：</p>
<p>CentOS 6，先执行(过程慢点，其实可以手动下载，然后在本地运行)：<br>
<br>
<pre code_snippet_id="231511" snippet_file_name="blog_20140312_1_8243440"  name="code" class="plain">rpm -ivh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum -y install nginx
yum -y php-fpm
service php-fpm restart
service nginx restart
chkconfig php-fpm on
chkconfig nginx on</pre><br>
<br>
</p>
<p>下面是配置：</p>
<p>vi /etc/nginx/conf.d/default.conf<br>
</p>
<p><pre code_snippet_id="231511" snippet_file_name="blog_20140312_2_7228901"  name="code" class="plain">server {
    listen       80;
    server_name  localhost;
    autoindex    on;
    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;

    location / {
        root   /var/www/html;
        index  index.html index.htm index.php;
    }

    location ~ \.php$ {
        root           /var/www/html;
        fastcgi_pass   127.0.0.1:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /var/www/html$fastcgi_script_name;
        include        fastcgi_params;
    }....</pre>以下全是#号。</p>
<p><br>
</p>


<pre>
referer:http://blog.csdn.net/e421083458/article/details/21089901
</pre>
