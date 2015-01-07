---
layout: post
title: "使用Python的OpenSSL库来进行RSA加密"
categories: python
tags: [python, openssl, rsa, 加密]
date: 2015-01-07 09:43:45
---

使用Python的OpenSSL库（如pyopenssl）可以很便捷地对数据进行RSA的加密，方法如下：

* 1 使用openssl命令生成私钥
<pre>
    openssl genrsa -out private.pem -f4 1024    #生成私钥，指数值为10001
</pre>

* 2 使用Python进行加密：

    

<pre>
    from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign  
    import base64  
      
    key = load_privatekey(FILETYPE_PEM, open("private.pem").read())  
    content = 'test_message'  
      
    d =  sign(key, content, 'sha1')  #d为经过SHA1算法进行摘要、使用私钥进行签名之后的数据  
    b = base64.b64encode(d)  #将d转换为BASE64的格式  
    print b  

</pre>


<pre>
referer:http://blog.csdn.net/huzhenwei/article/details/7524648
</pre>
