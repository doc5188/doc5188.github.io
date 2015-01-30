---
layout: post
title: "Netflow v9示例"
categories: 技术文章
tags: []
date: 2015-01-30 13:38:11
---

<p> 因工作需要对Netflow v9协议进行了一些分析，其灵活的模板机制令人印象深刻。本着无代码无真相的原则，使用libpcap库做了一个简单的demo示例，其中对Netflow v9中需要获取的信息做了如下定义： </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">typedef struct _netflow_v9_record {
	u_int8_t ip_ver;
	union {
		u_int32_t v4_srcaddr;
		struct in6_addr v6_srcaddr;
	} srcaddr;
	union {
		u_int32_t v4_dstaddr;
		struct in6_addr v6_dstaddr;
	} dstaddr;
	union {
		u_int32_t v4_nexthop;
		struct in6_addr v6_nexthop;
	} nexthop;
	u_int32_t orig_pkts;
	u_int32_t orig_bytes;
	u_int32_t reply_pkts;
	u_int32_t reply_bytes;
	u_int32_t first;
	u_int32_t last;
	u_int16_t srcport;
	u_int16_t dstport;
	u_int16_t icmp_type;
	u_int16_t src_vlan;
	u_int16_t dst_vlan;
	u_int8_t src_mac[6];
	u_int8_t dst_mac[6];
	u_int8_t prot;
	u_int8_t tos;
} __attribute__((__packed__)) netflow_v9_record;</pre> 仿netfilter-conntrack中tuple机制，做链接管理结构如下（未单独提取tuple）： 
<pre class="brush:cpp; toolbar: true; auto-links: false;">struct link_info_t {
	struct hlist_node link;
	netflow_v9_record record;
	/* there will be something else */
};
static struct link_info_t tmp_link;

static struct hlist_head link_table[TABLE_SIZE];

static inline uint16_t hash_ip_port(struct link_info_t link)
{
	return ((link.record.dstaddr.v4_dstaddr ^ link.record.srcaddr.v4_srcaddr) ^ \
		(link.record.dstport ^ link.record.srcport)) &amp; 0x1ffff;
}</pre> 因为没有单独将tuple提取出来，且将ORIGINAL与REPLY做为同一个tuple以标示同一条连接，所以对连接的判断和统计繁琐了一些： 
<pre class="brush:cpp; toolbar: true; auto-links: false;">hlist_for_each_entry(cur_link, pos, head, link) {
			if (cur_link-&gt;record.srcaddr.v4_srcaddr == tmp_link.record.srcaddr.v4_srcaddr &amp;&amp; \
			    cur_link-&gt;record.dstaddr.v4_dstaddr == tmp_link.record.dstaddr.v4_dstaddr &amp;&amp; \
			    cur_link-&gt;record.srcport == tmp_link.record.srcport &amp;&amp; \
			    cur_link-&gt;record.dstport == tmp_link.record.dstport) {
				cur_link-&gt;record.orig_pkts++;
				cur_link-&gt;record.orig_bytes += len;
				flag = 1;
				break;
			} else if (cur_link-&gt;record.srcaddr.v4_srcaddr == tmp_link.record.dstaddr.v4_dstaddr &amp;&amp; \
			    cur_link-&gt;record.dstaddr.v4_dstaddr == tmp_link.record.srcaddr.v4_srcaddr &amp;&amp; \
			    cur_link-&gt;record.srcport == tmp_link.record.dstport &amp;&amp; \
			    cur_link-&gt;record.dstport == tmp_link.record.srcport) {
				cur_link-&gt;record.reply_pkts++;
				cur_link-&gt;record.reply_bytes += len;
				flag = 1;
				break;
			}
		}</pre> gen_nfv9模块负责构造、发送数据包，作为示例，仅手工构造了包含两个字段信息的template与数据信息，由lo:9999发送。 
<p> （不能添加附件??...:-(...） </p> 
<p> <br> </p> 
<p> <br> </p> 
<p> <br> </p>



<pre>
referer:http://my.oschina.net/u/180497/blog/150151
</pre>
