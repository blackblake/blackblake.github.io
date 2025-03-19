---
title: lab3
categories:
  - cs61b
---
## 1️⃣总结
---
1. Timing Tests：**测量算法时间效率的方法** （`stopwatch`, `microsec/op`）
2. 条件断点

## 2️⃣IntelliJ Configuration : 
---
#### 1）源代码根目录

> 为什么lab1和其他文件的颜色不一样？而且在application的main设置中也无法选择lab1之外的.java文件

 lab1 文件夹显示为蓝色，而其他文件夹 (.idea, lab2, lab3) 显示为灰色，这是因为 IntelliJ IDEA 使用不同的颜色来表示不同类型或状态的文件夹。这种颜色差异通常有以下几种可能的原因：

1. ****源代码根目录标记****：蓝色通常表示该文件夹被标记为源代码根目录（Source Root）。在 IntelliJ 中，源代码根目录是编译器查找源文件的特殊目录。
2. ****内容根目录****：蓝色可能表示该文件夹是一个内容根目录（Content Root）或模块目录。  
3. ****不同的模块****：lab1 可能是一个独立的模块，而其他文件夹属于不同的模块或不是模块。
  
关于无法在 Application 的 main 设置中选择 lab1 之外的 .java 文件，这可能是因为：

1. 其他 lab 文件夹中没有包含 main 方法的类文件

2. 其他 lab 文件夹没有被正确标记为源代码目录

3. 其他 lab 文件夹中的 Java 文件可能有编译错误

##### 解决方法：

1. ****将其他 lab 文件夹标记为源代码根目录****：

   - 右键点击 lab2 或 lab3 文件夹

   - 选择 "Mark Directory as" > "Sources Root"
   - ![[截屏2025-03-06 11.02.14.png|300]]
  ---
  
#### 2）`Application`和`Junit`

> 这两个都是IntelliJ的run configuration的选项，如果有要测试的类，就用`Junit`，普通的运行就配置为Application。


## 3️⃣`Algs4.jar`的StopWatch秒表类
---
```java
import edu.princeton.cs.algs4.Stopwatch;

public class StopwatchDemo {
    
    private static int fib(int n) {
        if (n < 0) {
            return 0;
        }
        if (n == 1) {
            return 1;
        }
        return fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) {
        Stopwatch sw = new Stopwatch();
        
        int fib41 = fib(41);
        
        double timeInSeconds = sw.elapsedTime();
        
        System.out.println("Time taken to compute 41st fibonacci number: " + timeInSeconds + " seconds.");
    }
}

```

上面的代码以计算斐波那契数列的算法`fib()`为例，使用stopwatch类对象sw来统计fib算法的执行时间。

通常，一个 Stopwatch 类的工作原理如下：

1. 创建实例时，它会记录当前系统时间作为起始点。
2. 当调用 `elapsedTime()` 方法时，它会再次获取当前系统时间，然后计算与起始点的时间差。
3. 返回的时间差通常以秒为单位。

## 4️⃣创建数组的语法
---
```cpp
AList<Integer> Ns = new AList<Integer>();//括号里填什么----不用填!
```

## 5️⃣导入`Junit`包的语句
---
```java
import org.junit.Test;
import static org.junit.Assert.*;
```
这两个import语句是Java语言中用于单元测试的导入语句，它们来自JUnit测试框架。

1. `import org.junit.Test;` - 导入JUnit框架的Test注解。在Java中，你可以使用@Test注解来标记测试方法，这样JUnit测试运行器就知道哪些方法是需要执行的测试。
    
2. `import static org.junit.Assert.*;` - 这是一个静态导入，它导入了JUnit Assert类中的所有静态方法，如assertEquals(), assertTrue(), assertFalse()等。这些方法用于在测试中验证预期结果。

## 6️⃣什么时候加`@Test`
---
>什么时候需要加 @Test ？

- **测试方法需要添加**：任何你希望JUnit测试运行器自动执行的测试方法都需要添加`@Test`注解。
- **方法级别而非类级别**：`@Test`注解应用于方法，而非类。
- **公共无参方法**：被`@Test`注解的方法通常应该是public、无参数、无返回值(void)的方法。

>什么时候不能加 @Test ？

- **辅助方法**：测试类中的辅助方法不需要`@Test`注解。
- **setUp和tearDown方法**：这些方法使用`@Before`/`@After`或`@BeforeEach`/`@AfterEach`注解。
- 带参数的方法、private方法、有返回值的方法 都不能带`@Test`，否则会造成紊乱。

## 7️⃣条件断点
---
在原来断点的基础上右击，可以设置断点条件，满足条件才暂停
![[截屏2025-03-06 14.36.46.png|500]]

## 8️⃣Resume按键和执行断点
---
#### 1）Resume按钮

Resume按钮（通常显示为绿色三角形图标）是调试过程中的继续执行功能。当程序在断点处暂停时，点击Resume按钮会让程序继续运行，直到遇到 **下一个断点** 或程序结束。

**功能特点：**
- 不同于"单步执行"，Resume会运行所有代码直到下一个断点

#### 2）执行断点（Evaluate Expression）

执行断点（或称为条件断点/表达式求值）允许你在调试暂停时评估任意代码表达式，而不需要修改源代码：

**实用场景：**

- 检查复杂表达式的值
- 调用当前上下文中的方法
- 在运行时测试修复方案
- 在不改变代码的情况下修改变量值

除了执行断点表达式，IntelliJ还提供了条件断点功能，你可以右击断点，设置条件表达式，只有当条件为true时才会暂停程序执行。

#### 3）条件断点vs.执行断点
[见bilibili收藏夹]
##### 条件断点 (Conditional Breakpoint)

条件断点是一种特殊类型的断点，它只有在满足指定条件时才会触发程序暂停（比如我想直接跳到我想开始调试的地方，但是由于递归调用等等因素没法用单纯的在某一行打断点来调试，那么就在该行设置一个条件断点，点击调试，就能直接跳转到满足这个条件式的地方）。

- 在设置断点后，右键单击断点并添加条件表达式
- 程序每次运行到该断点位置时，都会评估条件表达式
- 只有当条件表达式计算结果为true时，程序才会暂停
- 例如：`index > 5 && list.size() > 10`

##### 执行表达式 (Evaluate Expression)

"执行表达式"通常指的是在程序已经暂停的情况下，临时执行某个Java表达式的功能。

**特点：**

- 通过Alt+F8或调试菜单访问
- 可以在程序暂停状态下随时执行
- 允许评估任何有效的表达式，查看结果，甚至修改变量值
- 不会自动触发程序暂停，而是在已暂停的状态下使用
