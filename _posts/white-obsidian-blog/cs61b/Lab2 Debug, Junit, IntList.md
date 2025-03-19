---
title: lab2
categories:
  - cs61b
---
[Debugging-guide](https://sp21.datastructur.es/materials/guides/debugging-guide.html)

## Debug 
---
1. 调试模式下, 当前高亮部分并非程序已执行的步骤, 而是程序**将要**执行的.

2. 如果一个类不含有`main(String[] args)`而只写了一些方法, 那么我们会发现它在IntelliJ中也可以被`run`或`debug`, 只不过运行/调试的是调用它的那另一个类！（如果该类成员未被其他类调用则无法运行）

3. 点击屏幕最下方的 [AddConstantTest.java:12]，Junit会自动跳转到测试出错的代码行, 在我们自己编码时也可以这样做   ![[Pasted image 20250228213258.png]]

4. 调试操作 ![[Pasted image 20250228213646.png|60]]
	第一个图标是`step over`, 不会进入函数体；
	第二个图标是`step into`, 会进入函数体逐步骤执行；
	第三个图标是`step out`, 会跳出当前函数体；
