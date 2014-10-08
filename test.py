#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: test.py
# Author: Gavin Tao
# mail: gavin.tao17@gmail.com
# Created Time: Wed 08 Oct 2014 11:09:16 AM CST
#########################################################################

# coding=utf-8  
import urllib2  
import string  
import urllib  
import cookielib
import re  
  
def my_urlencode(str):  
    reprStr = repr(str).replace(r'\x','%')  
    return reprStr[1:-1]  
      
  
def clearTag(text):  
    p = re.compile(u'<[^>]+>')  
    retval = p.sub("",text)  
    return retval  
  
  
def get_res_list_and_next_page_url(target_url):  
    #获得一个cookieJar实例  
    cj = cookielib.CookieJar()  
    #cookieJar作为参数，获得一个opener的实例  
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));  
    #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。  
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]  
    urllib2.install_opener(opener);  
    res = urllib2.urlopen(target_url)  
    html=res.read()  
    content = unicode(html, 'utf-8','ignore')  
    content = html

    #fp = open('/tmp/11.html', 'w')
    #fp.write(html)
    #fp.close()
  
    #获取res_list  
    pattern = re.compile(r'<div[^>]*?class="result c-container.*?>[\s\S]*?</div>')#大部分情况  
    resList_1 = pattern.findall(html)  
    pattern = re.compile(r'<div class="result-op c-container.*?>[\s\S]*?</div>.*?</div>')#少数情况  
    resList_2 = pattern.findall(html)  
    res_lists = resList_1 + resList_2 #合并搜索结果  
      
    #获取next_page_url  
    pattern = re.compile(r'<p id="page".*?>[\s\S]*</p>')  
    m = pattern.search(html)  
    if m:  
        t = m.group()  
        pattern = re.compile(r'<a href=".*?"')  
        mm = pattern.findall(t)  
        tt = mm[len(mm)-1]  
        tt = tt[9:len(tt)-1]  
        next_page_url = 'http://www.baidu.com'+tt  
    return res_lists,next_page_url  
  
def get_title(div_data):  
    pattern = re.compile(r'<a[\s\S]*?>.*?<em>.*?</em>')  
    m = pattern.search(div_data)  
    if m:  
        #title = clearTag(m.group(0).decode('utf-8').encode('gb18030'))  
        title = clearTag(m.group(0))  
              
    pattern = re.compile(r'</em>.*?</a>') #加?号是最小匹配  
    m=pattern.search(div_data)  
    if m:  
        #title += clearTag(m.group(0).decode('utf-8').encode('gb18030'))  
        title += clearTag(m.group(0))
    return title.strip()  
  
def get_url(div_data):  
    pattern = re.compile(r'mu="[\s\S]*?"')  
    m = pattern.search(div_data)  
    url = ""
    if m: #mu模式  
        url = m.group(0)  
        url = url.replace("mu=","")   
        url = url.replace(r'"''"',"") 
    else: #href模式 
        pattern = re.findall(r'href[\s\S]*?=[\s\S]*?"([\s\S]*?)"', div_data)
        if pattern: url = pattern[0]
    if not url: print m;print div_data
    return url  
  
def get_abstract(div_data):  
    pattern = re.compile(r'<div class="c-abstract">[\s\S]*?</div>')  
    m = pattern.search(div_data)  
    if m: #普通模式  
        abstract=clearTag(m.group(0))  
    else: #奇怪模式1，貌似是外国网站  
        pattern = re.compile(r'<div class="op_url_size".*?</div>')  
        mm = pattern.search(div_data)  
        if mm:  
            abstract=clearTag(mm.group(0))  
        else:#奇怪模式2，貌似是百科等自己的，反正和别人用的不是一个div class~  
            pattern = re.compile(r'<div class="c-span18 c-span-last">[\s\S]*?</p>')  
            mmm = pattern.search(div_data)#这里用match和search结果不一致  
            #match是从字符串的起点开始做匹配，而search是从字符串做任意匹配。                     
            if mmm:  
                abstract=clearTag(mmm.group(0))  
            else:  
                abstract="No description!"  
                #print i  
    return abstract.strip()  
  
  
if __name__ == "__main__":  
    #初始化  
    keyword = raw_input('Please enter the keyword you want to search:')  
    #url = 'http://www.baidu.com/s?wd=' + my_urlencode(keyword) + '&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391'  
    url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduhome_pg&bar=&wd=python&rsv_spt=1&rsv_enter=0&inputT=1100'
    target_urls = []  
    target_urls.append(url)  
  
    page_num = 1 #想多少页就多少页。。只要你有。。  
  
    for cnt in range(page_num):  
        print "===============第",cnt+1,"页==============="  
  
        if target_urls[cnt] == "END_FLAG":  
            break  
          
        res_lists,next_page_url = get_res_list_and_next_page_url(target_urls[cnt])  
  
        if next_page_url: #考虑没有“下一页”的情况  
            target_urls.append(next_page_url)  
        else:  
            target_urls.append("END_FLAG")  
              
        titles = []  
        urls = []  
        abstracts = []  
  
        for index in range(len(res_lists)):  
            print "第",index+1,"个搜索结果..."  
            #print res_lists[index]
            #continue
              
            #获取title  
            title = get_title(res_lists[index])  
            titles.append(title)  
            print "标题：",title  
  
            #获取URL  
            url = get_url(res_lists[index])  
            urls.append(url)  
            print "URL：",url  
              
            #获取描述  
            abstract = get_abstract(res_lists[index])  
            abstracts.append(abstract)  
            print "概要：",abstract  
  
              
            print "\r\n\r\n"  
