#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def sanitize_filename(title, category=""):
    """清理文件名，使其符合Jekyll要求"""
    # 移除特殊字符，替换为连字符
    filename = re.sub(r'[^\w\s\u4e00-\u9fff.-]', '', title)
    filename = re.sub(r'\s+', '-', filename)
    filename = filename.strip('-')
    
    # 如果有分类，添加到文件名中
    if category and category not in filename.lower():
        filename = f"{category}-{filename}"
    
    return filename

def extract_date_from_frontmatter(content):
    """从frontmatter提取日期"""
    if not content.strip().startswith('---'):
        return "2024-12-31"
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return "2024-12-31"
    
    frontmatter = parts[1]
    date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', frontmatter)
    if date_match:
        return date_match.group(1)
    
    return "2024-12-31"

def extract_title_from_frontmatter(content):
    """从frontmatter提取标题"""
    if not content.strip().startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    frontmatter = parts[1]
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
    if title_match:
        return title_match.group(1).strip()
    
    return None

def process_file(file_path, posts_dir):
    """处理单个文件，移动并重命名"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"⚠️  无法读取文件 {file_path}")
        return False
    
    # 提取信息
    date_str = extract_date_from_frontmatter(content)
    title = extract_title_from_frontmatter(content)
    
    if not title:
        # 从文件名提取标题
        title = file_path.stem.replace('-', ' ')
    
    # 确定分类（从目录路径）
    relative_path = file_path.relative_to(posts_dir)
    category = ""
    if len(relative_path.parts) > 1:
        category = relative_path.parts[-2]  # 父目录作为分类
    
    # 生成新文件名
    clean_title = sanitize_filename(title, category)
    new_filename = f"{date_str}-{clean_title}.md"
    new_path = posts_dir / new_filename
    
    # 避免文件名冲突
    counter = 1
    while new_path.exists() and new_path != file_path:
        new_filename = f"{date_str}-{clean_title}-{counter}.md"
        new_path = posts_dir / new_filename
        counter += 1
    
    # 如果已经在正确位置且文件名正确，跳过
    if file_path == new_path:
        print(f"✅ 跳过 {file_path.name} (已正确)")
        return False
    
    # 移动文件
    try:
        shutil.move(str(file_path), str(new_path))
        print(f"📝 移动: {file_path.relative_to(posts_dir)} → {new_path.name}")
        return True
    except Exception as e:
        print(f"❌ 移动失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    posts_dir = Path('_posts')
    
    if not posts_dir.exists():
        print("❌ 错误: _posts目录不存在")
        return
    
    # 找到所有markdown文件
    md_files = []
    for file_path in posts_dir.rglob('*.md'):
        # 跳过已经在根目录且符合命名规范的文件
        if file_path.parent == posts_dir:
            filename = file_path.name
            if re.match(r'^\d{4}-\d{2}-\d{2}-.+\.md$', filename):
                continue
        md_files.append(file_path)
    
    print(f"📁 找到 {len(md_files)} 个需要处理的markdown文件")
    print("-" * 60)
    
    moved_count = 0
    for file_path in md_files:
        if process_file(file_path, posts_dir):
            moved_count += 1
    
    print("-" * 60)
    print(f"🎉 处理完成! 共移动/重命名了 {moved_count} 个文件")
    
    # 清理空目录
    for root, dirs, files in os.walk(posts_dir, topdown=False):
        if root == str(posts_dir):
            continue
        try:
            if not files and not dirs:
                os.rmdir(root)
                print(f"🗑️  删除空目录: {Path(root).relative_to(posts_dir)}")
        except OSError:
            pass

if __name__ == "__main__":
    main() 