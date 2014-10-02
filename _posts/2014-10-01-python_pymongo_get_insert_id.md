---
layout: post
title: "python mongodb返回刚插入数据的id用什么方法"
categories: python
tags: [python, pymongo]
date: 2014-10-02 01:48:51
---

<pre>
def add_post():
    post = db.Post()
    post.title = request.form['title']
    post.text = request.form['text']
    post.save()
    return post._id
</pre>
