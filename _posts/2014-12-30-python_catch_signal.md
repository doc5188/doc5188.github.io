---
layout: post
title: "python捕获kill事件"
categories: python
tags: [python, signal, 信号]
date: 2014-12-30 12:24:53
---

1. 关于signal的信息： http://www.gnu.org/savannah-checkouts/gnu/libc/manual/html_node/Termination-Signals.html

copy如下：
24.2.2 Termination Signals

These signals are all used to tell a process to terminate, in one way or another. They have different names because they're used for slightly different purposes, and programs might want to handle them differently.

The reason for handling these signals is usually so your program can tidy up as appropriate before actually terminating. For example, you might want to save state information, delete temporary files, or restore the previous terminal modes. Such a handler should end by specifying the default action for the signal that happened and then reraising it; this will cause the program to terminate with that signal, as if it had not had a handler. (See Termination in Handler.)

The (obvious) default action for all of these signals is to cause the process to terminate.
— Macro: int SIGTERM

    The SIGTERM signal is a generic signal used to cause program termination. Unlike SIGKILL, this signal can be blocked, handled, and ignored. It is the normal way to politely ask a program to terminate.

    The shell command kill generates SIGTERM by default. 

— Macro: int SIGINT

    The SIGINT (“program interrupt”) signal is sent when the user types the INTR character (normally C-c). See Special Characters, for information about terminal driver support for C-c. 

— Macro: int SIGQUIT

    The SIGQUIT signal is similar to SIGINT, except that it's controlled by a different key—the QUIT character, usually C-\—and produces a core dump when it terminates the process, just like a program error signal. You can think of this as a program error condition “detected” by the user.

    See Program Error Signals, for information about core dumps. See Special Characters, for information about terminal driver support.

    Certain kinds of cleanups are best omitted in handling SIGQUIT. For example, if the program creates temporary files, it should handle the other termination requests by deleting the temporary files. But it is better for SIGQUIT not to delete them, so that the user can examine them in conjunction with the core dump. 

— Macro: int SIGKILL

    The SIGKILL signal is used to cause immediate program termination. It cannot be handled or ignored, and is therefore always fatal. It is also not possible to block this signal.

    This signal is usually generated only by explicit request. Since it cannot be handled, you should generate it only as a last resort, after first trying a less drastic method such as C-c or SIGTERM. If a process does not respond to any other termination signals, sending it a SIGKILL signal will almost always cause it to go away.

    In fact, if SIGKILL fails to terminate a process, that by itself constitutes an operating system bug which you should report.

    The system will generate SIGKILL for a process itself under some unusual conditions where the program cannot possibly continue to run (even to run a signal handler). 

— Macro: int SIGHUP

    The SIGHUP (“hang-up”) signal is used to report that the user's terminal is disconnected, perhaps because a network or telephone connection was broken. For more information about this, see Control Modes.

    This signal is also used to report the termination of the controlling process on a terminal to jobs associated with that session; this termination effectively disconnects all processes in the session from the controlling terminal. For more information, see Termination Internals. 

2. 如何捕获kill事件

参考danial的blog: http://danielkaes.wordpress.com/2009/06/04/how-to-catch-kill-events-with-python/

需要走墙。

内容copy如下：

How To Catch “Kill” Events with Python

Currently I’m working on a small MRCPv2 client written in Python, which is part of a bigger project at my laboratory. The client is started remotely by a program which controls and monitors several applications in the whole network and is stopped by it again.

In the Linux world catching “kill events” would be a simple task, to shut down another program a process just has to send a SIGTERM signal which can be caught be Python easily using the signal module which comes with every Python installation. However, on Windows things are a little bit harder, because the operating system never produces SIGTERM (and SIGILL) events according to the signal.h documentation from MSDN. That’s why it took me some time to figure out how to catch “kill” events under Windows with Python.

First of all, there are two different ways to close a program in Windows using the .NET API. The first one is to use Process.Kill which is the Microsoft version of SIGKILL and there is Process.CloseMainWindow which works similar to SIGTERM. To catch the latter one with Python you have to install the pywin32 library and define a handler by using win32api.SetControlCtrlHandler.

Here is a small example how to install an “exit handler” under Linux or Windows:
<pre>
import os, sys
def set_exit_handler(func):
    if os.name == "nt":
        try:
            import win32api
            win32api.SetConsoleCtrlHandler(func, True)
        except ImportError:
            version = “.”.join(map(str, sys.version_info[:2]))
            raise Exception(”pywin32 not installed for Python ” + version)
    else:
        import signal
        signal.signal(signal.SIGTERM, func)

if __name__ == "__main__":
    def on_exit(sig, func=None):
        print "exit handler triggered"
        import time
        time.sleep(5)
    set_exit_handler(on_exit)
    print "Press  to quit"
    raw_input()
    print "quit!"
</pre>

Edit: I’ve cleaned up the code, this version should work with Python 2.4 and 2.6, I didn’t tried it with Python 3000 yet.
