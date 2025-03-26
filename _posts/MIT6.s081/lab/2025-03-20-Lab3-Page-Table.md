---
title: "lab3 pgtbl"
date: 2025-03-26 03:39:16 +0800
categories: [MIT6.S081, os_Lab]
tags: [os]     # TAG names should always be lowercase
---

Print a page table
---
---
在这一节我们需要实现一个`vmprint()`函数用于打印页表，它接受一个`pagetable_t`类型的参数，我们先来看一下`pagetable_t`是什么

### 1）pagetable_t
在`riscv.h`中发现其定义：
```c
typedef uint64 *pagetable_t; // 512 PTEs
```

- 这说明它是指向页表的指针，而页表本身是一个由 uint64（64 位无符号整数）组成的数组
- 在xv6中，每个页表包含 2^9 = 512 个页表项（PTE），因此注释中注明 `// 512 PTEs`
- 所以我们的这个`vmprint`函数接受一个页表作为参数

### 2）`freewalk`

文档中提示我们可以参考这个函数：
```c
// 递归地释放页表中的页
// 此函数正常运行的前提——所有叶子结点都已被移除
void
freewalk(pagetable_t pagetable)
{
  // 遍历当前页表中的所有 512 个页表项 (PTE)
  for(int i = 0; i < 512; i++){
    pte_t pte = pagetable[i];  // 获取第 i 个页表项
    
    // 检查 PTE 是否有效（PTE_V）且不是叶子节点（非 R/W/X）
    if((pte & PTE_V) && (pte & (PTE_R|PTE_W|PTE_X)) == 0){
      // 这个 PTE 指向一个更低层级的页表（非叶子）
      uint64 child = PTE2PA(pte);     // 从 PTE 中提取子页表的物理地址
      freewalk((pagetable_t)child);   // 递归释放子页表
      pagetable[i] = 0;               // 清零当前 PTE
    } 
    
    // 如果 PTE 有效且是叶子节点（R/W/X 至少一个被设置）
    else if(pte & PTE_V){
      panic("freewalk: leaf"); // 叶子映射应已被移除（这是freewalk函数正常运行的前提），否则报错
    }
    
    // 如果 PTE 无效（PTE_V = 0），则直接跳过
  }
  
  // 释放当前页表占用的物理页
  kfree((void*)pagetable);
}
```
1. `pte_t`：一个宏，和`pagetable_t`一起被定义在`riscv.h`的末尾
2. `pagetable[i]`：
3. `PTE2PA(pte)`：通过 PTE2PA 宏将 PTE 转换为物理地址


### 3）叶子结点

解释一下`freewalk`函数中的“叶子结点”的概念：

在 多级页表结构（如 xv6 的三级页表）中：

1. 非叶子节点：
页表项（PTE）指向 下一级页表（例如顶级页表的 PTE 指向中间页表）。
   - 特征：PTE 的 PTE_V 位为 1，但 PTE_R/PTE_W/PTE_X（可读/可写/可执行）权限位均为 0。
   - 作用：仅用于索引下一级页表，不直接映射物理页。

2. 叶子节点：
页表项（PTE）直接指向 物理页帧（即最终的数据页或代码页）。
   - 特征：PTE 的 PTE_V 位为 1，且至少有一个权限位（PTE_R/PTE_W/PTE_X）为 1。
   - 作用：完成虚拟地址到物理地址的最终映射。

### 4）`vmprint()`实现

```c
void 
vmprint(pagetable_t pagetable, uint dep){
  if(dep == 0)
    printf("page table %p\n", pagetable);
  for(int i = 0; i < 512; i++){
    pte_t pte = pagetable[i];
    if(pte & PTE_V){
      for(int j = 0; j < dep; j++)
        printf(".. ");
      uint64 child = PTE2PA(pte);
      printf("..%d: pte %p pa %p\n", i, pte, child);
      if(dep < 2)
        // 如果层数等于 2 就不需要继续递归了，因为这是叶子节点
        vmprint((pagetable_t) child, dep + 1);
    }
  } 
}
```

