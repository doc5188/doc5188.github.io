---
layout: post
categories: linux
tags: [ruby, nodejs, linux]
date: 2014-09-13 09:59:21
title: "rails `autodetect’: Could not find a JavaScript runtime"
---

rails `autodetect’: Could not find a JavaScript runtime.

解决了问题。采用了以下方法：

{% highlight bash %}
# gem install execjs
# gem install therubyracer
{% endhighlight %}

或者
{% highlight bash %}
# apt-get install nodejs 
{% endhighlight %}
