---
layout: post
title: "CDN技术原理"
categories: 网络
tags: [cdn]
date: 2014-11-21 12:56:07
---

<p>要了解CDN的实现原理，首先让我们来回顾一下网站传统的访问过程，以便理解其与CDN访问方式之间的差别：</p>
<table class="ln" bordercolordark="#ffffff" bordercolorlight="#999999" align="center" bgcolor="#ddddd" border="1" cellspacing="0">
<tbody>
<tr>
<td bgcolor="#ffffff"><a href="/upload/images/1554200.gif" target="_blank"><img class="fit-image" onload="javascript:if(this.width>498)this.width=498;" onmousewheel="javascript:return big(this)" alt="" src="/upload/images/1554200.gif" height="40" border="0" width="441"></a></td></tr>
<tr></tr></tbody></table>
<p>由上图可见，传统的网站访问过程为:</p>
<p>1. 用户在浏览器中输入要访问的域名；<br>2. 浏览器向域名解析服务器发出解析请求，获得此域名对应的IP地址；<br>3. 浏览器利用所得到的IP地址，向该IP对应的服务器发出访问请求；<br>4. 服务器对此响应，将数据回传至用户浏览器端显示出来。</p>
<p>与传统访问方式不同，CDN网络则是在用户和服务器之间增加Cache层，将用户的访问请求引导到Cache节点而不是服务器源站点，要实现这一目的，主要是通过接管DNS实现，下图为使用CDN缓存后的网站访问过程：</p>
<table class="ln" bordercolordark="#ffffff" bordercolorlight="#999999" align="center" bgcolor="#ddddd" border="1" cellspacing="0">
<tbody>
<tr>
<td bgcolor="#ffffff"><a href="/upload/images/1554201.gif" target="_blank"><img class="fit-image" onload="javascript:if(this.width>498)this.width=498;" onmousewheel="javascript:return big(this)" alt="" src="/upload/images/1554201.gif" height="340" border="0" width="392"></a></td></tr>
<tr></tr></tbody></table>
<p>由上图可见，使用CDN缓存后的网站访问过程演变为：</p>
<p>1.&nbsp; 用户在浏览器中输入要访问的域名； <br>2.&nbsp; 浏览器向域名解析服务器发出解析请求，由于CDN对域名解析过程进行了调整，所以用户端一般得到的是该域名对应的CNAME记录，此时浏览器需要再次对获得的CNAME域名进行解析才能得到缓存服务器实际的IP地址。<br><em>注：在此过程中，全局负载均衡DNS解析服务器会根据用户端的源IP地址，如地理位置（深圳还是上海）、接入网类型（电信还是网通）将用户的访问请求定位到离用户路由最短、位置最近、负载最轻的Cache节点（缓存服务器）上，实现就近定位。定位优先原则可按位置、可按路由、也可按负载等。</em> <br>3. 再次解析后浏览器得到该域名CDN缓存服务器的实际IP地址，向缓存服务器发出访问请求； <br>4.&nbsp; 缓存服务器根据浏览器提供的域名，通过Cache内部专用DNS解析得到此域名源服务器的真实IP地址，再由缓存服务器向此真实IP地址提交访问请求； <br>5.&nbsp; 缓存服务器从真实IP地址得到内容后，一方面在本地进行保存，以备以后使用，同时把得到的数据发送到客户端浏览器，完成访问的响应过程； <br>6.&nbsp; 用户端得到由缓存服务器传回的数据后显示出来，至此完成整个域名访问过程。 </p>
<p>通过以上分析可以看到，不论是否使用CDN网络，普通用户客户端设置不需做任何改变，直接使用被加速网站原有域名访问即可。对于要加速的网站，只需修改整个访问过程中的域名解析部分，便能实现透明的网络加速服务。 </p>
