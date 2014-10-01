---
layout: post
title: "PHP isset 函数作用"
categories: php
tags: [php, isset]
date: 2014-10-01 11:25:24
---

isset函数是检测变量是否设置。

格式：bool isset ( mixed var [, mixed var [, ...]] )

返回值：

<pre>
若变量不存在则返回 FALSE
若变量存在且其值为NULL，也返回 FALSE
若变量存在且值不为NULL，则返回 TURE
同时检查多个变量时，每个单项都符合上一条要求时才返回 TRUE，否则结果为 FALSE
如果已经使用 unset() 释放了一个变量之后，它将不再是 isset()。若使用 isset() 测试一个被设置成 NULL 的变量，将返回 FALSE。同时要注意的是一个 NULL 字节（"\0"）并不等同于 PHP 的 NULL 常数。
</pre>

警告: isset() 只能用于变量，因为传递任何其它参数都将造成解析错误。若想检测常量是否已设置，可使用 defined() 函数。

{% highlight bash %}
<?php
	$var = '';
	if (isset($var)) {
		print "This var is set set so I will print.";
	}

// 在后边的例子中，我们将使用 var_dump函数 输出 isset() 的返回值。
	$a = "test";
	$b = "anothertest";
	var_dump( isset($a) ); 
	// TRUEvar_dump( isset ($a, $b) ); 
	// TRUEunset ($a);
	var_dump( isset ($a) ); 
	// FALSEvar_dump( isset ($a, $b) ); 
	// FALSE
	$foo = NULL;
	var_dump( isset ($foo) ); 
	// FALSE
?>

{% endhighlight %}

{% highlight bash %}
<?php

$a = array ('test' => 1, 'hello' => NULL);

var_dump( isset ($a['test') ); // TRUE
var_dump( isset ($a['foo') ); // FALSE
var_dump( isset ($a['hello') ); // FALSE

// 'hello' 等于 NULL，所以被认为是未赋值的。
// 如果想检测 NULL 键值，可以试试下边的方法。
var_dump( array_key_exists('hello', $a) ); // TRUE

?>
{% endhighlight %}
