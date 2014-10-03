---
layout: post
title: "Compiling libtorrent-rasterbar and qBittorrent on CentOS 6.5 x64"
categories: linux
tags: [linux, qbittorrent, libtorrent-rasterbar]
date: 2014-10-03 21:10:38
---

Recently I finally found the proper uTorrent (wine/Server) replacement for Linux (preferably headless) systems – qBittorrent.

Unfortunately there seems to be no repository out there providing qBittorrent for CentOS 6, so I had to compile it from source – not the easiest task I have to admit.

First off, you’ll need to install some requirements. Since I’m running this on a development box I had most of the compiler tools and libraries already installed, but one thing I did need to install was the boost library (and it’s dev counterpart):
yum install boost boost-devel

If you don’t have the compilers installed, you’ll also need to install them:
yum groupinstall "Development Tools"
or
yum install make gcc gcc-c++ kernel-devel

I used this forum post and initially tried exactly the versions listed there, but that failed (with a very weird compilation error in libtorrent).

So I gave it another try but with the (almost latest) versions available at the time of writing this: libtorrent-rasterbar-0.16.12 and qbittorrent-3.1.3. The absolute latest libtorrent-rasterbar 0.6.13 had an issue not seeing the boost library installed.

 

Compiling libtorrent-rasterbar
Download, configure and compile libtorrent-rasterbar:


{% highlight bash %}
# cd /usr/src
# wget http://libtorrent.googlecode.com/files/libtorrent-rasterbar-0.16.12.tar.gz
# tar xf libtorrent-rasterbar-0.16.12.tar.gz
# cd /usr/src/libtorrent-rasterbar-0.16.12
# ./configure --disable-debug --prefix=/usr --with-boost-libdir=/usr/lib64
# ln -s /usr/lib/pkgconfig/libtorrent-rasterbar.pc /usr/lib64/pkgconfig/libtorrent-rasterbar.pc
{% endhighlight %}
The last command above is very important for x64 system, as it creates the correct symlink for applications looking at the 32bit version of the libraries; without it compiling qbittorrent will fail on x64 systems.
 

Compiling qBittorrent
Then download, configure, compile and install qbittorrent:

{% highlight bash %}
# cd /usr/src/
# wget http://downloads.sourceforge.net/qbittorrent/qbittorrent-3.1.3.tar.gz?use_mirror=osdn
# tar xf qbittorrent-3.1.3.tar.gz
# cd qbittorrent-3.1.3
# ./configure
# /usr/bin/gmake
# make install
{% endhighlight %}
Use ./configure --disable-gui instead to build qbittorrent-nox (CLI only version suitable for headless servers). Then run qbittorrent-nox –webui-port=X to configure the web UI port (defaults to 8080). The rest of the configuration can be done via the web UI (default username is admin and password is adminadmin).
 

Running bittorrent-nox as a service
I found a service script here which works perfectly on CentOS:


<pre>
#!/bin/sh
#
# chkconfig: - 80 20
# description: qBittorrent headless torrent server
# processname: qbittorrent-nox
#
# Source function library.
. /etc/init.d/functions
 
QBT_USER="root"
QBT_LOG="/var/log/qbittorrent.log"
 
prog=qbittorrent-nox
RETVAL=0
 
start() {
        if [ -x /etc/rc.d/init.d/functions ]; then
                daemon --user $QBT_USER $prog
        else
                su - $QBT_USER -c "$prog" > /var/log/qbittorrent.log &
        fi
    echo -n $"Starting $prog: "
        RETVAL=$?
        [ $RETVAL = 0 ] && success || failure
    echo
        return $RETVAL
}
 
stop() {
    echo -n $"Stopping $prog: "
    killall qbittorrent-nox
    success
        echo
}
 
# See how we were called.
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart|reload)
        stop
        sleep 2
        start
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|reload}"
        exit 1
esac
 
exit $RETVAL
#
# end
</pre>

Simply save it as /etc/init.d/qbittorrentd, then chmod +x it and you’re good to go
{% highlight bash %}
# service qbittorrentd start
{% endhighlight %}
 

Remember to use (and periodically update) a P2P IP blocklist.

This forum post helped me figure out that libtorrent-rasterbar wouldn’t compile on my 64bit system without adding –with-boost-libdir=/usr/lib64.

<pre>
referfer: http://www.zedt.eu/tech/linux/compiling-libtorrent-rasterbar-and-qbittorrent-on-centos-6-5-x64/
</pre>
