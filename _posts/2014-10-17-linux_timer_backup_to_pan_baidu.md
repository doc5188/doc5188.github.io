---
layout: post
title: "Linux定时备份数据到百度云盘"
categories: linux
tags: [备份到百度盘]
date: 2014-10-17 00:01:48
---


<p>一直在想，要是百度云盘支持FTP多好，就可以实现Linux定时备份数据到百度云盘了。尤其在各云盘容量都达到T级后，更是有种浪费的感觉。</p>
<p>昨天无意间发现了一个脚本，可以实现<strong>Linux定时备份数据到百度云盘</strong>。</p>
<h2>安装bpcs_uploader</h2>
<p>虽然关于<strong>bpcs_uploader</strong>的教程不少，但都千篇一律。虽然网上也有很详细的教程，不过可能还有漏掉的细节。</p>
<p>废话不多说了，开工。</p>
<p>下载程序包：</p>
<p><code>wget https://github.com/oott123/bpcs_uploader/zipball/master</code></p>
<p>解压：</p>
<p><code>unzip master</code></p>
<p>默认的文件夹名字很长，为了方便以后操作，重命名文件夹：</p>
<p><code>mv oott123-bpcs_uploader-3a33d09 baidu</code></p>
<p>这里我将文件夹名字修改成了baidu，需要注意的是，以后的默认文件夹名字可能有所不同，毕竟程序会升级，你需要看一下解压出来的文件夹名称是什么。</p>
<p>进入程序目录：</p>
<p><code>cd baidu</code></p>
<p>设置权限：</p>
<p><code>chmod +x bpcs_uploader.php</code></p>
<p>运行程序：</p>
<p><code>./bpcs_uploader.php</code></p>
<p>你可能会看到出错提示，因为运行程序需要PHP环境，而你的服务器上的PHP路径可能与程序中设置的不同，修改一下程序文件bpcs_uploader.php中的PHP路径即可。</p>
<p>查看PHP路径：</p>
<p><code>which php</code></p>
<p>编辑bpcs_uploader.php文件：</p>
<p><code>vi&nbsp;bpcs_uploader.php</code></p>
<p>将第一句#!后的路径修改为你的PHP路径，如果你安装的是WDCP一键包，路径为：/www/wdlinux/php/bin/php</p>
<p>登录百度开发者中心：<a href="http://developer.baidu.com/" target="_blank">http://developer.baidu.com/</a></p>
<p>创建一个Web应用，应用名称自定义，例如：huihuige，其他默认设置就可以了。</p>
<p>此时，我们可以得到该应用的API Key，运行./bpcs_uploader.php后首先要输入的就是Key。</p>
<p>另外我们还要在应用管理中找到API管理，开启PCS API，设置一个目录，该目录将用于存放服务器上传过来的数据。</p>
<p>温馨提示：开启PCS API时设置的目录不可更改，但可以在“操作”菜单中删除应用重建。</p>
<p>输入Key后，接下来需要输入app floder name，也就是刚才开启PCS API时设置的目录名称。</p>
<p>然后需要输入access token，将你的Key填入以下地址相应位置，在浏览器打开得到的地址：</p>
<p><code>https://openapi.baidu.com/oauth/2.0/authorize?response_type=token&amp;client_id=<span style="color: #ff0000;">KEY</span>&amp;redirect_uri=oob&amp;scope=netdisk</code></p>
<p>然后你会看到一个写着“百度 Oauth2.0”的页面，将浏览器地址栏中的URL复制下来，找到access_token=和&amp;之间的字符串，这就是access token，输入access token后就完成了，你会看到SSH终端显示出了你的百度云盘容量。</p>
<p>如果之前有安装过bpcs_uploader，那么可以执行以下命令初始化：</p>
<p><code>./bpcs_uploader.php init</code></p>
<h2>bpcs_uploader用法</h2>
<p>查询容量：</p>
<p><code>./bpcs_uploader.php quota</code></p>
<p>上传文件：</p>
<p><code>./bpcs_uploader.php upload [path_local] [path_remote]</code></p>
<p>[path_local]是指服务器上的文件路径，[path_remote]是指百度云盘中的路径。</p>
<p>下载文件：</p>
<p><code>./bpcs_uploader.php download [path_local] [path_remote]</code></p>
<p>删除文件：</p>
<p><code>./bpcs_uploader.php delete [path_remote]</code></p>
<p>离线下载：</p>
<p><code>./bpcs_uploader.php fetch [path_remote] [path_to_fetch]</code></p>
<h2>自动备份脚本</h2>
<p>接下来需要设置自动备份数据，网上有许多自动备份脚本，所以我就不再复述了。</p>
<p>这里要介绍的是，由于我们多半都在Linux服务器上安装了控制面板，而控制面板都有自动备份数据的功能，比如WDCP就可以设置自动备份数据到/www/backup目录，那么我们就不再需要自动备份数据的脚本了，只需要一个脚本将备份目录下的所有文件上传到百度云盘即可。</p>
<p>下载脚本至baidu目录下：</p>
<p><code>wget&nbsp;http://www.huihuige.com/wp-content/uploads/2013/10/baidubd.zip</code></p>
<p>解压：</p>
<p><code>unzip baidubd.zip</code></p>
<p>这个脚本实用于WDCP面板用户，如果你的备份目录不同，可以打开脚本修改。</p>
<p>测试脚本是否有效：</p>
<p><code>sh baidubd.sh</code></p>
<p>最后设置计划任务：</p>
<p><code>crontab -e</code></p>
<p>加入一行：</p>
<p><code>0 0 * * * /root/baidu/baidubd.sh</code></p>
<p>这里设置了每天的凌晨零点自动备份数据到百度云盘。</p>
			
