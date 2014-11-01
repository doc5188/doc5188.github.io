---
layout: post
title: "Mongodb数据导出工具mongoexport和导入工具mongoimport介绍"
categories: 数据库
tags: [mongoexport, mongoimport]
date: 2014-11-01 17:42:32
---

一、导出工具mongoexport

Mongodb中的mongoexport工具可以把一个collection导出成JSON格式或CSV格式的文件。可以通过参数指定导出的数据项，也可以根据指定的条件导出数据。mongoexport具体用法如下所示：

{% highlight bash %}
[root@localhost mongodb]# ./bin/mongoexport --help  
Export MongoDB data to CSV, TSV or JSON files.  
  
options:  
  --help                    produce help message  
  -v [ --verbose ]          be more verbose (include multiple times for more   
                            verbosity e.g. -vvvvv)  
  --version                 print the program's version and exit  
  -h [ --host ] arg         mongo host to connect to ( <set name>/s1,s2 for   
                            sets)  
  --port arg                server port. Can also use --host hostname:port  
  --ipv6                    enable IPv6 support (disabled by default)  
  -u [ --username ] arg     username  
  -p [ --password ] arg     password  
  --dbpath arg              directly access mongod database files in the given   
                            path, instead of connecting to a mongod  server -   
                            needs to lock the data directory, so cannot be used  
                            if a mongod is currently accessing the same path  
  --directoryperdb          if dbpath specified, each db is in a separate   
                            directory  
  --journal                 enable journaling  
  -d [ --db ] arg           database to use  
  -c [ --collection ] arg   collection to use (some commands)  
  -f [ --fields ] arg       comma separated list of field names e.g. -f   
                            name,age  
  --fieldFile arg           file with fields names - 1 per line  
  -q [ --query ] arg        query filter, as a JSON string  
  --csv                     export to csv instead of json  
  -o [ --out ] arg          output file; if not specified, stdout is used  
  --jsonArray               output to a json array rather than one object per   
                            line  
  -k [ --slaveOk ] arg (=1) use secondaries for export if available, default   
                            true  
参数说明：
-h:指明数据库宿主机的IP
-u:指明数据库的用户名
-p:指明数据库的密码
-d:指明数据库的名字
-c:指明collection的名字
-f:指明要导出那些列
-o:指明到要导出的文件名
-q:指明导出数据的过滤条件
{% endhighlight %}
 
实例：test库中存在着一个students集合，集合中数据如下：
{% highlight bash %}
> db.students.find()  
{ "_id" : ObjectId("5031143350f2481577ea81e5"), "classid" : 1, "age" : 20, "name" : "kobe" }  
{ "_id" : ObjectId("5031144a50f2481577ea81e6"), "classid" : 1, "age" : 23, "name" : "nash" }  
{ "_id" : ObjectId("5031145a50f2481577ea81e7"), "classid" : 2, "age" : 18, "name" : "james" }  
{ "_id" : ObjectId("5031146a50f2481577ea81e8"), "classid" : 2, "age" : 19, "name" : "wade" }  
{ "_id" : ObjectId("5031147450f2481577ea81e9"), "classid" : 2, "age" : 19, "name" : "bosh" }  
{ "_id" : ObjectId("5031148650f2481577ea81ea"), "classid" : 2, "age" : 25, "name" : "allen" }  
{ "_id" : ObjectId("5031149b50f2481577ea81eb"), "classid" : 1, "age" : 19, "name" : "howard" }  
{ "_id" : ObjectId("503114a750f2481577ea81ec"), "classid" : 1, "age" : 22, "name" : "paul" }  
{ "_id" : ObjectId("503114cd50f2481577ea81ed"), "classid" : 2, "age" : 24, "name" : "shane" }  
{% endhighlight %}

由上可以看出文档中存在着3个字段：classid、age、name

1.直接导出数据到文件中
{% highlight bash %}
[root@localhost mongodb]# ./bin/mongoexport -d test -c students -o students.dat  
connected to: 127.0.0.1  
exported 9 records  
{% endhighlight %}
命令执行完后使用ll命令查看，发现目录下生成了一个students.dat的文件
{% highlight bash %}
-rw-r--r-- 1 root root   869 Aug 21 00:05 students.dat  
{% endhighlight %}
查看该文件信息，具体信息如下：
{% highlight bash %}
[root@localhost mongodb]# cat students.dat   
{ "_id" : { "$oid" : "5031143350f2481577ea81e5" }, "classid" : 1, "age" : 20, "name" : "kobe" }  
{ "_id" : { "$oid" : "5031144a50f2481577ea81e6" }, "classid" : 1, "age" : 23, "name" : "nash" }  
{ "_id" : { "$oid" : "5031145a50f2481577ea81e7" }, "classid" : 2, "age" : 18, "name" : "james" }  
{ "_id" : { "$oid" : "5031146a50f2481577ea81e8" }, "classid" : 2, "age" : 19, "name" : "wade" }  
{ "_id" : { "$oid" : "5031147450f2481577ea81e9" }, "classid" : 2, "age" : 19, "name" : "bosh" }  
{ "_id" : { "$oid" : "5031148650f2481577ea81ea" }, "classid" : 2, "age" : 25, "name" : "allen" }  
{ "_id" : { "$oid" : "5031149b50f2481577ea81eb" }, "classid" : 1, "age" : 19, "name" : "howard" }  
{ "_id" : { "$oid" : "503114a750f2481577ea81ec" }, "classid" : 1, "age" : 22, "name" : "paul" }  
{ "_id" : { "$oid" : "503114cd50f2481577ea81ed" }, "classid" : 2, "age" : 24, "name" : "shane" }  
参数说明：
-d:指明使用的库，本例中为test
-c:指明要导出的集合，本例中为students
-o:指明要导出的文件名，本例中为students.dat
{% endhighlight %}
从上面的结果可以看出，我们在导出数据时没有显示指定导出样式 ，默认导出了JSON格式的数据。如果我们需要导出CSV格式的数据，则需要使用--csv参数，具体如下所示：
{% highlight bash %}
[root@localhost mongodb]# ./bin/mongoexport -d test -c students --csv -f classid,name,age -o students_csv.dat  
connected to: 127.0.0.1  
exported 9 records  
[root@localhost mongodb]# cat students_csv.dat   
classid,name,age  
1.0,"kobe",20.0  
1.0,"nash",23.0  
2.0,"james",18.0  
2.0,"wade",19.0  
2.0,"bosh",19.0  
2.0,"allen",25.0  
1.0,"howard",19.0  
1.0,"paul",22.0  
2.0,"shane",24.0  
[root@localhost mongodb]#   
参数说明：
-csv：指明要导出为csv格式
-f：指明需要导出classid、name、age这3列的数据
{% endhighlight %}
由上面结果可以看出，mongoexport成功地将数据根据csv格式导出到了students_csv.dat文件中。
 
* 二、导入工具mongoimport

Mongodb中的mongoimport工具可以把一个特定格式文件中的内容导入到指定的collection中。该工具可以导入JSON格式数据，也可以导入CSV格式数据。具体使用如下所示：
{% highlight bash %}
[root@localhost mongodb]# ./bin/mongoimport --help  
options:  
  --help                  produce help message  
  -v [ --verbose ]        be more verbose (include multiple times for more   
                          verbosity e.g. -vvvvv)  
  --version               print the program's version and exit  
  -h [ --host ] arg       mongo host to connect to ( <set name>/s1,s2 for sets)  
  --port arg              server port. Can also use --host hostname:port  
  --ipv6                  enable IPv6 support (disabled by default)  
  -u [ --username ] arg   username  
  -p [ --password ] arg   password  
  --dbpath arg            directly access mongod database files in the given   
                          path, instead of connecting to a mongod  server -   
                          needs to lock the data directory, so cannot be used   
                          if a mongod is currently accessing the same path  
  --directoryperdb        if dbpath specified, each db is in a separate   
                          directory  
  --journal               enable journaling  
  -d [ --db ] arg         database to use  
  -c [ --collection ] arg collection to use (some commands)  
  -f [ --fields ] arg     comma separated list of field names e.g. -f name,age  
  --fieldFile arg         file with fields names - 1 per line  
  --ignoreBlanks          if given, empty fields in csv and tsv will be ignored  
  --type arg              type of file to import.  default: json (json,csv,tsv)  
  --file arg              file to import from; if not specified stdin is used  
  --drop                  drop collection first   
  --headerline            CSV,TSV only - use first line as headers  
  --upsert                insert or update objects that already exist  
  --upsertFields arg      comma-separated fields for the query part of the   
                          upsert. You should make sure this is indexed  
  --stopOnError           stop importing at first error rather than continuing  
  --jsonArray             load a json array, not one item per line. Currently   
                          limited to 4MB.  
参数说明：
-h:指明数据库宿主机的IP
-u:指明数据库的用户名
-p:指明数据库的密码
-d:指明数据库的名字
-c:指明collection的名字
-f:指明要导入那些列
{% endhighlight %}
 
示例：先删除students中的数据，并验证
{% highlight bash %}
> db.students.remove()  
> db.students.find()  
>   
{% endhighlight %}
然后再导入上面导出的students.dat文件中的内容
{% highlight bash %}
[root@localhost mongodb]# ./bin/mongoimport -d test -c students students.dat   
connected to: 127.0.0.1  
imported 9 objects  
[root@localhost mongodb]#   
参数说明：
-d:指明数据库名，本例中为test
-c:指明collection名，本例中为students
students.dat：导入的文件名
{% endhighlight %}
查询students集合中的数据
{% highlight bash %}
> db.students.find()  
{ "_id" : ObjectId("5031143350f2481577ea81e5"), "classid" : 1, "age" : 20, "name" : "kobe" }  
{ "_id" : ObjectId("5031144a50f2481577ea81e6"), "classid" : 1, "age" : 23, "name" : "nash" }  
{ "_id" : ObjectId("5031145a50f2481577ea81e7"), "classid" : 2, "age" : 18, "name" : "james" }  
{ "_id" : ObjectId("5031146a50f2481577ea81e8"), "classid" : 2, "age" : 19, "name" : "wade" }  
{ "_id" : ObjectId("5031147450f2481577ea81e9"), "classid" : 2, "age" : 19, "name" : "bosh" }  
{ "_id" : ObjectId("5031148650f2481577ea81ea"), "classid" : 2, "age" : 25, "name" : "allen" }  
{ "_id" : ObjectId("5031149b50f2481577ea81eb"), "classid" : 1, "age" : 19, "name" : "howard" }  
{ "_id" : ObjectId("503114a750f2481577ea81ec"), "classid" : 1, "age" : 22, "name" : "paul" }  
{ "_id" : ObjectId("503114cd50f2481577ea81ed"), "classid" : 2, "age" : 24, "name" : "shane" }  
>   
{% endhighlight %}
证明数据导入成功

上面演示的是导入JSON格式的文件中的内容，如果要导入CSV格式文件中的内容，则需要通过--type参数指定导入格式，具体如下所示：

先删除数据

{% highlight bash %}
> db.students.remove()  
> db.students.find()  
>   
{% endhighlight %}
再导入之前导出的students_csv.dat文件
{% highlight bash %}
[root@localhost mongodb]# ./bin/mongoimport -d test -c students --type csv --headerline --file students_csv.dat   
connected to: 127.0.0.1  
imported 10 objects  
[root@localhost mongodb]#   
参数说明：
-type:指明要导入的文件格式
-headerline:指明第一行是列名，不需要导入
-file：指明要导入的文件
{% endhighlight %}
查询students集合，验证导入是否成功：
{% highlight bash %}
> db.students.find()  
{ "_id" : ObjectId("503266029355c632cd118ad8"), "classid" : 1, "name" : "kobe", "age" : 20 }  
{ "_id" : ObjectId("503266029355c632cd118ad9"), "classid" : 1, "name" : "nash", "age" : 23 }  
{ "_id" : ObjectId("503266029355c632cd118ada"), "classid" : 2, "name" : "james", "age" : 18 }  
{ "_id" : ObjectId("503266029355c632cd118adb"), "classid" : 2, "name" : "wade", "age" : 19 }  
{ "_id" : ObjectId("503266029355c632cd118adc"), "classid" : 2, "name" : "bosh", "age" : 19 }  
{ "_id" : ObjectId("503266029355c632cd118add"), "classid" : 2, "name" : "allen", "age" : 25 }  
{ "_id" : ObjectId("503266029355c632cd118ade"), "classid" : 1, "name" : "howard", "age" : 19 }  
{ "_id" : ObjectId("503266029355c632cd118adf"), "classid" : 1, "name" : "paul", "age" : 22 }  
{ "_id" : ObjectId("503266029355c632cd118ae0"), "classid" : 2, "name" : "shane", "age" : 24 }  
>   
{% endhighlight %}
说明已经导入成功



<pre>
referer: http://chenzhou123520.iteye.com/blog/1641319
</pre>
