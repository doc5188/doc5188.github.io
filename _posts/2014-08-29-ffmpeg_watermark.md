---
layout: post
title: "ffmpeg加文字水印并控制水印显示时间或显示周期"
categories: linux
tags: [linux, ffmpeg, watermark]
date: 2014-08-29 09:19:21
---

<pre>
#以下脚本保存成.sh文件运行，不会出现中文乱码问题 网上查到用enable关键字控制，实际是draw
#加水印 水印位置由x,y,w,h来控制
#ffmpeg编译时需--enable-libfreetype才能用此功能
#!/bin/bash
ffmpeg -y -i jiushu.mpg -acodec libfaac -b:a 30k -ar 44100 -r 15 -ac 2 -s 480x272 -vcodec libx264 -refs 2 -x264opts keyint=150:min-keyint=15 -vprofile baseline -level 20 -b:v 200k -vf "drawtext=fontfile=/mnt/hgfs/zm/simhei.ttf: text='来源：迅雷':x=100:y=x/dar:fontsize=24:fontcolor=yellow@0.5:shadowy=2"  drawtext.mp4     
       
#加水印，显示10秒
#!/bin/bash
ffmpeg -y -i jiushu.mpg -acodec libfaac -b:a 30k -ar 44100 -r 15 -ac 2 -s 480x272 -vcodec libx264 -refs 2 -x264opts keyint=150:min-keyint=15 -vprofile baseline -level 20 -b:v 200k -vf "drawtext=fontfile=/mnt/hgfs/zm/simhei.ttf: text='来源：迅雷':x=100:y=x/dar:draw='if(gt(n,0),lt(n,250))':fontsize=24:fontcolor=yellow@0.5:shadowy=2"  drawtext.mp4   
       
#加水印，每3秒显示1秒
#!/bin/bash
ffmpeg -y -i jiushu.mpg -acodec libfaac -b:a 30k -ar 44100 -r 15 -ac 2 -s 480x272 -vcodec libx264 -refs 2 -x264opts keyint=150:min-keyint=15 -vprofile baseline -level 20 -b:v 200k -vf "drawtext=fontfile=/mnt/hgfs/zm/simhei.ttf: text='来源：迅雷':x=w-100:y=100:draw=lt(mod(t\,3)\,1):fontsize=24:fontcolor=yellow@0.5:shadowy=2"  drawtext.mp4

</pre>
