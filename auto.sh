#!/bin/bash

# 定义博客所在目录
BLOG_DIR="/Users/floyd/blackblake.github.io"

# 进入博客目录
cd $BLOG_DIR || { echo "无法进入博客目录: $BLOG_DIR"; exit 1; }

# 提示信息
echo "开始自动提交博客更新..."

# 添加所有更改
git add .

# 获取当前时间作为提交消息
COMMIT_MSG="博客更新 - $(date '+%Y-%m-%d %H:%M:%S')"

# 提交更改
git commit -m "$COMMIT_MSG"

# 推送到远程仓库
git push origin main

# 完成提示
echo "博客更新已成功推送到 Git 仓库！"
