---
title: c-to-riscv
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
---

### (1) 乘法

```RISC-V
slli t0, x28, 3 # t0 = i * 8 (将 i 左移 3 位，即乘以 8)
```
记住如果要乘以8，不能写成`slli t0, x28, 8`，而是3

---

### (2) “0(t0)”

在RISC-V汇编中，像 `0(t0)` 这样的表达式是**基址寻址**（**base addressing**）的形式，用于访问内存中的某个地址。
##### `0(t0)` 的整体作用：

`0(t0)` 其实表示一个内存地址，该地址是由 `t0` 寄存器的值（基地址）加上 `0` 这个偏移量计算出来的。对于内存操作指令，比如 `lw`（加载字）和 `sw`（存储字），这个地址就是用来加载或存储数据的位置。

---
### 示例：

假设寄存器 `t0` 中的值是 `0x1000`（某个内存地址），那么 `0(t0)` 就表示内存地址 `0x1000 + 0 = 0x1000`。如果用在指令中：

```RISC-V
`lw t1, 0(t0)   # 从内存地址 t0 + 0 处加载32位数据到寄存器 t1`
```

这里会从内存地址 `0x1000` 处加载一个32位的数据到 `t1` 寄存器中。

---
### 为什么用"0(t0)"而非"t0"?

在RISC-V汇编中，**不直接使用寄存器如`t0`来访问内存**，而是通过**基址加偏移量**的方式（如`0(t0)`）来访问，是因为RISC-V是一种**基址寻址架构**（load/store architecture），即所有的内存访问必须通过加载（load）或存储（store）指令，使用特定的**地址计算方式**来确定内存位置。

### 具体原因：

1. **内存地址与寄存器内容的区别**：
    
    - 寄存器（如`t0`）存储的是**地址值**，即一个指向内存的基地址，但并不是内存中的数据本身。
    - 你不能直接使用寄存器的内容作为数据进行计算，必须先通过基址寻址计算出实际内存中的数据位置，然后用加载指令（如`lw`）从这个地址取出数据。
    
    **例子：**
```RISC-V
lw t1, 0(t0)   # 从 t0 指向的内存地址处加载数据到 t1

#如果你直接使用 `t0` 作为操作数，它会被当作是寄存器中的**地址值**而不是内存中的数据。
```
    
**错误的做法：**
    
```RISC-V
add t1, t0, t2  # t1 = t0 + t2
（这里把 t0 视为一个普通寄存器值，不会从内存中加载数据）
```