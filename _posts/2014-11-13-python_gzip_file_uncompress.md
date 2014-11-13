---
layout: post
title: "python gzip解压"
categories: python 
tags: [python, gzip]
date: 2014-11-13 15:44:22
---


<pre>
    #!/usr/bin/env python    
    # encoding=utf-8    
        
    import StringIO, gzip   
      
    #解压gzip  
    def gzdecode(data) :  
        compressedstream = StringIO.StringIO(data)  
        gziper = gzip.GzipFile(fileobj=compressedstream)    
        data2 = gziper.read()   # 读取解压缩后数据   
        return data2   

</pre>
