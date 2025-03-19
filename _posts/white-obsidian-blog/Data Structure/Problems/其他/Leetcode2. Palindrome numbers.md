---
title: lc2 palindrome numbers
categories:
  - DSA
  - others
---
1. **to_string** converting int to string

```cpp
#include <string> //remember to include the <string> headfile!
using namespace std;

string s = to_string(42);
```

  \#stoi convert string to int
```cpp
stoi( str )
```

2. MY MISUNDERSTANDINGS
```cpp
string str=to_string(x);//convert x to a string 
int result =0; 
int muti =1;//倍数 

for(int i=0;i<str.length();i++){ 
	result =result + str[i]*muti; 
	muti=muti*10;
}
```

---
```cpp
         string str=to_string(x);//convert x to a string

         string result;

         for(int i=str.length()-1;i>=0;i--){

            result+=str[i];//let the result be a string,too

         }

```

---
2024-07-27 02:32



