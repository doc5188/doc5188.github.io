---
layout: post
title: "python,时间加减,时间计算,时间格式化,时间提取汇总"
categories: python
tags: [python]
date: 2014-11-17 23:41:35
---

<FONT style="BACKGROUND-COLOR: #cccccc" color=#20124d size=4>我要解决的问题是,发现某个文件超过30分钟时间不被更新,则报警<BR><BR>&gt;&gt;&gt; t1=[2010,11,9,19,20,30] #2010年11月9日 19:30:30<BR>&gt;&gt;&gt; last_time=datetime.datetime(t1[0],t1[1],t1[2].t1[3],t1[4],t1[5]) #上次更新时间<BR>&gt;&gt;&gt; now_time = datetime.datetime.now() #当前时间<BR>&gt;&gt;&gt; #以下是亮点<BR>&gt;&gt;&gt; mkt_last = time.mktime(last_time.timetuple()) <BR>&gt;&gt;&gt; mkt_now = time.mktime(now_time.timetuple())<BR>&gt;&gt;&gt; delt_time = (mkt_now-mkt_last)/60&nbsp;&nbsp; #转成分钟<BR>&gt;&gt;&gt; if (delt_time -30) &gt; 0 :<BR>&gt;&gt;&gt;&nbsp;&nbsp;&nbsp;&nbsp; print "超过30分钟没有更新啦!"</FONT>

<P><FONT style="BACKGROUND-COLOR: #cccccc" color=#20124d size=4>这是我在解决问题时,发现的其他一些有用的函数,呵呵,留着备用吧<BR><BR>计算两个时间的差，如两个时间相差几天，几小时等<BR><STRONG>1.计算两个日期相差天数的计算</STRONG> <BR>&gt;&gt;&gt; import datetime<BR>&gt;&gt;&gt; d1 = datetime.datetime(2005, 2, 16)<BR>&gt;&gt;&gt; d2 = datetime.datetime(2004, 12, 31)<BR>&gt;&gt;&gt; (d1 - d2).days<BR>输出结果:47<BR><BR><STRONG>2.计算两个时间相差的秒数</STRONG><BR>&gt;&gt;&gt; import datetime<BR>&gt;&gt;&gt; starttime = datetime.datetime.now()<BR>&gt;&gt;&gt; #long running<BR>&gt;&gt;&gt; endtime = datetime.datetime.now()<BR>&gt;&gt;&gt; print (endtime - starttime).seconds</FONT></P>

<P><FONT style="BACKGROUND-COLOR: #cccccc" color=#20124d size=4>3.计算当前时间向后10小时的时间<BR>&gt;&gt;&gt; d1 = datetime.datetime.now()<BR>&gt;&gt;&gt; d3 = d1 + datetime.timedelta(hours=10)<BR>&gt;&gt;&gt; d3.ctime()</FONT></P>

<P><BR><FONT style="BACKGROUND-COLOR: #cccccc" color=#20124d size=4>对时间的操作,其本上常用的类有：datetime和timedelta两个。它们之间可以相互加减。每个类都有一些方法和属</FONT><FONT style="BACKGROUND-COLOR: #cccccc" color=#20124d size=4>性可以查看具体的值，如datetime可以查看：天数(day)，小时数(hour)，星期几(weekday())等;timedelta可以查</FONT><FONT style="BACKGROUND-COLOR: #cccccc" color=#20124d size=4>看：天数(days)，秒数(seconds)等。<BR><BR>4.日期的操作必须使用time或datetime库 <BR>import time <BR>&gt;&gt;&gt; s="2006-1-2" <BR>&gt;&gt;&gt; time.strptime(s,"%Y-%m-%d) <BR>这是将字符串格式的日期及时间转成日期对象 <BR>转义符对应意义如下 <BR>%a 本地简化星期名称 <BR>%A 本地完整星期名称 <BR>%b 本地简化的月份名称 <BR>%B 本地完整的月份名称 <BR>%c 本地相应的日期表示和时间表示 <BR>%d 月内中的一天（0-31） <BR>%H 24小时制小时数（0-23） <BR>%I 12小时制小时数（01-12） <BR>%j 年内的一天（001-366） <BR>%m 月份（01-12） <BR>%M 分钟数（00=59） <BR>%p 本地A.M.或P.M.的等价符 <BR>%S 秒（00-59） <BR>%U 一年中的星期数（00-53）星期天为星期的开始 <BR>%w 星期（0-6），星期天为星期的开始 <BR>%W 一年中的星期数（00-53）星期一为星期的开始 <BR>%x 本地相应的日期表示 <BR>%X 本地相应的时间表示 <BR>%y 两位数的年份表示（00-99） <BR>%Y 四位数的年份表示（000-9999） <BR>%Z 当前时区的名称 <BR>%% %号本身</FONT></P>

