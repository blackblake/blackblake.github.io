---
title: assert input
date: 2025-03-20 03:39:16 +0800
categories:
- 数据结构
- 知识点
---

```cpp
#include<cctype>

//先假定为char输入（因为char能接受数字输入,而int不能接受字母）
    char c;
    cin>>c;
    
    if(isdigit(c) )
        cout<<"是数字";
    
    else if(isalpha(c) )
        cout<<"是字母";
```

- 头文件**\<cctype>**
	
- **一开始要把输入变量的类型设置为**char****
	
- ****isdigit(c) 、isalpha(c)****的语法是: 被判断的字符作为参数
	
- **如果c是digit/alpha，则isdigit/isalpha会返回**true****