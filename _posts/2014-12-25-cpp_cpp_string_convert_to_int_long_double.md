---
layout: post
title: "c++中的一些类型转换 : CString,string,int ,long,double"
categories: c/c++
tags: [c++, string类转换]
date: 2014-12-25 09:15:12
---

最近做项目用到c++，才发现c++中的数据类型不是一般的BT。尤其是我和婷还是分开操作的。我写底层，用的是WIN32控制台；而婷写MFC。由于没有经验，所以没有写中间的转换程序。当集成时，类型转换特别麻烦。以下都是我收集的类型转换的方法和一些经验，供大家参考。欢迎补充~~

1. char* to string

<pre>
string s(char *); 
</pre>

注：在不是初始化的地方最好用assign().

！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

2. string to const char*

<pre>
string a="strte";
const char* r=a.c_str();
</pre>

注意是const的。还要转到char*：
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2.2. const char* to char*

<pre>
const char* r="123";
char   *p1   =   new   char[strlen(r)+1];
strcpy(p1,r);
</pre>

附：http://hi.baidu.com/cfans/blog/item/06970ef4b671f366dcc4745d.html
 这个页面是具体讲述区别的。
·············································································································

3. cstring to string

vs2005 Unicode下：

<pre>
  CStringW   str(L"test");  
  CStringA   stra(str.GetBuffer(0));  
  str.ReleaseBuffer();      
  std::string   strs   (stra.GetBuffer(0));  
  stra.ReleaseBuffer();
</pre>

非Unicode下：

<pre>
CString cs("test");
std::string str=cs.getBuffer(0);
cs.ReleaseBuffer();
</pre>

注：GetBuffer()后一定要ReleaseBuffer(),否则就没有释放缓冲区所占的空间.
++++++++++++++++++++++++++++++++++++++++++++++++++++

4. double ,int to string

<pre>
#include <sstream>
using namespace std;

stringstream ss;
string result;
long n=11111;
stream << n; //从long型数据输入
stream >>result; //转换为 string
</pre>


===================================================

5.char*  to int, double ,long

<pre>
char *s; double x; int i; long l;

s = " -2309.12E-15"; /* Test of atof */
x = atof( s );
printf( "atof test: ASCII string: %s\tfloat: %e\n", s, x );

s = "7.8912654773d210"; /* Test of atof */
x = atof( s );
printf( "atof test: ASCII string: %s\tfloat: %e\n", s, x );

s = " -9885 pigs"; /* Test of atoi */
i = atoi( s );
printf( "atoi test: ASCII string: %s\t\tinteger: %d\n", s, i );

s = "98854 dollars"; /* Test of atol */
l = atol( s );
printf( "atol test: ASCII string: %s\t\tlong: %ld\n", s, l );

</pre>
------------------------------------------------------------------------------------------------

6. string to int ,long ,double            

<pre>
 int s;
 string str="123";
 stringstream ss;
 ss<<str;//从str输入
 ss>>s;//输出到int
 ss.clear();
</pre>


——————————————————————————————————————————

7. date to string

<pre>
#include <time>
using namespace std;

char dateStr [9];
char timeStr [9];
 _strdate( dateStr);
printf( "The current date is %s \n", dateStr);
_strtime( timeStr );
printf( "The current time is %s \n", timeStr);

</pre>

--------实践证明是正确的版本--------------------------------------------------------------

<pre>
#include <iostream>
#include <ctime>
#include <cerrno>
 
int main()
{
     //Find the current time
     time_t curtime = time(0);
     
      //convert it to tm
      tm now=*localtime(&curtime);
    
     //BUFSIZ is standard macro that expands to a integer constant expression
     //that is greater then or equal to 256. It is the size of the stream buffer
     //used by setbuf()
     char dest[BUFSIZ]={0};
    
     //Format string determines the conversion specification's behaviour
     const char format[]="%A, %B %d %Y. The time is %X";
    
     //strftime - converts date and time to a string
     if (strftime(dest, sizeof(dest)-1, format, &now)>0)
       std::cout<<dest<<std::endl;
     else
       std::cerr<<"strftime failed. Errno code: "<<errno<<std::endl;
}

</pre>

|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

8.string to cstring

+++++++++++++++++++++++++++++++++++++++++++++++++++++

非Unicode下：

int 转 CString：
<pre>
CString.Format("%d",int);
</pre>

...............................

string 转 CString 

<pre>
CString.format("%s", string.c_str()); 
</pre>

用c_str()确实比data()要好. 

.......................................

char* 转 CString 

<pre>
CString.format("%s", char*); 
 CString strtest; 
 char * charpoint; 
 charpoint="give string a value"; 
 strtest=charpoint; //直接付值
</pre>

.....................................................

CString 转 int
<pre>
 CString  ss="1212.12"; 
 int temp=atoi(ss); //atoi _atoi64或atol
</pre>

...................................................................................................................................

9.在Unicode下的CString to double

<pre>
CSting sTemp("123.567");
double dTemp = _wtof(sTemp.GetString());
</pre>


<pre>
referfer:http://blog.chinaunix.net/uid-22982394-id-2983800.html
</pre>
