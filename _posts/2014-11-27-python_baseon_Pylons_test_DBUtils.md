---
layout: post
title: "在基于Pylons的服务器上测试使用DBUtils前后的性能"
categories: python
tags: [pylons, DBUtils]
date: 2014-11-27 13:01:32
---

<p><h1>在基于Pylons的服务器上测试使用DBUtils前后的性能</h1>
<p><p><a name="id1"></a>目录</p>
<ul>
<li><a href="#id2" name="id11">1   测试环境</a></li>
<li><a href="#id3" name="id12">2   10线程并发</a></li>
<li><a href="#id4" name="id13">3   50线程并发</a></li>
<li><a href="#id5" name="id14">4   远程10线程并发</a></li>
<li><a href="#id6" name="id15">5   远程50线程并发</a></li>
<li><a href="#id7" name="id16">6   干扰因素</a></li>
<li><a href="#id8" name="id17">7   单线程测试</a></li>
<li><a href="#id9" name="id18">8   单线程测试</a></li>
<li><a href="#id10" name="id19">9   结论</a></li>
</ul>
<p>为了测试使用DBUtils实现的数据库连接池的性能，在Pylons写了一个测试服务，并将服务器架设在lab2服务器上，使用apache  ab进行服务器压力测试。</p>
<p><h1><a href="#id11" name="id2">1   测试环境</a></h1>
<p>lab2服务器，MySQL 4.1.20，Pylons 0.9.4.1，apache ab 2.0.59。</p>
<p>为了确保测试的可靠性，每次测试之前都重启服务器。</p>
<p>在Pylons上假设的应用有3个URL用于测试，分别如下：</p>
<table border="1">
<thead valign="bottom">
<tr>
<th>URL</th>
<th>说明</th>
</tr>
<tr>
<td>/testdb/test1</td>
<td>不使用连接池，每次访问都建立对数据库的连接</td>
</tr>
<tr>
<td>/testdb/test2</td>
<td>使用DBUtils.PersistentDB连接池，线程专用连接</td>
</tr>
<tr>
<td>/testdb/test3</td>
<td>使用DBUtils.PooledDB连接池，线程间共享连接</td>
</tr>
</table>
<p>测试代码如下:</p>
<pre>from helloworld.lib.base import *
import time
import random
import MySQLdb
import DBUtils.PersistentDB
import DBUtils.PooledDB

conn_kwargs={'host':'192.168.1.239','user':'ro','passwd':'','db':'test','port':3306}
sql="""SELECT * FROM test_table WHERE id=%d"""
persist=DBUtils.PersistentDB.PersistentDB(dbapi=MySQLdb,maxusage=1000,**conn_kwargs)
pooled=DBUtils.PooledDB.PooledDB(dbapi=MySQLdb,maxusage=1000,**conn_kwargs)

def query(conn):
    cur=conn.cursor()
    cur.execute(sql%(random.randint(1,1000)))
    data=cur.fetchall()
    cur.close()
    return data

class TestdbController(BaseController):
    def index(self):
        return Response('index')

    def test1(self):
        conn=MySQLdb.connect(**conn_kwargs)
        data=query(conn)
        conn.close()
        return Response(str(data))

    def test2(self):
        conn=persist.connection()
        data=query(conn)
        conn.close()
        return Response(str(data))

    def test3(self):
        conn=pooled.connection()
        data=query(conn)
        conn.close()
        return Response(str(data))</pre>
<p><h1><a href="#id12" name="id3">2   10线程并发</a></h1>
<p>一共10000次测试，测试所用命令如下:</p>
<pre>./ab -n 10000 -c 10 http://192.168.1.239:5000/testdb/test*</pre>
<p>测试结果如下：</p>
<table border="1">
<thead valign="bottom">
<tr>
<th>测试目标</th>
<th>总时间</th>
<th>请求处理速度</th>
<th>平均处理时间</th>
<th>错误率</th>
<th>100%</th>
<th>99%</th>
<th>90%</th>
<th>50%</th>
</tr>
<tr>
<td>/test1</td>
<td>32.764</td>
<td>305.22</td>
<td>32.764 ms</td>
<td>10.32%</td>
<td>776</td>
<td>237</td>
<td>40</td>
<td>29</td>
</tr>
<tr>
<td>/test2</td>
<td>27.895</td>
<td>358.49</td>
<td>27.895 ms</td>
<td>10.00%</td>
<td>3032</td>
<td>222</td>
<td>31</td>
<td>22</td>
</tr>
<tr>
<td>/test3</td>
<td>29.513</td>
<td>338.83</td>
<td>29.513 ms</td>
<td>10.46%</td>
<td>3037</td>
<td>58</td>
<td>36</td>
<td>27</td>
</tr>
</table>
<p><h1><a href="#id13" name="id4">3   50线程并发</a></h1>
<p>一共10000次测试，测试所用命令如下:</p>
<pre>./ab -n 10000 -c 50 http://192.168.1.239:5000/testdb/test*</pre>
<p>测试结果如下：</p>
<table border="1">
<thead valign="bottom">
<tr>
<th>测试目标</th>
<th>总时间</th>
<th>请求处理速度</th>
<th>平均处理时间</th>
<th>错误率</th>
<th>100%</th>
<th>99%</th>
<th>90%</th>
<th>50%</th>
</tr>
<tr>
<td>/test1</td>
<td>32.786</td>
<td>305.00</td>
<td>163.932 ms</td>
<td>9.48%</td>
<td>21031</td>
<td>3048</td>
<td>49</td>
<td>31</td>
</tr>
<tr>
<td>/test2</td>
<td>27.884</td>
<td>358.62</td>
<td>139.424 ms</td>
<td>9.65%</td>
<td>9227</td>
<td>3032</td>
<td>33</td>
<td>22</td>
</tr>
<tr>
<td>/test3</td>
<td>29.256</td>
<td>341.81</td>
<td>146.281 ms</td>
<td>9.88%</td>
<td>3654</td>
<td>328</td>
<td>151</td>
<td>136</td>
</tr>
</table>
<p><h1><a href="#id14" name="id5">4   远程10线程并发</a></h1>
<p>一共10000次测试，测试所用命令如下:</p>
<pre>./ab -n 10000 -c 10 http://192.168.1.241:5000/testdb/test*</pre>
<p>测试结果如下：</p>
<table border="1">
<thead valign="bottom">
<tr>
<th>测试目标</th>
<th>总时间</th>
<th>请求处理速度</th>
<th>平均处理时间</th>
<th>错误率</th>
<th>100%</th>
<th>99%</th>
<th>90%</th>
<th>50%</th>
</tr>
<tr>
<td>/test1</td>
<td>24.891</td>
<td>401.75</td>
<td>24.891 ms</td>
<td>9.07%</td>
<td>3035</td>
<td>44</td>
<td>31</td>
<td>22</td>
</tr>
<tr>
<td>/test2</td>
<td>21.652</td>
<td>461.85</td>
<td>21.652 ms</td>
<td>9.86%</td>
<td>256</td>
<td>59</td>
<td>26</td>
<td>19</td>
</tr>
<tr>
<td>/test3</td>
<td>23.952</td>
<td>432.99</td>
<td>23.095 ms</td>
<td>9.59%</td>
<td>239</td>
<td>38</td>
<td>28</td>
<td>22</td>
</tr>
</table>
<p><h1><a href="#id15" name="id6">5   远程50线程并发</a></h1>
<p>一共10000次测试，测试命令如下:</p>
<pre>./ab -n 10000 -c 50 http://192.168.1.241:5000/testdb/test*</pre>
<p>测试结果如下：</p>
<table border="1">
<thead valign="bottom">
<tr>
<th>测试目标</th>
<th>总时间</th>
<th>请求处理速度</th>
<th>平均处理时间</th>
<th>错误率</th>
<th>100%</th>
<th>99%</th>
<th>90%</th>
<th>50%</th>
</tr>
<tr>
<td>/test1</td>
<td>24.915</td>
<td>401.36</td>
<td>124.575 ms</td>
<td>9.82%</td>
<td>9280</td>
<td>3033</td>
<td>53</td>
<td>27</td>
</tr>
<tr>
<td>/test2</td>
<td>21.521</td>
<td>464.66</td>
<td>107.607 ms</td>
<td>9.47%</td>
<td>9621</td>
<td>3022</td>
<td>32</td>
<td>20</td>
</tr>
<tr>
<td>/test3</td>
<td>22.808</td>
<td>438.45</td>
<td>114.038 ms</td>
<td>9.11%</td>
<td>9107</td>
<td>145</td>
<td>114</td>
<td>95</td>
</tr>
</table>
<p><h1><a href="#id16" name="id7">6   干扰因素</a></h1>
<p>测试过程中发现，MySQL服务器的同时并发连接数一直没有超过10，所以在进行50线程并发操作时可能会出现一些干扰。</p>
<p><h1><a href="#id17" name="id8">7   单线程测试</a></h1>
<p>使用代码如下:</p>
<pre>import time
import random
import MySQLdb
import DBUtils.PersistentDB
import DBUtils.PooledDB

conn_kwargs={'host':'192.168.1.239','user':'ro','passwd':'','db':'test','port':3306}
sql="""SELECT * FROM test_table WHERE id=%d"""
persist=DBUtils.PersistentDB.PersistentDB(dbapi=MySQLdb,maxusage=1000,**conn_kwargs)
pooled=DBUtils.PooledDB.PooledDB(dbapi=MySQLdb,maxusage=1000,**conn_kwargs)

def query(conn):
    cur=conn.cursor()
    cur.execute(sql%(random.randint(1,1000)))
    data=cur.fetchall()
    cur.close()
    return data

def print_now():
    print time.strftime("%H:%M:%S")
    return

def test1(times):
    print_now()
    for i in range(0,times):
        conn=MySQLdb.connect(**conn_kwargs)
        query(conn)
        conn.close()
    print_now()
    return

def test2(times):
    print_now()
    for i in range(0,times):
        conn=persist.connection()
        query(conn)
        conn.close()
    print_now()
    return

def test3(times):
    print_now()
    for i in range(0,times):
        conn=pooled.connection()
        query(conn)
        conn.close()
    print_now()
    return</pre>
<p><h1><a href="#id18" name="id9">8   单线程测试</a></h1>
<p>执行10000次查询，进入Python交互模式，调用各个函数并传递执行次数，每次执行过后重启MySQL服务器:</p>
<pre># python -i ttss.py
&gt;&gt;&gt; test1(10000)
18:59:30
18:59:40
&gt;&gt;&gt; test2(10000)
19:00:16
19:00:19
&gt;&gt;&gt; test3(10000)
19:00:46
19:00:49</pre>
<p>可见查询次数太少，以致难以精确测定时间，所以执行100000次查询，过程如下:</p>
<pre># python -i ttss.py
&gt;&gt;&gt; test1(100000)
19:01:57
_mysql_exceptions.OperationalError: (2003, "Can't connect to MySQL server on '192.168.1.239' (99)")</pre>
<p>连续两次都出现异常，之后改为30000也是如此。出现这个异常之后数据库服务器不经过重启就无法再使用了。经过测试发生这种连接异常之后，还是可以使用mysql客户端登录本机的MySQL服务器的。所以改为20000次查询，过程如下:</p>
<pre># python -i ttss.py
&gt;&gt;&gt; test1(20000)
19:06:47
19:07:07
&gt;&gt;&gt; test2(20000)
19:28:23
19:28:28
&gt;&gt;&gt; test3(20000)
19:29:27
19:29:34</pre>
<p>测试远程连接MySQL服务器:</p>
<pre># python -i ttss.py
&gt;&gt;&gt; test1(10000)
20:25:23
20:25:57
&gt;&gt;&gt; test2(10000)
20:27:18
20:27:26
&gt;&gt;&gt; test3(10000)
20:27:46
20:27:56</pre>
<p><h1><a href="#id19" name="id10">9   结论</a></h1>
<p>总体上来看，使用了DBUtils之后数据库的访问性能有了很大的提高。</p>



<pre>
referer:http://gashero.yeax.com/?p=25
</pre>
