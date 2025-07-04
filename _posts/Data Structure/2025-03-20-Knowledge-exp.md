---
title: exp
date: 2025-03-20 03:39:16 +0800
categories:
- 数据结构
- 知识点
tags:
- dl
- java
---

1. **如果用IDE写代码的时候，本来应该有提示（即可以用tab打出来）的变量/对象等，如果没有提示了，一定要当心，基本上是出错了.**
```java

public LinkedListDeque() {  
    private Node sentinel=new Node(null,10,null);  
    ...
}  
  
public void addFirst(T item) {  
    Node newNode = new Node(sentinel,item,sentinel.next)  
    ...
}
```

  比如上例，我在addFirst函数中输入sentinel时，本来应该如下显示：![Pasted image 20240807131626](/assets/Image/Pasted image 20240807131626.png)
**但是却没有显示，所以我发觉应该是出问题了。果然，我把哨兵结点sentinel的定义放在LinkedListDeque这个函数里了，所以它变成了局部变量，只在LinkedListDeque函数中有生命**

2. **- 如何避免****测试用例能通过，但提交就是Wrong Answer**？**
1. 按照测试用例调试一遍，注意哪些语句是没有被调试到的，做个标记，回过头仔细检查；
2. 一定要画 **原理图、写注释**，光靠瞪是瞪不出来的
3. 注意 **细节**！
4. 也有可能是**理解错题意**了，比如**HDU2594—两串的最长相同前后缀**这题，题目给的例子是ss="aaa"，实际上是一种误导，因为它的意思是，比如有s1="abcdefg", s2="efgxxx"，那么ss就等于"efg"，而用aaa当示例就让人误以为是s1="abcdefg", s2="gfexxx"，那么ss="gfe"，实际上有一个顺序问题。