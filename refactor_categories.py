#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import yaml

def get_frontmatter(content):
    """从文件内容中提取 frontmatter 和正文"""
    match = re.match(r'---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter, body
        except yaml.YAMLError:
            return None, content # 解析失败则返回原始内容
    return None, content

def set_frontmatter(frontmatter, body):
    """将 frontmatter 和正文合并为文件内容"""
    if not frontmatter:
        return body
    
    fm_yaml = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    return f"---\n{fm_yaml}---\n\n{body}"

def refactor_categories():
    """重构文章的分类"""
    posts_dir = Path('_posts')
    if not posts_dir.is_dir():
        print(f"❌ 错误: 目录 '{posts_dir}' 不存在。")
        return

    # 定义顶级分类与其对应的子目录/关键词
    top_level_map = {
        "计算机组成原理": "Computer Organization",
        "数据结构": "Data Structure",
        "算法": "Acwing",
        "LLM": "LLM",
        "设计模式": "Design Pattern",
        "Java核心技术": "Core Java",
        "CS61B": "cs61b",
        "CMU 15-213": "cmu15213",
        "MIT 6.S081": "MIT6.s081",
        "操作系统": "WHUOS",
        "多智能体强化学习": "MARL"
    }
    
    # 子分类到顶级分类的映射 (小写 -> 标准顶级分类名)
    sub_to_top_level = {v.lower(): k for k, v in top_level_map.items()}

    # 需要特殊处理的子分类映射 (小写 -> 标准子分类名)
    subcategory_remap = {
        "笔记": "笔记",
        "题目": "题解",
        "note": "笔记",
        "solution": "题解",
        "图论": "图论",
        "动态规划": "动态规划",
        "基础算法": "基础算法",
        "二叉树": "二叉树",
        "图": "图",
        "字符串": "字符串",
        "栈": "栈",
        "线性表": "线性表",
        "队列": "队列",
        "knowledge": "知识点",
        "problems": "题解",
        "cs 224n": "CS224N",
        "lab": "实验"
    }

    processed_count = 0
    changed_count = 0

    for filepath in posts_dir.rglob('*.md'):
        processed_count += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"⚠️  无法读取文件: {filepath} - {e}")
            continue

        frontmatter, body = get_frontmatter(original_content)

        if not frontmatter or 'categories' not in frontmatter:
            continue

        original_categories = frontmatter.get('categories', [])
        if isinstance(original_categories, str):
            original_categories = [original_categories] # 兼容单字符串的情况
        
        new_categories = []
        
        # 1. 确定顶级分类
        top_category = None
        # 从文件路径中寻找顶级分类
        for part in filepath.parts:
            if part.lower() in sub_to_top_level:
                top_category = sub_to_top_level[part.lower()]
                break
        
        if not top_category:
            continue # 如果路径中没有顶级分类信息，则暂时不处理

        new_categories.append(top_category)

        # 2. 确定子分类
        sub_category = None
        # 从已有的分类中寻找
        if original_categories:
            for cat in original_categories:
                cat_lower = str(cat).lower()
                if cat_lower in subcategory_remap:
                    sub_category = subcategory_remap[cat_lower]
                    break
        
        # 如果还没找到，再从路径中寻找
        if not sub_category:
            for part in filepath.parts:
                part_lower = part.lower()
                if part_lower in subcategory_remap:
                     sub_category = subcategory_remap[part_lower]
                     break

        if sub_category and sub_category not in new_categories:
            new_categories.append(sub_category)

        # 如果分类发生了变化
        if new_categories != original_categories:
            print(f"🔄 更新 '{filepath.relative_to(posts_dir)}'")
            print(f"   原分类: {original_categories} → 新分类: {new_categories}")
            frontmatter['categories'] = new_categories
            
            # 写回文件
            new_content = set_frontmatter(frontmatter, body)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                changed_count += 1
            except Exception as e:
                print(f"❌ 写入文件失败: {filepath} - {e}")

    print("-" * 60)
    print(f"🎉 处理完成! 共检查 {processed_count} 个文件，更新了 {changed_count} 个文件。")

if __name__ == "__main__":
    refactor_categories() 