---
layout: post
title: "C++ STL vector assign用法  "
categories: c/c++
tags: [c/c++, STL, vector]
date: 2014-12-08 15:18:39
---

vector::assign //用来构造一个vector的函数，类似于copy函数

void assign( size_type _Count, const Type& _Val);

//_Count指要构造的vector成员的个数，   _Val指成员的数值，他的类型必须与vector类型一致！

<pre>
template<class InputIterator>
void assign( InputIterator _First, InputIterator _Last );

//两个指针，分别指向复制开始和结束的地方!

// vector_assign.cpp
// compile with: /EHsc
#include <vector>
#include <iostream>

int main( )
{
   using namespace std;
   vector<int> v1, v2, v3;
   vector<int>::iterator iter;

   v1.push_back(10);
   v1.push_back(20);
   v1.push_back(30);
   v1.push_back(40);
   v1.push_back(50);

   cout << "v1 = " ;
   for (iter = v1.begin(); iter != v1.end(); iter++)
       cout << *iter << " ";
   cout << endl;

   v2.assign(v1.begin(), v1.end());
   cout << "v2 = ";
   for (iter = v2.begin(); iter != v2.end(); iter++)
       cout << *iter << " ";
   cout << endl;

   v3.assign(7, 4) ;
   cout << "v3 = ";
   for (iter = v3.begin(); iter != v3.end(); iter++)
       cout << *iter << " ";
   cout << endl;
}
</pre>

输出结果为：

<pre>
v1 = 10 20 30 40 50
v2 = 10 20 30 40 50
v3 = 4 4 4 4 4 4 4 

</pre>
