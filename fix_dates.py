#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from datetime import datetime, timedelta

def fix_file_date(filepath):
    """修正单个文件的日期"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"⚠️  无法读取文件 {filepath}")
        return False
    
    # 检查是否有frontmatter
    if not content.strip().startswith('---'):
        return False
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    frontmatter = parts[1]
    main_content = parts[2]
    
    # 查找日期行
    date_pattern = r'date:\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\+\d{4})'
    date_match = re.search(date_pattern, frontmatter)
    
    if not date_match:
        return False
    
    # 提取日期信息
    date_str = date_match.group(1)
    time_str = date_match.group(2)
    timezone_str = date_match.group(3)
    
    # 解析日期
    try:
        file_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return False
    
    # 如果日期是未来日期，修正为今天之前的日期
    # 使用固定的当前日期（2024年12月），因为系统时间可能不准确
    current_date = datetime(2024, 12, 31)
    if file_date > current_date:
        # 尝试从文件名提取日期
        filename_date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', filepath.name)
        if filename_date_match:
            # 使用文件名中的日期
            new_date_str = filename_date_match.group(1)
        else:
            # 使用当前日期
            new_date_str = current_date.strftime('%Y-%m-%d')
        
        # 替换日期
        old_date_line = f"date: {date_str} {time_str} {timezone_str}"
        new_date_line = f"date: {new_date_str} {time_str} {timezone_str}"
        
        new_frontmatter = frontmatter.replace(old_date_line, new_date_line)
        new_content = f"---{new_frontmatter}---{main_content}"
        
        # 写回文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 修正日期: {filepath.name} ({date_str} → {new_date_str})")
            return True
        except Exception as e:
            print(f"❌ 写入失败 {filepath}: {e}")
            return False
    else:
        print(f"✅ 跳过 {filepath.name} (日期正确: {date_str})")
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
    
    fixed_count = 0
    for filepath in md_files:
        if filepath.name.startswith('.'):  # 跳过隐藏文件
            continue
        if fix_file_date(filepath):
            fixed_count += 1
    
    print("-" * 50)
    print(f"🎉 处理完成! 共修正了 {fixed_count} 个文件的日期")
    
    if fixed_count == 0:
        print("💡 所有文件的日期都正确，无需修正")

if __name__ == "__main__":
    main() 