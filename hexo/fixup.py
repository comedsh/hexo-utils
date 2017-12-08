#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import fileinput

'common module for fixup the contents of the hexo pages'


__author__ = 'ShangYang'


# 目前的场景是，因为添加了数学顶层分类，所以将原有的 IT 技术相关的文章新增了一个类别，既"计算机科学与技术"

class Categories:

    # 该方法的初衷是遍历所有的文档，找到包含 (/categories/Java/Lambda/) 的文章，并将其替换为 (/categories/计算机科学与技术/Java/Lambda/)
    # 有些特殊场景需要考虑，比如 (/categories/Java/Lambda/) 与 (/categories/Spring/Security/OAuth) 之间的异同，详情参考相关的测试方法
    @staticmethod
    def replacement_categories_url(rootpath):

        #rootpath = '/Users/mac/blog/www.shangyang.me/source/_drafts'

        pattern = re.compile('\((/categories)(.*?)\)')

        # 注意这里返回的是三元组
        for parent, dirnames, filenames in os.walk(rootpath):

            for filename in filenames:

                path = os.path.join(parent, filename)

                # 过滤掉子目录以及后缀不是 .md 的文件
                if parent != rootpath or os.path.splitext(path)[1] != ".md":
                    continue

                # 替换文件内容，将类似于 /categories/Java/Lambda/ 替换为 /categories/计算机科学与技术/Java/Lambda/
                else:
                    # 首先判断该文件是否是需要被替换的对象
                    found = False
                    f = open(path, 'r')
                    lines = f.readlines()
                    source_to_replace = ''
                    target_to_replace = ''
                    file_content = ''
                    for line in lines:
                        match = pattern.search(line)
                        if match:
                            found = True
                            # 返回 (/categories/Java/Lambda/) 所以两边不加括号
                            source_to_replace = match.group(0)
                            # match.group(1) 返回的是 /categories，match.group(2) 同样是这样的，所以两边需要加上括号；
                            target_to_replace = "(" + match.group(1) + "/计算机科学与技术" + match.group(2) + ")"
                            ff = open(path, 'r')
                            file_content = ff.read()
                            ff.close()
                            print(source_to_replace + " --> " + target_to_replace + "; the filename is: "+filename)
                            break
                    f.close()

                    # 然后，替换文件中的内容，实现逻辑是全覆盖；

                    if found:
                        f = open(path, 'w')
                        file_content = file_content.replace(source_to_replace, target_to_replace)
                        f.write(file_content)
                        f.close()
                        print("file "+filename+" gets overwrited!")


    # 测试替换 /categories 部分内容
    # 该部分内容引用了 http://blog.csdn.net/five3/article/details/7104466 相关 Python 正则表达式的内容
    ############## 注意 ###############
    # 注意，有个很重要的地方，就是 (/categories/Java/Lambda/) 与 (/categories/Spring/Security/OAuth) 之间的异同
    # 一个有最后的 / 一个没有；所以为了统一，只能将正则表达式从 '\((/categories)(.*/)\)' 改为 '\((/categories)(.*)\)' 既统一修改改为
    # 最后不带斜杠的方式；
    ############## 注意 2 #############
    # 改成上述的方式以后
    # 但是出现了下面的情况，问题就在于不会在第一个 ) 结束的时候结束匹配而是会尽量的匹配一句话的后一个 )；
    # (/categories/Java/Lambda/)之一；本文是笔者在深入分析完官文 [lambda state final](http://cr.openjdk.java.net/~briangoetz/lambda/lambda-state-final.html) --> (/categories/计算机科学与技术/Java/Lambda/)之一；本文是笔者在深入分析完官文 [lambda state final](http://cr.openjdk.java.net/~briangoetz/lambda/lambda-state-final.html)
    # java-lambda-02-basics.md
    # 所以要使用懒匹配的方式，既是匹配到第一个 ) 便结束即可；根据官方文档，使用懒加载的话，需要使用到符号 ?，参考 https://docs.python.org/2/library/re.html
    # 所以，最终的正则表达式为 '\((/categories)(.*?)\)'，其中多了这么一个 ? 号；
    @staticmethod
    def test_replacement_categories_url():
        line = '本文是由笔者所原创的[深入 Java Lambda 系列](/categories/Java/Lambda/)之一；'
        #line = '本文是对 Spring Security OAuth 2.0 进行源码分析的[系列文章](/categories/Spring/Security/OAuth)之一；'
        # 因为要替换 /categories 为 /categories/计算机科学与技术/ 所以，需要为 /categories 通过 () 的方式来建立一个 group
        pattern = re.compile('\((/categories)(.*?)\)')
        # 注意，这里不能使用 match 方法而必须使用 search，因为 match 默认行为是从字符串开始处进行匹配，既相当于使用了 ^
        match = pattern.search(line, re.I)
        if match:
            # 打印出所有的文本
            print(match.string)
            # 打印出 (/categories/Java/Lambda/)
            print("group 1: " + match.group(1))
            print("group 2: " + match.group(2))

            def func(m):
                return "(" + m.group(1)+"/计算机科学与技术"+m.group(2) + ")"

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
    Categories.replacement_categories_url('/Users/mac/blog/www.shangyang.me/source/_posts')