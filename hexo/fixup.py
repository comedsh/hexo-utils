#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re


'common module for fixup the contents of the hexo pages'


__author__ = 'ShangYang'


pattern = re.compile('\((/categories)(.*)/\)')


# 目前的场景是，因为添加了数学顶层分类，所以将原有的 IT 技术相关的文章新增了一个类别，既"计算机科学与技术"
def match_and_replacement_categories():

    rootpath = '/Users/mac/tmp/draft'

    # 注意这里返回的是三元组
    for parent, dirnames, filenames in os.walk(rootpath):

        for filename in filenames:

            path = os.path.join(parent, filename)

            # 过滤掉子目录以及后缀不是 .md 的文件
            if parent != rootpath or os.path.splitext(path)[1] != ".md":
                continue
            # 替换文件内容，将类似于 /categories/Java/Lambda/ 替换为 /categories/计算机科学与技术/Java/Lambda/
            else:
                print(path)


# 测试替换 /categories 部分内容
# 该部分内容引用了 http://blog.csdn.net/five3/article/details/7104466 相关 Python 正则表达式的内容
def test_match_and_replacement_categories():
    line = '本文是由笔者所原创的[深入 Java Lambda 系列](/categories/Java/Lambda/)之一；'
    match = pattern.search(line)
    if match:
        # 打印出所有的文本
        print(match.string)
        # 打印出 (/categories/Java/Lambda/)
        print(match.group(1))

        def func(m):
            return "(" + m.group(1)+"/计算机技术与科学"+m.group(2) + ")"

        # 使用 pattern.sub 函数来替换文本
        print(pattern.sub(func, line))
    else:
        print('NO Matched')

def test3():
    # 将正则表达式编译成Pattern对象
    pattern = re.compile('hello')

    # 使用 Pattern 匹配文本，获得匹配结果，无法匹配时将返回 None
    # 要特别注意的是，match 默认从文本开始的地方匹配，既是相当于使用了 ^；如果不匹配则直接返回 None
    match = pattern.match('hello world!')

    if(match):
        print('matched')


if __name__ == '__main__':
    match_and_replacement_categories()