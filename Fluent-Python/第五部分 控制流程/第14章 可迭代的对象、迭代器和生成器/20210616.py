"""3、Sentence类第2版：典型的迭代器"""
import itertools
import re
import reprlib

RE_WORD = re.compile('\w+')

class SentenceIterator:  # 迭代器类
    def __init__(self, words):
        self.words = words
        self.index = 0  # 用于确定下一个要获取的单词

    def __next__(self):
        try:
            word = self.words[self.index]  # 获取Index索引上的单词
        except IndexError:
            raise StopIteration()  # 没有单词抛出StopIteration异常
        self.index += 1
        return word  # 返回单词

    def __iter__(self):
        return self


class Sentence:  # 通过索引从文本中提取单词
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # 返回一个字符串列表，里面的元素是正则表达式的全部非重叠匹配

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr函数用于生成大型数据结构的简略字符串表示形式

    def __iter__(self):  # 类可以迭代，因为实现了__iter__方法
        return SentenceIterator(self.words)  # 实例化并返回一个迭代器


"""4、Sentence类第3版：生成器函数"""
# 实现相同功能，但却更符合Python习惯的方式是，用生成器函数代替SentenceIterator类
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr函数用于生成大型数据结构的简略字符串表示形式

    def __iter__(self):  # __iter__方法是生成器函数
        for word in self.words:  # 迭代self.words
            yield word  # 产出当前word
        return   # return语句可以不要，这个函数直接“落空”，自动返回。不管有没有return语句，生成器函数都不会抛出StopInteration异常，而是在生成全部值之后直接退出


''' 生成器函数的工作原理
定义：只要Python函数的定义体中有yield关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象，生成器函数是生成器工厂
'''
def gen_123():  # 只要定义体内含有yield就是生成器函数
    yield 1
    yield 2
    yield 3


print(gen_123)  # gen_123是函数对象
# <function gen_123 at 0x000001E063744E18>
print(gen_123())  # 调用函数时，返回一个生成器对象
# <generator object gen_123 at 0x000001E063424A20>

for i in gen_123():  # 生成器是迭代器，会生成传给yield关键字的表达式的值
    print(i)
'''
1
2
3
'''

g = gen_123()  # g是迭代器
print(next(g))  # 调用next会获取yield生成的下一个元素
# 1


''' 生成器函数定义体的执行过程 '''
def gen_AB():
    print('start')
    yield 'A'  # 在for循环中第一次隐式调用next()函数时，会打印'start'，然后停在第一个yield语句，生成值'A'
    print('continue')
    yield 'B'  # 在for循环中第二次隐式调用next()函数时，会打印'continue'，然后停在第二个yield语句，生成值'B'
    print('end.')  # 第三次调用next()函数时，会打印'end.'，然后到达函数定义体的末尾，导致生成器对象抛出StopInteration异常

for c in gen_AB():  # 迭代时，for机制用于获取生成器对象，然后每次迭代时调用next()函数
    print('-->', c)
'''
start
--> A  # 生成器函数定义体中的yield 'A'语句会生成值A，提供给for循环使用，而A会赋值给变量c，最终输出 --> A
continue
--> B
end.  # 第三次调用next()，继续迭代，前进到生成器末尾，文本end.是由生成器函数定义体中第三个print函数输出的
# 到达生成器函数定义体的末尾时，生成器对象抛出StopIteration异常，for机制会捕获异常，因此循环终止时没有报错
'''


"""5、Sentence类第4版：惰性实现"""
# 目前版本的Sentence类都不具有惰性，因为__init__方法急迫地构建好了文本中的单词列表，然后将其绑定到self.words属性上。这样就得处理整个文本，列表使用的内存量可能与文本本身一样多
# re.finditer函数是re.findall函数的惰性版本，返回的不是列表，而是一个生成器，按需生成re.MatchObject实例。如果有很多匹配，re.finditer函数能够节省大量内存
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text  # 不需要words列表

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr函数用于生成大型数据结构的简略字符串表示形式

    def __iter__(self):  # __iter__方法是生成器函数
        for match in RE_WORD.finditer(self.text):  # finditer函数构建一个迭代器，包含self.text中匹配RE_WORD的单词，产生MatchObject实例
            yield match.group()  # 从MatchObject实例中提取匹配正则表达式的具体文本
        return


"""6、Sentence类第5版：生成器表达式"""
# 生成器表达式可以理解为列表推导的惰性版本：不会迫切地构建列表，而是返回一个生成器，按需惰性生成元素。生成器表达式是语法糖，完全可以替换成生成器函数。
res1 = [x*3 for x in gen_AB()]  # 列表推导式迫切地迭代gen_AB()函数生成地生成器对象产出的元素：'A'和'B'
'''
start
continue
end.
'''
for i in res1:  # 迭代res1列表
    print('-->', i)
'''
--> AAA
--> BBB
'''

res2 = (x*3 for x in gen_AB())  # 生成器表达式返回生成器，但是这里并不使用
print(res2)
# <generator object <genexpr> at 0x000001D15F10B480>
for i in res2:  # 只有for循环迭代res2时，gen_AB函数的定义体才会真正执行
    print('-->', i)
'''
start
--> AAA
continue
--> BBB
end.
'''

import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text  # 不需要words列表

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr函数用于生成大型数据结构的简略字符串表示形式

    def __iter__(self):  # 不再是生成器函数了，因为没有yield关键字，最终效果没变————还是返回一个生成器对象
        return (match.group() for match in RE_WORD.finditer(self.text))  # 使用生成器表达式构建生成器，然后将其返回

''' 何时使用生成器表达式
遇到简单的情况时，可以使用生成器表达式，扫一眼就知道代码作用；如果生成器表达式要分成多行写，则更应该定义生成器函数，以便提高可读性

'''


"""8、等差数列生成器"""
class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None -> 无穷数列

    def __iter__(self):
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None  # 是否是无穷数列
        index = 0
        while forever or result < self.end:  # 要么一直运行，要么result小于self.end时退出
            yield result  # 生成当前的result值
            index += 1
            result = self.begin + self.step * index  # 计算可能存在的下一个结果

ap = ArithmeticProgression(1, .5, 3)
print(list(ap))
# [1.0, 1.5, 2.0, 2.5]

''' 使用itertools模块生成等差数列 '''
# itertools.count()函数会生成从零开始的整数数列，然而这个函数从不停止
# itertools.takewhile()函数会生成一个使用另一个生成器的生成器，在指定的条件计算结果为False时停止
gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))  # 结合两个函数
print(list(gen))
# [1, 1.5, 2.0, 2.5]

def aritprog_gen(begin, step, end=None):  # 不是生成器函数，因为没有yield关键字
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)  # 生成器
    if end is not None:  # 如果不是无穷数列
        ap_gen = itertools.takewhile(lambda n: n < 3, ap_gen)
    return ap_gen  # 返回一个生成器
