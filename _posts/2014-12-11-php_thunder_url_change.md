---
layout: post
title: "php 迅雷thunder://地址与普通url地址转换"
categories: php
tags: [php]
date: 2014-12-11 01:22:20
---

其实迅雷的thunder://地址就是将普通url地址加前缀‘AA’、后缀‘ZZ’，再base64编码后得到的字符串

普通url转thunder

{% highlight bash %}
<?php
function ThunderEncode($url) {
	$thunderPrefix="AA";
	$thunderPosix="ZZ";
	$thunderTitle="thunder://";
	$thunderUrl=$thunderTitle.base64_encode($thunderPrefix.$url.$thunderPosix);
	return $thunderUrl;
}
?>
{% endhighlight %}

thunder转普通url

{% highlight bash %}
<?php
function ThunderDecode($thunderUrl) {
	$thunderPrefix="AA";
	$thunderPosix="ZZ";
	$thunderTitle="thunder://";
	$url=substr(trim($thunderUrl),10);
	$url=base64_decode($url);
	$url=substr($url,2,-2);
	return $url;
}
?>

{% endhighlight %}


<pre>
referer:http://mrasong.com/a/thunder-encode-decode
</pre>
