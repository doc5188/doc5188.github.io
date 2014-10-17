---
layout: post
title: "CentOS5.4-安装Nginx-0.7.65+php-5.3.2+MongoDB-1.4.2"
categories: linux
tags: [linux, nginx+php+mongodb]
date: 2014-10-16 23:23:12
---

安装Nginx-0.7.65 + php-5.3.2 + MongoDB-1.4.2

编译安装Nginx服务器.

* 0. 确保安装了如下软件. 
<pre>
# yum install gcc openssl-devel pcre-devel zlib-devel libjpeg-devel libpng-devel freetype-devel
</pre>

* 1. 创建nginx运行的用户.
<pre>
# groupadd nginx
# useradd nginx -g nginx 
</pre>

* 2. 创建网页文件存储目录. 

<pre>
# mkdir /mnt/disk1/www
# chmod +w /mnt/disk1/www
# chown -R nginx:nginx /mnt/disk1/www 
</pre>

* 3. 下载Nginx源码包

<pre>
# tar zxvf nginx-0.7.65.tar.gz
# cd nginx-0.7.65
# ./configure \
--prefix=/mnt/disk1/nginx-0.7.65 \
--sbin-path=/usr/sbin/nginx \
--conf-path=/etc/nginx/nginx.conf \
--error-log-path=/var/log/nginx/error.log \
--pid-path=/var/run/nginx/nginx.pid \
--lock-path=/var/lock/nginx.lock \
--user=nginx \
--group=nginx \
--with-http_ssl_module \
--with-http_flv_module \
--with-http_gzip_static_module \
--http-log-path=/var/log/nginx/access.log \
--http-client-body-temp-path=/var/tmp/nginx/client/ \
--http-proxy-temp-path=/var/tmp/nginx/proxy/ \
--http-fastcgi-temp-path=/var/tmp/nginx/fcgi/ \
--with-http_stub_status_module
# make && make install 

# with-http_stub_status_module 模块可用来统计当前连接数
# 添加指定的 Nginx 扩展模块只需要 configure 时带上 --with-模块名 即可
# 小技巧：如已经安装好了Nginx，好添加一个新模块，只需要重新配置，重新 configure && make 但别 make install, 直接将objs/nginx 拷贝到{$prefix}/sbin下即可，【注意备份原来的】 
</pre>

* 4. 创建nginx需要的文件/文件夹.
<pre>
# mkdir -p /var/tmp/nginx
</pre>

* 5. 启动 nginx.
<pre>
# /usr/sbin/nginx
</pre>

* 6. 访问一下看看.

看到 Welcome to nginx! 安装便算OK了!

编译安装PHP （FastCGI模式）使用php-fpm管理方式.

* 1.安装 libiconv.
<pre>
# tar zxvf libiconv-1.13.1.tar.gz
# cd libiconv-1.13.1
# ./configure --prefix=/usr && make && make install
</pre>

* 2.安装mhash.
<pre>
# tar -zxvf mhash-0.9.9.9.tar.gz
# cd mhash-0.9.9.9
# ./configure --prefix=/usr && make && make install
</pre>

* 3.安装mcrypt.
<pre>
# tar -zxvf libmcrypt-2.5.8.tar.gz
# cd libmcrypt-2.5.8
# ./configure && make && make install
# /sbin/ldconfig
# cd libltdl/
# ./configure --enable-ltdl-install && make && make install

# tar -zxvf mcrypt-2.6.8.tar.gz
# cd mcrypt-2.6.8
# LD_LIBRARY_PATH=/usr/local/lib ./configure --prefix=/usr && make && make install
</pre>

* 4. 安装libevent.
<pre>
# tar zxvf libevent-1.4.13-stable.tar.gz
# cd libevent-1.4.13-stable 
# ./configure --prefix=/usr && make && make install
# libtool --finish /usr/lib

</pre>

4. 安装PHP.
<pre>
# tar jxvf php-5.3.2.tar.bz2
</pre>

5. 安装php-fpm.
<pre>
tar zxvf dreamcat4-php-fpm-0.6-5.3.0-0-gdd5ebd0.tar.gz
dreamcat4-php-fpm-3bb2b9b/generate-fpm-patch
cd php-5.3.2
patch -p1 < ../fpm.patch
./buildconf --force
mkdir fpm-build
cd fpm-build

../configure --prefix=/mnt/disk1/php-5.3.2 \
--with-config-file-path=/etc/php5 \
--with-iconv-dir=/usr \
--with-freetype-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib \
--with-libxml-dir=/usr \
--enable-xml \
--enable-discard-path \
--enable-safe-mode \
--enable-bcmath \
--enable-shmop \
--enable-sysvsem \
--enable-inline-optimization \
--with-curl \
--with-curlwrappers \
--enable-mbregex \
--enable-fastcgi \
--with-fpm \
--with-libevent=shared \
--enable-force-cgi-redirect \
--enable-mbstring \
--with-mcrypt \
--with-gd \
--enable-gd-native-ttf \
--with-openssl \
--with-mhash \
--enable-pcntl \
--enable-sockets \
--with-ldap \
--with-ldap-sasl \
--with-xmlrpc \
--enable-zip \
--enable-soap \
--with-pear \
--enable-so

make clean
make ZEND_EXTRA_LIBS='-liconv'
make install

cd ..
mkdir /etc/php5
cp php.ini-production /etc/php5/php.ini

# 应当可以看到这一行
# Installing PHP SAPI module: fpm
# …
# 并且存在 /mnt/disk1/php-5.3.2/bin/php-fpm 即代表安装成功
</pre>

启动php-fpm
<pre>
ldconfig
/etc/init.d/php-fpm start
</pre>

配置Nginx

<pre>
vi /etc/nginx/nginx.conf
修改或添加内容如下：
 location ~ \.php$ {
 root html;
 fastcgi_pass 127.0.0.1:9000;
 fastcgi_index index.php;
 # fastcgi_param SCRIPT_FILENAME /scripts$fastcgi_script_name;
 fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
 fastcgi_param SCRIPT_NAME $fastcgi_script_name;
 include fastcgi_params;
 }
</pre>


附常见错误1：

No input file specified.

注意如下两个参数的值
<pre>
fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
fastcgi_param SCRIPT_NAME $fastcgi_script_name;
</pre>

配置文件的位置

Nginx的配置文件在 /etc/nginx 下面

PHP的配置文件，即熟悉的php.ini 在 /etc/php5 中

php-fpm的配置文件为 /etc/php-fpm.conf

Nginx日志文件在 /var/log/nginx 下面

php-fpm日志文件在 /var/log/php-fpm.log

重启命令：
<pre>
killall -9 nginx
/usr/sbin/nginx
</pre>

安装MongoDB
<pre>
mkdir -p /data/db
tar zxvf mongodb-linux-x86_64-1.4.2.tgz
mv mongodb-linux-x86_64-1.4.2 /mnt/disk1/
cd /mnt/disk1/mongodb-linux-x86_64-1.4.2/
</pre>

工具
<pre>
 bin/mongod - MongoDB server
 bin/mongo - MongoDB client

 bin/mongodump - MongoDB dump tool - for backups, snapshots, etc..
 bin/mongorestore - MongoDB restore a dump
 bin/mongoexport - Export a single collection to test (json,csv)
 bin/mongoimportjson - Import a json file into a collection

 bin/mongofiles - Utility for putting and getting files from MongoDB gridfs
</pre>

运行
<pre>
 bin/mongod --dbpath=/data/db &
</pre>

测试
<pre>
 bin/mongo
> db.foo.save( { a : 1 } )
> db.foo.find()
</pre>

停止
<pre>
 bin/mongo
> db.shutdownServer()
</pre>

安装php-mongodb-dirver
<pre>
tar zxvf mongodb-mongo-php-driver-1.0.6-0-gd261d7a.tar.gz
cd mongodb-mongo-php-driver-a54a5f7
/mnt/disk1/php-5.3.2/bin/phpize
./configure --with-php-config=/mnt/disk1/php-5.3.2/bin/php-config --enable-mongo
make
make install
</pre>

验证mongo php driver
<pre>
/mnt/disk1/php-5.3.2/bin/php -i | grep extension_dir
extension_dir => /mnt/disk1/php-5.3.2//lib/php/extensions/no-debug-non-zts-20090626 => /mnt/disk1/php-5.3.2//lib/php/extensions/no-debug-non-zts-20090626

/mnt/disk1/php-5.3.2/bin/php -i | grep mongo
PWD => /mnt/disk1/software/mongodb-mongo-php-driver-a54a5f7
_SERVER["PWD"] => /mnt/disk1/software/mongodb-mongo-php-driver-a54a5f7
_ENV["PWD"] => /mnt/disk1/software/mongodb-mongo-php-driver-a54a5f7

</pre>

把extension=mongo.so加入到php.ini重启 apache
<pre>
vi /etc/php5/php.ini
;;;;;;;;;;;;;;;;;;;;;;
; Dynamic Extensions ;
;;;;;;;;;;;;;;;;;;;;;;
extension=mongo.so
</pre>

<pre>
/mnt/disk1/php-5.3.2/bin/php -i | grep mongo
mongo
mongo.allow_persistent => On => On
mongo.auto_reconnect => On => On
mongo.chunk_size => 262144 => 262144
mongo.cmd => $ => $
mongo.default_host => localhost => localhost
mongo.default_port => 27017 => 27017
mongo.utf8 => 1 => 1
</pre>

修改php.ini后，重启Nginx,php-fpm
<pre>
killall -9 nginx
/usr/sbin/nginx

/etc/init.d/php-fpm stop
/etc/init.d/php-fpm start
</pre>

运行测试

建立一个php文档，输入

<pre>
vi /mnt/disk1/nginx-0.7.65/html/mondb.php
<?php
$m = new Mongo(); //connect 
$db = $m->test; //选择一个数据库(test)
$collection = $db->foo; //选择一个collection(默认foo)
$result = $collection->find();
foreach($result as $val){
 print_r($val);
}
// disconnect
$m->close();
?>

</pre>

浏览测试

http://192.168.11.39/mondb.php

php 使用,官方手册：http://www.php.net/manual/en/class.mongo.php
