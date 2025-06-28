---
title: "chap5_solutions"
date: 2025-03-20 03:39:16 +0800
categories: [cod, solutions]
tags: [cod]     # TAG names should always be lowercase
---
### 5.2
---
- **块大小为1个字——offset字段为0位**
- **块大小为2个字——offset字段为1位**

### 5.3
---
- 块大小为2个字——offset字段为1位字偏移量+3位
- 32KiB = 2^15 bytes

### 5.4
---
- cache块大小——只看offset位数，其中有3位是固定的字偏移量，剩下的若有n位，则块大小为2^n
- 
