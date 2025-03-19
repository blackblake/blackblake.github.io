---
title: lc24. swapPairs
categories:
  - DSA
  - others
---
### 1# 报错：member acces within null pointer

![[屏幕截图 2024-09-10 100655.png]]

![[屏幕截图 2024-09-10 100516.png]]

**这个报错的意思是当前指针有可能为空指针，但你却把它默认当成非空指针，导致运行时错误。 要解决这个问题，你需要先检查 `head` 是否为 `nullptr`（即链表是否为空），或者 `head->next` 是否为 `nullptr`（即链表中只有一个节点，无法进行交换）**

```cpp
// 检查链表是否为空或只有一个节点 
if (!head || !head->next) { return head; }
```
