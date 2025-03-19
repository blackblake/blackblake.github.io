---
title: Dijkstra 网络延迟时间
categories:
  - DSA
  - graph
---
```cpp
class Solution {

public:

    int networkDelayTime(vector<vector<int>>& times, int n, int k) {

		//记录源点k到各点的最短距离的【dist数组】
		vector<int> dist(n+1, INT_MAX);//初始化为n+1的长度，是因为下标0不会用到
        dist[k] = 0;// 初始化dist数组(置源点k到自己的最小距离为0)
        
        //记录顶点已考虑(true)和未考虑(false)的【done数组】
        vector<bool> done(n+1, false);

        // 建立并用times数组初始化【邻接矩阵】
        vector<vector<int>> edges(n+1, vector<int>(n+1, INT_MAX));
        for(int i=0;i<times.size();i++){
            edges[times[i][0]][times[i][1]] = times[i][2];
        }

        

        // Dijkstra算法
        for(int i = 0; i < n; i++){

            // 找出dist数组中[尚未访问过的][dist值最小]的顶点u
            int u=-1;
            int minDist = INT_MAX;
            for(int j = 1; j <= n; j++){
                if(!done[j] && dist[j] < minDist){
                    u = j;
                    minDist = dist[j];
                }
            }
            
            if(u==-1){break;}//把u的初始值设为-1很重要！！

            // 标记u为已访问
            done[u] = true;

            // 遍历dist数组,更新所有[因u的添加而可以被缩小路径]的顶点
            for(int j = 1; j <= n; j++){
                if(!done[j] && edges[u][j] != INT_MAX){
                    dist[j] = min(dist[j], dist[u] + edges[u][j]);
                }
            }
        }
        

        // 输出最大时间的for循环就不细写了
    }

};
```

1. **==dist, done, edges数组的长度都是n+1而不是n==**
	因为输入的times数组是这样的: `times = [[2,1,1],[2,3,1],[3,4,1]]`，所以为了让下标和顶点序号对应，下标0就需要被跳过，而长度为n+1的数组才能有下标为n的元素；

2. 琢磨用times初始化邻接矩阵的语句
	`edges[times[i][0]][times[i][1]] = times[i][2];`

3. `dist`一开始初始化为全`INT_MAX`，`done`一开始全初始化为`f`(除了源点k的`done[k]`)
	
4. **Dijkstra算法就三步 (除三个数组的初始化外)**
	a) 找出`dist`数组未访问过的最小值对应的顶点u
	b) 标记u为已访问
	c) 遍历dist数组,更新所有\[因u的添加而可以被缩小路径]的顶点

5. 主循环体只循环`n-1`次，因为n个顶点只有n-1条最短路径！
	
6. 找dist中的最小距离顶点、更新dist数组这两个时候,一定要记得有一个条件是`done[i]==false` !
	
7. 找dist中的最小距离顶点时，存储最小距离顶点序号的int u，一定要==初始化为-1，再在循环结束后紧跟着一句 `if(u==-1){break;}`==，否则若不存在这个最小值，就会导致“heap overflow”！