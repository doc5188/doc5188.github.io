---
layout: post
date: 2014-08-14 16:41:23
title: "Bash expect使用示例"
categories: linux
tags: [expect, bash, shell, linux]
---

二种expect在bash中的用法.
示例一： 自动git push
{% highlight bash %}
#!/bin/sh
cd /work/scm/test
git add .
git commit -asm "Add post"
expect<<- END
spawn git push
expect "Username"
send "test\n"
expect "Password"
send "test\n"
expect eof
exit
END 
{% endhighlight %}

示例二: 自动ssh
#!/bin/sh
ip=10.18.12.11
password=root

{% highlight bash %}
expect -c "set timeout -1;
                spawn ssh -o StrictHostKeyChecking=no root@$ip;
                expect {
                    *assword:* {send -- $password\r;
                                 expect {
                                    *denied* {exit 2;}
                                    eof
                                 }
                    }
                    eof         {exit 1;}
                }
                "

{% endhighlight %}
