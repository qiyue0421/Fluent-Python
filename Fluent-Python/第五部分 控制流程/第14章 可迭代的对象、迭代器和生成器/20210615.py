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


"""2、可迭代的对象与迭代器的对比"""
''' 可迭代的对象与迭代器
# 定义
可迭代的对象：使用iter内置函数可以获取迭代器的对象。如果对象实现了能返回迭代器的__iter__方法，那么对象就是可迭代的。序列都可以迭代；实现了__getitem__方法，而且其参数是从零开始的索引，这种对象也可以迭代
迭代器：实现了无参数的__next__方法，返回序列中的下一个元素；如果没有元素了，那么抛出StopIteration异常的对象就是迭代器。Python中的迭代器还实现了__iter__方法，因此迭代器也可以迭代
两者间的关系：Python从可迭代的对象中获取迭代器

# 简单for循环
>>> s = 'ABC'  # 可迭代对象，背后有迭代器，只是我们看不到
>>> for char in s:
...    print(char)
...
A
B
C

# 没有for语句，不得不使用while循环模拟
>>> s = 'ABC'
>>> it = iter(s)  # 使用可迭代的对象构建迭代器it
>> while True:
...    try:
...        print(next(it))  # 不断在迭代器上调用next函数，获取下一个字符
...    except StopIteration:  # 没有字符了，会抛出StopIteration异常
...        del it  # 释放对it的引用，即废弃迭代器对象
...        break  # 退出循环
...
A
B
C
'''


''' 两个标准的迭代器接口方法：
__next__  返回下一个可用的元素，如果没有元素了，抛出StopIteration异常
__iter__  返回self，以便在应该使用可迭代对象的地方使用迭代器，例如在for循环中

# 这个接口在collections.abc.Iterator抽象基类中制定，abc.Iterator源码：
class Iterator(Iterable):  # 继承自Iterable类

    __slots__ = ()

    @abstractmethod
    def __next__(self):  # 定义了__next__抽象方法
        'Return the next item from the iterator. When exhausted, raise StopIteration'
        raise StopIteration

    def __iter__(self):  # __iter__抽象方法在Iterable类中定义
        return self  # 实现__iter__方法的方式是返回实例本身，这样在需要可迭代对象的地方可以使用迭代器

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterator:
            return _check_methods(C, '__iter__', '__next__')
        return NotImplemented
'''

s3 = Sentence('Pig and Pepper')  # 创建实例s3，包含3个单词
it = iter(s3)  # 从s3中获取迭代器
print(it)
# <iterator object at 0x0000029446BFAB00>
print(next(it))  # 调用next(it)，获取下一个单词
# Pig
print(next(it))
# and
print(next(it))
# Pepper
'''
print(next(it))  # 没有单词会抛出StopIteration
Traceback (most recent call last):
  ...
StopIteration
'''

print(list(it))  # 元素取完后迭代器为空
# []
print(list(iter(s3)))  # 再次迭代需要重新构建迭代器
# ['Pig', 'and', 'Pepper']


