#!/bin/bash

# 设置目标目录
POSTS_DIR="_posts"  # 修改为你的 Markdown 文件目录

# 检查目录是否存在
if [ ! -d "$POSTS_DIR" ]; then
    echo "错误: 目录 $POSTS_DIR 不存在"
    exit 1
fi

# 获取今天的日期
TODAY=$(date +"%Y-%m-%d")

# 使用 find 命令递归查找所有 md 文件
find "$POSTS_DIR" -type f -name "*.md" | while read file; do
    # 获取文件名和目录路径
    filename=$(basename "$file")
    dir_path=$(dirname "$file")
    
    # 检查文件名是否已经有日期前缀
    if [[ ! $filename =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
        # 替换空格为连字符
        new_filename="${TODAY}-${filename// /-}"
        mv "$file" "$dir_path/$new_filename"
        echo "重命名: $file -> $dir_path/$new_filename"
    fi
done
