---
layout: post
title: "python使用RSA加密解密"
categories: python
tags: [python, python加密解密, RSA]
date: 2014-12-10 10:00:46
---


rsa 安装

pip install rsa

<pre>
import rsa
(bob_pub, bob_priv) = rsa.newkeys(512)
message = 'hello Bob!'
crypto = rsa.encrypt(message, bob_pub)
message = rsa.decrypt(crypto, bob_priv)
print message

</pre>
