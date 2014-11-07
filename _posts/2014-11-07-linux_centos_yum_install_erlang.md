---
layout: post
title: "在CentOS下yum安装Erlang"
categories: linux
tags: [erlang安装]
date: 2014-11-07 12:43:20
---

yum安装erlang需下载的安装包大约需要100M空间

在https://www.erlang-solutions.com/downloads/download-erlang-otp的CentOS那一栏：

1. Adding repository entry

wget http://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm

rpm -Uvh erlang-solutions-1.0-1.noarch.rpm

2. Installing Erlang

sudo yum install erlang
