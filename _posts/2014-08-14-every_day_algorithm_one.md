---
layout: post
title: "每日算法题--01--找出数组中唯一出现一次的两个数字 "
categories: 算法
tags: [algorithm, 每日算法题, 算法]
date: 2014-08-14 14:44:32
---

一问题描述

    一个数组中，存在两个只出现一次的数字，其余的数字均出现两次。要求在时间复杂度o(n)，空间复杂度为o(1)的情况下找出这两个数字。
 
二 问题分析

     此题实际考察了，对位操作的理解。首先进行简化，考虑只有一个数组中，只存在出现了一次的一个数字，其余数字在数组中出现两次，试
     找出这个数字。

 三 解决方案

   首先 回忆 异或操作， <span style="color:red">任意数字与自身相异或，结果都为0.</span>

   还有一个重要的性质，<span style="color:red">即任何元素与0相异或，结果都为元素自身。</span>
   
   解决方案：

  1   从数组的起始位置开始，对元素执行异或操作，则最后的结果，即为此只出现了一次的元素。
 
  2  题目中，数组中存在两个不同的元素，若是能仿造上述的解决方案，将两个元素分别放置在两个数组中，然后分别对每个数组进行异或操作，
     则所求异或结果即为所求。
  
  3  首先对原数组进行全部元素的异或，得到一个必然不为0的结果，然后判断该结果的2进制数字中，为1的最低的一位。
      然后根据此位是否为1 ，可以把原数组分为两组。则两个不同的元素，必然分别在这两个数组中。

 4  然后对两个数组，进行异或操作，即可得到所求。

四 代码示例
{% highlight c %}
#include <iostream>
using namespace std;

void Calc(int* arr,int n)
{
    int result=0;
    int a=0,b=0,index=0;
    for(int i=0;i<n;++i)
        result=result^arr[i];
    while(result)
    {
        if(result & 0x1==0)
        {
            index++;
            result=result>>1;
        }
        else
            break;
    }
    int cmp=1<<index;
    for(int i=0;i<n;++i)
    {
        if(arr[i] & cmp)
            a=a^arr[i];
        else
            b=b^arr[i];
    }
    cout <<a<<" "<<b<<endl;
}

int main()
{
    int n;
    cin >>n;
    int* arr=new int[n];
    for(int i=0;i<n;++i)
        cin >>arr[i];
    Calc(arr,n);
    return 0;
}
{% endhighlight %}

