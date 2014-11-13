---
layout: post
title: "Linux平台下基于BitTorrent应用层协议的下载软件开发---位图模块（bitfield.c）"
categories: c/c++
tags: [bt开发, dht开发, 系列教程, BitTorrent协议规范, 协议规范, 项目连载]
date: 2014-11-13 17:40:27
---

<pre name="code" class="cpp">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;string.h&gt;
#include &lt;malloc.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;sys/types.h&gt;
#include &lt;sys/stat.h&gt;
#include &quot;parse_metafile.h&quot;
#include &quot;bitfield.h&quot;

extern int  pieces_length;
extern char *file_name;

Bitmap      *bitmap = NULL;         // 指向位图
int         download_piece_num = 0; // 当前已下载的piece数 

// 如果存在一个位图文件,则读位图文件并把获取的内容保存到bitmap
// 如此一来,就可以实现断点续传,即上次下载的内容不至于丢失
int create_bitfield()
{
	bitmap = (Bitmap *)malloc(sizeof(Bitmap));
	if(bitmap == NULL) { 
		printf(&quot;allocate memory for bitmap fiailed\n&quot;); 
		return -1;
	}

	// pieces_length除以20即为总的piece数
	bitmap-&gt;valid_length = pieces_length / 20;
	bitmap-&gt;bitfield_length = pieces_length / 20 / 8;//总的piece数，如果用字节来表示的话，需要多少字节？一个字节为8位
	if( (pieces_length/20) % 8 != 0 )  bitmap-&gt;bitfield_length++;

	bitmap-&gt;bitfield = (unsigned char *)malloc(bitmap-&gt;bitfield_length);//分配多少个字节
	if(bitmap-&gt;bitfield == NULL)  { 
		printf(&quot;allocate memory for bitmap-&gt;bitfield fiailed\n&quot;); 
		if(bitmap != NULL)  free(bitmap);
		return -1;
	}

	char bitmapfile[64];
	sprintf(bitmapfile,&quot;%dbitmap&quot;,pieces_length);
	
	int  i;
	FILE *fp = fopen(bitmapfile,&quot;rb&quot;);
	if(fp == NULL) {  // 若打开文件失败,说明开始的是一个全新的下载
		memset(bitmap-&gt;bitfield, 0, bitmap-&gt;bitfield_length);
	} else {
		fseek(fp,0,SEEK_SET);
		for(i = 0; i &lt; bitmap-&gt;bitfield_length; i++)
			(bitmap-&gt;bitfield)[i] = fgetc(fp);
		fclose(fp); 
		// 给download_piece_num赋新的初值
		download_piece_num = get_download_piece_num();
	}
	
	return 0;
}

int get_bit_value(Bitmap *bitmap,int index)  
{
	int           ret;
	int           byte_index;
	unsigned char byte_value;
	unsigned char inner_byte_index;

	if(index &gt;= bitmap-&gt;valid_length)  return -1;

	byte_index = index / 8;
	byte_value = bitmap-&gt;bitfield[byte_index];
	inner_byte_index = index % 8;

	byte_value = byte_value &gt;&gt; (7 - inner_byte_index);//假设这里index为3，那么inner_byte_index为3,这里就要右移4位。正好可以用2是否整除来判断
	if(byte_value % 2 == 0) ret = 0;
	else                    ret = 1;

	return ret;
}

int set_bit_value(Bitmap *bitmap,int index,unsigned char v)
{
	int           byte_index;
	unsigned char inner_byte_index;

	if(index &gt;= bitmap-&gt;valid_length)  return -1;//每一个piece都是1位
	if((v != 0) &amp;&amp; (v != 1))   return -1;//这里v的取值不是0就是1.

	byte_index = index / 8;
	inner_byte_index = index % 8;

	v = v &lt;&lt; (7 - inner_byte_index);//还是假设要设置第三位的值，那么左移4位，使其为1.然后再用或求其值
	bitmap-&gt;bitfield[byte_index] = bitmap-&gt;bitfield[byte_index] | v;

	return 0;
}

int all_zero(Bitmap *bitmap)
{
	if(bitmap-&gt;bitfield == NULL)  return -1;
	memset(bitmap-&gt;bitfield,0,bitmap-&gt;bitfield_length);
	return 0;
}
 
int all_set(Bitmap *bitmap)
{
	if(bitmap-&gt;bitfield == NULL)  return -1;
	memset(bitmap-&gt;bitfield,0xff,bitmap-&gt;bitfield_length);//memset都是以字节来赋值，所以0xff相当于将每一个字节都置为1.
	return 0;	
}

void release_memory_in_bitfield()
{
	if(bitmap-&gt;bitfield != NULL) free(bitmap-&gt;bitfield);
	if(bitmap != NULL)  free(bitmap);
}

int print_bitfield(Bitmap *bitmap)
{
	int i;

	for(i = 0; i &lt; bitmap-&gt;bitfield_length; i++) {//将每一个字节的值都打印出来，保留2位小数。
		printf(&quot;%.2X &quot;,bitmap-&gt;bitfield[i]);
		if( (i+1) % 16 == 0)  printf(&quot;\n&quot;);//每16个数打印一个换行符。从上面的程序中可以看到，打印的数字应该在0到255之间
	}
	printf(&quot;\n&quot;);

	return 0;
}

int restore_bitmap()
{
	int  fd;
	char bitmapfile[64];
	
	if( (bitmap == NULL) || (file_name == NULL) )  return -1;
	
	sprintf(bitmapfile,&quot;%dbitmap&quot;,pieces_length);
	fd = open(bitmapfile,O_RDWR|O_CREAT|O_TRUNC,0666);//如果文件存在，则将文件清零，且原有的存储属性不发生变化。
	if(fd &lt; 0)  return -1;
	
	write(fd,bitmap-&gt;bitfield,bitmap-&gt;bitfield_length);//将位图写入fd描述符所对应的文件中。
	close(fd);
	
	return 0;
}

int is_interested(Bitmap *dst,Bitmap *src)
{
	unsigned char const_char[8] = { 0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x01};
	unsigned char c1, c2;
	int           i, j;
	
	if( dst==NULL || src==NULL )  return -1;
	if( dst-&gt;bitfield==NULL || src-&gt;bitfield==NULL )  return -1;//这里说的一个问题是，如果两个位图不同，则不会发生比较
	if( dst-&gt;bitfield_length!=src-&gt;bitfield_length ||         //这里不同就是位图的大小不一样，或者有效位不一样
	    dst-&gt;valid_length!=src-&gt;valid_length )
		return -1;
	
	for(i = 0; i &lt; dst-&gt;bitfield_length-1; i++) { //如果dest中的某一位为1，而src为0，则说明src对des感兴趣
		for(j = 0; j &lt; 8; j++) {
		        c1 = (dst-&gt;bitfield)[i] &amp; const_char[j];//这里大于0，但是不一定等于1
			c2 = (src-&gt;bitfield)[i] &amp; const_char[j];
			if(c1&gt;0 &amp;&amp; c2==0) return 1;
		}
	}
	
	j  = dst-&gt;valid_length % 8; //从上面可以看出，上面比较的是bitfield_length-1个字节，现在比较的是最后一个字节
	c1 = dst-&gt;bitfield[dst-&gt;bitfield_length-1];
	c2 = src-&gt;bitfield[src-&gt;bitfield_length-1];
	for(i = 0; i &lt; j; i++) {
		if( (c1&amp;const_char[i])&gt;0 &amp;&amp; (c2&amp;const_char[i])==0 )
			return 1;
	}
	
	return 0;
}
/*  
    以上函数的功能测试代码如下：
	测试时可以交换map1.bitfield和map2.bitfield的值或赋其他值

	Bitmap map1, map2;
	unsigned char bf1[2] = { 0xa0, 0xa0 };
	unsigned char bf2[2] = { 0xe0, 0xe0 };
  
	map1.bitfield        = bf1;
	map1.bitfield_length = 2;
	map1.valid_length    = 11;
	map2.bitfield        = bf2;
	map2.bitfield_length = 2;
	map2.valid_length    = 11;
	  
    int ret = is_interested(&amp;map1,&amp;map2);	
	printf(&quot;%d\n&quot;,ret);
 */

// 获取当前已下载到的总的piece数
int get_download_piece_num()
{
	unsigned char const_char[8] = { 0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x01};
	int           i, j;
	
	if(bitmap==NULL || bitmap-&gt;bitfield==NULL)  return 0;
	
	download_piece_num =0;

	for(i = 0; i &lt; bitmap-&gt;bitfield_length-1; i++) {
		for(j = 0; j &lt; 8; j++) {
			if( ((bitmap-&gt;bitfield)[i] &amp; const_char[j]) != 0) 
			  download_piece_num++; //获取前bitfield_length-1个字节
		}
	}

	unsigned char c = (bitmap-&gt;bitfield)[i]; // c存放位图最后一个字节
	j = bitmap-&gt;valid_length % 8;            // j是位图最后一个字节的有效位数
	for(i = 0; i &lt; j; i++) {
		if( (c &amp; const_char[i]) !=0 ) download_piece_num++;
	}
		
	return download_piece_num;
}
</pre><br>



<pre>
referer:http://blog.csdn.net/airfer/article/details/8971460
</pre>
