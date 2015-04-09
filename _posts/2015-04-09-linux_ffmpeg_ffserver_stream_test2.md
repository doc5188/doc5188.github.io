---
layout: post
title: "ubuntu 12.04 ffserver流媒体测试-2"
categories: linux
tags: [ffmpeg, 流媒体]
date: 2015-04-09 15:22:29
---
ubuntu 12.04 ffserver流媒体测试-2

本次测试使用屏幕录制+声音的音视频流

* 1. 安装ffmpeg
{% highlight bash %}
doc5188.com$ sudo apt-get install ffmpeg
{% endhighlight %}

* 2. 配置文件test_ffserver.conf
{% highlight bash %}
Port 8090 
RTSPPort 5554
BindAddress 0.0.0.0 
MaxHTTPConnections 2000
MaxClients 1000
MaxBandwidth 10000000
CustomLog -
################################################################
<Feed feed1.ffm>

File /tmp/feed1.ffm
FileMaxSize 20000K 
ACL allow 127.0.0.1
Truncate
</Feed>
################################################################
<Stream test.rtp>

Feed feed1.ffm

Format rtp

VideoCodec mpeg2video  
#VideoFrameRate 0 
VideoBitRate 800k 
#VideoBufferSize 1000000
VideoSize 640x480 
#VideoSize 1280x720 
#AVPresetVideo default
#AVPresetVideo superfast
VideoBitRateTolerance 1000
VideoGopSize 12 
StartSendOnKey

VideoQMin 3
VideoQMax 31
AVOptionVideo flags +global_header
AVOptionVideo qmin 3 
AVOptionVideo qmax 31 
#AVOptionVideo me_range 4
AVOptionVideo qdiff 4

#MulticastAddress 224.124.0.1 
#MulticastPort 5000
#MulticastTTL 16
#NoLoop

#AudioCodec  mp2 #libmp3lame #libvorbis #libogg  #libfaac
AudioBitRate  128kb 
AudioChannels 2 
AudioSampleRate 44100 
AVOptionAudio flags +global_header
</Stream>
##################################################################
<Stream stat.html>

Format status
ACL allow 127.0.0.1 
ACL allow 192.168.0.0 192.168.255.255

</Stream>

<Redirect index.html>

URL http://www.ffmpeg.org/

</Redirect>

{% endhighlight %}


* 3. 启动ffserver
{% highlight bash %}
doc5188.com$ avserver -d -f ./test_ffserver.conf 
avserver version 0.8.15-4:0.8.15-0ubuntu0.12.04.1, Copyright (c) 2000-2014 the Libav developers
  built on Aug 10 2014 18:16:51 with gcc 4.6.3
Thu Apr  9 14:58:59 2015 AVserver started.

{% endhighlight %}

* 4. 屏幕录制并推送到ffsever

注意参数要与配置文件相一致

{% highlight bash %}
doc5188.com$ avconv -f x11grab -r 25 -s 640x800 -i :0.0 -f alsa -i pulse http://localhost:8090/feed1.ffm

avconv version 0.8.15-4:0.8.15-0ubuntu0.12.04.1, Copyright (c) 2000-2014 the Libav developers
  built on Aug 10 2014 18:16:51 with gcc 4.6.3
[x11grab @ 0xbef9c0] device: :0.0 -> display: :0.0 x: 0 y: 0 width: 640 height: 800
[x11grab @ 0xbef9c0] shared memory extension  found
[x11grab @ 0xbef9c0] Estimating duration from bitrate, this may be inaccurate
Input #0, x11grab, from ':0.0':
  Duration: N/A, start: 1428564089.710593, bitrate: 409600 kb/s
    Stream #0.0: Video: rawvideo, bgra, 640x800, 409600 kb/s, 25 tbr, 1000k tbn, 25 tbc
[alsa @ 0xbfb980] capture with some ALSA plugins, especially dsnoop, may hang.
[alsa @ 0xbfb980] Estimating duration from bitrate, this may be inaccurate
Input #1, alsa, from 'pulse':
  Duration: N/A, start: 1428564091.940379, bitrate: N/A
    Stream #1.0: Audio: pcm_s16le, 48000 Hz, 2 channels, s16, 1536 kb/s
Incompatible pixel format 'bgra' for codec 'mpeg1video', auto-selecting format 'yuv420p'
[buffer @ 0xbeb4e0] w:640 h:800 pixfmt:bgra
[avsink @ 0xbfdea0] auto-inserting filter 'auto-inserted scaler 0' between the filter 'src' and the filter 'out'
[scale @ 0xbfe5c0] w:640 h:800 fmt:bgra -> w:640 h:800 fmt:yuv420p flags:0x4
Output #0, ffm, to 'http://localhost:8090/feed1.ffm':
  Metadata:
    encoder         : Lavf53.21.1
    Stream #0.0: Video: mpeg1video, yuv420p, 640x800, q=2-31, 200 kb/s, 1000k tbn, 25 tbc
    Stream #0.1: Audio: mp2, 48000 Hz, 2 channels, s16, 128 kb/s
Stream mapping:
  Stream #0:0 -> #0:0 (rawvideo -> mpeg1video)
  Stream #1:0 -> #0:1 (pcm_s16le -> mp2)
Press ctrl-c to stop encoding
frame=  629 fps= 28 q=31.0 Lsize=    5916kB time=23.18 bitrate=2090.4kbits/s dup=83 drop=37 
{% endhighlight %}


* 5. ffplay播放视频流
{% highlight bash %}
doc5188.com$ ffplay rtsp://localhost:5554/test.rtp
{% endhighlight %}

{% highlight bash %}
{% endhighlight %}
