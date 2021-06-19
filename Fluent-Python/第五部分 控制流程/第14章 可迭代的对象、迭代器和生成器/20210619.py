"""10、Python3.3中新出现的句法：yield from"""
# 作用：将不同的生成器结合在一起使用，可以代替内层的for循环
import random


def chain(*iterables):
    for it in iterables:
        for i in it:
            yield i

s = 'ABC'
t = tuple(range(3))
print(list(chain(s, t)))
# ['A', 'B', 'C', 0, 1, 2]

def chain(*iterables):
    for i in iterables:
        yield from i

print(list(chain(s, t)))
# ['A', 'B', 'C', 0, 1, 2]


"""11、可迭代的归约函数"""
# 定义：接受一个可迭代的对象，然后返回单个结果
'''
   模块             函数                                                        说明
（内置）           all(it)                          it中的所有元素都为真值时返回True，否则返回False；all([])返回True
（内置）           any(it)                          只要it中有元素为真值就返回True，否则返回False；any([])返回False
（内置）           max(it, [key=,][default=])       返回it中值最大的元素；key是排序函数，与sorted函数中的一样；如果可迭代的对象为空，返回default
（内置）           min(it, [key=,][default=])       返回it中值最小的元素；key是排序函数，与sorted函数中的一样；如果可迭代的对象为空，返回default
functools         reduce(func, it, [initial])      把前两个元素传给func，然后把计算结果和第三个元素传给func，以此类推，返回最后的结果；如果提供了initial，把它当作第一个元素传入
（内置）           sum(it, start=0)                 it中所有元素的总和，如果提供可选的start，会把它加上
'''


"""12、深入分析iter函数"""
''' iter函数的一个用法：
传入两个参数，使用常规的函数或任何可调用的对象创建迭代器。这样使用时，第一个参数必须是可调用的对象，用于不断调用（没有参数），产出各个值；
第二个值是哨符，这是个标记值，当可调用的对象返回这个值时，触发迭代器抛出StopIteration异常，而不产出哨符
'''
def d6():
    return random.randint(1, 6)

d6_iter = iter(d6, 1)  # 返回1时，抛出StopIteration异常
print(d6_iter)
for roll in d6_iter:
    print(roll)

''' 逐行读取文件，直到遇到空行或到达文件末尾为止：
with open('filename') as f:
    for line in iter(f.readline, '\n'):
        process_line(line)
'''
