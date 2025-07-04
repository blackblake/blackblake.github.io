---
title: "chap4 Class"
date: 2025-03-24 03:39:16 +0800
categories: [Core Java]
tags: ['java']
---

对象变量
---
---
```java
Date rightNow = new Date();
```
这里的`rightNow`称作“对象变量”，很重要的一点是认识到：对象变量并不实际包含一个对象，而只是一个指向对象的指针！

比如两个Date类的对象变量a和b都能同时引用同一个Date对象。

访问器方法
---
---

### 1）访问器方法
```java
LocalDate aThousandDaysLater = newYearsEve.plusDays(1000);
```
这个调用之后newYearsEve会有什么变化?它会改为1000天之后的日期吗?事实上，并没
有。plusDays方法会生成一个新的 LocalDate对象，然后把这个新对象赋给 aThousandDaysLater变
量。原来的对象不做任何改动。我们说 plusDays方法没有更改调用这个方法的对象。

这类似于第3章中见过的String类的 toUpperCase方法。在一个字符串上调用 toUpperCase时，这个字
符串仍保持不变，会返回一个将字符大写的新字符串

### 2）更改器方法

Java库曾经有另一个处理日历的类，名为GregorianCalendar。可以如下为这个类表示的一个日期增加1000天：
```java
GregorianCalendar someDay = new GregorianCalendar(1999,11,31);

someDay.add(Calendar.DAY_0F_MONTH,1800);
```
与LocalDate.plusDays方法不同，GregorianCalendar.add方法是一个更改器方法(mutator method)。
调用这个方法后，someDay 对象的状态会改变： 
```java
year = someDay.get(Calendar.YEAR);//2002
month = someDay.get(Calendar.MONTH)+1;//09
day = someDay.get(Calendar.DAY_0F MONTH);// 26
```

类的并列关系
---
---
比如我的文件名叫A.java，那么我们知道如果有main方法，那么它一定是被包含在class A{...}里面的；

但是如果我在这个文件里又定义了一个employee类，那么employee类的代码放在哪里？是class A{...}的...里面吗？

不是的：

>- 一个 .java 文件可以有多个类，但只能有一个 public 类（且文件名必须与该 public 类名一致，这里是 A.java）。
其他类（如 Employee）不能是 public 的（只能是默认包权限——即不写任何修饰词，或 static 嵌套类）
>
>- 所有类都是独立的，不能嵌套在另一个类的 {} 内（除非是嵌套类）

正确的写法是：

```java
//in A.java
public class A{
  ...
}

class Employee{
  ...
}
```