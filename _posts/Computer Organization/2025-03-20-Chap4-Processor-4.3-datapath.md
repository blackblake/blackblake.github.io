---
title: 4.3 datapath
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
math: true
---

### 4.3 基本的数据通路
---
-  默写PC、Registers、Data Memory、ALU的示意图（带上控制信号）
	
-  Registers只有一个***RegWrite***控制信号（因为Registers是一定要被read的，无需设置MemRead），而Data Memory有***MemRead和MemWrite***这两个控制信号
	
-  ImmGen-- 如果是load, store或分支条件成立时的Branch分支指令，则它会将指令中的12位imm**符号**扩展为32位结果输出
	
-  load、store和branch指令的立即数都是**12位**的吗？是
	
-  设计一个Shift left的意义：计算branch分支目标地址时，需要将偏移量左移1位以表示半字为单位的偏移量，使偏移量的有效范围扩大到2倍。所以偏移量在经过ImmGen的符号扩展后，还要被Shift left左移1位，再进入Add加法器与PC相加（这个加法器是为了branch指令专门新加的）
  （分支目标地址=分支指令所在地址+指令中的偏移量）
	
-  Shift left的机制：它只是简单地给符号扩展后的偏移量的低位加上一个$0_2$，因为偏移量是从12位扩展而来的，所以移位只丢弃符号位（没懂） 
	
-  默写branch指令的完整的datapath(p172图4-9)
	
-  branch指令用ALU判断reg1和reg2存储的值是否相等。但该ALU提供的是一个表示结果是否为0的输出信号，故方法是将ALU控制设置为减法，如果ALU输出的**0信号有效**，则说明reg1\==reg2
	
-  根据add,ld,sw,branch这四种基本的指令，逐步构建一个较完整的数通路（p174图4-11）记住：**有3个mux，2个add**
	
- 3个mux分别叫什么？ALUsrc、MemtoReg、PCsrc
	
- 画图的时候按以下步骤：
  1. 第一步当然是先画PC, InsMem, Registers, ALU, DataMem**五大件**
  2. 然后把**mux、add**画上去
  3. 最后再连线（这样就不必擦来擦去了）

### 4.4 控制
---
##### ALU operation控制信号的生成
- 在画ALU的示意图的时候，应当注意到了4-bit的ALU operation控制信号输入。那么这4个bit控制ALU的什么？（and,or,add,sub四种运算）又是怎样控制的？（通过取0000,0001,0010,0110四种值）
	
- 我们知道ALU在不同指令下做不同的运算，即ALU operation控制信号在不同的指令下取不同的值，那么它的0000,0001,0010,0110这四种取值又是由什么确定的呢？
	
- 1.有一个小型控制单元，它输入指令的funct7, funct3字段和2位的ALUOp字段。ALUOp指明要执行的操作是load和store指令要做的加法($00_2$)，还是beq指令要做的减法并检测是否为0($01_2$)，或是由funct7和funct3字段决定($10_2$)；（ALUOp是由指令类型决定的）
  2. 该控制单元输出一个4位信号，即前面介绍的4位组合之一来直接控制ALU，具体如何设置的原理如下：![Pasted image 20241123031357](/assets/Image/Pasted image 20241123031357.png)
	a.当ALUOp为00或01时，ALU操作不依赖于funct7或funct3字段，这种情况下“不关心”操作码的值，所以将其记为一串X；
	b.当ALUOp为10时，根据funct7和funct3来设置ALU的输入控制信号
	

-  简化：由于只有少数funct字段有意义，并且funct仅在ALUOp位等于10时才被"关心"，因此可以使用一个小逻辑单元来输出ALU operation控制信号：![Pasted image 20241123032303](/assets/Image/Pasted image 20241123032303.png)

##### 其他控制信号
- PCsrc：Branch控制单元确定的“branch if equal”**＋**ALU的0输出有效
	
- 其它控制信号：由指令opcode+funct字段设置
	
-  ![Pasted image 20241123162843](/assets/Image/Pasted image 20241123162843.png)
	
- 默写完整的、带所有控制单元、控制信号、mux、add的数据通路
	![Pasted image 20241024171404](/assets/Image/Pasted image 20241024171404.png)
	
- 为什么这个输入是Instruction\[31-0]？是把整个指令都作为ImmGen、Write data的输入吗？
	![Pasted image 20241123163435](/assets/Image/Pasted image 20241123163435.png){: w="300"}
	
- 注意ALU control的输入不是指令的\[31,0] 字段，而是\[30,14-12]
	
- 注意这些输入字段各是多少
	![Pasted image 20241123163955](/assets/Image/Pasted image 20241123163955.png)
	第一个\[6,0]是control unit的输入，即opcode字段

---