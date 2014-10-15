---
layout: post
title: "Permission denied for relation [closed]"
categories: 数据库
tags: []
date: 2014-10-15 09:00:29
---

I tried to run simple sql command:

select * from site_adzone;

and I got this error

ERROR:  permission denied for relation site_adzone

What could be the problem here?

I tried also to do select for other tables and got same issue. I also tried to do this:

GRANT ALL PRIVILEGES ON DATABASE jerry to tom;

but I got this response from console

WARNING:  no privileges were granted for "jerry"

Do you have some idea what can be wrong?


============================Solution==========================

GRANT on the database is not what you need. Grant on the tables directly.

Granting privileges on the database mostly is used to grant or revoke connect privileges. This allows you to specify who may do stuff in the database if they have sufficient other permissions.

You want instead:

 GRANT ALL PRIVILEGES ON TABLE side_adzone TO jerry;

This will take care of this issue.

