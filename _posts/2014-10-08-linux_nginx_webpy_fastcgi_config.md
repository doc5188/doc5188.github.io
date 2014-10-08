---
layout: post
title: "nginx + webpy + fastcgi cache 配置详解"
categories: linux 
tags: [webpy, nginx, fastcgi]
date: 2014-10-08 17:31:44
---

<p>为了使nginx + webpy + fastcgi 这一组合达到性能最优，决定配置nginx的fastcgi cache，本文将详述配置的步骤和所遇到的问题。</p>
<h2>一. 安装nginx最新稳定版本和nginx_ngx_cache_purge模块</h2>
<p>我（即<a href="http://OutOfMemory.CN">OutOfMemory.CN</a>）使用的nginx版本是最新稳定版nginx 1.2.6, 首先需要在Linux安装此nginx版本。</p>
<p>首先需要切换到某个安装目录，执行下面命令下载nginx安装包：</p>
<pre style="" class="prettyprint shell prettyprinted"><span class="pln">wget http</span><span class="pun">:</span><span class="com">//nginx.org/download/nginx-1.2.6.tar.gz</span></pre>

<p>并解压tar.gz文件：</p>
<pre style="" class="prettyprint shell prettyprinted"><span class="pln">tar </span><span class="pun">-</span><span class="pln">xvf </span><span class="pun">./</span><span class="pln">nginx</span><span class="pun">-</span><span class="lit">1.2</span><span class="pun">.</span><span class="lit">6.tar</span><span class="pun">.</span><span class="pln">gz</span></pre>

<p>按照上面步骤下载并解压nginx模块<a href="http://labs.frickle.com/nginx_ngx_cache_purge/">nginx_ngx_cache_purge</a>的最新稳定版本，我用的是ngx_cache_purge-2.0</p>
<p>文件下载解压完毕之后就可以安装了，切换到nginx路径下，执行如下命令：</p>
<pre style="" class="prettyprint shell prettyprinted"><span class="pun">.</span><span class="str">/configure --prefix=/</span><span class="pln">data0</span><span class="pun">/</span><span class="pln">nginx</span><span class="pun">-</span><span class="lit">1.2</span><span class="pun">.</span><span class="lit">6</span><span class="pun">/</span><span class="pln"> </span><span class="pun">--</span><span class="pln">user</span><span class="pun">=</span><span class="pln">web </span><span class="pun">--</span><span class="kwd">group</span><span class="pun">=</span><span class="pln">web </span><span class="pun">--</span><span class="kwd">with</span><span class="pun">-</span><span class="pln">http_ssl_module </span><span class="pun">--</span><span class="pln">add</span><span class="pun">-</span><span class="kwd">module</span><span class="pun">=../</span><span class="pln">ngx_cache_purge</span><span class="pun">-</span><span class="lit">2.0</span><span class="pln"> </span><span class="pun">--</span><span class="kwd">with</span><span class="pun">-</span><span class="pln">http_stub_status_module</span></pre>

<p>这里configure配置了安装的路径，和nginx的用户以及用户组（需要预先创建好），和nginx  fastcgi cache最为相关的是加上 --add-module=../ngx_cache_pruge-2.0 指定要添加purge缓存的模块。</p>
<p>然后执行 <code>make</code> 一切顺利，再执行<code>make install</code></p>
<h2>二. 配置nginx fastcgi cache 和purge</h2>
<p>首先在http范围内（您也可以根据需要添加到server配置内）添加下面配置：</p>
<pre style="" class="prettyprint conf prettyprinted"><span class="com">#fast cgi cache def</span><span class="pln">
fastcgi_cache_path  </span><span class="pun">/</span><span class="pln">data0</span><span class="pun">/</span><span class="pln">nginx</span><span class="pun">-</span><span class="lit">1.2</span><span class="pun">.</span><span class="lit">6</span><span class="pun">/</span><span class="pln">cache levels</span><span class="pun">=</span><span class="lit">1</span><span class="pun">:</span><span class="lit">2</span><span class="pln"> keys_zone</span><span class="pun">=</span><span class="pln">nginx_webpy_cache</span><span class="pun">:</span><span class="lit">1m</span><span class="pln"> inactive</span><span class="pun">=</span><span class="lit">1d</span><span class="pun">;</span><span class="pln">

fastcgi_temp_path </span><span class="pun">/</span><span class="pln">data0</span><span class="pun">/</span><span class="pln">nginx</span><span class="pun">-</span><span class="lit">1.2</span><span class="pun">.</span><span class="lit">6</span><span class="pun">/</span><span class="pln">cache</span><span class="pun">/</span><span class="pln">temp</span><span class="pun">;</span><span class="pln">

fastcgi_cache_key </span><span class="str">"$scheme$request_method$host$request_uri$is_args$args"</span><span class="pun">;</span></pre>

<p>这三行配置说明如下：</p>
<ul>
<li>第一行指定了fastcgi缓存的路径为 /data0/nginx-1.2.6/cache , levels=1:2 表示生成缓存文件路径规则，示例：5/29/f08bc91a7a0ff59aad7121e2c1d79295，keys_zone=nginx_webpy_cache:1m 指定缓存使用共享内存的名称为nginx_webpy_cache共享内存大小为1m，inactive=1d表示缓存在1天之后过期。</li>
<li>第二行指定fastcgi缓存的临时路径的地址</li>
<li>第三行指定缓存键的格式$scheme$request_method$host$request_uri$is_args$args 这样配置的缓存键示例： httpGEToutofmemory.cn/code-snippet/2075/java-ArrayList-yichu-repeat-item </li>
</ul>
<p><strong>需要特别注意nginx运行用户必须有上面配置的缓存路径和临时路径的读写权限</strong>, 否则缓存不了</p>
<p>然后需要在location配置中根据需要添加相应的缓存配置</p>
<p>例如我的配置：</p>
<pre style="" class="prettyprint conf prettyprinted"><span class="pln">        location </span><span class="pun">~^</span><span class="pln"> </span><span class="pun">/</span><span class="pln">code</span><span class="pun">-</span><span class="pln">snippet</span><span class="pun">/</span><span class="pln"> </span><span class="pun">{</span><span class="pln">
                fastcgi_param REQUEST_METHOD $request_method</span><span class="pun">;</span><span class="pln">
                fastcgi_param QUERY_STRING $query_string</span><span class="pun">;</span><span class="pln">
                fastcgi_param CONTENT_TYPE $content_type</span><span class="pun">;</span><span class="pln">
                fastcgi_param CONTENT_LENGTH $content_length</span><span class="pun">;</span><span class="pln">
                fastcgi_param GATEWAY_INTERFACE CGI</span><span class="pun">/</span><span class="lit">1.1</span><span class="pun">;</span><span class="pln">
                fastcgi_param SERVER_SOFTWARE nginx</span><span class="pun">/</span><span class="pln">$nginx_version</span><span class="pun">;</span><span class="pln">
                fastcgi_param REMOTE_ADDR $remote_addr</span><span class="pun">;</span><span class="pln">
                fastcgi_param REMOTE_PORT $remote_port</span><span class="pun">;</span><span class="pln">
                fastcgi_param SERVER_ADDR $server_addr</span><span class="pun">;</span><span class="pln">
                fastcgi_param SERVER_PORT $server_port</span><span class="pun">;</span><span class="pln">
                fastcgi_param SERVER_NAME $server_name</span><span class="pun">;</span><span class="pln">
                fastcgi_param SERVER_PROTOCOL $server_protocol</span><span class="pun">;</span><span class="pln">
                fastcgi_param SCRIPT_FILENAME $fastcgi_script_name</span><span class="pun">;</span><span class="pln">
                fastcgi_param PATH_INFO $fastcgi_script_name</span><span class="pun">;</span><span class="pln">

                fastcgi_pass </span><span class="lit">127.0</span><span class="pun">.</span><span class="lit">0.1</span><span class="pun">:</span><span class="lit">9002</span><span class="pun">;</span><span class="pln">

</span><span class="com">#fastcgi cache def</span><span class="pln">
                fastcgi_cache   nginx_webpy_cache</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定使用缓存共享内存的名字，和上面定义相对应</span><span class="pln">
                fastcgi_cache_valid   </span><span class="lit">200</span><span class="pln"> </span><span class="lit">302</span><span class="pln">  </span><span class="lit">1h</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定200和302要缓存的时长</span><span class="pln">
                fastcgi_cache_valid   </span><span class="lit">301</span><span class="pln">      </span><span class="lit">1d</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定301要缓存的时间</span><span class="pln">
                fastcgi_cache_valid   any      </span><span class="lit">10m</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定其他状态号要缓存的时间</span><span class="pln">
                fastcgi_cache_min_uses  </span><span class="lit">1</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定缓存的最少使用次数</span><span class="pln">
                fastcgi_ignore_headers </span><span class="str">"Cache-Control"</span><span class="pln"> </span><span class="str">"Expires"</span><span class="pln"> </span><span class="str">"Set-Cookie"</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定要忽略fast cgi cache输出的头</span><span class="pln">
                fastcgi_hide_headers </span><span class="str">"Set-Cookie"</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定在输出缓存时要忽略的http相应头</span><span class="pln">
                fastcgi_cache_use_stale error  timeout invalid_header http_500</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定500的处理</span><span class="pln">

                fastcgi_cache_valid  </span><span class="lit">60m</span><span class="pun">;</span><span class="pln"> </span><span class="com">#指定一般性的缓存时间</span><span class="pln">

                add_header X</span><span class="pun">-</span><span class="typ">Cache</span><span class="pln"> $upstream_cache_status</span><span class="pun">;</span><span class="pln"> </span><span class="com">#添加表示缓存是否命中的响应头</span><span class="pln">
</span><span class="com">#end            </span><span class="pln">
       </span><span class="pun">}</span></pre>

<p>这里fastcgi cache相关的配置在注释#fastcgi cache def 和 #end之间，每一行都有对应的注释，这里要特别注意fastcgi_ignore_headers这个不配置会导致缓存的状态一直是MISS。</p>
<p>以上配置完毕后，就可以在浏览器中查看是否成功缓存了，但是只缓存还是不够的，我们还需要在需要的时候能够清除缓存，比如对于<a href="http://OutOfMemory.CN">OutOfMemory.CN</a>来说在用户编辑了代码之后，必须马上清除对应url的缓存，这样用户才可以马上看到修改后的结果。</p>
<p>如下是purge缓存相关的配置：</p>
<pre style="" class="prettyprint conf prettyprinted"><span class="pln">   location </span><span class="pun">~</span><span class="pln"> </span><span class="str">/purge(/</span><span class="pun">.*)</span><span class="pln"> </span><span class="pun">{</span><span class="pln">
            allow              </span><span class="lit">127.0</span><span class="pun">.</span><span class="lit">0.1</span><span class="pun">;</span><span class="pln">
            deny               all</span><span class="pun">;</span><span class="pln">
            fastcgi_cache_purge     nginx_webpy_cache  </span><span class="str">"$scheme$request_method$host$1$is_args$args"</span><span class="pun">;</span><span class="pln">
        </span><span class="pun">}</span></pre>

<p>这个配置使用了nginx_ngx_cache_purge模块，这个配置里面首先要指定purge url的规则为 /purge(/.*) purge后的括号内的正则表达式要在下面使用，在location里面的allow指定允许那些ip访问purge，deny all配置禁止其他所有ip访问此路径；</p>
<p><code>fastcgi_cache_purge     nginx_webpy_cache  "$scheme$request_method$host$1$is_args$args";</code> 指定purge对应的cache名称为nginx_webpy_cache，其缓存键的格式为<code>$scheme$request_method$host$1$is_args$args</code>，这里<code>$1</code>就是在location正则括号内定义的部分，这个键值要和上面缓存的键值一致。</p>
<h2>三. 做webpy fastcgi cache 时遇到的问题</h2>
<p>我做这个配置很曲折，经过了4天才完全解决问题，我遇到的问题如下：</p>
<ol>
<li>fastcgi_ignore_headers 这个配置中如果响应中有cookie的话必须要加上Set-Cookie否则缓存状态会一直MISS</li>
<li>用户权限问题，注意nginx运行使用的用户必须有缓存路径和缓存临时路径两个路径的读写权限，否则缓存一直会MISS</li>
<li>注意对于webpy 的fastcgi做缓存用的是nginx fastcgi cache 而不是 proxy cache</li>
<li>注意purge中配置的缓存键是要和上面一致的，$1要替代上面的$request_uri</li>
</ol>
<p>就是这样子了，webpy + nginx + fastcgi + fastcgi cache 还是非常给力的！！</p>

<pre>
来源: http://outofmemory.cn/code-snippet/2154/nginx-webpy-fastcgi-cache-configuration-explain-in-detail
</pre>
