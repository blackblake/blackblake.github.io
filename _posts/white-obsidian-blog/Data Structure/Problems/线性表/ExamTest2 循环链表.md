---
title: ext2 循环链表
categories:
  - DSA
  - list
---
### **Description**

![[4aba8780ca7ae59076ed62f2e9afcd9.png]]

### **Solution**

```cpp
#include<iostream>
#include<string>
#include<sstream>
using namespace std;
//链表结点node定义省略  

int main(){

    node* rear=new node();//题目要求只能用rear尾指针
    rear->next=rear;

    string str;//用于存储第一行输入的字符串
    getline(cin,str);//getline读取第一行输入
    istringstream iss(str);//用iss逐个处理str的每个字符

    char ch;
    // 使用字符串流逐个读取整数
    while (iss >> ch) {

        int n=ch-'0';//记得要把char转换成int！
        node* p = new node(n);

		//尾插法
        node* ptr = rear->next;
        rear->next = p;
        rear = rear->next;
        rear->next = ptr;
    }

    int k;
    cin>>k;

for(int x=k;x>=0;x--){
    int i=0;int n;node*p=rear->next->next;
    while(i<x){
        p=p->next;
        i++;
    }n=p->data;
  
    node*p1=new node(n);
       node*ptr1=rear->next;
       rear->next=p1;
       rear=rear->next;
       rear->next=ptr1;
}

/* then print the list */
    return 0;
}
```

### Link
- 这道题的一个问题是输入处理：没有实现输入队列元素的个数，那么怎么知道第几个元素才到k呢？于是采用getline直接获取第一行整行的输入；
	[用getline获取整行输入](obsidian://open?vault=Obsidian%20Vault&file=Coding%2FKnowledge%2FGetline)
- 用getline处理输入时，是用string来存储输入的，所以记得要把char转换成int！