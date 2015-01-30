---
layout: post
title: "一个简单的布隆过滤器"
categories: 技术文章
tags: []
date: 2015-01-30 13:38:09
---

<p> 布隆过滤器（Bloom Filter）是1970年由布隆提出的。它实际上是一个很长的二进制向量和一系列随机映射函数。布隆过滤器可以用于检索一个元素是否在一个集合中。它的优点是空间效率和查询时间都远远超过一般的算法，缺点是有一定的误识别率和删除困难。 </p> 
<p> ——摘自维基百科 </p> 
<p> <span style="font-size:10pt;line-height:1.5;">因为查找别的资料，偶尔发现这一利器。兴趣所致，写了一个简单的C实现。当然很多问题没有考虑在内，仅就核心概念给出了一个缩略版实现，做为一个提醒，加深一下印象。</span> </p> 
<p> simple_bf.h: </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">#ifndef _SIMPLE_BF_H_
#define _SIMPLE_BF_H_

#include &lt;stdint.h&gt;
#include &lt;stdbool.h&gt;

#define VEC_LEN (1024 * 1024 * 64 + 1)

#ifdef __cplusplus
extern "C" {
#endif

typedef struct _bf_vec {
        uint64_t part[VEC_LEN];
} bf_vec_t;

extern bool bf_add(bf_vec_t *vec, const char *str);

extern bool bf_is_contains(bf_vec_t *vec, const char *str);

#ifndef likely
#define likely(x) __builtin_expect((x),1)
#endif

#ifndef unlikely
#define unlikely(x) __builtin_expect((x),0)
#endif

#ifdef __cplusplus
}
#endif

#endif
</pre> simple_bf.c: 
<pre class="brush:cpp; toolbar: true; auto-links: false;">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include "simple_bf.h"

/* return false means the arg bit is over the bit length of the arg vec,
 * otherwise return true means successfully set the right bit.
 * for simple, only consider about these two conditions */
static inline __attribute__((always_inline)) bool bf_set_bit(bf_vec_t *vec, uint64_t bit)
{
	uint64_t part_cnt = bit / 64;
	if (unlikely(part_cnt &gt; VEC_LEN))
		return false;
	uint8_t mod = bit % 64;
	vec-&gt;part[part_cnt] |= (1ULL &lt;&lt; mod);
	return true;	
}

static inline __attribute__((always_inline)) bool bf_test_bit(bf_vec_t *vec, uint64_t bit)
{
	uint64_t part_cnt = bit / 64;
	if (unlikely(part_cnt &gt; VEC_LEN))
		return false;
	uint8_t mod = bit % 64;
	return ((vec-&gt;part[part_cnt] &amp; (1ULL &lt;&lt; mod)) != 0);	
}

/* the seed vector and the BKDR hash function */
static uint32_t seeds[8] = {31, 131, 1313, 13131, 131313, 1313131, 13131313, 131313131};
static uint32_t bkdr_hash_modified(const char *str, uint32_t seed)
{
	register uint32_t hash = 0;
	uint32_t ch;
	while ((ch = (uint32_t)*str++)) {
		hash = hash * seed + ch;
	}
	return hash;
}

bool bf_add(bf_vec_t *vec, const char *str)
{
	int i;
	for (i = 0; i &lt; 8; ++i) {
		uint32_t val = bkdr_hash_modified(str, seeds[i]);
		if (!bf_set_bit(vec, val))
			return false;
	}
	return true;
}

bool bf_is_contains(bf_vec_t *vec, const char *str)
{
	int i;
	for (i = 0; i &lt; 8; ++i) {
		uint32_t val = bkdr_hash_modified(str, seeds[i]);
		if (!bf_test_bit(vec, val))
			return false;
	}
	return true;
}

#ifndef NDEBUG 
int main1(int argc, char *argv[])
{
	if (argc &lt; 3) {
		fprintf(stderr, "usage: bf as0 [as1 as2 ...] ts\n"
				"as means string to add to the bloom filter\n"
				"ts means the string to test if it is in the filter vector\n"
				);
		return 1;
	}

	bf_vec_t *vec = calloc(1, sizeof(bf_vec_t));
	if (vec == NULL)
		return 1;
		
	int i;
	for (i = 1; i &lt; argc - 1; ++i) {
		if (bf_add(vec, argv[i]))
			printf("add to bloom filter successed, string %s\n", argv[i]);
		else
			printf("add to bloom filter FAILED, string %s\n", argv[i]);
	}
	printf("------------------------------------------------------------------\n");
	if (bf_is_contains(vec, argv[argc - 1]))
		printf("test string %s is in bloom filter\n", argv[argc - 1]);
	else
		printf("test string %s is NOT in bloom filter\n", argv[argc - 1]);

	free(vec);
	return 0;
}

int main2(int argc, char *argv[])
{
	if (argc != 3) {
		fprintf(stderr, "usage: bf filename ts\n"
			"file of filename contains the strings to be added\n"
			"ts means the string to test if it is in the filter vector\n"
			);
		return 1;
	}

	bf_vec_t *vec = calloc(1, sizeof(bf_vec_t));
	if (vec == NULL)
		return 1;
	
	char buf[128] = {0};	
	FILE *fp = fopen(argv[1], "rt");
	if (fp == NULL) {
		free(vec);
		return 1;
	}
	while (fgets(buf, sizeof(buf), fp) != NULL) {
		buf[strlen(buf) - 1] = '\0';
		if (bf_add(vec, buf))
			printf("add to bloom filter successed, string %s\n", buf);
		else
			printf("add to bloom filter FAILED, string %s\n", buf);
	}

	printf("------------------------------------------------------------------\n");
	if (bf_is_contains(vec, argv[2]))
		printf("test string %s is in bloom filter\n", argv[2]);
	else
		printf("test string %s is NOT in bloom filter\n", argv[2]);
	
	free(vec);
	return 0;
}

int main(int argc, char *argv[])
{
	return main2(argc, argv);
}
#endif</pre> 在Linux 2.6.39.4 SMP x86_64&nbsp;gcc version 4.4.3下做了简单测试，效率还是比较可观的。没有做量化的效率测试，也没有对误判率做量化测试。 
<p> 我在考虑是不是要加一个谓词回调接口，类似于： </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">typedef int (*bf_contains_cb)(void *data);
int bf_oper_if_contains(bf_vec_t *vec, const char *str, bf_contains_cb callback, void *data);</pre> 这样可用性应该会好一些。暂且放下，等到真正要用时，再做详细的量化测试和代码完善吧。



<pre>
referer:http://my.oschina.net/u/180497/blog/142039
</pre>
