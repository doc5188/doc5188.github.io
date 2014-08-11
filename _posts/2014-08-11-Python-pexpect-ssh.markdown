---
layout: post
title:  "python 利用pexpect进行多机远程命令执行"
date:   2014-08-11 11:39:11
categories: Python
---

在安装之前，确认你的机器安装了python,和easy_install.通常python是自动安装的，如果没有安装easy_install，那么wget -q http://peak.telecommunity.com/dist/ez_setup.py 获取一下

python ez_setup.py

pexpect是python一个模块，可以通过：easy_install pexpect 来安装。

这里主要是用pexpect执行ssh，查看远程uptime和df -h看硬盘状况。

{% highlight python %}
#ssh_cmd.py
#coding:utf-8

import pexpect

def ssh_cmd(ip, user, passwd, cmd):
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
    r = ''
    try:
        i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
    except pexpect.EOF:
        ssh.close()
    else:
        r = ssh.read()
        ssh.expect(pexpect.EOF)
        ssh.close()
    return r

hosts = '''
192.168.0.12:smallfish:1234:df -h,uptime
192.168.0.13:smallfish:1234:df -h,uptime
'''

for host in hosts.split("/n"):
    if host:
        ip, user, passwd, cmds = host.split(":")
        for cmd in cmds.split(","):
            print "-- %s run:%s --" % (ip, cmd)
            print ssh_cmd(ip, user, passwd, cmd)

{% endhighlight %}

来源:http://blog.csdn.net/linkyou/article/details/6104420
