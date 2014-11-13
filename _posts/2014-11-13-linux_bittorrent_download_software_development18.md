---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--哈希模块（sha1.h）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:37
---

<pre name="code" class="cpp">#ifndef SHA1_H
#define SHA1_H

/*
 *	本文件中的函数用于对一段文本使用sha1算法计算其HASH值
 *  本文件为自由的开放源代码,可以任意使用,实现细节不必理会,只需使用即可
 */

/*
SHA-1 in C   By Steve Reid &lt;steve@edmweb.com&gt;   100% Public Domain

Test Vectors (from FIPS PUB 180-1)
&quot;abc&quot;
  A9993E36 4706816A BA3E2571 7850C26C 9CD0D89D
&quot;abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq&quot;
  84983E44 1C3BD26E BAAE4AA1 F95129E5 E54670F1
A million repetitions of &quot;a&quot;
  34AA973C D4C4DAA4 F61EEB2B DBAD2731 6534016F
*/

#include &lt;sys/types.h&gt;

#define SHA1HANDSOFF

#ifdef __cplusplus
extern &quot;C&quot; {
#endif

typedef struct {
    unsigned long state[5];
    unsigned long count[2];
    unsigned char buffer[64];
} SHA1_CTX;

void SHA1Transform(unsigned long state[5], unsigned char buffer[64]);
void SHA1Init(SHA1_CTX* context);
void SHA1Update(SHA1_CTX* context, unsigned char* data, unsigned int len);
void SHA1Final(unsigned char digest[20], SHA1_CTX* context);

#ifdef __cplusplus
}
#endif

#endif
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971540
</pre>
