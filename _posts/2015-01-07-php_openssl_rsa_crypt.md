---
layout: post
title: "php openssl rsa 加密解密应用"
categories: php
tags: [php, openssl, rsa, 加密解密]
date: 2015-01-07 09:38:39
---

php openssl rsa 加密解密应用

 

* 1、安装openssl

<pre>
yum -y install openssl-devel
</pre>


* 2、安装php openssl

到php源码包的目录 ext/openssl 下执行：

<pre>
/data/apps/php/bin/phpize

./configure --with-openssl --with-php-config=/data/apps/php/bin/php-config
make
make install
</pre>

(可能需要mv config0.m4 config.m4)

把生成的 openssl.so 文件添加到php.ini中

<pre>
extension = /xxx/openssl.so;
</pre>


可以用以下命令查看安装的模块：

<pre>
php -m |grep openssl
</pre>


* 3、生成公钥和私钥

生成私钥：
<pre>
openssl genrsa 1024 > private.key
</pre>

(注意，1024是密钥的长度，如果密钥较长，相应加密后的密文也会较长)

生成公钥：
<pre>
openssl rsa -in private.key -pubout > public.key
</pre>

 

* 4、利用php加密和解密文本，代码如下：

{% highlight bash %}
    <?php  
      
    class mycrypt {  
      
        public $pubkey;  
        public $privkey;  
      
        function __construct() {  
                    $this->pubkey = file_get_contents('/home/openssl/public.key');  
                    $this->privkey = file_get_contents('/home/openssl/private.key');  
        }  
      
        public function encrypt($data) {  
            if (openssl_public_encrypt($data, $encrypted, $this->pubkey))  
                $data = base64_encode($encrypted);  
            else  
                throw new Exception('Unable to encrypt data. Perhaps it is bigger than the key size?');  
      
            return $data;  
        }  
      
        public function decrypt($data) {  
            if (openssl_private_decrypt(base64_decode($data), $decrypted, $this->privkey))  
                $data = $decrypted;  
            else  
                $data = '';  
      
            return $data;  
        }  
      
    }  
      
    $rsa = new mycrypt();  
    echo $rsa -> encrypt('abc');  
      
    //echo $rsa -> decrypt('W+ducpssNJlyp2XYE08wwokHfT0bm87yBz9vviZbfjAGsy/U9Ns9FIed684lWjYyyofi/1YWrU0Mp8vLOYi8l6CfklBY=');  
{% endhighlight %}


<pre>
referer:http://blog.csdn.net/jom_ch/article/details/9303617
</pre>
