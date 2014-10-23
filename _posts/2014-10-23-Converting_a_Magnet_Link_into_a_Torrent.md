---
layout: post
title: "Converting a Magnet Link into a Torrent"
categories: python
tags: [magnet]
date: 2014-10-23 14:53:35
---
<p>For some reason, my version of the rtorrent client on ubuntu does not open magnet files.  So, I wanted to see if there was a way to create torrent files from magnet files.  I couldn’t find a good example, so I wrote my own.</p>
<p><strong>This will convert a magnet link into a .torrent file:</strong></p>
<p>First, make sure your system has Python and the Python Library:</p>

<div class="wp_syntax"><table><tbody><tr><td class="code"><pre class="bash" style="font-family: monospace;"><span style="color: rgb(194, 12, 185); font-weight: bold;">sudo</span> <span style="color: rgb(194, 12, 185); font-weight: bold;">apt-get install</span> python-libtorrent</pre></td></tr></tbody></table></div>

<p>Then, you can run the following code by calling this command:</p>

<div class="wp_syntax"><table><tbody><tr><td class="code"><pre class="bash" style="font-family: monospace;">python Magnet2Torrent.py</pre></td></tr></tbody></table></div>

<p>File Magnet2Torrent.py:</p>

<div class="wp_syntax"><table><tbody><tr><td class="code"><pre class="python" style="font-family: monospace;"><span style="color: rgb(72, 61, 139);">'''
Created on Apr 19, 2012
@author: dan
'''</span>
&nbsp;
<span style="color: rgb(255, 119, 0); font-weight: bold;">if</span> __name__ <span style="color: rgb(102, 204, 102);">==</span> <span style="color: rgb(72, 61, 139);">'__main__'</span>:
    <span style="color: rgb(255, 119, 0); font-weight: bold;">import</span> libtorrent <span style="color: rgb(255, 119, 0); font-weight: bold;">as</span> lt
    <span style="color: rgb(255, 119, 0); font-weight: bold;">import</span> <span style="color: rgb(220, 20, 60);">time</span>
&nbsp;
    TorrentFilePath <span style="color: rgb(102, 204, 102);">=</span> <span style="color: rgb(72, 61, 139);">"/home/dan/torrentfiles/"</span> + <span style="color: rgb(0, 128, 0);">str</span><span style="color: black;">(</span><span style="color: rgb(220, 20, 60);">time</span>.<span style="color: rgb(220, 20, 60);">time</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span> + <span style="color: rgb(72, 61, 139);">"/"</span>
    TorrentFilePath2 <span style="color: rgb(102, 204, 102);">=</span> <span style="color: rgb(72, 61, 139);">"/home/dan/torrentfiles/"</span> + <span style="color: rgb(0, 128, 0);">str</span><span style="color: black;">(</span><span style="color: rgb(220, 20, 60);">time</span>.<span style="color: rgb(220, 20, 60);">time</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span> + <span style="color: rgb(72, 61, 139);">"/"</span> + <span style="color: rgb(0, 128, 0);">str</span><span style="color: black;">(</span><span style="color: rgb(220, 20, 60);">time</span>.<span style="color: rgb(220, 20, 60);">time</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span> + <span style="color: rgb(72, 61, 139);">".torrent"</span>
    ses <span style="color: rgb(102, 204, 102);">=</span> lt.<span style="color: black;">session</span><span style="color: black;">(</span><span style="color: black;">)</span>
    <span style="color: rgb(128, 128, 128); font-style: italic;">#ses.listen_on(6881, 6891)</span>
    params <span style="color: rgb(102, 204, 102);">=</span> <span style="color: black;">{</span>
        <span style="color: rgb(72, 61, 139);">'save_path'</span>: TorrentFilePath<span style="color: rgb(102, 204, 102);">,</span>
        <span style="color: rgb(72, 61, 139);">'duplicate_is_error'</span>: <span style="color: rgb(0, 128, 0);">True</span><span style="color: black;">}</span>
    link <span style="color: rgb(102, 204, 102);">=</span> <span style="color: rgb(72, 61, 139);">"magnet:?xt=urn:btih:599e3fb0433505f27d35efbe398225869a2a89a9&amp;dn=ubuntu-10.04.4-server-i386.iso&amp;tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&amp;tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&amp;tr=udp%3A%2F%2Ftracker.ccc.de%3A80"</span>
    handle <span style="color: rgb(102, 204, 102);">=</span> lt.<span style="color: black;">add_magnet_uri</span><span style="color: black;">(</span>ses<span style="color: rgb(102, 204, 102);">,</span> link<span style="color: rgb(102, 204, 102);">,</span> params<span style="color: black;">)</span>
<span style="color: rgb(128, 128, 128); font-style: italic;">#    ses.start_dht()</span>
    <span style="color: rgb(255, 119, 0); font-weight: bold;">print</span> <span style="color: rgb(72, 61, 139);">'saving torrent file here : '</span> + TorrentFilePath2 + <span style="color: rgb(72, 61, 139);">" ..."</span>
    <span style="color: rgb(255, 119, 0); font-weight: bold;">while</span> <span style="color: black;">(</span><span style="color: rgb(255, 119, 0); font-weight: bold;">not</span> handle.<span style="color: black;">has_metadata</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span>:
        <span style="color: rgb(220, 20, 60);">time</span>.<span style="color: black;">sleep</span><span style="color: black;">(</span><span style="color: rgb(255, 69, 0);">.1</span><span style="color: black;">)</span>
&nbsp;
    torinfo <span style="color: rgb(102, 204, 102);">=</span> handle.<span style="color: black;">get_torrent_info</span><span style="color: black;">(</span><span style="color: black;">)</span>
&nbsp;
    fs <span style="color: rgb(102, 204, 102);">=</span> lt.<span style="color: black;">file_storage</span><span style="color: black;">(</span><span style="color: black;">)</span>
    <span style="color: rgb(255, 119, 0); font-weight: bold;">for</span> <span style="color: rgb(0, 128, 0);">file</span> <span style="color: rgb(255, 119, 0); font-weight: bold;">in</span> torinfo.<span style="color: black;">files</span><span style="color: black;">(</span><span style="color: black;">)</span>:
        fs.<span style="color: black;">add_file</span><span style="color: black;">(</span><span style="color: rgb(0, 128, 0);">file</span><span style="color: black;">)</span>
    torfile <span style="color: rgb(102, 204, 102);">=</span> lt.<span style="color: black;">create_torrent</span><span style="color: black;">(</span>fs<span style="color: black;">)</span>
    torfile.<span style="color: black;">set_comment</span><span style="color: black;">(</span>torinfo.<span style="color: black;">comment</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span>
    torfile.<span style="color: black;">set_creator</span><span style="color: black;">(</span>torinfo.<span style="color: black;">creator</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span>
&nbsp;
    f <span style="color: rgb(102, 204, 102);">=</span> <span style="color: rgb(0, 128, 0);">open</span><span style="color: black;">(</span>TorrentFilePath2 + <span style="color: rgb(72, 61, 139);">"torrentfile.torrent"</span><span style="color: rgb(102, 204, 102);">,</span> <span style="color: rgb(72, 61, 139);">"wb"</span><span style="color: black;">)</span>
    f.<span style="color: black;">write</span><span style="color: black;">(</span>lt.<span style="color: black;">bencode</span><span style="color: black;">(</span>torfile.<span style="color: black;">generate</span><span style="color: black;">(</span><span style="color: black;">)</span><span style="color: black;">)</span><span style="color: black;">)</span>
    f.<span style="color: black;">close</span><span style="color: black;">(</span><span style="color: black;">)</span>
    <span style="color: rgb(255, 119, 0); font-weight: bold;">print</span> <span style="color: rgb(72, 61, 139);">'saved and closing...'</span>
&nbsp;
<span style="color: rgb(128, 128, 128); font-style: italic;">#Uncomment to Download the Torrent:</span>
<span style="color: rgb(128, 128, 128); font-style: italic;">#    print 'starting torrent download...'</span>
&nbsp;
<span style="color: rgb(128, 128, 128); font-style: italic;">#    while (handle.status().state != lt.torrent_status.seeding):</span>
<span style="color: rgb(128, 128, 128); font-style: italic;">#        s = handle.status()</span>
<span style="color: rgb(128, 128, 128); font-style: italic;">#        time.sleep(55)</span>
<span style="color: rgb(128, 128, 128); font-style: italic;">#        print 'downloading...'</span></pre></td></tr></tbody></table></div>

<p>This will create a folder inside of ‘/home/dan/torrentfiles/’ with a structure like:</p>
<pre lang="bash">/home/dan/torrentfiles/545465456.12/545465456.12.torrent
<pre><p>I added this to GitHub if you want to Fork it.<br>
<a href="https://github.com/danfolkes/Magnet2Torrent">https://github.com/danfolkes/Magnet2Torrent</a></p>
<p>ENJOY!</p>
