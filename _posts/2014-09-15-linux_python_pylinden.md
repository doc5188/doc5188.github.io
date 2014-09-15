---
layout: post
title: "在linux vps上搭建基于python2.7的静态博客程序-pylinden"
categories: linux
tags: [pylinden, linux, python, 博客程序]
date: 2014-09-15 22:01:21
---

PyLinden是Python实现的一个静态博客生成器。不使用Django等任何臃肿的框架，基于简单够用的设计哲学构建。

<pre>
    可轻松部署于BAE（Baidu App Engine）。
    纯文件存储，没有繁琐的数据库以及BAE的bucket等存储服务。
    兼容Github Pages博客，将日志文件拷贝过来即可。
    支持且仅支持markdown格式书写日志。
    支持代码着色（pygments），兼容Github Pages方式
</pre>

{% highlight python %}
# git clone https://github.com/lingyunyumo/PyLinden.git pylinden
# cd pylinden
# ls
admin     LICENSE       pygments  pylinden.wpr  README.md   
app.conf  local_run.py  pylinden  pylinden.wpu  site_source

# python local_run.py (这个就是生成/更新静态网站的命令）
# ls
admin     LICENSE       pygments  pylinden.wpr  README.md    site_source
app.conf  local_run.py  pylinden  pylinden.wpu  site_output
（新出现了site_output目录）
# cd site_output

# ls
404.html    gallery.html  photos       posts       static
about.html  index.html    photos.html  posts.html
(可见~/pylinden/site_output/就是静态网站的根目录）
{% endhighlight %}

发贴方法：

{% highlight python %}
# cd ~/pylinden/site_source/_posts/
{% endhighlight %}

按~/pylinden/site_source/_posts/里面的1970-08-22-hello-world.md的格式，新建帖子

2013-11-26-test1.md,格式如下：

{% highlight python %}
—
layout: post
title: 测试1
tags:
  – misc
—

这是测试1.
{% endhighlight %}

然后，


{% highlight python %}
# cd ~/pylinden

# python local_run.py
{% endhighlight %}

演示站点：http://pld.brite.biz

作者的演示站点：http://pylinden.duapp.com/

项目地址：https://github.com/lingyunyumo/PyLinden

http://pylindendocs.duapp.com/

python环境需为2.7版，需要先安装的python modules:pyYAML, markdown, jinja2, pygments.

