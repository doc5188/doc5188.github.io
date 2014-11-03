---
layout: post
title: "Python删除指定目录下的过期文件"
categories: python
tags: [python, linux删除过期文件]
date: 2014-11-03 16:29:22
---

服务器的文件每天不断增加,有很多文件碎片,需要定时清理,但还需要保留5天前的数据文件,用linux命令操作 
	
{% highlight bash %}
find /data/log -ctime +5 | xargs rm -f
{% endhighlight %}

会对系统造成很大压力,文件数会很多的说...

所以决定写个脚本,用crontab定时调用,来处理该需求

{% highlight bash %}
	
'''
Created on 2012-10-30
 
@author: max1984
'''
import os
import sys
import time
class DeleteLog:
 
 
    def __init__(self,fileName,days):
        self.fileName = fileName
        self.days = days
    def delete(self):
        if os.path.isfile(self.fileName):
            fd = open(self.fileName,'r')
            while 1:
                buffer = fd.readline()
                if not buffer : break
                if os.path.isfile(buffer):
                    os.remove(buffer)
            fd.close()
        elif os.path.isdir(self.fileName):
            for i in [os.sep.join([self.fileName,v]) for v in os.listdir(self.fileName)]:
                print i
                if os.path.isfile(i):
                    if self.compare_file_time(i):
                        os.remove(i)
                elif os.path.isdir(i):
                    self.fileName = i
                    self.delete()
    def compare_file_time(self,file):
        time_of_last_access = os.path.getatime(file)
        age_in_days = (time.time()-time_of_last_access)/(60*60*24)
        if age_in_days > self.days:
            return True
        return False
if __name__ == '__main__':
    if len(sys.argv) == 2:
        obj = DeleteLog(sys.argv[1],0)
        obj.delete()
    elif len(sys.argv) == 3:
        obj = DeleteLog(sys.argv[1],int(sys.argv[2]))
        obj.delete()
    else:
        print "usage: python %s listFileName|dirName [days]" % sys.argv[0]
        sys.exit(1)
{% endhighlight %}




<pre>
referer: http://my.oschina.net/max1984/blog/86132
</pre>
