---
title: DFS 省份数量
categories:
  - DSA
  - graph
---
```cpp
class Solution {
public:

void DFS(vector<vector<int>>&edges,vector<int>&done,int x){
    //对当前顶点的操作
    done[x]=1;
    int n=edges[0].size()-1;

    for(int i=1;i<=n;i++){
        if(done[i]==0&&edges[x][i]!=INT_MAX){
            DFS(edges,done,i);
        }
    }
}

int findCircleNum(vector<vector<int>>& isConnected) {
    //初始化done, edges数组
    int n=isConnected[0].size();
    vector<int>done(n+1,0);
    vector<vector<int>>edges(n+1,vector<int>(n+1,INT_MAX));
    for(int i=1;i<=n;i++){
        edges[i][i]=1;
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            if(isConnected[i-1][j-1]==1){
                edges[i][j]=isConnected[i-1][j-1];
                edges[j][i]=edges[i][j];//无向图对称
            }
        }
    }

    int a=0;//统计有多少个图
    for(int k=1;k<=n;k++){
        if(done[k]==0){
            DFS(edges,done,k);
            //每次DFS后a+1
            a=a+1;
        }        
    }
    return a;
}

};
```

1. 顶点序号从1开始，所以所有数组长度设置为`n+1`以使下标和顶点序号对应上；
2. 无向图的邻接矩阵对称，初始化时`edges[i][j]`和`edges[j][i]`都要初始化(二者相等)
3. **==各次DFS遍历的图不会遍历到相同的结点，因为早已标记为`done[i]=1`了！所以DFS遍历几次，就有几个连通图==**
4. 注意遍历非连通图的处理
```cpp
for(int k=1;k<=n;k++){
        if(done[k]==0){
            DFS();
        }        
    }
```
**==ps: 一定要保证到结束的时候，done数组中不存在"0",即不存在没遍历过的顶点！==**
