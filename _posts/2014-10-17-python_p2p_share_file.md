---
layout: post
title: "python实现一个P2P文件发布"
categories: 技术文章
tags: []
date: 2014-10-17 15:20:15
---


<p>考虑到我手上的服务器逐渐的增多，有时候需要大规模的部署同一个文件，例如因为方便使用systemtap这个工具定位问题，需要把手上几百台服务器同时安装kernel-debuginfo这个包，原有的方式采用一个源服务器，采用rsync或者scp之类的文件传输方式只能做到一个点往下分发这个文件，这个时候下发的速度就会比较的慢，基于以上原因，我写了一个基于bt协议传输文件的小工具，实际测试，传输到10个机房，70多台机器传输一个240M的这个内核文件，到所有的机器，源采用限速2m/s的上传速度，测试的结果大概只要140s，就可以全部传输完毕，这个效率是非常之高，如果不限速的情况下速度会更快，下面把这个程序开源出来。</p>
<pre class="brush: python">
#!/usr/bin/env python

import libtorrent as lt
import sys
import os
import time
from optparse import OptionParser
import socket
import struct
import fcntl

def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                            ifname[:15]))[20:24])
def ip2long(ip):
    return reduce(lambda a,b:(a<<8)+b,[int(i) for i in ip.split('.')])


def get_wan_ip_address():
    interfaces = set(['eth0', 'eth1', 'eth2', 'eth3', 'em1', 'em2', 'em3', 'em4'])
    ip = ''
    for i in interfaces:
        try:
            ip = get_interface_ip(i)
            if (ip2long(ip) < ip2long('10.0.0.0') or ip2long(ip) > ip2long('10.255.255.255')) \
                and (ip2long(ip) < ip2long('172.16.0.0') or ip2long(ip) > ip2long('172.33.255.255')) \
                and (ip2long(ip) < ip2long('192.168.0.0') or ip2long(ip) > ip2long('192.168.255.255')):
                return ip
        except:
            pass

    return ip

def make_torrent(path, save):
    fs = lt.file_storage()
    lt.add_files(fs, path)
    if fs.num_files() == 0:
        print 'no files added'
        sys.exit(1)

    input = os.path.abspath(path)
    basename = os.path.basename(path)
    t = lt.create_torrent(fs, 0, 4 * 1024 * 1024)

    t.add_tracker("http://10.0.1.5:8760/announce")
    t.set_creator('libtorrent %s' % lt.version)

    lt.set_piece_hashes(t, os.path.split(input)[0], lambda x: sys.stderr.write('.'))
    sys.stderr.write('\n')

    save = os.path.dirname(input)
    save = "%s/%s.torrent" % (save, basename)
    f=open(save, "wb")
    f.write(lt.bencode(t.generate()))
    f.close()
    print "the bt torrent file is store at %s" % save


def dl_status(handle):
    while not (handle.is_seed()):
        s = handle.status()

        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\ractive_time: %d, %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d, seeds: %d) %s' % \
                (s.active_time, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, s.num_seeds, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(1)
def seed_status(handle, seedtime=100):
    seedtime = int(seedtime)
    if seedtime < 100:
        seedtime = 100
    while seedtime > 0:
        seedtime -= 1
        s = handle.status()

        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\rseed_time: %d, %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d, seeds: %d) %s' % \
                (s.active_time, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, s.num_seeds, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(1)

def remove_torrents(torrent, session):
    session.remove_torrent(torrent)

def read_alerts(session):
    alert = session.pop_alert()
    while alert:
        #print alert, alert.message()
        alert = session.pop_alert()

def download(torrent, path, upload_rate_limit=0, seedtime=100):
    try:
        session = lt.session()
        session.set_alert_queue_size_limit(1024 * 1024)

        sts = lt.session_settings()
        sts.ssl_listen = False
        sts.user_agent = "Thunder deploy system"
        sts.tracker_completion_timeout = 5
        sts.tracker_receive_timeout = 5
        sts.stop_tracker_timeout = 5
        sts.active_downloads = -1
        sts.active_seeds = -1
        sts.active_limit = -1
        sts.auto_scrape_min_interval = 5
        sts.udp_tracker_token_expiry = 120
        sts.min_announce_interval = 1
        sts.inactivity_timeout = 60
        sts.connection_speed = 10
        sts.allow_multiple_connections_per_ip = True
        sts.max_out_request_queue = 128
        sts.request_queue_size = 3

        sts.use_read_cache = False
        session.set_settings(sts)

        session.set_alert_mask(lt.alert.category_t.tracker_notification | lt.alert.category_t.status_notification)
        session.set_alert_mask(lt.alert.category_t.status_notification)

        ipaddr = get_wan_ip_address()
        #print ipaddr
        if ipaddr == "":
            session.listen_on(6881, 6881)
        else:
            session.listen_on(6881, 6881, ipaddr)

        limit = int(upload_rate_limit)
        if limit>=100:
            session.set_upload_rate_limit(limit*1024)
            session.set_local_upload_rate_limit(limit*1024)
        print session.upload_rate_limit()
        torrent_info = lt.torrent_info(torrent)
        add_params = {
            'save_path': path,
            'storage_mode': lt.storage_mode_t.storage_mode_sparse,
            'paused': False,
            'auto_managed': True,
            'ti': torrent_info,
        }

        handle = session.add_torrent(add_params)

        read_alerts(session)
        st = time.time()
        dl_status(handle)
        et = time.time() - st
        print '\nall file download in %.2f\nstart to seeding\n' % et
        sys.stdout.write('\n')
        handle.super_seeding()
        seed_status(handle, seedtime)

        remove_torrents(handle, session)
        assert len(session.get_torrents()) == 0

    finally:
        print 'download finished'

if __name__ == '__main__':
    usage = "usage: %prog [options] \n \
      %prog -d -f <torrent file> -s <file save path>\n \
      or \n \
      %prog -m -p <file or dir> -s <torrent save path>\n"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--download", dest="download",
            help="start to download file", action="store_false", default=True)
    parser.add_option("-f", "--file", dest="file",
            help="torrent file")
    parser.add_option("-u", "--upload", dest="upload",
            help="set upload rate limit, default is not limit", default=0)
    parser.add_option("-t", "--time", dest="time",
            help="set seed time, default is 100s", default=100)
    parser.add_option("-p", "--path", dest="path",
            help="to make torrent with this path")
    parser.add_option("-m", "--make", dest="make",
            help="make torrent", action="store_false", default=True)
    parser.add_option("-s", "--save", dest="save",
            help="file save path, default is store to ./", default="./")
    (options, args) = parser.parse_args()
    #download(sys.argv[1])
    if len(sys.argv) != 6 and len(sys.argv) != 4 and len(sys.argv) != 8 and len(sys.argv) != 10:
        parser.print_help()
        sys.exit()
    if options.download == False and options.file !="":
        download(options.file, options.save, options.upload, options.time)
    elif options.make == False and options.path != "":
        make_torrent(options.path, options.save)
</pre>
<p>准备环境：<br />
需要在所有的os上面安装一个libtorrent的库，下载地址：</p>
<p>http://code.google.com/p/libtorrent/downloads/list</p>
<p>记得编译的时候带上./configure &#8211;enable-python-binding，然后mak，make install，进入binding目录，make，make install就<br />
可以运行这个小的工具<br />
当然大规模部署不可能采用每一台都去编译安装的方式，只要把编译出来的libtorrent.so libtorrent-rasterbar.so.7的文件跟bt.py这个文件放到同一个目录，另外写一个shell脚本</p>
<pre class="brush: python">
lib=`dirname $0`
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$lib
python bt.py -d -f <种子文件> -s <文件保存路径> -t <做种时间> -u <限制上传速度>
</pre>
<p>使用方法：<br />
首先在源服务器上面生成种子文件</p>
<pre class="brush: python">
python bt.py -m -p <要发布的文件或者文件夹> -s <种子保存地址>
</pre>
<p>发布文件<br />
在源服务器上面，执行</p>
<pre class="brush: python">
python bt.py -d -f <种子文件> -s <文件保存路径> -t <做种时间> -u <限制上传速度>
</pre>
<p>其中做种时间默认设置的是100s，上传速度默认不限制，限制的速度单位是KB</p>
<p>下面的机器，直接可以</p>
<pre class="brush: python">
python bt.py -d -f <种子文件> -s <文件保存路径> -t <做种时间>
</pre>
<p>只要有一台机器完成了，就自动作为种子，在下载的过程中也会上传，任何一台机器都可以作为源服务器，当然了这里面还有中心的tracker服务器，脚本当中，我搭建了一个tracker源服务器，放到10.0.1.5端口是8760上面，当然大家也可以采用opentracker这个软件自己搭建一个tracker服务器，修改其中的源代码对应部分，另外考虑到发布都是私有文件，代码当作已经禁止了dht，如果还想更安全，就自己搭建一个私有的tracker server，具体搭建方法就使用一下搜索引擎，查找一下搭建的方法！</p>
<p>目前基本做到可以使用，后续考虑更简单一点，采用磁力链接的方式，这样就可以做到不用每台都要拷贝一个种子文件，采用一个单独的命令行就可以发布整个文件</p>
					
<pre>
referer: http://blog.netzhou.net/?p=252
</pre>
