---
layout: post
title: "Finding the linux thread ID from within python using ctypes"
categories: python 
tags: [python, linux, python线程id]
date: 2014-12-04 15:08:56
---

<p>So I've got a multi-threaded application and suddenly I notice there's one thread running away and using all CPU.  Not good, probably a loop gone wrong.  But where?  One way to find this is revert history in the VCS and keep trying it out till you find the bad commit.  Another way is to find out which thread is doing this, this is of course much more fun!</p>
<p>Using <code>ps -p PID -f -L</code> you'll see the thread ID which is causing the problems.  To relate this to a Python thread I subclass <code>threading.Thread</code>, override it's <code>.start()</code> method to first wrap the <code>.run()</code> method so that you can log the thread ID before calling the original <code>.run()</code>.  Since I was already doing all of this apart from the logging of the thread ID this was less work then it sounds.  But the hard part is finding the thread ID.</p>
<p>Python knows of a <code><a href="http://docs.python.org/library/thread.html#thread.get_ident">threading.get_ident()</a></code> method but this is merely a long unique integer and does not correspond to the actual thread ID of the OS.  The kernel allows you to get the thread ID: <tt>getid(2)</tt>.  But this must be called using a system call with the constant name <tt>SYS_gettid</tt>.  Because it's hard to use constants in ctypes (at least I don't know how to do this), and this is not portable anyway, I used this trivial C program to find out the constant value:</p>
<code><pre>#include &lt;stdio.h&gt;
#include &lt;sys/syscall.h&gt;

int main(void)
{
    printf("%d\n", SYS_gettid);
    return 0;
}
</pre></code>
<p>In my case the constant to use is 186.  Now all that is left is using <a href="http://docs.python.org/library/ctypes.html">ctypes</a> to do the system call:</p>
<code><pre>import ctypes

SYS_gettid = 186
libc = ctypes.cdll.LoadLibrary('libc.so.6')
tid = libc.syscall(SYS_gettid)
</pre></code>
<p>That's it!  Now you have the matching thread ID!</p>
<p>Going back to the original problem you can now associate this thread ID with the thread name and you should be able to find the problematic thread.</p>
