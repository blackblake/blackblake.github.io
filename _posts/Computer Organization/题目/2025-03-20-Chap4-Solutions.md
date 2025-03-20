---
title: "chap4_solutions"
date: 2025-03-20 03:39:16 +0800
categories: [cod, solutions]
tags: [cod]     # TAG names should always be lowercase
---
### 4.1  
---
考虑如下指令
and rd, rs1, rs2
解释：Reg\[rd]=Reg\[rs1] AND Reg\[rs2]

**4.1.1　对于上述指令，图4-10中的控制信号各是什么数值？**
![[Pasted image 20241024204005.png|500]]

###### ==**在控制信号(control signals)中，值的表示方法如下：**==
- 对于ALUop：如果不记得00, 01, 10对应什么运算，可以直接写[and], [or], 
[add],[ sub]；
	
- 读/写信号(read/write)用[true] ,[false]表示；
	
- MUX的控制信号用[0],[1]表示 

**4.1.2　对于上述指令，将用到哪些功能单元？**
Registers, ALUsrc mux, ALU, and the MemToReg mux.
###### ==**`mux`也是功能单元，不要忽略**==

**4.1.3　对于上述指令，哪些功能单元不产生任何输出？哪些功能单元的输出不会被用到？**
所有块都会产生一些输出，但不使用datammemory和ImmGen的输出。
###### ==无论什么指令类型，所有的功能单元都会产生输出==，只不过如果没用到的unit若没有输入，就会输出默认值



### 4.3
---
![[Pasted image 20241024205027.png|500]]
4.3.1　发生数据访存的指令所占比例？
**25 + 10 = 35%. Only Load and Store use Data memory**
 
4.3.2　发生指令访存的指令所占比例？
**100%. Every instruction must be fetched from instruction memory before it can be executed.**

4.3.3　使用符号扩展的指令所占比例？
**28 + 25 + 10 + 11 + 2 = 76%. ==只有 R-type 不使用符号扩展==**

4.3.4　当不需要符号扩展的结果时，符号扩展单元的行为是什么？
**The sign extend produces an output during every cycle. If its output is not needed, it is simply ignored.**


### 4.4
在制造硅芯片时，材料（例如硅）缺陷和制造错误会导致电路故障。一个非常常见的故障是，信号线发生“断路”​，导致总是保持逻辑“0”​。这被称为“固定为0”故障。

**4.4.1　如果MemToReg信号发生以上故障，哪些指令会执行错误？**
Only loads are broken. MemToReg is either 1 or “don’t care” for all other instructions.

**4.4.2　如果ALUSrc信号发生以上故障，哪些指令会执行错误？**
I-type, loads , stores are all broken.
==B和J型的PC地址计算用的是Add加法器，不是用ALU，所以不会被影响！==

### 4.5
---
假设本周期处理器取来指令：0x00c6ba32

**4.5.1　此时ALU控制单元的输入值是多少？**
Th e encoded instruction is sd x12, 20(x13)
![[Pasted image 20241024205630.png]]
[详见真值表](obsidian://open?vault=Obsidian%20Vault&file=Images%2FPasted%20image%2020241024160153.png)

**4.5.2　该指令执行结束后新的PC地址是多少？**
Th e new PC is `the old PC + 4`.

**4.5.3　对于每一个多选器，给出执行该指令时的各个输入和输出值，列出寄存器Reg\[xn]中的数值。**
ALUsrc : 
	Inputs: Reg\[x12] and 0x0000000000000014 ; 
	Output: 0x0000000000000014

MemToReg : 
	Inputs: Reg\[x13] + 0x14 and \<undefined> ; 
	output:\<undefined>

Branch: Inputs: PC+4 and 0x000000000000000A

**4.5.4　此时ALU和另两个加法单元的输入数值是多少？**
	-ALU inputs: Reg\[x13] and 0x0000000000000014
	-PC + 4 adder inputs: PC and 4
	-Branch adder inputs: PC and 0x0000000000000028

> [!NOTE] Title
> 1）RISC-V datapath中只有 **2个**Add加法器，而且都是用于PC地址计算的：一个用来PC+4，一个用来PC+offset；
> 2）至于load/store指令的**offset(rs2)**的计算，是借助 **ALU** 的（通过一个**ALUSrs MUX**）


### 4.6
---
**4.6.1　如果要基于图4-25添加I型指令，需要额外的什么逻辑单元？**
No additional logic blocks are needed.

**4.6.2　为addi指令列出控制单元产生的信号值。**
Branch: false（**==除了mux的0和1之外的控制信号都用false和true==来表示是否有效，因为不一定低电平有效还是高电平有效**）
MemRead: false
MemToReg: 0
**ALUop: 10 (or simply saying “==add==” is suffi cient for this problem)**
MemWrite: false
ALUsrc: 1
RegWrite: 1


### 4.7
---
![[Pasted image 20241024210924.png]]
4.7.1　R型指令的延迟是多少？（如果想让这类指令工作正确，时钟周期最少为多少？）
R-type : [30 (read PC)] + 250 + 150 + [25 (ALUrcs mux)] + 200 
\+ [25 (MemtoReg mux)] + [20 (write rd)] = 700ps
`1）注意不要忘了mux的延迟`
`2）ImmGen和Adder的延迟为什么不加进来算？`

4.7.2　lw指令的延迟是多少？
lw : 30 + 250 + 150 + 25 + 200 + [250 (read Data-Memo)] + 25 + 20 = 950 ps

4.7.3　sw指令的延迟是多少？
sw : 30 + 250 + 150 + 200 + 25 + 250 = 905

4.7.4　beq指令的延迟是多少？
beq : 30 + 250 + 150 + 25 + 200 + [5 (branch信号和ALU的零输出相与)] + 25 + 20 = 705

4.7.5　算术、逻辑或者移位指令（I型，非load指令）的延迟是多少？
I-type : 30 + 250 + 150 + 25 + 200 + 25 + 20 = 700ps

4.7.6　该CPU的最小时钟周期是多少？
950ps
###### ==CPU的最小时间周期=耗时最长的一个指令所需的时间==


### 4.8
---
![[Pasted image 20241024214754.png|500]]

Using the results from Problem 4.7, we see that the average time per
instruction is **0.52\*700 + 0.25\*950 +0.11\*905 + 0.12\* 705 = 785.6ps（==加权平均，求这种比例分配所导致的平均的指令执行时间==）**

In contrast, a single-cycle CPU with a “normal” clock would require a
clock cycle time of 950.

Thus, the speedup would be 925/787.6 = 1.174

==加速比=**前/后**，从而若改变cpu后延迟减小则加速比大于1，效率降低则加速比小于1==

### 4.9
---
如果在图4-25的CPU中添加一个乘法器，这将给ALU增添300ps的延迟。但是，由于不再需要对乘法指令进行模拟，指令数量将会减少5%。
4.9.1　改动前后，时钟周期分别是多少？
before: 950; 
after: 1250

4.9.2　通过这个改动，将获得多少加速比？
The running time of a program on the original CPU is 950\*n.
The running time on the improved CPU is 1250\*(0.95)\*n = 1187.5. Th us, the “speedup” is 0.8.

4.9.3　在保证提升性能的条件下，新ALU最低频率是多少？
Because adding a multiply instruction will remove 5% of the instructions,
the cycle time can grow to as much as 950/(0.95) = 1000. Th us, the time
for the ALU can increase by up to 50 (from 200 to 250)

==执行时间=指令数\*每条指令的延迟==



### 4.12
---
尝试添加RISC-V中的指令：swap rs1, rs2。指令释义：Reg\[rs2]=Reg\[rs1]​；Reg\[rs1]=Reg\[rs2]
4.12.1　对于这条指令，需要添加的新功能部件是什么？
No new functional blocks are needed.

4.12.2　现有的哪些功能部件需要改造？
The register fi le needs to be modifi ed so that it can write to two registers
in the same cycle. Th e ALU would also need to be modifi ed to allow read
data 1 or 2 to be passed through to write data 1.

4.12.3　对于这条指令，需要新添加的数据通路是什么？
Th e answer depends on the answer given in 4.12.2: whichever input was
not allowed to pass through the ALU above must now have a data path to
write data 2.

4.12.4　为支持这条指令，为控制单元新添加的控制信号有哪些？
There would need to be a second RegWrite control wire.


### 4.13
---
尝试添加RISC-V中的指令：ss rs1, rs2, imm（存储两数之和）​。指令释义：Mem\[Reg\[rs1]​]=Reg\[rs2]+immediate
4.13.1　对于这条指令，需要添加的新功能部件是什么？
We need some additional muxes to drive the data paths discussed in 4.13.3.

4.13.2　现有的哪些功能部件需要改造？
No functional blocks need to be modifi ed.

4.13.3　对于这条指令，需要新添加的数据通路是什么？
Th ere needs to be a path from the ALU output to data memory’s write
data port. Th ere also needs to be a path from read data 2 directly to Data
memory’s Address input.

4.13.4　为支持这条指令，为控制单元新添加的控制信号有哪些？
These new data paths will need to be driven by muxes. These muxes will
require control wires for the selector.


### 4.16
---
- ==使用流水线的时钟周期=不使用流水线的时钟周期/流水线级数==

### 4.20
---
![[Pasted image 20250110073539.png|200]]
==addi-add属于WB型数据冒险，所以需要stall２个周期，即插入２条NOP==
（MEM型则只需stall一个周期）


### 4.22
---

![[Pasted image 20250110074556.png|600]]

![[Pasted image 20250110074629.png|500]]

- ==“流水线图”不是数据通路图！要知道画什么==
- **sub-bez是==WB==型（因为要等到sub把值写回x17才能用），所以要插入==2个气泡==！**
- **不可能通过NOP来解决==结构==冒险**

### 4.27
---
![[Pasted image 20250110080141.png|200]]
- 不要忽略掉这种==“隔行的冒险”==！
- add-ld和or-sd都属于WB型冒险，所以插入2个nop
- ld-or是 读取ld所加载的寄存器 引发的冒险，所以要停顿2个周期，因为是“隔行”的所以再插入1个就可以了

![[Pasted image 20250110080601.png|500]]

![[Pasted image 20250110081545.png|600]]

==Forward信号：WB型是01，MEM型是10==


### 4.28
---
![[Pasted image 20250110082750.png|600]]
![[Pasted image 20250110082813.png|600]]

4.28.1  ==**失败率×branch指令占比×3**==
  + CPI将变为：1+(1-0.55)(0.25)3 = 1.4125
  + 解释：1-0.55是如此预测的话预测错误的比例，0.25是Branch指令占指令总数的比例，3是因为每条预测错误的branch指令都会导致后续的3条（处于IF,ID,EX级的）指令被废弃。
4.28.2
- CPI=1 + (1 − .55)(.25)3=1.3375
4.28.3
- CPI=1 + (1 − .85)(.25)3=1.1125
4.28.4
- CPI= 1 + (1 − .85)(.125)3
4.28.6 
- The predictor is 25% accurate on the remaining branches. We know that
80% of branches are always predicted correctly and the overall accuracy is
0.85. Th us, **0.8\*1 + 0.2\*x = 0.85**.  x = 0.25. 
