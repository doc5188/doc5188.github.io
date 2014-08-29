---
layout: post
title: "ffmpeg添加水印"
categories: linux
tags: [linux, ffmpeg, watermark]
date: 2014-08-29 09:21:21
---

ffmpeg的configure选项：./configure --prefix=c:/mingw --disable-shared --enable-static --enable-filters --enable-gpl --enable-libx264 --enable-libxvid

完整命令行如下，ffmpeg -y -i input.flv  -vf “movie=watermark.png [wm];[in][wm] overlay=5:5 [out]” -strict experimental output.flv,其中的watermark要放在ffmpeg同目录下。


完整命令行如下，ffmpeg -y -i input.flv -acodec copy -b 300k -vfilters “movie=0:png:watermark.png [wm];[in][wm] overlay=5:5:1 [out]” output.flv
<pre>
-y 表示有同名的output.flv存在时不提示，直接覆盖
-i input.flv 表示要进行水印添加处理的视频
-acodec copy 表示保持音频不变
-b 300k 表示处理视频的比特率，用-vcodec copy时报错，使用其他工具获取到原始视频比特率后加到这里，保持比特率基本不变，不然默认为200k，视频有损。
output.flv 处理后的视频
-vfilters “…” 中间便是水印处理参数，重要的是overlay=后面的部分，第一个参数表示水印距离视频左边的距离，第二个参数表示水印距离视频上边的距离，第三个参数 为1，表示支持透明水印。使用透明的png图片进行视频编码后，成功获得带透明水印的视频，并且画质也比较好。
</pre>

Top left corner

ffmpeg –i inputvideo.avi -vf “movie=watermarklogo.png [watermark]; [in][watermark] overlay=10:10 [out]” outputvideo.flv

Top right corner

ffmpeg –i inputvideo.avi -vf “movie=watermarklogo.png [watermark]; [in][watermark] overlay=main_w-overlay_w-10:10 [out]” outputvideo.flv

Bottom left corner

ffmpeg –i inputvideo.avi -vf “movie=watermarklogo.png [watermark]; [in][watermark] overlay=10:main_h-overlay_h-10 [out]” outputvideo.flv

Bottom right corner

ffmpeg –i inputvideo.avi -vf “movie=watermarklogo.png [watermark]; [in][watermark] overlay=main_w-overlay_w-10:main_h-overlay_h-10 [out]” outputvideo.flv

有一篇-vfilters参数使用的文章可供参考，其中还例举了如何同时加入2个水印到画面不同位 置，http://www.techenigma.com/2010/05/ffmpeg-watermark-video-without- vhook-solution/。

ffmpeg -y -i sample.avi -vfilters “movie=0:png:watermark.png [wm];[in][wm] overlay=10:mainH-overlayH-10:1 [out]” -b 100k -ar 44100 -ab 24k -f flv -s 320×240 -acodec libmp3lame -ac 1 samplewithwater.flv

Which converted from AVI to FLV and added watermark. i‘ve included a couple of examples below for just adding the watermark.

Example 1 – insert transparent PNG watermark in bottom left corner of the video:
-vfilters “movie=0:png:logo.png [wm];[in][wm] overlay=10:mainH-overlayH-10:1 [out]”

Notice the last parameter to overlay “:1″ – this enables alpha blending.

Example 2 – insert 2 different transparent PNG watermarks (second watermark on bottom right corner):
-vfilters “movie=0:png:logo.png [wm];movie=0:png:logo2.png [awm];[in][wm] overlay=10:mainH-overlayH-10:1 [int];[int][awm] overlay=mainW-overlayW-10:mainH-overlayH-10:1 [out]”

You could chain and add more overlays this way but the efficiency of such approach is yet to be tested.

待解问题：H264/x264编码的flv经过上述ffmpeg加水印处理后变成了H263编码，即普通的flv编码，可能处理参数加的不对或是不全，或者就应该对普通flv和H264/x264编码的视频分别处理，后续再进一步测试想办法解决。

refer to：http://tuzwu.iteye.com/blog/1025337

refer to : http://www.ffmpeg.org/libavfilter.html#overlay-1

refer to : http://www.idude.net/index.php/how-to-watermark-a-video-using-ffmpeg/

