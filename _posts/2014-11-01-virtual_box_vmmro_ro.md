---
layout: post
title: "不能为虚拟电脑 xxx 打开一个新任务. Failed to load VMMR0.r0 (VERR_SUPLIB_OWNER_NOT_ROOT). 返回 代码:NS_ERROR_FAIL"
categories: 虚拟化
tags: [virtualbox]
date: 2014-11-01 16:49:31
---

<div id="article_content" class="article_content">

<p><br>
</p>
<h1><a name="t0"></a>描述：</h1>
<blockquote style="margin:0 0 0 40px; border:none; padding:0px">
<p><span style="font-family:Arial; font-size:14px; line-height:26px">不能为虚拟电脑 xxx 打开一个新任务.</span></p>
<p><span style="font-family:Arial; font-size:14px; line-height:26px">Failed to load VMMR0.r0 (VERR_SUPLIB_OWNER_NOT_ROOT).</span></p>
<p><span style="font-family:Arial; font-size:14px; line-height:26px">返回 代码:NS_ERROR_FAILURE (0x80004005)</span></p>
<p><span style="font-family:Arial; font-size:14px; line-height:26px">组件:Console</span></p>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
界面:IConsole {db7ab4ca-2a3f-4183-9243-c1208da92392}</p>
</blockquote>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
<br>
</p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
这是irtualbox报的一个错误。</p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
<br>
</p>
<h1><a name="t1"></a>解决办法：</h1>
<blockquote style="margin:0 0 0 40px; border:none; padding:0px">
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
ls -ld /usr &nbsp; &nbsp; &nbsp; /usr/lib &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;(注意： &nbsp;这是两个目录)</p>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
看下其所有者是否位root:root。如果不是，执行下面命令：</p>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
<span style="color:#ff0000">sudo chown root: root /usr &nbsp; &nbsp;/usr/lib</span></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
<br>
</p>
</blockquote>
<blockquote style="margin:0 0 0 40px; border:none; padding:0px">
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
</p>
<p style="line-height:25px; margin-top:0px; margin-bottom:10px; padding-top:0px; padding-bottom:0px; font-family:Arial,Helvetica,simsun,u5b8bu4f53; font-size:14px">
也有可能是因为 /opt 的 owner 不是 root 导致的，将其 owner 改成 root 即可：</p>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
</p>
<pre style="line-height:25px; font-size:14px"><span style="color:#ff0000">sudo chown root /opt</span></pre>
<p></p>
</blockquote>
<p></p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
<br>
</p>
<p style="margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px; font-family:Arial; font-size:14px; line-height:26px">
再次运行Virtualbox就ok了。</p>
<br>


总结：

查看~/VirtualBox\ VMs/win7/Logs/VBox.log　一步一步解决。

</div>
