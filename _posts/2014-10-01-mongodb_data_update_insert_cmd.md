---
layout: post
title: "Mongodb数据更新命令、操作符"
categories: 数据库
tags: [mongodb]
date: 2014-10-02 01:46:27
---

<pre>
一、Mongodb数据更新命令
Mongodb更新有两个命令：update、save。
1.1update命令
update命令格式：
db.collection.update(criteria,objNew,upsert,multi)
参数说明：
criteria：查询条件
objNew：update对象和一些更新操作符
upsert：如果不存在update的记录，是否插入objNew这个新的文档，true为插入，默认为false，不插入。
multi：默认是false，只更新找到的第一条记录。如果为true，把按条件查询出来的记录全部更新。
 
示例：

> db.classes.insert({"name":"c1","count":30})  
> db.classes.insert({"name":"c2","count":30})  
> db.classes.find()  
{ "_id" : ObjectId("5030f3a3721e16c4ab180cd9"), "name" : "c1", "count" : 30 }  
{ "_id" : ObjectId("5030f3ab721e16c4ab180cda"), "name" : "c2", "count" : 30 }  
>   
示例1：把count大于20的class name修改为c3

> db.classes.update({"count":{$gt:20}},{$set:{"name":"c3"}})  
> db.classes.find()  
{ "_id" : ObjectId("5030f3a3721e16c4ab180cd9"), "name" : "c3", "count" : 30 }  
{ "_id" : ObjectId("5030f3ab721e16c4ab180cda"), "name" : "c2", "count" : 30 }  
>   
由于没有指定upsert和multi的值，所以全部默认为false，由结果可以看出，只修改了第一条符合条件的记录。
示例2：把count大于20的class name修改为c4，设置multi为true

> db.classes.update({"count":{$gt:20}},{$set:{"name":"c4"}},false,true)  
> db.classes.find()  
{ "_id" : ObjectId("5030f3a3721e16c4ab180cd9"), "name" : "c4", "count" : 30 }  
{ "_id" : ObjectId("5030f3ab721e16c4ab180cda"), "name" : "c4", "count" : 30 }  
>   
由于指定了multi为true，所以对两条符合条件的记录都进行了更新。
示例3： 把count大于50的class name修改为c5，设置upsert为true

> db.classes.update({"count":{$gt:50}},{$set:{"name":"c5"}},true,false)  
> db.classes.find()  
{ "_id" : ObjectId("5030f3a3721e16c4ab180cd9"), "name" : "c4", "count" : 30 }  
{ "_id" : ObjectId("5030f3ab721e16c4ab180cda"), "name" : "c4", "count" : 30 }  
{ "_id" : ObjectId("5030f589ce8fa8884e6cd441"), "name" : "c5" }  
>   
在集合中没有count大于50的记录，但是由于指定了upsert为true，如果找不到则会插入一条新记录。
1.2save命令
Mongodb另一个更新命令是save，格式如下：
db.collection.save(obj)
obj代表需要更新的对象，如果集合内部已经存在一个和obj相同的"_id"的记录，Mongodb会把obj对象替换集合内已存在的记录，如果不存在，则会插入obj对象。
这条命令比较简单，示例就省略了。
 
二、数据更新操作符
1.$inc
用法：{$inc:{field:value}}
作用：对一个数字字段的某个field增加value
示例：将name为chenzhou的学生的age增加5

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou", "age" : 22 }  
#查询结果显示年龄为22  
> db.students.update({name:"chenzhou"},{$inc:{age:5}})  
#执行修改，把age增加5  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou", "age" : 27 }  
>   
#查询结果显示年龄为27，修改成功  
2.$set
用法：{$set:{field:value}}
作用：把文档中某个字段field的值设为value
示例： 把chenzhou的年龄设为23岁

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou", "age" : 27 }  
> db.students.update({name:"chenzhou"},{$set:{age:23}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou", "age" : 23 }  
>   
从结果可以看到，更新后年龄从27变成了23
3.$unset
用法：{$unset:{field:1}}
作用：删除某个字段field
示例： 将chenzhou的年龄字段删除

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou", "age" : 23 }  
> db.students.update({name:"chenzhou"},{$unset:{age:1}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou" }  
>   
4.$push
用法：{$push:{field:value}}
作用：把value追加到field里。注：field只能是数组类型，如果field不存在，会自动插入一个数组类型
示例：给chenzhou添加别名"michael"

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$push:{"ailas":"Michael"}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "Michael" ], "name" : "chenzhou" }  
>   
由结果可以看到，记录中追加了一个数组类型字段alias，且字段有一个为"Michael"的值
5.pushAll
用法：{$pushAll:{field:value_array}}
作用：用法同$push一样，只是$pushAll可以一次追加多个值到一个数组字段内。
示例：给chenzhou追加别名A1，A2
 

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "Michael" ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$pushAll:{"ailas":["A1","A2"]}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "Michael", "A1", "A2" ], "name" : "chenzhou" }  
>   
6.$addToSet
用法：{$addToSet:{field:value}}
作用：加一个值到数组内，而且只有当这个值在数组中不存在时才增加。
示例：往chenzhou的别名字段里添加两个别名A3、A4 

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "Michael", "A1", "A2" ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$addToSet:{"ailas":["A3","A4"]}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "Michael", "A1", "A2", [ "A3", "A4" ] ], "name" : "chenzhou" }  
>   
由结果可以看出，更新后ailas字段里多了一个对象，这个对象里包含2个数据，分别是A3、A4
7.$pop
用法：删除数组内第一个值：{$pop:{field:-1}}、删除数组内最后一个值：{$pop:{field:1}}
作用：用于删除数组内的一个值
示例： 删除chenzhou记录中alias字段中第一个别名

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "Michael", "A1", "A2", [ "A3", "A4" ] ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$pop:{"ailas":-1}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "A1", "A2", [ "A3", "A4" ] ], "name" : "chenzhou" }  
>   
由结果可以看书，第一个别名Michael已经被删除了。
我们再使用命令删除最后一个别名：

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "A1", "A2", [ "A3", "A4" ] ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$pop:{"ailas":1}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "A1", "A2" ], "name" : "chenzhou" }  
>   
由结果可以看出，alias字段中最后一个别名["A3","A4"]被删除了。
8.$pull
用法：{$pull:{field:_value}}
作用：从数组field内删除一个等于_value的值
示例：删除chenzhou记录中的别名A1

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "A1", "A2" ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$pull:{"ailas":"A1"}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "A2" ], "name" : "chenzhou" }  
>   
9.$pullAll
用法：{$pullAll:value_array}
作用：用法同$pull一样，可以一次性删除数组内的多个值。
示例： 删除chenzhou记录内的所有别名

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ "A1", "A2" ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$pullAll:{"ailas":["A1","A2"]}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ ], "name" : "chenzhou" }  
>   
可以看到A1和A2已经全部被删除了
10.$rename
用法：{$rename:{old_field_name:new_field_name}}
作用：对字段进行重命名
示例：把chenzhou记录的name字段重命名为sname

> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ ], "name" : "chenzhou" }  
> db.students.update({name:"chenzhou"},{$rename:{"name":"sname"}})  
> db.students.find()  
{ "_id" : ObjectId("5030f7ac721e16c4ab180cdb"), "ailas" : [ ], "sname" : "chenzhou" }  
>   
由结果可以看出name字段已经被更新为sname了。
</pre>
