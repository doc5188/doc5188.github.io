---
layout: post
title: "Python hashlib模块 （主要记录md5加密）"
categories: python
tags: [python, hashlib, md5加密]
date: 2014-10-12 02:03:52
---

python提供了一个进行hash加密的模块：hashlib

下面主要记录下其中的md5加密方式
{% highlight bash %}

    >>> import hashlib  
      
    >>> m = hashlib.md5()  
      
    >>> m.update("Nobody inspects")  
      
    >>> m.update(" the spammish repetition")  
      
    >>> m.digest()  
      
    '\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'  
      
    >>> m.hexdigest()  
      
    'bb649c83dd1ea5c9d9dec9a18df0ffe9'  
{% endhighlight %}


对以上代码的说明：

1.首先从python直接导入hashlib模块

2.调用hashlib里的md5()生成一个md5 hash对象

3.生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理

4.继续调用update方法会在前面加密的基础上更新加密

5.加密后的二进制结果

6.十六进制结果

如果只需对一条字符串进行加密处理，也可以用一条语句的方式：
{% highlight bash %}

    >>>print hashlib.new("md5", "Nobody inspects the spammish repetition").hexdigest()  
      
    'bb649c83dd1ea5c9d9dec9a18df0ffe9'  
{% endhighlight %}


引用官方文档部分：

The following values are provided as constant attributes of the hash objects returned by the constructors:

hash.digest_size

The size of the resulting hash in bytes.

hash.block_size

The internal block size of the hash algorithm in bytes.

A hash object has the following methods:

hash.update(arg)

Update the hash object with the string arg. Repeated calls are equivalent to a single call with the concatenation of all the arguments: m.update(a); m.update(b) is equivalent to m.update(a+b).

hash.digest()

Return the digest of the strings passed to the update() method so far. This is a string of digest_size bytes which may contain non-ASCII characters, including null bytes.

hash.hexdigest()

Like digest() except the digest is returned as a string of double length, containing only hexadecimal digits. This may be used to exchange the value safely in email or other non-binary environments.

hash.copy()

Return a copy (“clone”) of the hash object. This can be used to efficiently compute the digests of strings that share a common initial substring.
