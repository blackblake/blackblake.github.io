---
title: 4.6 pipelined_datapath
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
---

## Part I: Datapath
---
##### 1. 流水线寄存器
![Pasted image 20241218165212](/assets/Image/Pasted image 20241218165212.png){: w="600"}

- **寄存器的位宽**：必须足够大以存储通过它们的所有数据。例如，IF/ID寄存器的位宽必须为96位，因为它需要同时存储从存储器中提取出的32位指令以及自增的64位PC地址。目前，其他三个流水线寄存器的位宽分别为256位、193位和128位；

- 在发生例外时，PC中的内容必须被保存，而流水线寄存器中的内容则可以被丢弃；

##### 2. E.g. 流水线寄存器的使用(ld)

![Pasted image 20241218165748](/assets/Image/Pasted image 20241218165748.png){: w="500"}
![Pasted image 20241218165815](/assets/Image/Pasted image 20241218165815.png){: w="500"}
![Pasted image 20241218165834](/assets/Image/Pasted image 20241218165834.png){: w="500"}

（**左写右读**）

##### 3. 新增数据通路

问题：在ld指令流水的WB阶段，我们将要改写哪个寄存器？
- IF/ID流水线寄存器中的指令提供了写入寄存器编号。但是，这条“指令”是ld指令的**下一条指令**，所以 **此时IF/ID中的寄存器编号并不属于ld指令要写入的那个寄存器！**
- 所以，**我们需要添加一条数据通路，以保存ld指令的写入目的寄存器的编号**：这条通路 **从IF/ID出来，沿途经过后面的各个流水线寄存器** ，一直将写入目的寄存器的编号保存，直到进入WB阶段，此时该编号被存储在MEM/WB寄存器中，于是连接到Rigisters寄存器堆的 **Write register端口** (即目的寄存器编号的输入端口，下面的Write data是所要写入的数据内容的输入端口) 

  ![Pasted image 20241218171401](/assets/Image/Pasted image 20241218171401.png){: w="500"}

##### 4. 流水线的图形化表示

  1）多时钟周期图
  
![Pasted image 20241218171955](/assets/Image/Pasted image 20241218171955.png){: w="500"}

2）单时钟周期图（是多时钟周期图的一个垂直切片）

![Pasted image 20241218172158](/assets/Image/Pasted image 20241218172158.png){: w="500"}


## Part II: Control
---
##### 1. 复制了单周期的所有控制信号

##### 2. 根据流水线阶段 将控制线划分为五组
IF,ID：无

EX：ALUOp和ALUSrc

MEM：Branch、MemRead和MemWrite

WB：MemtoReg(决定是将ALU结果还是将存储器值发送到寄存器堆中)和RegWrite(写入所选值)

##### 3. 传递控制信号

传递这些控制信号最简单的方式就是 **扩展流水线寄存器** 以包含这些控制信息
![Pasted image 20241218172956](/assets/Image/Pasted image 20241218172956.png){: w="350"}

WB、M、EX分别是按组分好后的控制信号（ID、IF无需控制信号，不用传递）