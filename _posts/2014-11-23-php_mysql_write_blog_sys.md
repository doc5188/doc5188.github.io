---
layout: post
title: "利用PHP/MYSQL实现的简易微型博客"
categories: php
tags: [php, mysql, php小项目]
date: 2014-11-23 01:11:21
---

<p>数据库：ly_php_base</p>

<p>表：ly_micro_blog(仅仅有一个表)字段：id,title,date,content,hits</p>

<p>文件：</p>

<p>

<table border="2" width="800" cellspacing="2" cellpadding="1" align="center" style="font-weight:bold; text-align:center">

<caption>文件详细描述</caption>

<tbody>

<tr>

<td style="text-align:center">文件</td>

<td style="text-align:center">描述</td>

</tr>

<tr>

<td style="text-align:center">default.php</td>

<td style="text-align:center">默认主页。显示博文与操作连接。</td>

</tr>

<tr>

<td style="text-align:center">add.php</td>

<td style="text-align:center">添加新博文的功能模块。</td>

</tr>

<tr>

<td style="text-align:center">edit.php</td>

<td style="text-align:center">对已经添加过的博文进行修改操作。</td>

</tr>

<tr>

<td style="text-align:center">delete.php</td>

<td style="text-align:center">删除博文模块。</td>

</tr>

<tr>

<td style="text-align:center">view.php</td>

<td style="text-align:center">显示博文的详细信息（标题|添加日期|浏览次数|内容）。</td>

</tr>

<tr>

<td style="text-align:center">conn.php</td>

<td style="text-align:center">链接数据库操作。在其它文件中被引用。</td>

</tr>

</tbody>

</table>

</p>

<div style="text-align:center"><strong><br>

</strong></div>

<strong>conn.php</strong>

<p></p>

<pre name="code" class="php">&lt;?php
/**
 *ly_micro_blog
 *ID|TITLE|CONTENT|DATE
 **/
?&gt;
&lt;?php
//连接MySql数据库服务
$conn = @mysql_connect(&quot;localhost:3306&quot;,&quot;root&quot;,&quot;228580&quot;) or die(&quot;连接数据库服务器失败！&quot;);
//连接ly_php_base数据库
@mysql_select_db(&quot;ly_php_base&quot;,$conn) or die(&quot;未能连接到数据库！&quot;);
//mysql_query(&quot;SET NAMES 'GBK'&quot;);
?&gt;</pre><strong>default.php</strong><pre name="code" class="html">&lt;?php
include(&quot;conn.php&quot;);
//搜索关键字的管理
if(!empty($_GET['keys'])){
	$keys = &quot;WHERE title like '%&quot;.$_GET['keys'].&quot;%'&quot;;
} else {
	$keys = &quot;&quot;;
}
$sql = &quot;SELECT * FROM ly_micro_blog &quot;.$keys.&quot; ORDER BY id DESC LIMIT 10&quot;;
$query = mysql_query($sql);
$rs = mysql_fetch_array($query);
?&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;我的微博客主页&lt;/title&gt;
&lt;meta http-equiv=&quot;Content-Type&quot; content=&quot;text/html;charset=utf-8&quot;/&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;a href=&quot;add.php&quot;&gt;添加内容&lt;/a&gt;
&lt;form action=&quot;&quot; method=&quot;get&quot;&gt;
  &lt;input type=&quot;text&quot; name=&quot;keys&quot;/&gt;
  &lt;input type=&quot;submit&quot; name=&quot;submit&quot; value=&quot;内容搜索&quot;/&gt;
&lt;/form&gt;
&lt;hr color=&quot;#FF9900&quot; size=&quot;3&quot; /&gt;
&lt;?php
if(!$rs){
	echo &quot;没有相关内容！&quot;;
}
//没有实现分页导航功能
while($rs){
?&gt;
&lt;h2&gt;标题：&lt;?php echo $rs['title'];?&gt;|&lt;a href=&quot;edit.php?id=&lt;?php echo $rs['id'];?&gt;&quot;&gt;编辑&lt;/a&gt;|&lt;a href=&quot;delete.php?id=&lt;?php echo $rs['id'];?&gt;&quot;&gt;删除&lt;/a&gt;&lt;/h2&gt;
&lt;li&gt;日期：&lt;?php echo $rs['date'];?&gt;&lt;/li&gt;
&lt;p&gt;内容&lt;?php echo iconv_substr($rs['content'],0,50,&quot;UTF-8&quot;);?&gt;...... &lt;a href=&quot;view.php?id=&lt;?php echo $rs['id'];?&gt;&quot;&gt;|查看详细内容|&lt;/a&gt;&lt;/p&gt;
&lt;hr color=&quot;#0033FF&quot; size=&quot;5&quot; /&gt;
&lt;?php
	$rs = mysql_fetch_array($query);
}
?&gt;
&lt;/body&gt;
&lt;/html&gt;</pre><strong>add.php</strong>

<p></p>

<pre name="code" class="html">&lt;?php
//引入连接数据库文件
include(&quot;conn.php&quot;);

if(!empty($_POST['submit'])){
	$title = $_POST['title'];
	$content = $_POST['content'];
	$sql = &quot;INSERT INTO ly_micro_blog VALUES(NULL,'$title','$content',now())&quot;;
	mysql_query($sql);
}
?&gt;
&lt;!DOCTYPE HTML&gt;
&lt;html&gt;
&lt;head&gt;
&lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html;charset=utf-8&quot;/&gt;
&lt;title&gt;发布微博页面&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;a href=&quot;default.php&quot;&gt;查看内容&lt;/a&gt;
&lt;hr color=&quot;#0033CC&quot; size=&quot;3px&quot;/&gt;
&lt;form action=&quot;add.php&quot; method=&quot;post&quot;&gt;
  标题：
  &lt;input type=&quot;text&quot; name=&quot;title&quot;/&gt;
  &lt;br /&gt;
  内容：
  &lt;textarea rows=&quot;5&quot; cols=&quot;50&quot; name=&quot;content&quot;&gt;&lt;/textarea&gt;
  &lt;br /&gt;
  &lt;input type=&quot;submit&quot; name=&quot;submit&quot; value=&quot;提交&quot;/&gt;
  &lt;br /&gt;
&lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>

<p><strong>edit.php</strong></p>

<p></p>

<pre name="code" class="php">&lt;?php 
include(&quot;conn.php&quot;);
if(!empty($_GET['id'])){
	$id = $_GET['id'];
	$sql = &quot;select * from ly_micro_blog where id = &quot;.$_GET['id'];
	$query = mysql_query($sql);	
	$rc = mysql_fetch_array($query);
}

if(!empty($_POST['update'])){
	echo &quot;更新按钮提交成功！&quot;;
}
?&gt;

&lt;!DOCTYPE HTML&gt;
&lt;html&gt;
&lt;head&gt;
&lt;meta http-equiv=&quot;Content-Type&quot; content=&quot;text/html; charset=utf-8&quot;&gt;
&lt;title&gt;编辑页面&lt;/title&gt;
&lt;/head&gt;

&lt;body&gt;
&lt;form action=&quot;edit.php?id=&lt;?php echo $id;?&gt;&quot; method=&quot;post&quot;&gt;
  标题：
  &lt;input type=&quot;text&quot; name=&quot;title&quot; value=&quot;&lt;?php echo $rc['title'];?&gt;&quot;/&gt;
  &lt;br /&gt;
  内容：
  &lt;textarea rows=&quot;5&quot; cols=&quot;50&quot; name=&quot;content&quot;&gt;&lt;?php echo $rc['content'];?&gt;&lt;/textarea&gt;
  &lt;br /&gt;
  &lt;input type=&quot;submit&quot; name=&quot;update&quot; value=&quot;更新&quot;/&gt;
  &lt;br /&gt;
&lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;</pre><strong>delete.php</strong>

<p></p>

<p></p>

<pre name="code" class="php">&lt;?php
/**
 *ly_micro_blog
 *ID|TITLE|CONTENT|DATE
 **/
?&gt;
&lt;?php
//连接MySql数据库服务
$conn = @mysql_connect(&quot;localhost:3306&quot;,&quot;root&quot;,&quot;228580&quot;) or die(&quot;连接数据库服务器失败！&quot;);
//连接ly_php_base数据库
@mysql_select_db(&quot;ly_php_base&quot;,$conn) or die(&quot;未能连接到数据库！&quot;);
//mysql_query(&quot;SET NAMES 'GBK'&quot;);
?&gt;</pre><strong>view.php</strong>

<p></p>

<p></p>

<pre name="code" class="php">&lt;?php 
include(&quot;conn.php&quot;);

if(!empty($_GET['id'])){
	$sql = &quot;SELECT * FROM ly_micro_blog WHERE id = &quot;.$_GET['id'];
	$rc = mysql_fetch_array(mysql_query($sql));
	mysql_query(&quot;UPDATE ly_micro_blog SET hits = hits + 1 WHERE id = &quot;.$_GET['id']);
} else {
	echo &quot;参数引入失败！&quot;;
}
?&gt;

&lt;!DOCTYPE HTML&gt;
&lt;html&gt;
&lt;head&gt;
&lt;meta http-equiv=&quot;Content-Type&quot; content=&quot;text/html; charset=utf-8&quot;&gt;
&lt;title&gt;&lt;?php echo $rc['title'];?&gt;|我的微博客&lt;/title&gt;
&lt;/head&gt;

&lt;body&gt;
&lt;a href=&quot;default.php&quot;&gt;返回主页面&lt;/a&gt;
&lt;hr color=&quot;#00FFFF&quot; size=&quot;5px&quot;/&gt;
&lt;h2&gt;&lt;?php echo $rc['title'];?&gt;
  &lt;hr color=&quot;#006699&quot; size=&quot;3px&quot;&gt;
&lt;/h2&gt;
&lt;li&gt;&lt;?php echo &quot;日期：&quot;.$rc['date'].&quot;|浏览次数：&quot;.$rc['hits'];?&gt;&lt;/li&gt;
&lt;p&gt;&lt;?php echo $rc['content'];?&gt;&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</pre>自学MYSQL &#43; Apache &#43; PHP！第一次做网络方面的内容，感觉挺有趣的。不过，linux的许多知识还是特别陌生！留此内容以做备份，转载留下本文连接：<strong><span style="color:#ffffff"><a href="http://www.shopliyang.com.cn/" target="_blank">http://www.shopliyang.com.cn/</a></span></strong>

