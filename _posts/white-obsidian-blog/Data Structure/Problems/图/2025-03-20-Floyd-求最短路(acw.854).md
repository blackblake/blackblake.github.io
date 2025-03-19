---
title: Floyd 求最短路
categories:
  - DSA
  - graph
---
![[Pasted image 20241202210752.png|500]]


![[Pasted image 20241202210847.png]]

![[Pasted image 20241202211036.png]]

1. 注意处理重边！
	
2. A的二维数组、自环路径大小置0、`if (A[i][k] != INF && A[k][j] != INF)`、 `A[i][k] + A[k][j]而不是edges[i][k] + edges[k][j]`这些注意点都和lc1334一样
	
3. **query函数--INF/2是什么意思？**
	-  `INF / 2` 是为了避免整数加法时的溢出：因为在更新时，`A[i][k]` 和 `A[k][j]` 若都是 `INF`，则它们的和会大于等于 `INF`，导致溢出；
	
	- 但Floyd算法中更新`A[i][j]`的语句不需要`INF/2`，因为`if (A[i][k] != INF && A[k][j] != INF)`已经排除了`A[i][k]` 和 `A[k][j]` 都是 `INF`的情况 