---
layout: post
title: "在python web.py中使用百度富文本编辑器 UEditor"
categories: 技术文章
tags: []
date: 2014-10-20 13:57:31
---



<p>UEditor官方没有支持python的版本，有人改了个python的<a target="_blank" href="http://www.ueditorbbs.com/forum.php?mod=viewthread&amp;tid=9425" target="_blank" style="font-family:arial,sans-serif; font-size:14px; line-height:1; white-space:nowrap; color:rgb(102,0,153)">django</a>版本，但是没找到web.py的。</p>
<p>于是参考php版本，实现了一下web.py集成UEditor，包含了文件上传，图片上传，视频上传，图片远程抓取，涂鸦等。</p>
<p>可能会有一些session之类的没有处理。</p>
<p>Demo代码可以在<a target="_blank" href="https://github.com/meizhitu/100programhomework/tree/master/100-25-literal-10-todo">https://github.com/meizhitu/100programhomework/tree/master/100-25-literal-10-todo</a> 查看</p>
<p>首先改ueditor.config.js，把原来指向php的链接改成web.py的</p>
<p><pre code_snippet_id="186254" snippet_file_name="blog_20140213_1_6055669"  name="code" class="javascript"> //图片上传配置区
        ,imageUrl:&quot;/ue_imageUp&quot;             //图片上传提交地址
        ,imagePath:&quot;&quot;                     //图片修正地址，引用了fixedImagePath,如有特殊需求，可自行配置
        //,imageFieldName:&quot;upfile&quot;                  //图片数据的key,若此处修改，需要在后台对应文件修改对应参数
        //,compressSide:0                           //等比压缩的基准，确定maxImageSideLength参数的参照对象。0为按照最长边，1为按照宽度，2为按照高度
        //,maxImageSideLength:900                   //上传图片最大允许的边长，超过会自动等比缩放,不缩放就设置一个比较大的值，更多设置在image.html中
        //,savePath: [ 'upload1', 'upload2', 'upload3' ]    //图片保存在服务器端的目录， 默认为空， 此时在上传图片时会向服务器请求保存图片的目录列表，
                                                            // 如果用户不希望发送请求， 则可以在这里设置与服务器端能够对应上的目录名称列表
                                                            //比如： savePath: [ 'upload1', 'upload2' ]

        //涂鸦图片配置区
        ,scrawlUrl:&quot;/ue_scrawlUp&quot;           //涂鸦上传地址
        ,scrawlPath:&quot;&quot;                            //图片修正地址，同imagePath

        //附件上传配置区
        ,fileUrl:&quot;/ue_fileUp&quot;               //附件上传提交地址
        ,filePath:&quot;&quot;                   //附件修正地址，同imagePath
        //,fileFieldName:&quot;upfile&quot;                    //附件提交的表单名，若此处修改，需要在后台对应文件修改对应参数

        //远程抓取配置区
        //,catchRemoteImageEnable:true               //是否开启远程图片抓取,默认开启
        ,catcherUrl:&quot;/ue_getRemoteImage&quot;   //处理远程图片抓取的地址
        ,catcherPath:&quot;&quot;                  //图片修正地址，同imagePath
        //,catchFieldName:&quot;upfile&quot;                   //提交到后台远程图片uri合集，若此处修改，需要在后台对应文件修改对应参数
        //,separater:'ue_separate_ue'               //提交至后台的远程图片地址字符串分隔符
        //,localDomain:[]                            //本地顶级域名，当开启远程图片抓取时，除此之外的所有其它域名下的图片都将被抓取到本地,默认不抓取127.0.0.1和localhost

        //图片在线管理配置区
        ,imageManagerUrl:&quot;/ue_imageManager&quot;       //图片在线管理的处理地址
        ,imageManagerPath:&quot;&quot;                                    //图片修正地址，同imagePath

        //屏幕截图配置区
        ,snapscreenHost: location.hostname                                 //屏幕截图的server端文件所在的网站地址或者ip，请不要加http://
        ,snapscreenServerUrl: &quot;/ue_imageUp&quot; //屏幕截图的server端保存程序，UEditor的范例代码为“URL +&quot;server/upload/php/snapImgUp.php&quot;”
        ,snapscreenPath: &quot;&quot;
        ,snapscreenServerPort: location.port                                   //屏幕截图的server端端口
        //,snapscreenImgAlign: ''                                //截图的图片默认的排版方式

        //word转存配置区
        ,wordImageUrl:&quot;/ue_imageUp&quot;             //word转存提交地址
        ,wordImagePath:&quot;&quot;                       //
        //,wordImageFieldName:&quot;upfile&quot;                     //word转存表单名若此处修改，需要在后台对应文件修改对应参数

        //视频上传配置区
        ,getMovieUrl:&quot;/ue_getMovie&quot;                   //视频数据获取地址
        ,videoUrl:&quot;/ue_fileUp&quot;               //附件上传提交地址
        ,videoPath:&quot;&quot;                   //附件修正地址，同imagePath
        //,videoFieldName:&quot;upfile&quot;                    //附件提交的表单名，若此处修改，需要在后台对应文件修改对应参数</pre>然后配置web.py的urls映射</p>
<p><pre code_snippet_id="186254" snippet_file_name="blog_20140213_2_2610106"  name="code" class="python">urls = (
    '/', 'Index',
    '/ue_imageUp', Ue_ImageUp,
    '/ue_fileUp', Ue_FileUp,
    '/ue_scrawlUp', Ue_ScrawlUp,
    '/ue_getRemoteImage', Ue_GetRemoteImage,
    '/ue_getMovie', Ue_GetMovie,
    '/ue_imageManager', Ue_ImageManager,
)</pre>最后实现这些web.py的class。</p>
<p><pre code_snippet_id="186254" snippet_file_name="blog_20140213_3_5750433"  name="code" class="python">#coding=utf-8
import base64
import uuid
import urllib2
import os

import web

ueconfig_dir = 'static/upload'
ueconfig_url = '/' + ueconfig_dir


def listImage(rootDir, retlist):
    for cfile in os.listdir(rootDir):
        path = os.path.join(rootDir, cfile)
        if os.path.isdir(path):
            listImage(path, retlist)
        else:
            if cfile.endswith('.gif') or cfile.endswith('.png') or cfile.endswith('.jpg') or cfile.endswith('.bmp'):
                retlist.append('/static/upload/' + cfile)


def saveUploadFile(fileName, content):
    fileName = fileName.replace('\\', '/') # replaces the windows-style slashes with linux ones.
    fout = open(ueconfig_dir + '/' + fileName, 'wb') # creates the file where the uploaded file should be stored
    fout.write(content) # writes the uploaded file to the newly created file.
    fout.close() # closes the file, upload complete.


class Ue_ImageUp:
    def GET(self):
        reqData = web.input()
        if 'fetch' in reqData:
            web.header('Content-Type', 'text/javascript')
            return 'updateSavePath([&quot;upload&quot;]);'
        web.header(&quot;Content-Type&quot;, &quot;text/html; charset=utf-8&quot;)
        return &quot;&quot;

    def POST(self):
        postData = web.input(upfile={}, pictitle=&quot;&quot;)
        web.debug(postData)
        fileObj = postData.upfile
        picTitle = postData.pictitle
        fileName = fileObj.filename
        newFileName = str(uuid.uuid1()) + &quot;.png&quot;
        saveUploadFile(newFileName, fileObj.file.read())
        return &quot;{'url':'&quot; + ueconfig_url + '/' + newFileName + &quot;','title':'&quot; + picTitle + &quot;','original':'&quot; + fileName + &quot;','state':'&quot; + &quot;SUCCESS&quot; + &quot;'}&quot;


class Ue_FileUp:
    def GET(self):
        web.header(&quot;Content-Type&quot;, &quot;text/html; charset=utf-8&quot;)
        return &quot;&quot;

    def POST(self):
        postData = web.input(upfile={})
        fileObj = postData.upfile
        fileName = postData.Filename
        ext = '.' + fileName.split('.')[-1]
        #web.py的static目录对中文文件名不支持，会404
        newFileName = str(uuid.uuid1()) + ext
        #fileNameFormat = postData.fileNameFormat
        saveUploadFile(newFileName, fileObj.file.read())
        return &quot;{'url':'&quot; + ueconfig_url + '/' + newFileName + &quot;','fileType':'&quot; + ext + &quot;','original':'&quot; + fileName + &quot;','state':'&quot; + &quot;SUCCESS&quot; + &quot;'}&quot;


class Ue_ScrawlUp:
    def GET(self):
        web.header(&quot;Content-Type&quot;, &quot;text/html; charset=utf-8&quot;)
        return &quot;&quot;

    def POST(self):
        reqData = web.input(upfile={})
        if 'action' in reqData:
            if reqData.action == 'tmpImg':
                #上传背景
                fileObj = reqData.upfile
                fileName = fileObj.filename
                saveUploadFile(fileName, fileObj.file.read())
                return &quot;&lt;script&gt;parent.ue_callback(&quot; + ueconfig_url + '/' + fileName + &quot;','&quot; + &quot;SUCCESS&quot; + &quot;')&lt;/script&gt;&quot;
        else:
            base64Content = reqData.content
            fileName = str(uuid.uuid1()) + '.png'
            saveUploadFile(fileName, base64.decodestring(base64Content))
            return &quot;{'url':'&quot; + ueconfig_url + '/' + fileName + &quot;',state:'&quot; + &quot;SUCCESS&quot; + &quot;'}&quot;


class Ue_GetRemoteImage:
    def GET(self):
        web.header(&quot;Content-Type&quot;, &quot;text/html; charset=utf-8&quot;)
        return &quot;&quot;

    def POST(self):
        postData = web.input()
        urls = postData.upfile
        #urls = urls.replace('&amp;','&amp;')
        urllist = urls.split(&quot;ue_separate_ue&quot;)
        fileType = [&quot;.gif&quot;, &quot;.png&quot;, &quot;.jpg&quot;, &quot;.jpeg&quot;, &quot;.bmp&quot;]
        outlist = []
        for fileurl in urllist:
            if not fileurl.startswith('http'):
                continue
            ext = &quot;.&quot; + fileurl.split('.')[-1]
            web.debug(ext + &quot;|&quot; + fileurl)
            if ext in fileType:
                fileName = str(uuid.uuid1()) + ext
                saveUploadFile(fileName, urllib2.urlopen(fileurl).read())
                outlist.append(ueconfig_url + &quot;/&quot; + fileName)
        outlist = &quot;ue_separate_ue&quot;.join(outlist)
        return &quot;{'url':'&quot; + outlist + &quot;','tip':'远程图片抓取成功！','srcUrl':'&quot; + urls + &quot;'}&quot;


class Ue_GetMovie:
    def POST(self):
        reqData = web.input()
        skey = reqData.searchKey
        vtype = reqData.videoType
        surl = 'http://api.tudou.com/v3/gw?method=item.search&amp;appKey=myKey&amp;format=json&amp;kw=' + skey + '&amp;pageNo=1&amp;pageSize=20&amp;channelId=' + vtype + '&amp;inDays=7&amp;media=v&amp;sort=s'
        htmlContent = urllib2.urlopen(surl).read()
        web.debug(htmlContent)
        return htmlContent


class Ue_ImageManager:
    def POST(self):
        reqData = web.input()
        if 'action' in reqData:
            if reqData.action == 'get':
                retfiles = []
                listImage(ueconfig_dir, retfiles)
                htmlContent = &quot;ue_separate_ue&quot;.join(retfiles)
                return htmlContent</pre><br>
<br>
<br>
<br>
</p>



<pre>
referer: http://blog.csdn.net/problc/article/details/19155007
</pre>
