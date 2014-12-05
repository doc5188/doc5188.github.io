---
layout: post
title: "Coreseek + PHP + MySQL实战随记（一）"
categories: php
tags: [coreseek, php, 项目实战]
date: 2014-12-05 17:34:55
---

<span style="line-height: 18px;"><font size="3">近段时间把coreseek(<b>sphinx+中文分词</b>)用到了项目中，以前对sphinx的研究起了很大的帮助，花了大概3天左右的时间就把测试环境塔起来了，同时封装了对sphinxapi调用的代码，让各个项目均可以方便的调用，尽管还不是很完善，但是已经基本可以使用了。</font></span>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">好记忆不如烂笔头，在此记录下来，希望对自己，对其他人会有些帮助。</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">1.indexer</font></b></span></div>
<div><span style="line-height: 18px;"><font color="#ff0000" size="3"><b>建索引命令</b></font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">indexer后面加--help或-h无法得到帮助选项，直接输入indexer可以得到帮助选项</font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/coreseek/bin/indexer</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright (c) 2007-2010,</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp;Usage: indexer [OPTIONS] [indexname1 [indexname2 [...]]]</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Options are:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--config &lt;file&gt; &nbsp; &nbsp; &nbsp; &nbsp; read configuration from specified file</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (default is csft.conf)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--all &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; reindex all configured indexes</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--quiet &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; be quiet, only print errors</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--noprogress &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;do not display progress</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (automatically on if output is not to a tty)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--rotate &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;send SIGHUP to searchd when indexing is over</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; to rotate updated indexes automatically</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--buildstops &lt;output.txt&gt; &lt;N&gt;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; build top N stopwords and write them to given file</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--buildfreqs &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;store words frequencies to output.txt</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (used with --buildstops only)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--merge &lt;dst-index&gt; &lt;src-index&gt;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; merge 'src-index' into 'dst-index'</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 'dst-index' will receive merge result</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 'src-index' will not be modified</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--merge-dst-range &lt;attr&gt; &lt;min&gt; &lt;max&gt;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; filter 'dst-index' on merge, keep only those documents</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; where 'attr' is between 'min' and 'max' (inclusive)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--merge-killlists &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; merge src and dst killlists instead of applying src killlist to dst</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Examples:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">indexer --quiet myidx1 &nbsp;reindex 'myidx1' defined in 'csft.conf'</font></span></div>
<div><span style="line-height: 18px;"><font size="3">indexer --all &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; reindex all indexes defined in 'csft.conf'</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">例如</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">/usr/local/web/coreseek/bin/search -c /path/to/csft.conf novel</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">/usr/local/web/coreseek/bin/search -c /path/to/csft.conf search_engine</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">/usr/local/web/coreseek/bin/search -c /path/to/csft.conf novel search_engine</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">/usr/local/web/coreseek/bin/search -c /path/to/csft.conf --all</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">2.search</font></b></span></div>
<div><font color="#ff0000" size="3"><span style="line-height: 25px;"><b>搜索命令</b></span></font></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">search后面加--help或-h无法得到帮助选项，直接输入search可以得到帮助选项</font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/coreseek/bin/search</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright (c) 2007-2010,</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp;Usage: search [OPTIONS] &lt;word1 [word2 [word3 [...]]]&gt;</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Options are:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-c, --config &lt;file&gt; &nbsp; &nbsp; use given config file instead of defaults</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-i, --index &lt;index&gt; &nbsp; &nbsp; search given index only (default: all indexes)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-a, --any &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; match any query word (default: match all words)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-b, --boolean &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; match in boolean mode</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-p, --phrase &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;match exact phrase</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-e, --extended &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;match in extended mode</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-f, --filter &lt;attr&gt; &lt;v&gt; only match if attribute attr value is v</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-s, --sortby &lt;CLAUSE&gt; &nbsp; sort matches by 'CLAUSE' in sort_extended mode</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-S, --sortexpr &lt;EXPR&gt; &nbsp; sort matches by 'EXPR' DESC in sort_expr mode</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-o, --offset &lt;offset&gt; &nbsp; print matches starting from this offset (default: 0)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-l, --limit &lt;count&gt; &nbsp; &nbsp; print this many matches (default: 20)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-q, --noinfo &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;don't print document info from SQL database</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-g, --group &lt;attr&gt; &nbsp; &nbsp; &nbsp;group by attribute named attr</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-gs,--groupsort &lt;expr&gt; &nbsp;sort groups by &lt;expr&gt;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--sort=date &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; sort by date, descending</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--rsort=date &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;sort by date, ascending</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--sort=ts &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; sort by time segments</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--stdin &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; read query from stdin</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">This program (CLI search) is for testing and debugging purposes only;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">it is NOT intended for production use.</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">例如</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">#在所有的索引中搜索</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">/usr/local/web/coreseek/bin/search -c /path/to/csft.conf 海</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff"><br><font size="3"></font></font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">#在指定的索引main_novel_index中搜索</font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3">/usr/local/web/coreseek/bin/search -c /path/to/csft.conf main_novel_index 海</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">3.searchd</font></b></span></div>
<div><span style="line-height: 18px;"><font color="#ff0000" size="3"><b>启动搜索服务命令</b></font></span></div>
<div><span style="line-height: 18px;"><font color="#0000ff" size="3"><b>与indexer及search相反，searchd后面加--help或-h可以得到帮助选项，直接输入searchd无法得到帮助选项</b></font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/home/software/coreseek-3.2.13/testpack# /usr/local/web/coreseek/bin/searchd --help</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright (c) 2007-2010,</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp;Usage: searchd [OPTIONS]</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Options are:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-h, --help &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;display this help message</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-c, -config &lt;file&gt; &nbsp; &nbsp; &nbsp;read configuration from specified file</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (default is csft.conf)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--stop &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;send SIGTERM to currently running searchd</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--status &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;get ant print status variables</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (PID is taken from pid_file specified in config file)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--iostats &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; log per-query io stats</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--cpustats &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;log per-query cpu stats</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Debugging options are:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--console &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; run in console mode (do not fork, do not log to files)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-p, --port &lt;port&gt; &nbsp; &nbsp; &nbsp; listen on given port (overrides config setting)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-l, --listen &lt;spec&gt; &nbsp; &nbsp; listen on given address, port or path (overrides</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; config settings)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-i, --index &lt;index&gt; &nbsp; &nbsp; only serve one given index</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--nodetach &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;do not detach into background</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Examples:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">searchd --config /usr/local/csft/etc/csft.conf</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font color="#ff0000" size="3">启动searchd服务前必须先建立索引，否则会出现找不到索引文件的错误</font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/coreseek/etc# /usr/local/web/coreseek/bin/searchd -c /usr/local/web/coreseek/etc/csft_mysql.conf</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright (c) 2007-2010,</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">using config file '/usr/local/web/coreseek/etc/csft_mysql.conf'...</font></span></div>
<div><span style="line-height: 18px;"><font size="3">listening on all interfaces, port=9312</font></span></div>
<div><span style="line-height: 18px;"><font size="3">WARNING: index 'search_engine': preload: failed to open /usr/local/web/coreseek/var/data/search_engine.sph: No such file or directory; NOT SERVING</font></span></div>
<div><span style="line-height: 18px;"><font size="3">WARNING: index 'novel': preload: failed to open /usr/local/web/coreseek/var/data/novel.sph: No such file or directory; NOT SERVING</font></span></div>
<div><span style="line-height: 18px;"><font size="3">FATAL: no valid indexes to serve</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">4.indextool</font></b></span></div>
<div><font size="3"><span style="line-height: 24px; font-family: 'Times New Roman';"><font color="#ff0000">indextool 是版本0.9.9-rc2中引入的辅助工具。用于输出关于物理索引的多种调试信息。（未来还计划加入索引验证等功能，因此起名较indextool而不是indexdump）</font></span><span style="line-height: 24px; font-family: 'Times New Roman'; color: rgb(104, 127, 150); font-size: 12px;">。</span></font></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/coreseek/bin# ./indextool&nbsp;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright (c) 2007-2010,</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp;Usage: indextool &lt;COMMAND&gt; [OPTIONS]</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Commands are:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--dumpheader &lt;FILENAME.sph&gt; &nbsp; &nbsp; dump index header by file name</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--dumpheader &lt;INDEXNAME&gt; &nbsp; &nbsp; &nbsp; &nbsp;dump index header by index name</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--dumpdocids &lt;INDEXNAME&gt; &nbsp; &nbsp; &nbsp; &nbsp;dump docids by index name</font></span></div>
<div><span style="line-height: 18px;"><font size="3">--dumphitlist &lt;INDEXNAME&gt; &lt;KEYWORD&gt; &nbsp; &nbsp; dump hits</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Options are:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-c, --config &lt;file&gt; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; use given config file instead of defaults</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">5.spelldump</font></b></span></div>
<div><span style="line-height: 24px; font-family: 'Times New Roman';"><font size="3"><font color="#ff0000"><b>spelldump 是Sphinx的一个辅助程序。<br><br>用于从ispell或者MySpell格式的字典文件中可用来辅助建立词形列表（wordforms）的内容——词的全部可能变化都预先构造好。</b></font><br></font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/coreseek/bin# ./spelldump&nbsp;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">spelldump, an ispell dictionary dumper</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Usage: spelldump [options] &lt;dictionary&gt; &lt;affix&gt; [result] [locale-name]</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Options:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-c &lt;file&gt; &nbsp; &nbsp; &nbsp; use case convertion defined in &lt;file&gt;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-m &lt;mode&gt; &nbsp; &nbsp; &nbsp; output (conflict resolution) mode:</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; default - try to guess the best way to resolve a conflict</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; last - choose last entry</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; debug - dump all mappings (with rules)</font></span></div>
<div><span style="line-height: 18px;"><font size="3">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; duplicates - dump duplicate mappings only (with rules)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">6.mmseg</font></b></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/mmseg/bin# ./mmseg&nbsp;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek COS(tm) MM Segment 1.0</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright By Coreseek.com All Right Reserved.</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Usage: ./mmseg &lt;option&gt; &lt;file&gt;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-u &lt;unidict&gt; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Unigram Dictionary</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-r &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Combine with -u, used a plain text build Unigram Dictionary, default Off</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-b &lt;Synonyms&gt; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Synonyms Dictionary</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-t &lt;thesaurus&gt; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Thesaurus Dictionary</font></span></div>
<div><span style="line-height: 18px;"><font size="3">-h &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;print this help and exit</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">7.经测试，当关键字是“海”的时候，通过命令行search及sphinxapi.php搜索时只有10条记录，用MySQL的like会有12条记录，<font color="#0000ff">这是跟中文分词有关，当搜"海"的时候，由于"航海"、"海外"是个词，因此搜索结果里面没有这2项，当分别用“航海”及“海外”搜索的时候，可以搜索到这2项。</font></font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/mmseg/etc# grep 航海 unigram.txt</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海学家 &nbsp; &nbsp; &nbsp; &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海 &nbsp; &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海家 &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海图 &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海业 &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海灯 &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">航海法 &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/usr/local/web/mmseg/etc# grep 海外 unigram.txt&nbsp;</font></span></div>
<div><span style="line-height: 18px;"><font size="3">匿迹海外 &nbsp; &nbsp; &nbsp; &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">海外 &nbsp; &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><font size="3">海外版 &nbsp;1</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><b><font size="3">停止coreseek服务</font></b></span></div>
<div><span style="line-height: 18px;"><font size="3">debian:/home/software/coreseek-3.2.13/testpack# /usr/local/web/coreseek/bin/searchd -c etc/csft_mysql.conf --stop</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Coreseek Fulltext 3.2 [ Sphinx 0.9.9-release (r2117)]</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Copyright (c) 2007-2010,</font></span></div>
<div><span style="line-height: 18px;"><font size="3">Beijing Choice Software Technologies Inc (http://www.coreseek.com)</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">using config file 'etc/csft_mysql.conf'...</font></span></div>
<div><span style="line-height: 18px;"><font size="3">stop: succesfully sent SIGTERM to pid 1937</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>
<div><span style="line-height: 18px;"><font size="3">Query() executes a query using the given query and index. index can be blank and will by-default search all indexes. You can limit the search to certain indexes separated by anything other than letters, numbers, underscores, and dashes.</font></span></div>
<div><span style="line-height: 18px;"><br><font size="3"></font></span></div>


<pre>
referer:http://iamcaihuafeng.blog.sohu.com/183218600.html
</pre>
