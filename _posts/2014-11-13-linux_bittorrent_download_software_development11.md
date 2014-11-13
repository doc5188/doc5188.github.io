---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发--种子文件解析模块（parse_metafile.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:33
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;ctype.h&gt;
#include &lt;malloc.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &quot;parse_metafile.h&quot;
#include &quot;sha1.h&quot;

char  *metafile_content = NULL; // 保存种子文件的内容
long  filesize;                 // 种子文件的长度

int       piece_length  = 0;    // 每个piece的长度,通常为256KB即262144字节
char      *pieces       = NULL; // 保存每个pieces的哈希值,每个哈希值为20字节
int       pieces_length = 0;    // pieces缓冲区的长度

int       multi_file    = 0;    // 指明是单文件还是多文件
char      *file_name    = NULL; // 对于单文件,存放文件名;对于多文件,存放目录名
long long file_length   = 0;    // 存放待下载文件的总长度
Files     *files_head   = NULL; // 只对多文件种子有效,存放各个文件的路径和长度

unsigned char info_hash[20];    // 保存info_hash的值,连接tracker和peer时使用
unsigned char peer_id[20];      // 保存peer_id的值,连接peer时使用

Announce_list *announce_list_head = NULL; // 用于保存所有tracker服务器的URL


int read_metafile(char *metafile_name) //将种子文件读入缓存中
{
	long  i;
	
	// 以二进制、只读的方式打开文件
	FILE *fp = fopen(metafile_name,&quot;rb&quot;);
	if(fp == NULL) {
		printf(&quot;%s:%d can not open file\n&quot;,__FILE__,__LINE__);
		return -1;
	}
	
	// 获取种子文件的长度
	fseek(fp,0,SEEK_END);
	filesize = ftell(fp);
	if(filesize == -1) {
		printf(&quot;%s:%d fseek failed\n&quot;,__FILE__,__LINE__);
		return -1;
	}
	
	metafile_content = (char *)malloc(filesize+1);
	if(metafile_content == NULL) {
		printf(&quot;%s:%d malloc failed\n&quot;,__FILE__,__LINE__);
		return -1;
	}
	
	// 读取种子文件的内容到metafile_content缓冲区中
	fseek(fp,0,SEEK_SET);
	for(i = 0; i &lt; filesize; i++)
		metafile_content[i] = fgetc(fp);
	metafile_content[i] = '\0';

	fclose(fp); 

#ifdef DEBUG
	printf(&quot;metafile size is: %ld\n&quot;,filesize);
#endif	
	
	return 0;
}

int find_keyword(char *keyword,long *position)
{
	long i;

	*position = -1;
	if(keyword == NULL)  return 0;

	for(i = 0; i &lt; filesize-strlen(keyword); i++) {
		if( memcmp(&amp;metafile_content[i], keyword, strlen(keyword)) == 0 ) {
			*position = i;
			return 1;
		}
	}
	
	return 0;
}

int read_announce_list()
{
	Announce_list  *node = NULL;
	Announce_list  *p    = NULL;
	int            len   = 0;
	long           i;

	if( find_keyword(&quot;13:announce-list&quot;,&amp;i) == 0 ) {
		if( find_keyword(&quot;8:announce&quot;,&amp;i) == 1 ) {
			i = i + strlen(&quot;8:announce&quot;);
			while( isdigit(metafile_content[i]) ) {
				len = len * 10 + (metafile_content[i] - '0');
				i++;
			}
			i++;  // 跳过 ':'

			node = (Announce_list *)malloc(sizeof(Announce_list));
			strncpy(node-&gt;announce,&amp;metafile_content[i],len);
			node-&gt;announce[len] = '\0';
			node-&gt;next = NULL;
			announce_list_head = node;
		}
	} 
	else {  // 如果有13:announce-list关键词就不用处理8:announce关键词
		i = i + strlen(&quot;13:announce-list&quot;);
		i++;         // skip 'l'
		while(metafile_content[i] != 'e') {
			i++;     // skip 'l'
			while( isdigit(metafile_content[i]) ) {
				len = len * 10 + (metafile_content[i] - '0');
				i++;
			}
			if( metafile_content[i] == ':' )  i++;
			else  return -1;

			// 只处理以http开头的tracker地址,不处理以udp开头的地址
			if( memcmp(&amp;metafile_content[i],&quot;http&quot;,4) == 0 ) {
				node = (Announce_list *)malloc(sizeof(Announce_list));
				strncpy(node-&gt;announce,&amp;metafile_content[i],len);
				node-&gt;announce[len] = '\0';
				node-&gt;next = NULL;

				if(announce_list_head == NULL)
					announce_list_head = node;
				else {
					p = announce_list_head;
					while( p-&gt;next != NULL) p = p-&gt;next; // 使p指向最后个结点
					p-&gt;next = node; // node成为tracker列表的最后一个结点
				}
			}

			i = i + len;
			len = 0;
			i++;    // skip 'e'
			if(i &gt;= filesize)  return -1;
		}	
	}

#ifdef DEBUG
	p = announce_list_head;
	while(p != NULL) {
		printf(&quot;%s\n&quot;,p-&gt;announce);
		p = p-&gt;next;
	}
#endif	
	
	return 0;
}

// 连接某些tracker时会返回一个重定向URL,需要连接该URL才能获取peer
int add_an_announce(char *url)
{
	Announce_list *p = announce_list_head, *q;

	// 若参数指定的URL在tracker列表中已存在,则无需添加
	while(p != NULL) {
		if(strcmp(p-&gt;announce,url) == 0)  break;
		p = p-&gt;next;
	}
	if(p != NULL)  return 0;

	q = (Announce_list *)malloc(sizeof(Announce_list));
	strcpy(q-&gt;announce,url);
	q-&gt;next = NULL;
	
	p = announce_list_head;
	if(p == NULL)  { announce_list_head = q; return 1; }
	while(p-&gt;next != NULL)  p = p-&gt;next;
	p-&gt;next = q;
	return 1;
}

int is_multi_files()
{
	long i;

	if( find_keyword(&quot;5:files&quot;,&amp;i) == 1 ) {
		multi_file = 1;
		return 1;
	}

#ifdef DEBUG
	// printf(&quot;is_multi_files:%d\n&quot;,multi_file);
#endif

	return 0;
}

int get_piece_length() //得到每一个piece的长度，这里大部分情况下都是256K
{
	long i;

	if( find_keyword(&quot;12:piece length&quot;,&amp;i) == 1 ) {
		i = i + strlen(&quot;12:piece length&quot;);  // skip &quot;12:piece length&quot;
		i++;  // skip 'i'
		while(metafile_content[i] != 'e') {
			piece_length = piece_length * 10 + (metafile_content[i] - '0');
			i++;
		}
	} else {
		return -1;
	}

#ifdef DEBUG
	printf(&quot;piece length:%d\n&quot;,piece_length);
#endif

	return 0;
}

int get_pieces()//获得文件的hash值，每一个piece所占用的字节数为20个字节，所以根据得到的pieces_length可以得到piece数目。
{
	long i;

	if( find_keyword(&quot;6:pieces&quot;, &amp;i) == 1 ) {
		i = i + 8;     // skip &quot;6:pieces&quot;
		while(metafile_content[i] != ':') {
			pieces_length = pieces_length * 10 + (metafile_content[i] - '0');
			i++;
		}
		i++;           // skip ':'
		pieces = (char *)malloc(pieces_length+1);//这里是根据pieces_length的长度分配内存，然后将每一个piece的hash值拷贝到内存中
		memcpy(pieces,&amp;metafile_content[i],pieces_length);
		pieces[pieces_length] = '\0';
	} else {
		return -1;
	}

#ifdef DEBUG
	printf(&quot;get_pieces ok\n&quot;);
#endif

	return 0;
}

int get_file_name() //获得文件的名字
{
	long  i;
	int   count = 0;

	if( find_keyword(&quot;4:name&quot;, &amp;i) == 1 ) {
		i = i + 6;  // skip &quot;4:name&quot;
		while(metafile_content[i] != ':') {
			count = count * 10 + (metafile_content[i] - '0');
			i++;
		}
		i++;        // skip ':' 
		file_name = (char *)malloc(count+1);
		memcpy(file_name,&amp;metafile_content[i],count);
		file_name[count] = '\0';
	} else {
		return -1;
	}

#ifdef DEBUG
	// 由于可能含有中文字符,因此可能打印出乱码
	// printf(&quot;file_name:%s\n&quot;,file_name);
#endif

	return 0;
}

int get_file_length() //这个函数也是为了得到文件的长度，但是要首先判断是单文件还是多文件，对于多文件直接调用get_files_length_path
{
        long i;       //对于单文件则直接计算就可以了

	if(is_multi_files() == 1)  {
		if(files_head == NULL)  get_files_length_path();
		Files *p = files_head;
		while(p != NULL) { file_length += p-&gt;length; p = p-&gt;next; }
	} else {
		if( find_keyword(&quot;6:length&quot;,&amp;i) == 1 ) {
			i = i + 8;  // skip &quot;6:length&quot;
			i++;        // skip 'i' 
			while(metafile_content[i] != 'e') {
				file_length = file_length * 10 + (metafile_content[i] - '0');
				i++;
			}	
		}
	}
	
#ifdef DEBUG
	printf(&quot;file_length:%lld\n&quot;,file_length);
#endif

	return 0;
}

int get_files_length_path()  //从函数名也可以看出，这是得到文件的长度，以及文件所在的路径
{
	long   i;
	int    length;
	int    count;
	Files  *node  = NULL;
	Files  *p     = NULL;

	if(is_multi_files() != 1) {
		return 0;
	}
	
	for(i = 0; i &lt; filesize-8; i++) {
		if( memcmp(&amp;metafile_content[i],&quot;6:length&quot;,8) == 0 )
		{
			i = i + 8;  // skip &quot;6:length&quot;
			i++;        // skip 'i' 
			length = 0;
			while(metafile_content[i] != 'e') {
				length = length * 10 + (metafile_content[i] - '0');
				i++;
			}
			node = (Files *)malloc(sizeof(Files));
			node-&gt;length = length;
			node-&gt;next = NULL;
			if(files_head == NULL)
				files_head = node;
			else {
				p = files_head;
				while(p-&gt;next != NULL) p = p-&gt;next;
				p-&gt;next = node;
			}
		}
		if( memcmp(&amp;metafile_content[i],&quot;4:path&quot;,6) == 0 )
		{
			i = i + 6;  // skip &quot;4:path&quot;
			i++;        // skip 'l'
			count = 0;
			while(metafile_content[i] != ':') {
				count = count * 10 + (metafile_content[i] - '0');
				i++;
			}
			i++;        // skip ':'
			p = files_head;
			while(p-&gt;next != NULL) p = p-&gt;next;
			memcpy(p-&gt;path,&amp;metafile_content[i],count);
			*(p-&gt;path + count) = '\0';
		}
	}

#ifdef DEBUG
	// 由于可能含有中文字符,因此可能打印出乱码
	// p = files_head;
	// while(p != NULL) {
	//	 printf(&quot;%ld:%s\n&quot;,p-&gt;length,p-&gt;path);
	//	 p = p-&gt;next;
	// }
#endif

	return 0;
}

int get_info_hash()//将字典d与e之间多对应的字符串，作为输入，生成hash值。
{
	int   push_pop = 0;
	long  i, begin, end;

	if(metafile_content == NULL)  return -1;

	if( find_keyword(&quot;4:info&quot;,&amp;i) == 1 ) {
		begin = i+6;  // begin是关键字&quot;4:info&quot;对应值的起始下标
	} else {
		return -1;
	}

	i = i + 6;        // skip &quot;4:info&quot;
	for(; i &lt; filesize; )
		if(metafile_content[i] == 'd') { 
			push_pop++;
			i++;
		} else if(metafile_content[i] == 'l') {
			push_pop++;
			i++;
		} else if(metafile_content[i] == 'i') {
			i++;  // skip i
			if(i == filesize)  return -1;
			while(metafile_content[i] != 'e') {
				if((i+1) == filesize)  return -1;
				else i++;
			}
			i++;  // skip e
		} else if((metafile_content[i] &gt;= '0') &amp;&amp; (metafile_content[i] &lt;= '9')) {
			int number = 0;
			while((metafile_content[i] &gt;= '0') &amp;&amp; (metafile_content[i] &lt;= '9')) {
				number = number * 10 + metafile_content[i] - '0';
				i++;
			}
			i++;  // skip :
			i = i + number;
		} else if(metafile_content[i] == 'e') {
			push_pop--;
			if(push_pop == 0) { end = i; break; }
			else  i++; 
		} else {
			return -1;
		}
	if(i == filesize)  return -1;

	SHA1_CTX context;
	SHA1Init(&amp;context);
	SHA1Update(&amp;context, &amp;metafile_content[begin], end-begin+1);
	SHA1Final(info_hash, &amp;context);

#ifdef DEBUG
	printf(&quot;info_hash:&quot;);
	for(i = 0; i &lt; 20; i++)  
		printf(&quot;%.2x &quot;,info_hash[i]);
	printf(&quot;\n&quot;);
#endif

	return 0;
}

int get_peer_id()
{
	// 设置产生随机数的种子
	srand(time(NULL));
	// 生成随机数,并把其中12位赋给peer_id,peer_id前8位固定为-TT1000-
	sprintf(peer_id,&quot;-TT1000-%12d&quot;,rand());

#ifdef DEBUG
	int i;
	printf(&quot;peer_id:&quot;);
	for(i = 0; i &lt; 20; i++)  printf(&quot;%c&quot;,peer_id[i]);
	printf(&quot;\n&quot;);
#endif

	return 0;
}

void release_memory_in_parse_metafile()
{
	Announce_list *p;
	Files         *q;
	
	if(metafile_content != NULL)  free(metafile_content);
	if(file_name != NULL)         free(file_name);
	if(pieces != NULL)            free(pieces);
	
	while(announce_list_head != NULL) {
		p = announce_list_head;
		announce_list_head = announce_list_head-&gt;next;
		free(p);
	}

	while(files_head != NULL) {
		q = files_head;
		files_head = files_head-&gt;next;
		free(q);
	}
}

int parse_metafile(char *metafile)
{
	int ret;

	// 读取种子文件
	ret = read_metafile(metafile);
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }
	
	// 从种子文件中获取tracker服务器的地址
	ret = read_announce_list();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }

	// 判断是否为多文件
	ret = is_multi_files();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }
	
	// 获取每个piece的长度,一般为256KB
	ret = get_piece_length();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }
	
	// 读取各个piece的哈希值
	ret = get_pieces();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }
	
	// 获取要下载的文件名，对于多文件的种子，获取的是目录名
	ret = get_file_name();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }

	// 对于多文件的种子，获取各个待下载的文件路径和文件长度
	ret = get_files_length_path();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }
	
	// 获取待下载的文件的总长度
	ret = get_file_length();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }

	// 获得info_hash，生成peer_id
	ret = get_info_hash();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }
	ret = get_peer_id();
	if(ret &lt; 0) { printf(&quot;%s:%d wrong&quot;,__FILE__,__LINE__); return -1; }

	return 0;
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971508
</pre>
