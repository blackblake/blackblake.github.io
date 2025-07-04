---
title: 4.7 data_hazard
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
---

### （一）例子

```c
sub x2, x1, x3 // Register z2 written by sub
and x12, x2, x5 // 1st operand(x2) depends on sub
or x13, x6, x2 // 2nd operand(x2) depends on sub
add x14, x2, x2 // 1st(x2) & 2nd(x2) depend on sub
sd x15, 100(x2) // Base (x2) depends on sub
```

![Pasted image 20241218173258](/assets/Image/Pasted image 20241218173258.png){: w="500"}

- 如图，紧接着sub指令后面，要使用x2的and、or指令发生了数据冒险（蓝线向后）
- 但add指令并没有产生冒险，因为规定写操作发生在一个时钟周期的**前半部分**，而读操作发生在**后半部分**，所以读操作会安全地得到本周期内被写入的值。


### （二）数据冒险的分类
---
![Pasted image 20250110034225](/assets/Image/Pasted image 20250110034225.png){: w="300"}
    - `RegisterRs`：源寄存器 1
    - `RegisterRt`：源寄存器 2
    - `RegisterRd`：目的寄存器

###### **1a. `EX/MEM.RegisterRd = ID/EX.RegisterRs`**

- 表示当前处于 **存储阶段** 的指令目标寄存器（`RegisterRd`）与处于 **译码阶段** 的指令的第一个源寄存器（`RegisterRs`）相同。

###### **1b. `EX/MEM.RegisterRd = ID/EX.RegisterRt`**

- 表示当前处于 **存储阶段** 的指令目标寄存器（`RegisterRd`）与处于 **译码阶段** 的指令的第二个源寄存器（`RegisterRt`）相同。

###### **2a. `MEM/WB.RegisterRd = ID/EX.RegisterRs`**

- 表示当前处于 **写回阶段** 的指令目标寄存器（`RegisterRd`）与处于 **译码阶段** 的指令的第一个源寄存器（`RegisterRs`）相同。

###### **2b. `MEM/WB.RegisterRd = ID/EX.RegisterRt`**

- 表示当前处于 **写回阶段** 的指令目标寄存器（`RegisterRd`）与处于 **译码阶段** 的指令的第二个源寄存器（`RegisterRt`）相同。
---
###### EXA
![Pasted image 20250110034723](/assets/Image/Pasted image 20250110034723.png){: w="500"}
- 当sub指令执行到**MEM**阶段时，and指令处于**EX**阶段，所以确定sub-and的类型为EX/**MEM**. RegisterRd = ID/**EX**. RegisterRs（高亮的部分由sub、and分别处于的阶段来确定，Rs还是Rt看具体情况）
- 不论是类型1还是2，RegisterRs/t前面的一定是ID/EX，判断类型主要是根据：当前需要该寄存器作为操作数的指令（and,or）**处于EX阶段时，将该寄存器作为目的寄存器的指令（sub）是处于MEM还是WB阶段；**
- 注意流水线寄存器的表示方法："/"后面的是正在执行的阶段


##### 两点补充
- 但是，直接采用总是旁路的方式解决冒险是不正确的，因为某些指令可能不写回寄存器，就会产生一些不必要的旁路，所以需要通过检测流水线寄存器在 EX/MEM 级的 WB 控制字段以确定 **RegWrite 是否有效**
- 其次，还要考虑x0不能作为目标寄存器： 要在第一类冒险条件中加入附加条件 EX/MEM RegisterRd≠, 0 , 在第二类冒险条件中加入附加条件 MEM WB. RegisterRd≠0


### （三）旁路/前递的数据通路
![Pasted image 20250110044816](/assets/Image/Pasted image 20250110044816.png){: w="500"}
前递单元：以ID/EX的Rt、Rs和EX/MEM、MEM/WB的Rd作为输入，输出的控制信号控制ALU的两个操作数的MUX
![Pasted image 20250110045131](/assets/Image/Pasted image 20250110045131.png){: w="500"}

对于1a,1b类数据冒险，即MEM冒险，ForwardA, ForwardB设置为10；
对于2a,2b类数据冒险，即WB冒险，ForwardA, ForwardB设置为01；
若无冒险，则ForwardA, ForwardB设置为00；

### （四）无法用前递解决的数据冒险
---
1. 当有一条试图**读取一个 由前一条load指令读入的寄存器** 时，无法使用前递解决数据冒险，必须采用相应的机制**阻塞流水线**。
	![Pasted image 20250110045625](/assets/Image/Pasted image 20250110045625.png){: w="500"}

2. **冒险检测单元**
	![Pasted image 20250110045852](/assets/Image/Pasted image 20250110045852.png){: w="300"}
- 因为读取数据存储器的指令一定是load指令，所以第一行条件“if ID/EX.MemRead”检查指令是否是load指令；
- 后面的两行是检测在 EX 级的装载指令的目的寄存器是否与在 ID 级的指令的某个源寄存器相匹配
- 如果条件成立，指令将阻塞一个时钟周期
- 经过这一个周期的阻塞，前递逻辑就可以处理相关性并继续执行程序了；
	如果没有采用旁路，那么还需要多阻塞一个周期

3. 如果处于 ID 级的指令被阻塞，那么处于 IF 级的指令也必须被阻塞，否则，已取到的指
令就会丢失！防止这两条指令继续执行的方法是保持 PC 寄存器和 IF/ID 流水线寄存器不变。
	如果这些寄存器内容保持不变，在 IF 级的指令将继续使用相同的 PC 取指令，而在 ID 级将继
续使用 IF/ID 流水线寄存器中的相同的指令字段读寄存器堆

4.  **插入停顿/气泡/空指令的方法**
**把 ID/EX 流水线寄存器的 EX、MEM、WB 所有级的控制信号都置为0**
	这些控制信号在每个时钟周期都向前传递，但不会产生不 良后果，因为如果控制信号都是 0, 那么所有寄存器和存储器都不进行写操作。