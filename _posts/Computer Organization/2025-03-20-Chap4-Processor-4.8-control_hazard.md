---
title: 4.8 control_hazard
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
---

![Pasted image 20250110051326](/assets/Image/Pasted image 20250110051326.png){: w="600"}

### 4.8.2  缩短分支延迟
---
- 确定分支目标地址的时间越早，需要清除的指令就越少

- 为了将分支决策提前， 需要提前两个动作：计算分支目标地址和判断分支条件。

1. **计算分支目标地址**
	我们在 IF/ID 流水线寄存器中已经有了 PC 的值和立即数 段，所以只需要将分支地址计算从 EX 级移到 ID 级就可以了

2. **判断分支条件**
	![Pasted image 20250110053607](/assets/Image/Pasted image 20250110053607.png){: w="600"}

3. 为了在 IF 级清除指令，我们加入了一条称为IF.Flush 的控制信号，即将 IF/ID 流水线寄存
器的指令字段置为0；
  清空寄存器的结果是将预取到的指令转变成为空指令，该指令不作任何操作；


### 4.8.3  动态分支预测
---
- **分支预测缓存**
	也称为分支历史记录表，一小块**按照分支指令的低位地址索引**的存储器区，其中包括一位或多位数据用以说明最近是否发生过分支；
- 例子
	![Pasted image 20250110054932](/assets/Image/Pasted image 20250110054932.png){: w="600"}
- 
	![Pasted image 20250110054855](/assets/Image/Pasted image 20250110054855.png){: w="500"}