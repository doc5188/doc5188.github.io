---
layout: post
date: 2014-09-20 17:48:08
title: "修改CentOS 6.4 root用户的系统默认语言设置"
categories: linux
tags: [linux centos]
---

最近用Virtual Box 虚拟了一个CentOS系统，版本6.4，安装时使用简体中文。发现用普通用户登录的时候 设置语言环境为English(United States)，下次登录的时候系统会默认使用English环境。可是用root用户登录的时候不会记忆上次使用的语言环境而默认使用中文环境。由于中文语言环境可能导致出现乱码的问题。因此使用English环境是首选。我们可以用下面的方法设置CentOS的默认语言环境：

修改CentOS运行环境的默认语言环境变量值

[hilon@localhost ~]# gedit /etc/profile

找到export语句，在语句前面加入

LANG=”en_US.UTF-8″

再在export后面追加LANG

export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE INPUTRC LANG

保存配置，修改CentOS语言完成。
