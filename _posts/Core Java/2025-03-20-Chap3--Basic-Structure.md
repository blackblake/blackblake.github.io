---
title: "chap3 basic-structures"
date: 2025-03-20 03:39:16 +0800
categories: [Core Java]
tags: [java]     # TAG names should always be lowercase
---
### 修饰符
---
#### 1）访问控制修饰符

- **default** (即默认，什么也不写）: 在同一==包==内可见。使用对象：类、接口、变量、方法。
    
- **private** : 在同一==类==内可见。使用对象：变量、方法。 
	**注意：不能修饰类（外部类）**
    这里的"类"指的是声明该成员的**特定类**，而不是整个Java文件。
	
- **public** : 对==所有==类可见。使用对象：类、接口、变量、方法
	
- **protected** : 对同一==包==内的类和所有子类可见。使用对象：变量、方法。 **注意：不能修饰类（外部类）**。

#### 2）static修饰符

- **静态变量：**
    static 关键字用来声明独立于对象的静态变量，无论一个类实例化多少对象，它的静态变量**只有一份拷贝**。 
    
- **静态方法：**
    static 关键字用来声明独立于对象的静态方法。静态方法**不能使用类的非静态变量**。静态方法 **从参数列表得到数据** ，然后计算这些数据。
    
对类变量和方法的访问可以直接使用 **`classname.variablename`** 和 **`classname.methodname`** 的方式访问。

### System.out
---
- 不带参数的`println`方法只打印一个空行：`System.out.println();`
	
- System.out 还有一个print方法，它不在输出之后增加换行符。例如，System.out.print("Hello")打印“Hello”之后不换行，后面的输出紧跟在“o”之后。

### main
---
main方法没有为操作系统返回“退出码”。如果 main方法正常退出，那么 Java应用程
序的退出码为0,表示成功地运行了程序。如果希望在终止程序时返回其他的退出码，
那就需要使用Systen.exit 方法。

### 数值类型
---
1. Java==没有无符号==(unsigned)形式的int、long、short或 byte类型；
	   
2. 在Java中，所有的数值类型所占据的 **==字节数与平台无关==** （而C++则与平台相关，比如在32位处理器上long值为4字节，在64位处理器上则为8字节）；
	
3. “ 浮点数值不适用于无法接受舍入误差的计算中。例如，`System.out.println（2.0–1.1）`将打印出`0.8999999999999999`，而不是`0.9`。原因是浮点数值采用二进制系统表示，而在二进制系统中**无法精确地表示分数1/10**。这就好像十进制无法精确地表示分数1/3一样。如果在数值计算中不允许有任何舍入误差，就应该使用**`BigDecimal类`**，本章稍后将介绍这个类。”
	
4. 有`boolean`而无`bool`

### 常量
---
- 关键字`final`指示常量：`final double CM_PER_INCH=2.54;`
- `final`表示这个变量只能被赋值一次。一旦被赋值之后，就**不能够再更改**了。习惯上，常量名使用**全大写**；

### /与%
---
- 当参与`/`运算的两个操作数都是整数时，表示整数除法；否则只要操作数有一个浮点数，就表示浮点除法
	
	15/2等于7
	15.0/2等于7.5
	15%2等于1

- 整数被0除将会产生一个异常，而浮点数被0除将会得到无穷大或NaN结果。

### java.lang.Math
---
在Math类中，包含了各种各样的数学函数，如 $x^2$: `sqrt(x)`, $x^a$: `pow(x,a)`等

### 类型转换
---
#### 1）精度损失
![[截屏2025-03-18 16.11.24.png|350]]
图中有6个实线箭头，表示无信息丢失的转换；
另外有3个虚线箭头，表示可能有精度损失的转换。

结合下表发现：从字节数小的数据类型 **向大字节数据类型转换** 都是**无精度损失**的(如int->long)，而向 **相同/更小** 字节数的类型转换(int->float, long->float)都是可能有精度损失的
![[截屏2025-03-18 16.16.11.png|200]]

#### 2）隐式转换

如果两个操作数中有一个是double类型，另一个操作数就会转换为double类型。
	
- 否则，如果其中一个操作数是float类型，另一个操作数将会转换为float类型。
	
- 否则，如果其中一个操作数是long类型，另一个操作数将会转换为 long类型。
	
- 否则，两个操作数都将被转换为int类型。

#### 3）强制转换

```java
double x=9.997;
int nx=(int)x; //nx=9
```


### 移位运算
---
- 在C/C++中，不能保证>>是完成算术移位(扩展符号位)还是逻辑移位(填充0)
- 在Java中没有这个困惑：>>>运算符会用0填充高位，而>>会用符号位填充高位。

>移位运算符的右操作数要完成模32的运算(除非左操作数是long类型，在这种
情况下需要对右操作数模64)。例如，1<35的值等同于1<3或8。

### 字符串
---
#### 1）操作
1. `substirng(index1,index2)`方法可以从一个较大的字符串提取出一个子串；
	
2. `+`用于拼接
	   
3. 当将一个字符串与一个非字符串的值进行拼接时，后者会转换成字符
```java
int age=13;
String rating="PG"+ age;  //rating="PG13"
```
	
4. `join()`：多个字符串放在一起，用一个界定符分隔
```java
String all = String.join("/","S°,"N","L,"XL");
// all is the string "S/M/L/XL
```
	
5. `repeat()`
	
```java
String repeated ="Java*,repeat(3);// repeated is "JavaJavaJava°
```

#### 2）不可变性
- String类没有提供修改字符串中某个字符的方法，即不能修改Java字符串中的单个字符。修改字符串只能通过提取想要保留的子串，再与希望替换的字符拼接：`greeting=greeting.substring(θ,3)+"p!";`
	
- 可以想象将各种字符串存放在公共的存储池中。字符串变量指向存储池中相应的位置。如果复制一个字符串变量，原始字符串与复制的字符串共享相同的字符。
	
- C程序员第一次接触Java字符串的时候，常常会感到迷惑，因为他们总将字符串认
	为是字符数组：`char greeting[]="Hello";`

- 这种认识是错误的，Java字符串大致类似于 `char*`指针，
	`char* greeting ="Hello°;`

#### 3）字符串判等——`str1.equals(str2)`

- str1, str2也可以是字符串常量，如`"Hello".equals(greeting)`
- ==一定不要使用`==`运算符检测两个字符串是否相等==！这个运算符只能够确定两个字符串是否存放在同一个位置上。

#### 4）构建字符串

如果需要用许多小段的字符串来构建一个字符串，那么用`+`来拼接会很麻烦，应该按照下列步骤进行：
1. 首先构建一个空的字符串构建器：
```java
StringBuilder builder = new StringBuilder();
```
2. 当每次需要添加一部分内容时，就调用append方法。
```java
builder.append(ch);// appends a single character
builder.append(str);// appends a string
```
3. 在字符串构建完成时就调用 toString方法，将可以得到一个String对象，其中包含了构建器中的字符序列。
```java
String completedString = builder.toString();
```

### 输入/输出
---
#### 1）读取输入

1. 读取整行
```java
import java.util.*;  //Scanner类定义在java.util包中
Scanner in= new Scanner(System.in);
String name = in.nextLine();  //nextLine方法将读取一行输入(无视空格)
```
2. 读取一个单词（以空格为分隔符）
```java
String firstName = in.next();
```
3. 读取一个整数
```java
int age= in.nextInt();
```
4. 读取浮点数
```java
int num= in.nextDouble();
```

#### 2）格式化输出
	
```java
double x= 10000.0/3.0;  //输出8个字符，且精度为小数点后2个字符。
System.out.printf("8.2f",x);  //输出3333.33
```
	
![[截屏2025-03-18 17.04.31.png|500]]

### 3）文件输入/输出

1. 读取文件
```java
Scanner in = new Scanner(Path.of("myfile.txt"),StandardCharsets.UTF_8);
//然后就可以利用前面介绍的任何一个Scanner方法对文件进行读取这个文件了
```
2. 写入文件
```java
PrintWriter out = new PrintWriter("myfile.txt",StandardCharsets.UTF_8);
//然后就可以像输出到System.out一样使用print、println以及printf命令
```
