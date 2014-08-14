---
layout: post
date: 2014-08-14 09:03:23
title: "NPM无法安装"
categories: linux
tags: [nodejs, npm]
---


错误：

{% highlight bash %}
npm http GET https://registry.npmjs.org/supervisor

npm ERR! Error: failed to fetch from registry: supervisor
npm ERR!     at /usr/share/npm/lib/utils/npm-registry-client/get.js:139:12
npm ERR!     at cb (/usr/share/npm/lib/utils/npm-registry-client/request.js:31:9)
npm ERR!     at Request._callback (/usr/share/npm/lib/utils/npm-registry-client/request.js:136:18)
npm ERR!     at Request.callback (/usr/lib/nodejs/request/main.js:119:22)
npm ERR!     at Request.<anonymous> (/usr/lib/nodejs/request/main.js:212:58)
npm ERR!     at Request.emit (events.js:88:20)
npm ERR!     at ClientRequest.<anonymous> (/usr/lib/nodejs/request/main.js:209:10)
npm ERR!     at ClientRequest.emit (events.js:67:17)
npm ERR!     at ClientRequest.onError (/usr/lib/nodejs/request/tunnel.js:164:21)
npm ERR!     at ClientRequest.g (events.js:156:14)
npm ERR! You may report this log at:
npm ERR!     <http://bugs.debian.org/npm>
npm ERR! or use
npm ERR!     reportbug --attach /home/jon/npm-debug.log npm
npm ERR! 
npm ERR! System Linux 3.2.0-23-generic
npm ERR! command "node" "/usr/bin/npm" "install" "supervisor" "-g"
npm ERR! cwd /home/jon
npm ERR! node -v v0.6.12
npm ERR! npm -v 1.1.4
npm ERR! message failed to fetch from registry: supervisor
npm ERR! 
npm ERR! Additional logging details can be found in:
npm ERR!     /home/jon/npm-debug.log
npm not ok
{% endhighlight %}



解决方法：
{% highlight bash %}
    # npm config set registry http://registry.npmjs.org/  
{% endhighlight %}

 
