---
title: "getline()"
date: 2025-03-20 03:39:16 +0800
categories: [Knowledge]
tags: ['dl']
---

##### **Header: \<string>**

##### **Function**
The getline() function extracts characters from the input stream and appends it to the string object until the `delimiting character` is encountered.

##### **Syntax**
```cpp
string str;
getline(cin,str);
```

##### **Parameters**
- ***str:***  It is a string object, the `input is stored in this object` after being read from the stream.
- ***delim:*** It is the `delimitation character` which tells the function to`stop reading` further input after reaching this character.

##### **E.g.**
```cpp
    string name;
    string city;
    cout << "Please enter your name: ";
    getline(cin, name);
    cout << "Enter the city you live in: ";
    getline(cin, city);
    cout << "Hello, " << name << endl;
    cout << "You live in " << city << endl;
/*
Please enter your name: John Doe  
Enter the city you live in: Chicago  
Hello, John Doe  
You live in Chicago
*/
```

未指定休止符的情况下，getline默认以**换行符**为休止符

#### **对getline输入的str进行逐个字符的处理**
##### header: \<sstream>
##### code

```cpp
   #include<sstream>//必须有
   
	string slist[100];
	
    //这三行的顺序绝对不能改变！否则无效
    string str;
    getline(cin,str);
	istringstream iss(str);//把str当作参数！

    int i=0;
    while(iss>>slist[i]){//注意箭头方向（输入到slist里作为第i个元素）
        i++;
    }
    /*至此,输入的一行的所有内容(包括空白符)都被储存到slist数组里面*/
```

****istringstream iss(str)****
1）**记住, 前面有个i, 不是stringstream！(从iss的名字就能看出来)**
2）**记住, 是需要把str当作参数的！**

##### [实战](obsidian://open?vault=Obsidian%20Vault&file=Coding%2FProblems%2FExamTest2%20%E5%BE%AA%E7%8E%AF%E9%93%BE%E8%A1%A8)

##### 补充
another feasible method
```cpp
string slist[100];
    stringstream  ss;
    string s;
    getline(cin,s);
    ss<<s;
    int i=0;
    while(ss>>slist[i]){
        i++;
    }
```

##### 不用sstream也能操作str
![Pasted image 20241029235637](/assets/Image/Pasted image 20241029235637.png)