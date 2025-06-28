#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from datetime import datetime

def has_complete_frontmatter(content):
    """检查文件是否已有完整的frontmatter"""
    if not content.strip().startswith('---'):
        return False
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    frontmatter = parts[1].strip()
    # 检查是否包含基本必需字段
    has_title = re.search(r'title:\s*["\']?[^"\'\n]+["\']?', frontmatter)
    has_date = re.search(r'date:\s*\d{4}-\d{2}-\d{2}', frontmatter)
    
    return bool(has_title and has_date)

def extract_title_from_filename(filename):
    """从文件名提取标题"""
    # 移除日期前缀和扩展名
    title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
    title = re.sub(r'\.md$', '', title)
    # 替换连字符和下划线为空格
    title = title.replace('-', ' ').replace('_', ' ')
    return title.strip()

def extract_title_from_content(content):
    """从内容中提取标题"""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line.startswith('## '):
            return line[3:].strip()
        elif line.startswith('### '):
            return line[4:].strip()
    return None

def determine_category_from_path(filepath):
    """根据文件路径确定分类"""
    path_parts = filepath.parts
    if len(path_parts) > 2:  # _posts/category/file.md
        category = path_parts[-2]  # 取目录名作为分类
        return [category]
    return []

def determine_tags_from_path_and_content(filepath, content):
    """根据路径和内容确定标签"""
    tags = []
    path_parts = filepath.parts
    
    # 从路径中提取标签
    for part in path_parts:
        if part.lower() in ['algorithm', 'dp', 'java', 'python', 'git', 'llm', 'ml', 'marl']:
            tags.append(part.lower())
    
    # 从内容中提取标签
    content_lower = content.lower()
    if 'algorithm' in content_lower or '算法' in content:
        tags.append('algorithm')
    if 'java' in content_lower:
        tags.append('java')
    if 'python' in content_lower:
        tags.append('python')
    if 'machine learning' in content_lower or 'ml' in content_lower:
        tags.append('ml')
    if 'deep learning' in content_lower or 'dl' in content_lower:
        tags.append('dl')
    
    return list(set(tags))  # 去重

def extract_date_from_filename(filename):
    """从文件名提取日期"""
    match = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1) + ' 03:39:16 +0800'
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S +0800')



def generate_frontmatter(title, date, categories, tags, has_math=False):
    """生成标准的frontmatter"""
    frontmatter = f"""---
title: "{title}"
date: {date}"""
    
    if categories:
        if len(categories) == 1:
            frontmatter += f"\ncategories: [{categories[0]}]"
        else:
            frontmatter += f"\ncategories:\n"
            for cat in categories:
                frontmatter += f"    - {cat}\n"
    
    if tags:
        frontmatter += f"\ntags: {tags}"
    
    if has_math:
        frontmatter += f"\nmath: true"
    
    frontmatter += f"\n---"
    
    return frontmatter

def process_file(filepath):
    """处理单个markdown文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"⚠️  无法读取文件 {filepath} (编码问题)")
        return False
    
    # 检查是否已有完整frontmatter
    if has_complete_frontmatter(content):
        print(f"✅ 跳过 {filepath.name} (已有完整frontmatter)")
        return False
    
    print(f"🔄 处理 {filepath.name}")
    
    # 提取现有内容（移除不完整的frontmatter）
    if content.strip().startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            main_content = parts[2].strip()
        else:
            main_content = content.strip()
    else:
        main_content = content.strip()
    
    filename = filepath.name
    
    # 确定标题
    title = extract_title_from_content(main_content)
    if not title:
        title = extract_title_from_filename(filename)
    
    # 确定日期
    date = extract_date_from_filename(filename)
    
    # 确定分类
    categories = determine_category_from_path(filepath)
    
    # 确定标签
    tags = determine_tags_from_path_and_content(filepath, main_content)
    
    # 检查是否包含数学公式
    has_math = '$' in main_content or '\\(' in main_content or '\\[' in main_content
    
    # 生成新的frontmatter
    new_frontmatter = generate_frontmatter(title, date, categories, tags, has_math)
    
    # 组合最终内容
    final_content = new_frontmatter + '\n\n' + main_content
    
    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"✅ 已添加frontmatter到 {filepath.name}")
        return True
    except Exception as e:
        print(f"❌ 写入文件失败 {filepath}: {e}")
        return False

def main():
    """主函数"""
    posts_dir = Path('_posts')
    
    if not posts_dir.exists():
        print("❌ 错误: _posts目录不存在")
        return
    
    # 找到所有.md文件
    md_files = list(posts_dir.rglob('*.md'))
    
    print(f"📁 找到 {len(md_files)} 个markdown文件")
    print("-" * 50)
    
    processed_count = 0
    for filepath in md_files:
        if filepath.name.startswith('.'):  # 跳过隐藏文件
            continue
        if process_file(filepath):
            processed_count += 1
    
    print("-" * 50)
    print(f"🎉 处理完成! 共为 {processed_count} 个文件添加了frontmatter")
    
    if processed_count == 0:
        print("💡 所有文件都已有完整的frontmatter，无需处理")

if __name__ == "__main__":
    main() 