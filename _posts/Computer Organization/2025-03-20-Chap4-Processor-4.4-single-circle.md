---
title: 4.4 single-circle
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
math: true
---

# Build DataPath  
#### (R-Type for E.g.)

### 1. R-Type

##### 1）PC 
![Pasted image 20241023210922](/assets/Image/Pasted image 20241023210922.png)

##### **2）寄存器堆(register file)**
![Pasted image 20241023211319](/assets/Image/Pasted image 20241023211319.png)

##### 以add x1, x2, x3为例：

  a) 由于R型指令有三个寄存器操作数x1,x2,x3，每条指令需要从寄存器堆中读出两个Data，再写入一个Data。
	  
  b)   为读出一个Data，需要一个输入指定要读的寄存器编号（注意 **输入的是寄存器的 [编号]**），以及一个从寄存器堆读出的输出（**输出的Read data1, Read data2和register1, register2 是[对应]的）**；
    为写入一个数据字，寄存器堆需要两个输入：一个输入指定要写的寄存器号，另一个提供要写入寄存器的数据；
	  
  c) Write操作由控制信号 **RegWrite** 控制，在写操作发生的时钟边沿，写控制信号必须是 **有效(asserted)** 的（这里的表述是 "RegWrite是有效的" 而非 "RegWrite为1" , 是因为有时可能低电平0才是有效的）；
	  
  d) 如图4-7所示，我们总共需要四个输入（三个寄存器编号和一个写入数据）和两个输出（两个读出的数据）​。输入的寄存器编号为 **5位宽** ，用于指定 $2^5=32$ 个寄存器中的一个；
  

### 2. Load/Store
---
**以lw/sw x1 , offset(x2)为例：**

![Pasted image 20241023214659](/assets/Image/Pasted image 20241023214659.png)

##### （1）数据存储单元
a) 必须输入Address，否则无法知道要对哪个地址的data进行读/写；
	
b) 是启用Read data从内存中读取数据，还是启用Write data向内存中写入data，取决于MemRead和MemWrite哪个有效(asserted)，但二者不可能同时有效；
	
**Registers只有一个RegWrite控制信号（因为Registers是一定要被read的，无需设置MemRead），而Data Memory有MemRead和MemWrite这两个控制信号**

##### （2）立即数生成器 (ImmGen)
ImmGen有一个32位指令的输入，如果是**load, store或分支条件成立时的Branch分支指令，则它会 **将指令中的一个12位字段[符号扩展]为32位结果输出** **（load和store的立即数也都是12位！）

### 3. Branch
---
**以beq x1, x2, offset为例：**
第三个操作数是12位的偏移量offset，如果x1≠x2,就会跳转到"相对于分支指令所在地址的分支目标地址"
**由于offset是**12位**的，所以为了实现beq指令，需将PC值与[符号扩展后的]指令偏移量offset相加以得到分支目标地址**

##### （1）一些规定

• 指令系统体系结构规定了计算分支目标地址的 **基址** 是分支指令所在地址；
• 指令系统体系结构还说明了计算分支目标地址时，**将偏移量左移1位** 以表示半字为单位的偏移量，这样偏移量的有效范围就扩大到2倍，使指令可以跳转到更远的地址；

在RISC-V指令系统的体系结构中，当计算分支的目标地址时，使用的偏移量是以“半字”（16位）为单位的。为了将这个偏移量转换为以字节为单位的偏移量，系统需要将偏移量左移1位,也就是将数字乘以2,使得有效的偏移量范围扩大到2倍。

##### （2）DataPath

![Pasted image 20241024150600](/assets/Image/Pasted image 20241024150600.png)
 
 这个数据通路实现了两个操作：
	a.计算分支目标地址Address (由Add实现--PC+offset) 
	b.检测分支条件 (由ALU实现)

##### （3）检测分支条件的机制

- 分支指令的数据通路执行两个操作：**计算目标地址**和**检测分支条件**；
	
- 为计算分支目标地址，分支指令数据通路包含一个ImmGen和一个加法器Add。为执行比较，需要寄存器堆(register file)提供两个寄存器操作数​。此外，使用ALU完成相等性比较；
	
- 由于该ALU提供一个表示结果是否为0的输出信号，故可 **将两个寄存器操作数发给ALU，并将控制设置为减法。如果ALU输出的零信号有效，可知两个寄存器值相等** ；

### 4. 建立数据通路
---

![Pasted image 20241024152614](/assets/Image/Pasted image 20241024152614.png)
`组合不同类型指令所需的功能单元，形成RISC-V指令系统的简单数据通路`

但这里缺少了控制单元，我们接下来讨论Control


# Control

### ALU工作原理

ALU有四根输入控制线，它们有以下四种组合，分别决定4种算术计算：
![Pasted image 20241024154112](/assets/Image/Pasted image 20241024154112.png)
根据不同的指令类型，ALU需执行以上四种功能中的一种：
	- 对于load和store指令，ALU做加法计算存储器地址；
	- 对于R型指令，根据指令的7位funct7字段（位31:25）和3位funct3字段（位14:12）​​，ALU需执行四种操作（与、或、加、减）中的一种；
	- 对于条件分支指令，ALU将两个操作数做减法并检测结果是否为0；

![Pasted image 20241024160153](/assets/Image/Pasted image 20241024160153.png)

**指令被decode后，其类型决定了ALUOp的值，共有00、01、10三种取值：**
- 如果ALUOp=00或01，则ALU操作不依赖于funct7或funct3字段，在这种情况下，​“不关心”操作码的值，所以将其记为一串X；
- 当ALUOp为10时，根据funct7和funct3字段来设置ALU的输入控制信号

**所以，ALU的工作原理是这样的：**
   `指令类型` —>`ALUOp`
   `funct3, funct7`+`ALUOp`—>`ALU control input`
其中自变量是指令类型、funct3、funct7，中间要素是ALUOp(由指令类型决定)，最终结果是生成**ALU control input**，它**直接[根据此图](obsidian://open?vault=Obsidian%20Vault&file=Images%2FPasted%20image%2020241024154112.png)决定ALU的操作**

![Pasted image 20241024164213](/assets/Image/Pasted image 20241024164213.png)

### 控制单元(Control Unit)

##### 添加了control lines和MUX后的datapath
![Pasted image 20241024165532](/assets/Image/Pasted image 20241024165532.png)
##### **各control signal的作用**
![Pasted image 20241024170244](/assets/Image/Pasted image 20241024170244.png)

> [!NOTE] 记忆
> **3个MUX控制信号、3个读/写(read/write)信号**


解释：
- 由于每个MUX都有2个输入，所以每个MUX都需要一条单独的控制线
	
-  4.20是对4.19种每个控制信号的解释
	
-  `ALUSrs`是"ALU Sources"的意思，即选择ALU的输入数据的MUX
	
-  **除`PCSrc`外，所有的控制信号可由控制单元 仅根据指令的Opcode和funct字段设置**；
	
- `PCSrc`是例外：若指令是beq（由控制单元确定）并且做相等检测的ALU的零输出有效，那么PCSrc控制信号有效。**为生成PCSrc信号，需要将来自控制单元（称为“Branch”​）的信号与来自ALU的零输出信号相“与”​** ；
（若Branch信号和ALU的零输出信号相与的结果有效asserted，说明二者皆为有效，即当前指令是一个B型分支指令且满足分支条件，将执行跳转）

##### 添加control unit后的datapath
![Pasted image 20241024171404](/assets/Image/Pasted image 20241024171404.png)
控制单元Control Unit的输入是指令的7位Opcode--**Instruction\[6,0]**；

> [!NOTE] 记忆

> 1）为了便于记忆，记一下PC、Ins-Memo、寄存器堆、ALU、Data-Memo的端口数：**2-2-6-3-3**；

> 2）如果考试要求画出这个图，就先后实现add, lw, sw, beq这四个指令，一步步完善；> 

> 3）只有两个Add加法器，全都用在PC的地址计算上；其他计算全用ALU

##### 各指令类型所对应的各个控制信号的值
![Pasted image 20241024171636](/assets/Image/Pasted image 20241024171636.png)

##### 各类型指令的代表示例（用于帮助理解）
R型--`add  rd, rs1, rs2`
I型--`addi  rd, rs1, imm`,  `lw rd, imm(rs1)`
S型--`sw  rs2, imm(rs1)`
B型--`beq  rs1, rs2, label`