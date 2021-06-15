""" 迭代是数据处理的基石
* 扫描内存中放不下的数据集时，需要找到一种惰性获取数据项的方式，即按需一次获取一个数据项，这就是迭代器模式。
* Python2.2加入了yield关键字，这个关键字用于构建生成器，其作用与迭代器一样，所有生成器都是迭代器，因为生成器完全实现了迭代器接口。
* 迭代器与生成器的区别：迭代器用于从集合中取出元素；而生成器用于“凭空”生成元素。斐波那契数列中的数有无穷多个，在一个集合里放不下。
* 在Python3中，生成器有着广泛的用途。现在，即使是内置的range()函数也返回一个类似生成器的对象，而以前则返回完整的列表
* 在Python中，所有集合都可以迭代。在Python语言内部，迭代器用于支持：
    for循环
    构建和扩展集合类型
    逐行遍历文本文件
    列表推导、字典推导和集合推导
    元组拆包
    调用函数时，使用*拆包实参
"""


"""1、Sentence类第1版：单词序列"""
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:  # 通过索引从文本中提取单词
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # 返回一个字符串列表，里面的元素是正则表达式的全部非重叠匹配

    def __getitem__(self, index):  # 任何序列都可以迭代，只要实现了__getitem__方法
        return self.words[index]  # 返回指定索引位上的单词

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr函数用于生成大型数据结构的简略字符串表示形式


s = Sentence('"The time has come," the Walrus said,')
print(s)
# Sentence('"The time ha... Walrus said,')

# 测试能否迭代
for word in s:
    print(word)
'''
The
time
has
come
the
Walrus
said
'''

print(list(s))  # 因为可以迭代，所以Sentence实例可以用来构建列表和其他可迭代的类型
# ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']

'''序列可以迭代的原因：iter函数
解释器需要迭代对象x时，会自动调用iter(x)。内置iter函数有以下作用：
    * 检查对象是否实现了__iter__方法，如果实现了就调用它，获取一个迭代器
    * 如果没有实现__iter__方法，但是实现了__getitem__方法，Python会创建一个迭代器，尝试按顺序（从索引0开始）获取元素
    * 如果尝试失败，Python抛出TypeError异常，通常会提示“C object is not aiterable”（C对象不可迭代），其中C是目标对象所属的类

任何Python序列都可迭代的原因是，它们都实现了__getitem__方法，
'''




