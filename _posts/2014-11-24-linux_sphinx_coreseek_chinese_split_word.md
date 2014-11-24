---
layout: post
title: "Linux 下配置 Sphinx(coreseek) 中文分词"
categories: linux
tags: [linux, sphinx, coreseek, 中文分词]
date: 2014-11-24 08:59:49
---

<p>系统环境</p>

<ul>
<li>CentOS 6.4 x86_64</li>
</ul>


<h4 id="download">下载 <a href="#download">¶</a></h4>

<pre class="prettyprint"><code><span class="pln">$ wget http</span><span class="pun">:</span><span class="com">//www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz</span></code></pre>

<p>coreseek-4.1-beta.tar.gz 包含了分词包 <code>mmseg-3.2.14</code> 和搜索包 <code>csft-4.1</code>。</p>

<h4 id="install-mmseg">安装 mmseg <a href="#install-mmseg">¶</a></h4>

<pre class="prettyprint"><code><span class="pln">$ cd </span><span class="pun">/</span><span class="pln">usr</span><span class="pun">/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">src</span><span class="pun">/</span><span class="pln">
$ sudo tar xf </span><span class="pun">/</span><span class="pln">path</span><span class="pun">/</span><span class="pln">to</span><span class="pun">/</span><span class="pln">coreseek</span><span class="pun">-</span><span class="lit">4.1</span><span class="pun">-</span><span class="pln">beta</span><span class="pun">.</span><span class="pln">tar</span><span class="pun">.</span><span class="pln">gz
$ cd coreseek</span><span class="pun">-</span><span class="lit">4.1</span><span class="pun">-</span><span class="pln">beta</span><span class="pun">/</span><span class="pln">mmseg</span><span class="pun">-</span><span class="lit">3.2</span><span class="pun">.</span><span class="lit">14</span><span class="pun">/</span><span class="pln">
$ </span><span class="pun">./</span><span class="pln">bootstrap    </span><span class="com">##输出的warning信息可以忽略，如果出现error则需要解决</span><span class="pln">
$ </span><span class="pun">./</span><span class="pln">configure </span><span class="pun">--</span><span class="pln">prefix</span><span class="pun">=</span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mmseg3
$ make
$ sudo make install</span></code></pre>

<p>测试：</p>

<pre class="prettyprint"><code><span class="pln">$ </span><span class="pun">/</span><span class="pln">usr</span><span class="pun">/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mmseg3</span><span class="pun">/</span><span class="pln">bin</span><span class="pun">/</span><span class="pln">mmseg </span><span class="pun">-</span><span class="pln">d </span><span class="pun">/</span><span class="pln">usr</span><span class="pun">/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mmseg3</span><span class="pun">/</span><span class="pln">etc </span><span class="pun">../</span><span class="pln">testpack</span><span class="pun">/</span><span class="kwd">var</span><span class="pun">/</span><span class="pln">test</span><span class="pun">/</span><span class="pln">test</span><span class="pun">.</span><span class="pln">xml</span></code></pre>

<h4 id="install-csft">安装 csft <a href="#install-csft">¶</a></h4>

<pre class="prettyprint"><code><span class="pln">$ cd </span><span class="pun">../</span><span class="pln">csft</span><span class="pun">-</span><span class="lit">4.1</span><span class="pun">/</span><span class="pln">
$ </span><span class="pun">./</span><span class="pln">buildconf</span><span class="pun">.</span><span class="pln">sh    </span><span class="com">##输出的warning信息可以忽略，如果出现error则需要解决</span><span class="pln">
$ </span><span class="pun">./</span><span class="pln">configure </span><span class="pun">--</span><span class="pln">prefix</span><span class="pun">=</span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">coreseek </span><span class="pun">--</span><span class="pln">without</span><span class="pun">-</span><span class="pln">unixodbc </span><span class="pun">--</span><span class="kwd">with</span><span class="pun">-</span><span class="pln">mmseg </span><span class="pun">--</span><span class="kwd">with</span><span class="pun">-</span><span class="pln">mmseg</span><span class="pun">-</span><span class="pln">includes</span><span class="pun">=</span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mmseg3</span><span class="pun">/</span><span class="pln">include</span><span class="pun">/</span><span class="pln">mmseg</span><span class="pun">/</span><span class="pln"> </span><span class="pun">--</span><span class="kwd">with</span><span class="pun">-</span><span class="pln">mmseg</span><span class="pun">-</span><span class="pln">libs</span><span class="pun">=</span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mmseg3</span><span class="pun">/</span><span class="pln">lib</span><span class="pun">/</span><span class="pln"> </span><span class="pun">--</span><span class="kwd">with</span><span class="pun">-</span><span class="pln">mysql    </span><span class="com">##如果提示mysql问题</span><span class="pln">
$ make
$ sudo make install</span></code></pre>

<h4 id="configuration-csft.conf">配置 csft.conf <a href="#configuration-csft.conf">¶</a></h4>

<p>导入测试数据：</p>

<pre class="prettyprint"><code><span class="pln">$ mysql </span><span class="pun">-</span><span class="pln">uroot </span><span class="pun">-</span><span class="pln">p test </span><span class="pun">&lt;</span><span class="pln"> </span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">src</span><span class="pun">/</span><span class="pln">coreseek</span><span class="pun">-</span><span class="lit">4.1</span><span class="pun">-</span><span class="pln">beta</span><span class="pun">/</span><span class="pln">csft</span><span class="pun">-</span><span class="lit">4.1</span><span class="pun">/</span><span class="pln">example</span><span class="pun">.</span><span class="pln">sql
</span><span class="typ">Enter</span><span class="pln"> password</span><span class="pun">:</span></code></pre>

<p>配置 csft.conf，coreseek 默认会找 <code>安装目录下的 etc/csft.conf</code> 作为配置文件</p>

<pre class="prettyprint"><code><span class="pln">$ cd </span><span class="pun">/</span><span class="pln">usr</span><span class="pun">/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">coreseek</span><span class="pun">/</span><span class="pln">
$ cp etc</span><span class="pun">/</span><span class="pln">sphinx</span><span class="pun">-</span><span class="pln">min</span><span class="pun">.</span><span class="pln">conf</span><span class="pun">.</span><span class="pln">dist etc</span><span class="pun">/</span><span class="pln">csft</span><span class="pun">.</span><span class="pln">conf</span></code></pre>

<p>首先进入 MySQL 查看 <code>client - connection - server - results</code> 四项的编码，需要保持一致，<code>以下 coreseek 的配置也要保持编码一致</code>：</p>

<pre class="prettyprint"><code><span class="pln">mysql</span><span class="pun">&gt;</span><span class="pln"> show variables like </span><span class="str">'character_set_%'</span><span class="pun">;</span><span class="pln">
</span><span class="pun">+--------------------------+----------------------------------+</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> </span><span class="typ">Variable_name</span><span class="pln">            </span><span class="pun">|</span><span class="pln"> </span><span class="typ">Value</span><span class="pln">                            </span><span class="pun">|</span><span class="pln">
</span><span class="pun">+--------------------------+----------------------------------+</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_client     </span><span class="pun">|</span><span class="pln"> utf8                             </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_connection </span><span class="pun">|</span><span class="pln"> utf8                             </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_database   </span><span class="pun">|</span><span class="pln"> utf8                             </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_filesystem </span><span class="pun">|</span><span class="pln"> binary                           </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_results    </span><span class="pun">|</span><span class="pln"> utf8                             </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_server     </span><span class="pun">|</span><span class="pln"> utf8                             </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_set_system     </span><span class="pun">|</span><span class="pln"> utf8                             </span><span class="pun">|</span><span class="pln">
</span><span class="pun">|</span><span class="pln"> character_sets_dir       </span><span class="pun">|</span><span class="pln"> </span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mysql</span><span class="pun">/</span><span class="pln">share</span><span class="pun">/</span><span class="pln">charsets</span><span class="pun">/</span><span class="pln"> </span><span class="pun">|</span><span class="pln">
</span><span class="pun">+--------------------------+----------------------------------+</span><span class="pln">
</span><span class="lit">8</span><span class="pln"> rows </span><span class="kwd">in</span><span class="pln"> </span><span class="kwd">set</span><span class="pln"> </span><span class="pun">(</span><span class="lit">0.01</span><span class="pln"> sec</span><span class="pun">)</span></code></pre>

<p>这里使用的 utf8 编码，如果你使用的 gbk 编码，可能需要额外转换你的 mmseg 分词词库为 gbk 了。</p>

<p>编辑 <code>etc/csft.conf</code>， 1) 配置要索引的数据库：</p>

<pre class="prettyprint"><code><span class="pln">source src1
</span><span class="pun">{</span><span class="pln">
    type                </span><span class="pun">=</span><span class="pln"> mysql

    sql_host            </span><span class="pun">=</span><span class="pln"> localhost
    sql_user            </span><span class="pun">=</span><span class="pln"> test
    sql_pass            </span><span class="pun">=</span><span class="pln">
    sql_db              </span><span class="pun">=</span><span class="pln"> test
    sql_port            </span><span class="pun">=</span><span class="pln"> </span><span class="lit">3306</span><span class="pln">  </span><span class="com"># optional, default is 3306</span><span class="pln">

    </span><span class="com"># 设置数据库编码</span><span class="pln">
    sql_query_pre       </span><span class="pun">=</span><span class="pln"> SET NAMES utf8

    </span><span class="pun">...</span><span class="pln">
</span><span class="pun">}</span></code></pre>

<p>2) 配置中分分词：</p>

<pre class="prettyprint"><code><span class="pln">index test1
</span><span class="pun">{</span><span class="pln">
    </span><span class="pun">...</span><span class="pln">

    </span><span class="com"># 中文分词词典文件 uni.lib 的目录</span><span class="pln">
    charset_dictpath    </span><span class="pun">=</span><span class="pln"> </span><span class="str">/usr/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">mmseg3</span><span class="pun">/</span><span class="pln">etc</span><span class="pun">/</span><span class="pln">
    </span><span class="com"># 启用中文分词功能</span><span class="pln">
    charset_type        </span><span class="pun">=</span><span class="pln"> zh_cn</span><span class="pun">.</span><span class="pln">utf</span><span class="pun">-</span><span class="lit">8</span><span class="pln">
</span><span class="pun">}</span></code></pre>

<h4 id="test">测试 <a href="#test">¶</a></h4>

<p>1) <strong>索引</strong></p>

<pre class="prettyprint"><code><span class="pln">$ </span><span class="pun">./</span><span class="pln">bin</span><span class="pun">/</span><span class="pln">indexer </span><span class="pun">--</span><span class="pln">all

</span><span class="typ">Coreseek</span><span class="pln"> </span><span class="typ">Fulltext</span><span class="pln"> </span><span class="lit">4.1</span><span class="pln"> </span><span class="pun">[</span><span class="pln"> </span><span class="typ">Sphinx</span><span class="pln"> </span><span class="lit">2.0</span><span class="pun">.</span><span class="lit">2</span><span class="pun">-</span><span class="pln">dev </span><span class="pun">(</span><span class="pln">r2922</span><span class="pun">)]</span><span class="pln">
</span><span class="typ">Copyright</span><span class="pln"> </span><span class="pun">(</span><span class="pln">c</span><span class="pun">)</span><span class="pln"> </span><span class="lit">2007</span><span class="pun">-</span><span class="lit">2011</span><span class="pun">,</span><span class="pln">
</span><span class="typ">Beijing</span><span class="pln"> </span><span class="typ">Choice</span><span class="pln"> </span><span class="typ">Software</span><span class="pln"> </span><span class="typ">Technologies</span><span class="pln"> </span><span class="typ">Inc</span><span class="pln"> </span><span class="pun">(</span><span class="pln">http</span><span class="pun">:</span><span class="com">//www.coreseek.com)</span><span class="pln">

 </span><span class="kwd">using</span><span class="pln"> config file </span><span class="str">'/usr/local/coreseek/etc/csft.conf'</span><span class="pun">...</span><span class="pln">
indexing index </span><span class="str">'test1'</span><span class="pun">...</span><span class="pln">
collected </span><span class="lit">4</span><span class="pln"> docs</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.0</span><span class="pln"> MB
sorted </span><span class="lit">0.0</span><span class="pln"> </span><span class="typ">Mhits</span><span class="pun">,</span><span class="pln"> </span><span class="lit">100.0</span><span class="pun">%</span><span class="pln"> </span><span class="kwd">done</span><span class="pln">
total </span><span class="lit">4</span><span class="pln"> docs</span><span class="pun">,</span><span class="pln"> </span><span class="lit">193</span><span class="pln"> bytes
total </span><span class="lit">0.014</span><span class="pln"> sec</span><span class="pun">,</span><span class="pln"> </span><span class="lit">12906</span><span class="pln"> bytes</span><span class="pun">/</span><span class="pln">sec</span><span class="pun">,</span><span class="pln"> </span><span class="lit">267.48</span><span class="pln"> docs</span><span class="pun">/</span><span class="pln">sec
skipping non</span><span class="pun">-</span><span class="pln">plain index </span><span class="str">'testrt'</span><span class="pun">...</span><span class="pln">
total </span><span class="lit">3</span><span class="pln"> reads</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.000</span><span class="pln"> sec</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.1</span><span class="pln"> kb</span><span class="pun">/</span><span class="pln">call avg</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.0</span><span class="pln"> msec</span><span class="pun">/</span><span class="pln">call avg
total </span><span class="lit">9</span><span class="pln"> writes</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.000</span><span class="pln"> sec</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.1</span><span class="pln"> kb</span><span class="pun">/</span><span class="pln">call avg</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0.0</span><span class="pln"> msec</span><span class="pun">/</span><span class="pln">call avg</span></code></pre>

<p>如果你的 coreseek 安装目录下没有 <code>etc/csft.conf</code> 默认配置文件，使用 <code>-c /path/to/filename.conf</code> 指定配置文件，如：</p>

<pre class="prettyprint"><code><span class="pln">$ </span><span class="pun">./</span><span class="pln">bin</span><span class="pun">/</span><span class="pln">indexer </span><span class="pun">-</span><span class="pln">c etc</span><span class="pun">/</span><span class="pln">sphinx</span><span class="pun">-</span><span class="pln">min</span><span class="pun">.</span><span class="pln">conf</span><span class="pun">.</span><span class="pln">dist </span><span class="pun">--</span><span class="pln">all</span></code></pre>

<p>2) <strong>搜索</strong></p>

<pre class="prettyprint"><code><span class="pln">$ </span><span class="pun">./</span><span class="pln">bin</span><span class="pun">/</span><span class="pln">search </span><span class="str">"this is a test"</span><span class="pln">

</span><span class="typ">Coreseek</span><span class="pln"> </span><span class="typ">Fulltext</span><span class="pln"> </span><span class="lit">4.1</span><span class="pln"> </span><span class="pun">[</span><span class="pln"> </span><span class="typ">Sphinx</span><span class="pln"> </span><span class="lit">2.0</span><span class="pun">.</span><span class="lit">2</span><span class="pun">-</span><span class="pln">dev </span><span class="pun">(</span><span class="pln">r2922</span><span class="pun">)]</span><span class="pln">
</span><span class="typ">Copyright</span><span class="pln"> </span><span class="pun">(</span><span class="pln">c</span><span class="pun">)</span><span class="pln"> </span><span class="lit">2007</span><span class="pun">-</span><span class="lit">2011</span><span class="pun">,</span><span class="pln">
</span><span class="typ">Beijing</span><span class="pln"> </span><span class="typ">Choice</span><span class="pln"> </span><span class="typ">Software</span><span class="pln"> </span><span class="typ">Technologies</span><span class="pln"> </span><span class="typ">Inc</span><span class="pln"> </span><span class="pun">(</span><span class="pln">http</span><span class="pun">:</span><span class="com">//www.coreseek.com)</span><span class="pln">

 </span><span class="kwd">using</span><span class="pln"> config file </span><span class="str">'/usr/local/coreseek/etc/csft.conf'</span><span class="pun">...</span><span class="pln">
index </span><span class="str">'test1'</span><span class="pun">:</span><span class="pln"> query </span><span class="str">'this is a test '</span><span class="pun">:</span><span class="pln"> returned </span><span class="lit">0</span><span class="pln"> matches of </span><span class="lit">0</span><span class="pln"> total </span><span class="kwd">in</span><span class="pln"> </span><span class="lit">0.000</span><span class="pln"> sec

words</span><span class="pun">:</span><span class="pln">
</span><span class="lit">1.</span><span class="pln"> </span><span class="str">'this'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">4</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">4</span><span class="pln"> hits
</span><span class="lit">2.</span><span class="pln"> </span><span class="str">'is'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">4</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">4</span><span class="pln"> hits
</span><span class="lit">3.</span><span class="pln"> </span><span class="str">'a'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">0</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">0</span><span class="pln"> hits
</span><span class="lit">4.</span><span class="pln"> </span><span class="str">'test'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">3</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">5</span><span class="pln"> hits

index </span><span class="str">'testrt'</span><span class="pun">:</span><span class="pln"> search error</span><span class="pun">:</span><span class="pln"> failed to open </span><span class="pun">/</span><span class="pln">usr</span><span class="pun">/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">coreseek</span><span class="pun">/</span><span class="kwd">var</span><span class="pun">/</span><span class="pln">data</span><span class="pun">/</span><span class="pln">testrt</span><span class="pun">.</span><span class="pln">sph</span><span class="pun">:</span><span class="pln"> </span><span class="typ">No</span><span class="pln"> such file </span><span class="kwd">or</span><span class="pln"> directory</span><span class="pun">.</span></code></pre>

<p>其中 <code>'test': 3 documents, 5 hits</code> 表示：有 3 条记录符合要求，命中 5 次（即出现 5 次）。</p>

<p>3) 搜索中文</p>

<p>先插入一段中文：</p>

<pre class="prettyprint"><code><span class="pln">insert </span><span class="kwd">into</span><span class="pln"> documents</span><span class="pun">(</span><span class="pln">title</span><span class="pun">,</span><span class="pln"> content</span><span class="pun">)</span><span class="pln"> values
</span><span class="pun">(</span><span class="str">'锄禾日当午'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'锄禾日当午，上班真辛苦，一台破电脑，一坐一下午'</span><span class="pun">),</span><span class="pln">
</span><span class="pun">(</span><span class="str">'你有尺子吗'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'昨天看电视说＂吸烟导致猝死＂吓的我心里哆嗦！一咬牙一跺脚下定决心！＂以后不看电视了＂'</span><span class="pun">);</span></code></pre>

<p>重建索引：</p>

<pre class="prettyprint"><code><span class="pln">$ </span><span class="pun">./</span><span class="pln">bin</span><span class="pun">/</span><span class="pln">indexer </span><span class="pun">--</span><span class="pln">all</span></code></pre>

<p>搜索：</p>

<pre class="prettyprint"><code><span class="pln">$ </span><span class="pun">./</span><span class="pln">bin</span><span class="pun">/</span><span class="pln">search </span><span class="str">"以后不看电脑了"</span><span class="pln">

</span><span class="typ">Coreseek</span><span class="pln"> </span><span class="typ">Fulltext</span><span class="pln"> </span><span class="lit">4.1</span><span class="pln"> </span><span class="pun">[</span><span class="pln"> </span><span class="typ">Sphinx</span><span class="pln"> </span><span class="lit">2.0</span><span class="pun">.</span><span class="lit">2</span><span class="pun">-</span><span class="pln">dev </span><span class="pun">(</span><span class="pln">r2922</span><span class="pun">)]</span><span class="pln">
</span><span class="typ">Copyright</span><span class="pln"> </span><span class="pun">(</span><span class="pln">c</span><span class="pun">)</span><span class="pln"> </span><span class="lit">2007</span><span class="pun">-</span><span class="lit">2011</span><span class="pun">,</span><span class="pln">
</span><span class="typ">Beijing</span><span class="pln"> </span><span class="typ">Choice</span><span class="pln"> </span><span class="typ">Software</span><span class="pln"> </span><span class="typ">Technologies</span><span class="pln"> </span><span class="typ">Inc</span><span class="pln"> </span><span class="pun">(</span><span class="pln">http</span><span class="pun">:</span><span class="com">//www.coreseek.com)</span><span class="pln">

 </span><span class="kwd">using</span><span class="pln"> config file </span><span class="str">'/usr/local/coreseek/etc/csft.conf'</span><span class="pun">...</span><span class="pln">
index </span><span class="str">'test1'</span><span class="pun">:</span><span class="pln"> query </span><span class="str">'以后不看电脑了 '</span><span class="pun">:</span><span class="pln"> returned </span><span class="lit">0</span><span class="pln"> matches of </span><span class="lit">0</span><span class="pln"> total </span><span class="kwd">in</span><span class="pln"> </span><span class="lit">0.000</span><span class="pln"> sec

words</span><span class="pun">:</span><span class="pln">
</span><span class="lit">1.</span><span class="pln"> </span><span class="str">'以后'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> hits
</span><span class="lit">2.</span><span class="pln"> </span><span class="str">'不'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> hits
</span><span class="lit">3.</span><span class="pln"> </span><span class="str">'看'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">2</span><span class="pln"> hits
</span><span class="lit">4.</span><span class="pln"> </span><span class="str">'电脑'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> hits
</span><span class="lit">5.</span><span class="pln"> </span><span class="str">'了'</span><span class="pun">:</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> documents</span><span class="pun">,</span><span class="pln"> </span><span class="lit">1</span><span class="pln"> hits

index </span><span class="str">'testrt'</span><span class="pun">:</span><span class="pln"> search error</span><span class="pun">:</span><span class="pln"> failed to open </span><span class="pun">/</span><span class="pln">usr</span><span class="pun">/</span><span class="kwd">local</span><span class="pun">/</span><span class="pln">coreseek</span><span class="pun">/</span><span class="kwd">var</span><span class="pun">/</span><span class="pln">data</span><span class="pun">/</span><span class="pln">testrt</span><span class="pun">.</span><span class="pln">sph</span><span class="pun">:</span><span class="pln"> </span><span class="typ">No</span><span class="pln"> such file </span><span class="kwd">or</span><span class="pln"> directory</span><span class="pun">.</span></code></pre>

<p>到此 sphinx 中文分词索引的基本环境完成了。</p>













<pre>
referer: http://blog.aboutc.net/linux/47/linux-configure-sphinx-chinese-word-segmentation
</pre>
