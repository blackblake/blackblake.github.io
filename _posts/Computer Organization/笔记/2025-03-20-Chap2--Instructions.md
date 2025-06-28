---
title: "chap2 instructions"
date: 2025-03-20 03:39:16 +0800
categories: [cod, note]
tags: [cod]     # TAG names should always be lowercase
math: true
---
##  指令
---

除了store指令外，所有指令的**目的寄存器都是第一个操作数**！

##### 1. 存取指令、算术指令 
- d、w、h、b分别是双字、字、半字、字节
- lbu：取字节（无符号数）
- lui：取左移12位后的20位立即数（在后面加3个0）
	![Pasted image 20250107175510](/assets/Image/Pasted image 20250107175510.png)
- 
  ![Pasted image 20250107202418](/assets/Image/Pasted image 20250107202418.png){: w="300"}

##### 2. 移位操作

```RISC-V
  sll x5,x6,x7      #逻辑左移 x5=x6<<x7
  srl                逻辑右移
  sra                算术右移
```
   `上面三个指令加上u就是无符号版本

##### 3. 条件分支（有条件跳转）

```RISC-V
  beq x5,x6,100      #相等即跳转  if(x5==x6) go to PC+100
  bne                 不等即跳转（unequal）
  blt                 x5<x6跳转（little than）
  bge                 x5≥x6跳转（greater or equal）
```

a)注意这里的第三个操作数，即立即数100，并不是说跳转到地址为100的指令，而是==PC+100==！
b)上面三个指令加上u就是无符号版本

##### 3.无条件跳转
![Pasted image 20250107214641](/assets/Image/Pasted image 20250107214641.png){: w="450"}
a)存进返回地址寄存器x1的不是PC而是PC+4
b)jal是PC相对寻址,jalr是[寄存器+偏移量]寻址,所以有个"r"
c)jalr用于过程返回(return)


## \[存储器操作数]
---
##### 1）32位(bit)=1字(word)=4字节(byte)

##### 2）RISC-V中所有指令中的offset都是以byte为单位的（而非bit）
###### E.g.1
![Pasted image 20241102184518](/assets/Image/Pasted image 20241102184518.png)
这里每一个矩形代表 **1字(word)**，即4byte的数据，即$4*8=32bit$；

###### E.g.2
![Pasted image 20241102184825](/assets/Image/Pasted image 20241102184825.png){: w="500"}
`1(x5)`中的offset `1`就代表1个`字节(byte)`，即`8bit`，所以`1(x5)`指向的是`03`即`0000 0011`这个字节(byte)。

###### E.g.3
```RISC-V
如果想取数组A的下标为2的元素：

ld  x9,2(x22)是错的
ld  x9,4(x22)才能取到A[2]
```


## \[原码vs补码]
---
##### 1. 原码to补码
- 正数的补码等于其原码
-  负数的补码=原码除符号位按位取反后+1

##### 2. 原码和补码的区别
- 原码：最高位是1则负，0则正，最高位不参与数值的计算，只表示正负；
- 补码：最高位不仅1负0正，还带者权值参与数值的计算

##### 3.补码求相反数
- 方法：把每一位（包括符号位）都取反，然后`+1`
- 原理：一个数与其取反表达式的和一定是$111...111_2$，即`-1`；由于$x+\overline{x}=-1$，因此有$\overline{x}+1=-x$


## \[符号扩展]
---
**如何将一个16位数转换为64位数？**

- 正数：把最高有效位（符号位）`0`复制48次并放到左侧
	
- 负数：把最高有效位（符号位）`1`复制48次并放到左侧

## \[例题：分支指令翻译]
---
1. 无条件分支：`beq x0,x0,label`

2. 例题：把下列循环语句翻译为RISC-V代码
```cpp
if (i == j)
	f = g + h; 
else f = g − h;
```

```
bne x22, x23, Else // go to Else if i != j
add x19, x20, x21 // f = g + h (skipped if i != j)
beq x0, x0, Exit // if 0 == 0, go to Exit
Else:
sub x19, x20, x21 // f = g − h (skipped if i = j)
Exit:
```


## \[例题：循环指令翻译]
---
```cpp
while (save[i] == k)
	i += 1;
```

```
Loop: 
slli x10, x22, 2 // Temp reg x10 = i * 4
add x10, x10, x25 // x10 = address of save[i]
lw x9, 0(x10) // Temp reg x9 = save[i]
bne x9, x24, Exit // go to Exit if save[i] != k
addi x22, x22, 1 // i = i + 1
beq x0, x0, Loop // go to Loop
Exit:
```

- 只有通过`lw x9, 0(x10)`将`0(x10)`这个地址存储的值（即save\[i]）存入x9，才能进行比较，因为`bne`指令只能通过比较两个**寄存器**来确定是否分支

## \[无符号比较]

![Pasted image 20241103000245](/assets/Image/Pasted image 20241103000245.png)
无符号比较指令在检查x与y的大小关系的同时，也检测了x是否为负数；如图例：若满足ge条件或x20<0则跳转

## \[指令格式]
---
1.  所有RISC-V指令都是32位长
 
2.  RISC-V是小端法

3. ![Pasted image 20241005112213](/assets/Image/Pasted image 20241005112213.png)
B型＝SB型  
J型＝UJ型  
B,J相比于S,U型，都是立即数多一位(0默认，左移乘2)


## \[逻辑操作]
---
1. **slli**常用于乘法
	左移i位相当于乘以$2^i$ (尤其常见于计算数组元素地址)
2. **AND**常用于掩码



## \[过程]
---
##### 1. **寄存器**
x10~x17：传递参数/返回值
x1：返回地址寄存器
x2：栈指针
x5～x7以及x28～x31：临时寄存器，在过程调用中不被 被调用者（被调用的过程）保存
x8～x9以及x18～x27：保存寄存器，在过程调用中必须被保存。​（一旦使用，由被调用者保存并恢复）

##### 2. **跳转指令**

![Pasted image 20241013124744](/assets/Image/Pasted image 20241013124744.png)


> [!Note] Jal vs. jalr
> (a) jalr 指令和jal指令都是跳转指令,不同的是**jalr**指令是PC相对跳转,它把当前指令的地址加上一个相对偏移量, 然后跳到新的地址；
> (b) **jalr** 指令常用于函数调用,它可以在**返回(return)**时自动跳回调用函数的地址,而jal指令则更适用于跳到程序的不同部分。

比如，**函数返回return常用的指令是`jalr x0, 0(x1)`**：
-将rd写为x0，意为不会保存当前PC+4的地址作为返回地址（因为这里是当前函数结束了，要return，而不是要调用其他函数，所以不会跳转回当前指令，故不用保存）;
-而`0(x1)`意为跳转到x1中保存的地址值，即返回地址；

设想，如果函数return不使用`jalr x0, 0(x1)`，而改用`jal`指令，那么计算返回地址的绝对地址立即数值将是很麻烦的，所以return一般用jalr翻译;
##### 3. **栈** 是**向下增长**的
	通过`减小`栈指针来将值`压栈`，通过`增大`栈指针来`弹栈`
指令中的地址是栈中项目所占的**下边沿**，如"0(sp)"指的是[sp+0,sp+4]这4个字节(32bit machine)

##### 4.例题

```cpp
int leaf_example (int g, int h, int i, int j)
{
	int f;
	f = (g + h) − (i + j);
	return f;
}
```

```
leaf_example:

addi sp, sp, -12 // adjust stack to make room for 3 items
sw x5, 8(sp) // save register x5 for use afterwards
sw x6, 4(sp) // save register x6 for use afterwards
sw x20, 0(sp) // save register x20 for use afterwards

add x5, x10, x11 // register x5 contains g + h
add x6, x12, x13 // register x6 contains i + j
sub x20, x5, x6 // f = x5 − x6, which is (g + h) − (i + j)
addi x10, x20, 0 // returns f (x10 = x20 + 0)

lw x20, 0(sp) // restore register x20 for caller
lw x6, 4(sp) // restore register x6 for caller
lw x5, 8(sp) // restore register x5 for caller
addi sp, sp, 12 // adjust stack to delete 3 items

jalr x0, 0(x1) // branch back to calling routine
```

![Pasted image 20241103093542](/assets/Image/Pasted image 20241103093542.png)
###### 疑问
a）这个例题的情景，==为什么需要压栈？==不能直接进行加减操作吗？**
b）压栈必须遵循16(sp), 8(sp), 0(sp)的==顺序==吗？弹栈必须遵循0(sp), 8(sp), 16(sp)的顺序吗？

##### 5. **嵌套过程**

**遇到问题**
	假设主程序调用过程A，参数为3，将值3存入寄存器x10然后使用jal x1，A。再假设过程A通过jal x1，B调用过程B，参数为7，也存入x10。由于A尚未结束任务，所以寄存器x10的使用存在冲突。同样在寄存器x1中的返回地址也存在冲突，因为它现在具有B的返回地址。

**解决方法**
	- 解决方法是将所有**必须保存**的寄存器**压栈**。
	- 调用者将所有调用后还需要的参数寄存器(x10～x17)或临时寄存器（x5～x7和x28～x31）压栈。
	- 被调用者**将返回地址寄存器x1和被调用者使用的保存寄存器（x8～x9和x18～x27）压栈**。调整栈指针sp以计算压栈寄存器的数量。
	- 返回时，**从内存中恢复寄存器**并重新调整栈指针。

**例题：**
```c
int fact (int n)
{
	if (n < 1) return (1);
		else return (n * fact(n − 1));
}
```

```RISC-V
fact: //函数开始的标签一定要有

//不管有没有嵌套调用，都要在函数的一开始将返回地址和参数入栈保存
addi sp, sp, -8 // adjust stack for 2 items
sw x1, 4(sp) // save the return address
sw x10, 0(sp) // save the argument n

//如果n≥1则跳转到L1
addi x5, x10, -1 // x5 = n - 1
bge x5, x0, L1 // if (n - 1) >= 0, go to L1

//如果n小于1，fact将1放入一个值寄存器中以返回1
addi x10, x0, 1 // return 1
addi sp, sp, 8 // 因为n<1的操作是直接返回1,不会嵌套调用其他函数,所以x1和n没有改变.故直接弹栈,不需要把x1和n加载回寄存器
jalr x0, 0(x1) // return to caller

如果n<1,那么到此,fact函数就结束了,但如果n≥1,则下面是剩余的操作

//如果n≥1
L1: 
addi x10, x10, -1 // n >= 1: argument gets (n − 1)
jal x1, fact // call fact with (n − 1)

addi x6, x10, 0 // return from jal: move result of fact
(n - 1) to x6:
lw x10, 0(sp) // restore argument n
lw x1, 4(sp) // restore the return address
addi sp, sp, 8 // adjust stack pointer to pop 2 items
//这里发生了嵌套调用,所以需要把返回地址x1和参数n原来在fact函数一开始被压栈保存的值恢复到x1和x10寄存器里，然后才能进行弹栈(对比第3段)

mul x10, x10, x6 // return n * fact (n − 1)
jalr x0, 0(x1) // return to the caller
```

**解释**
-如果在起初，调用fact函数的地址是a0，那么通过jal，把a0+4的地址存到x1中，记该地址为a1；
-然后在fact1（这里用factn表示第n次调用fact）的一开始，把x1也就是a1的值压栈；
-若n<1，fact1直接返回1，然后弹栈，不需要恢复x1的值（因为没变）；---若n≥1，递归调用了fact2，则fact2在一开始把返回地址a2=a1+4压栈，假设fact2直接返回1，则在fact2结束时，x1的值是a2。
-但fact2结束后，程序应该继续进行这一段fact1里的指令：
```RISC-V
addi x6, x10, 0 // return from jal: move result of fact
(n - 1) to x6:
lw x10, 0(sp) // restore argument n
lw x1, 4(sp) // restore the return address
addi sp, sp, 8 // adjust stack pointer to pop 2 items
```
这就把在fact1之初压栈保存的返回地址a1恢复到了x1寄存器中，使fact1能正确地返回。

![Pasted image 20241013141823](/assets/Image/Pasted image 20241013141823.png)
 
##### 疑问

	调用者将所有调用后还需要的参数寄存器(x10～x17)或临时寄存器（x5～x7和x28～x31）压栈。被调用者将返回地址寄存器x1和被调用者使用的保存寄存器（x8～x9和x18～x27）压栈

**答：**
- **调用者（Caller）压栈保存需要的寄存器**：
    - 调用者是发起函数调用的一方。在调用另一个函数之前，它会把**所有调用后还需要的参数寄存器**（x10～x17）和**临时寄存器**（x5～x7 和 x28～x31）压入栈中。
    - 这样做的目的是，如果调用的函数在执行过程中修改了这些寄存器，调用者可以在函数返回后通过栈恢复原有的值，以确保调用函数前后的状态一致。
- **被调用者（Callee）压栈保存返回地址和保存寄存器**：
    - 被调用者是被调用的函数。在执行时，它会把**返回地址寄存器 x1**和**它会使用到的保存寄存器（x8～x9 和 x18～x27）压入栈中**。
    - 这样做是因为返回地址寄存器 x1 存储的是函数返回时需要跳转的地址，**如果被调用者函数调用了其他函数，可能会覆盖 x1 的内容，所以要压栈保存**。
    - 保存寄存器（x8～x9 和 x18～x27）是约定为“被调用者保存”的寄存器，如果在函数中使用这些寄存器，就必须先保存原值，函数执行结束后再恢复，以保证调用者的上下文不被破坏。


##### \[补充]  保存寄存器vs临时寄存器

- **保存寄存器是指在函数调用前后必须保持相同值的寄存器**，因为调用者期望在调用后能够继续使用这些寄存器的值。
	
- 临时寄存器，是指在函数调用中可以自由修改的寄存器，**不需要保存和恢复**。
	
- 函数调用时，**如果一个函数需要修改保留寄存器的值，那么它必须在修改前将它们保存到堆栈上，并在返回前将它们从堆栈上恢复**。这样可以避免破坏调用者的寄存器内容。而如果一个函数**只修改非保留寄存器的值，就不需要保存和恢复它们**，因为调用者不会再使用它们。

![Pasted image 20241103095752](/assets/Image/Pasted image 20241103095752.png)


##  \[过程帧]
---
**（1）引入**
- **栈**也可以用于存储过程的**局部变量**，但这些变量**不适用于寄存器**，例如局部数组或结构体；
- 栈中包含过程所**保存寄存器**和**局部变量**的段称为**过程帧**。
- FP(freame pointer)、SP(stack pointer)分别值的是帧指针、栈指针；
- **x8**也可以用于表示帧指针

![Pasted image 20241013142529](/assets/Image/Pasted image 20241013142529.png)

（2）疑问：帧指针到底有什么用？
帧指针的方便性在于对过程中栈内变量的所有引用都具有相同的偏移；
但是，帧指针并不是必需的。RISC-V C编译器仅在改变了栈指针的过程中使用帧指针；
### 6. 堆(heap)

除了局部变量之外，程序还需要为静态变量和动态数据结构分配内存空间

![Pasted image 20241013193912](/assets/Image/Pasted image 20241013193912.png)
其中：
 - Text：RISC-V机器代码，通常称为代码段
 - static data： 静态数据段，用于存放常量和其他静态变量
 - Dynamic data：由malloc和new分配的动态数据
 - 存放数组和链表这类数据结构的段通常称为堆(heap)，它放在内存中

### 7.寄存器约定

下图总结了RISC-V汇编语言的寄存器约定，可以看出大多数过程可以使用多达8个参数寄存器、12个保留寄存器和7个临时寄存器而无须进入内存。

![Pasted image 20241013194714](/assets/Image/Pasted image 20241013194714.png)

但是，如果参数超过8个怎么办？
答：**前8个**参数在**寄存器x10到x17中**，其余参数放在**内存**中--帧指针的上方，可通过**帧指针寻址**。

---
**load指令是I型格式**
