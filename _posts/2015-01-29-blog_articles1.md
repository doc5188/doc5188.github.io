---
layout: post
title: "快速读取进程内存（摘自《Debug Hacks》，略做修改）"
categories: 技术文章
tags: []
date: 2015-01-30 13:38:08
---

<p> Linux下使用ptrace调用可以监视和控制其他进程，并能够改变进程的寄存器值和内核映像。ptrace提供了PTRACE_PEEKDATA来实现进程内存读取，这是原语级的操作，在x86_64下一次仅读取8字节。因此在读取量较大时，需要反复调用ptrace。/proc/&lt;PID&gt;/mem接口提供了read调用，只需一次就可以读取任意大小内存，可谓价格便宜量又足。 </p> 
<p> 以下示例代码摘自《Debug Hacks》，使用了/proc/&lt;PID&gt;/mem接口： </p> 
<pre class="brush:cpp; toolbar: true; auto-links: false;">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;unistd.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/ptrace.h&gt;
#include &lt;sys/wait.h&gt;
#include &lt;errno.h&gt;

int main(int argc, char *argv[])
{
	if (argc &lt; 5) {
		fprintf(stdout, "usage: dumpmem pid start_addr length filaname\n");
		return -1;
	}

	/*get argvs*/
	off_t start_addr;
	int len;
	pid_t pid;
	pid = atoi(argv[1]);
	sscanf(argv[2], "%x", &amp;start_addr);
	sscanf(argv[3], "%x", &amp;len);
	
	/*attach the memory of pid*/
	int ptrace_ret;
	ptrace_ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);
	if (ptrace_ret == -1) {
		fprintf(stderr, "ptrace attach failed.\n");
		perror("ptrace");
		return -1;
	}
	if (waitpid(pid, NULL, 0) == -1) {
		fprintf(stderr, "waitpid failed.\n");
		perror("waitpid");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		return -1;
	}
	
	/*open /proc/&lt;pid&gt;/mem to attach the memory*/
	int fd;
	char path[256] = {0};
	sprintf(path, "/proc/%d/mem", pid);
	fd = open(path, O_RDONLY);
	if (fd == -1) {
		fprintf(stderr, "open file failed.\n");
		perror("open");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		return -1;
	}
	
	/*seek the file pointer*/
	off_t off;
	off = lseek(fd, start_addr, SEEK_SET);
	if (off == (off_t)-1) {
		fprintf(stderr, "lseek failed.\n");
		perror("lseek");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		close(fd);
		return -1;
	}
	
	/*read mem*/
	unsigned char *buf = (unsigned char *)malloc(len);
	if (buf == NULL) {
		fprintf(stderr, "malloc failed.\n");
		perror("malloc");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		close(fd);
		return -1;
	}
	int rd_sz;
	rd_sz = read(fd, buf, len);
	if (rd_sz &lt; len) {
		fprintf(stderr, "read failed.\n");
		perror("read");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		free(buf);
		close(fd);
		return -1;
	}
	
	/*now show mem*/
	int i = 0;
	FILE *fp = fopen(argv[4], "wb+");
	if (fp == NULL) {
		fprintf(stderr, "fopen failed.\n");
		perror("fopen");
		ptrace(PTRACE_DETACH, pid, NULL, NULL);
		free(buf);
		close(fd);
		return -1;
	}
	fwrite(buf, 1, len, fp);
	fclose(fp);
	
	ptrace(PTRACE_DETACH, pid, NULL, NULL);
	free(buf);
	close(fd);
	return 0;
}</pre> 
<p> 需要注意的是，读取可能因权限问题而失败。读取前可参考/proc/&lt;PID&gt;/maps内存映射，选取带有r标识的可读部分（如代码段，数据段或堆内存）。 </p>



<pre>
referer:http://my.oschina.net/u/180497/blog/141673
</pre>
