---
title: "lec2"
date: 2025-03-20 03:39:16 +0800
categories: [cs61b]
tags: ['java']
---

## 类的一般形式
---
1. ![Pasted image 20250228160938](/assets/Image/Pasted image 20250228160938.png)

2. **非静态方法**：又称实例方法, 如果方法将被类的实例调用, 那么它就应该是非静态方法。
	**If the method needs to use “my instance variables”, the method must be non-static.**

3. **实例化（Instantiating）**
```java
Dog hugeDog = new Dog(150);

hugeDog.makeNoise();
```

4. **对象数组（Arrays of Objects）**
```java
Dog[] dogs = new Dog[2];

dogs[0] = new Dog(8);

dogs[1] = new Dog(20);

dogs[0].makeNoise();
```


## 静态变量vs.实例成员（Static vs. Instance Members）
---
1. 静态方法和非静态（又称实例）方法的主要区别：
	- 静态方法使用类名调用，例如 Dog.makeNoise()；
	- 实例方法使用实例名调用，例如 maya.makeNoise()；
	- 静态方法不能访问 "我的“ 实例变量，因为没有 "我"；	

2. 示例![Pasted image 20250228162521](/assets/Image/Pasted image 20250228162521.png)

## Public and Static
---
Java的这两个关键词很重要, 比起c++更经常地被用于修饰class和method.
在今后的编程中要好好注意体会这两个关键词什么时候被用到.