---
title: "2.2 数据预处理"
date: 2025-03-20 03:39:16 +0800
categories: [深度学习, Chap2 预备知识]
tags: [dl]     # TAG names should always be lowercase
---

读取数据集
---
---

### 1）创建数据集

首先创建一个人工数据集，并存储在CSV（逗号分隔值）文件 ../data/house_tiny.csv中。 以其他格式存储的数据也可以通过类似的方式进行处理。
```python
# 导入 os 模块，用于处理文件和目录路径
import os

# 创建目录（如果不存在）：
# - os.path.join('..', 'data') 生成跨平台的路径 "../data"
# - exist_ok=True 表示如果目录已存在，不会报错
os.makedirs(os.path.join('..', 'data'), exist_ok=True)

# 定义 CSV 文件路径：
# - os.path.join('..', 'data', 'house_tiny.csv') 生成 "../data/house_tiny.csv"
data_file = os.path.join('..', 'data', 'house_tiny.csv')

# 打开文件并写入数据：
# - 'w' 表示写入模式（如果文件存在则覆盖，不存在则创建）
with open(data_file, 'w') as f:
# 写入 CSV 的列名（表头）
f.write('NumRooms,Alley,Price\n')  # 列名：房间数量, 小巷类型, 价格

    # 写入 4 条房屋数据记录（每行一个样本）
    f.write('NA,Pave,127500\n')   # 房间数缺失，小巷铺砌，价格 127500
    f.write('2,NA,106000\n')      # 2 个房间，小巷信息缺失，价格 106000
    f.write('4,NA,178100\n')      # 4 个房间，小巷信息缺失，价格 178100
    f.write('NA,NA,140000\n')     # 房间数和小巷信息均缺失，价格 140000

# 文件会在 with 块结束后自动关闭
```

### 2）读入数据集
要从创建的CSV文件中加载原始数据集，我们导入pandas包并调用read_csv函数
```python
import pandas as pd

data = pd.read_csv(data_file)
print(data)
```

### 3）处理缺失值
```python
# ":" 表示选择所有行, "0:2" 表示选择第 0 列到第 1 列
inputs, outputs = data.iloc[:, 0:2], data.iloc[:, 2]

inputs = inputs.fillna(inputs.mean()) # mean函数用于求平均值
```
