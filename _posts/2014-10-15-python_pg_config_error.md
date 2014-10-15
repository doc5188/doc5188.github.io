---
layout: post
title: "pg_config executable not found"
categories: linux
tags: [pg_config]
date: 2014-10-15 09:03:10
---

I am having trouble installing psycopg2. I get the following error when I try to pip install psycopg2:
<pre>

Error: pg_config executable not found.

Please add the directory containing pg_config to the PATH

or specify the full executable path with the option:



    python setup.py build_ext --pg-config /path/to/pg_config build ...



or with the pg_config option in 'setup.cfg'.

----------------------------------------
Command python setup.py egg_info failed with error code 1 in /tmp/pip-build/psycopg2
</pre>

But the problem is pg_config is actually in my PATH; it runs without any problem:

<pre>
$ which pg_config
/usr/pgsql-9.1/bin/pg_config
</pre>

I tried adding the pg_config path to the setup.cfg file and building it using the source files I downloaded from their website (http://initd.org/psycopg/) and I get the following error message!

Error: Unable to find 'pg_config' file in '/usr/pgsql-9.1/bin/'

But it is actually THERE!!!

I am baffled by these errors. Can anyone help please?

By the way, I sudo all the commands. Also I am on RHEL 5.5.

=================================================Solution================================








UPDATE /etc/yum.repos.d/CentOS-Base.repo, [base] and [updates] sections

ADD exclude=postgresql*

<pre>
# curl -O http://yum.postgresql.org/9.1/redhat/rhel-6-i386/pgdg-centos91-9.1-4.noarch.rpmr  
# rpm -ivh pgdg-centos91-9.1-4.noarch.rpm
# 
# yum install postgresql  
# yum install postgresql-devel
# 
# PATH=$PATH:/usr/pgsql-9.1/bin/
# 
# pip install psycopg2

</pre>
