"""9、标准库中的生成器函数"""
''' 用于过滤的生成器函数：从输入的可迭代对象中产出元素的子集，而且不修改元素本身
   模块                  函数                                                                         说明
itertools     compress(it, selector_it)                             并行处理两个可迭代的对象；如果selector_it中的元素是真值，产出it中对应的元素
itertools     dropwhile(predicate, it)                              处理it，跳过predicate的计算结果为真值的元素，然后产出剩下的各个元素（不再进一步检查）.
(内置)         filter(predicate, it)                                把it中的各个元素传给predicate，如果predicate(item)返回真值，那么产出对应的元素；如果predicate是None，那么只产出真值元素
itertools     filterfalse(predicate, it)                            与filter函数的作用类似，不过predicate的逻辑是相反的：predicate返回假值时产出对应的元素
itertools     islice(it, stop)或islice(it, start, stop, step=1)     产出it的切片，作用类似于s[:stop]或s[start:stop:step]，不过it可以是任何可迭代的对象，而且这个函数实现的是惰性操作
itertools     takewhile(predicate, it)                              predicate返回真值时产出对应的元素，然后立即停止，不再继续检查
'''
import itertools

def vowel(c):
    return c.lower() in 'aeiou'

strings = 'Aardvark'
print(list(filter(vowel, strings)))
# ['A', 'a', 'a']

print(list(itertools.filterfalse(vowel, strings)))
# ['r', 'd', 'v', 'r', 'k']

print(list(itertools.dropwhile(vowel, strings)))  # 当predicate的结果为true时，跳过，直到第一次遇到为false的情况。从第一个为false的元素开始，后面的元素全部返回。
# ['r', 'd', 'v', 'a', 'r', 'k']
# dropwhile非常适合过滤配置文件
'''
# with open('filename', 'r') as f:
#     for line in itertools.dropwhile(lambda n: n.starswith('#'), f):
#         print(line, end='')  # 返回注释后的文件内容
'''

print(list(itertools.takewhile(vowel, strings)))  # 当predicate的结果为true时，产出元素，直到第一次遇到为false时停止
# ['A', 'a']

print(list(itertools.compress(strings, (1, 0, 1, 1, 0, 1))))
# ['A', 'r', 'd', 'a']

print(list(itertools.islice(strings, 4)))  # 一系列切片操作
# ['A', 'a', 'r', 'd']
print(list(itertools.islice(strings, 4, 7)))
# ['v', 'a', 'r']
print(list(itertools.islice(strings, 1, 7, 2)))
# ['a', 'd', 'a']


''' 用于映射的生成器函数：在输入的单个可迭代对象（map和starmap函数处理多个可迭代的对象）中的各个元素上做计算，然后返回结果
   模块                  函数                                                                         说明
itertools           accumulate(it, [func])                        产出累积的总和；如果提供了func，那么把前两个元素传给它，然后把计算结果和下一个元素传给它，以此类推，最后产出结果
(内置)              enumerate(iterable, start=0)                  产出由两个元素组成的元组，结构是(index, item)，其中index从start开始计数，item则从iterable中获取
(内置)              map(func, it1, [it2, ..., itN])               把it中的各个元素传给func，产出结果；如果传入N个可迭代的对象，那么func必须能够接受N个参数，而且要并行 处理各个可迭代的对象                                 
itertools          starmap(func, it)                             把it中的各个元素传给func，产出结果；输入的可迭代对象应该产出可迭代的元素iit，然后以func(*itt)形式调用func
'''
import operator

sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]

print(list(itertools.accumulate(sample)))  # 没有func直接计算总和
# [5, 9, 11, 19, 26, 32, 35, 35, 44, 45]
print(list(itertools.accumulate(sample, min)))  # 计算最小值
# [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]
print(list(itertools.accumulate(sample, max)))  # 计算最大值
# [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]
print(list(itertools.accumulate(sample, operator.mul)))  # 计算乘积
# [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
print(list(itertools.accumulate(range(1, 11), operator.mul)))  # 计算1!到10!各个数的阶乘
# [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

strings = 'albatroz'
print(list(enumerate(strings, 1)))  # 对字符编号
# [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]
print(list(map(operator.mul, range(11), range(11))))  # 计算各个整数的平方
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
print(list(map(operator.mul, range(11), [2, 4, 8])))  # 元素少的可迭代对象到头后停止
# [0, 4, 16]
print(list(map(lambda a, b: (a, b), range(11), [2, 4, 8])))  # 模拟内置函数zip的行为
# [(0, 2), (1, 4), (2, 8)]

print(list(itertools.starmap(operator.mul, enumerate(strings, 1))))  # 根据字母所在位置，重复相应的次数
# ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']
print(list(itertools.starmap(lambda a, b: b/a, enumerate(itertools.accumulate(sample), 1))))  # 计算平均值
# [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]


''' 用于合并的生成器函数：从输入的多个可迭代对象中产出元素
   模块                  函数                                                                         说明
itertools            chain(it1, ..., itN)                                    先产出it1中的所有元素，然后产出it2中的所有元素，以此类推，无缝连接在一起
itertools            chain.from_iterable(it)                                 产出it生成的各个可迭代对象中的元素，一个接一个，无缝连接在一起；it应该产出可迭代的元素，例如可迭代的对象列表
itertools            product(it1, ..., itN, repeat=1)                        计算笛卡尔积：从输入的各个可迭代对象中获取元素，合并成由N个元素组成的元组，与嵌套的for循环效果一样；repeat指明重复处理多少次输入的可迭代对象
(内置)                zip(it1, ..., itN)                                      并行从输入的各个可迭代对象中获取元素，产出由N个元素组成的元组，只要有一个可迭代的对象到头了，就停止
itertools            zip_longest(it1, ..., itN, fillvalue=None)              并行从输入的各个可迭代对象中获取元素，产出由N个元素组成的元组，等到最长的可迭代对象到头后才停止，空缺的值使用fillvalue填充
'''
print(list(itertools.chain('ABC', range(2))))  # 通常传入两个或更多个可迭代对象
# ['A', 'B', 'C', 0, 1]
print(list(itertools.chain(enumerate('ABC'))))  # 只传入一个可迭代对象没啥用
# [(0, 'A'), (1, 'B'), (2, 'C')]
print(list(itertools.chain.from_iterable(enumerate('ABC'))))  # 从可迭代对象中获取每个元素，同时每个元素也是可迭代的对象，按顺序连接每个元素
# [0, 'A', 1, 'B', 2, 'C']

print(list(zip('ABC', range(5))))  # 两个可迭代的对象合并成一系列元组
# [('A', 0), ('B', 1), ('C', 2)]
print(list(zip('ABC', range(5), [10, 20, 30, 40])))  # 只要有一个可迭代对象到头了，生成器就停止
# [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
print(list(itertools.zip_longest('ABC', range(5))))  # 输入的任何可迭代对象都会处理到头，如果需要默认填充None
# [('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]
print(list(itertools.zip_longest('ABC', range(5), fillvalue='?')))  # fillvalueg关键字参数用于指定填充的值
# [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]

print(list(itertools.product('ABC', range(2))))  # 笛卡尔积，3*2=6
# [('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]
print(list(itertools.product('高一 高二 高三'.split(), '一班 二班 三班'.split())))
# [('高一', '一班'), ('高一', '二班'), ('高一', '三班'), ('高二', '一班'), ('高二', '二班'), ('高二', '三班'), ('高三', '一班'), ('高三', '二班'), ('高三', '三班')]
print(list(itertools.product('ABC')))  # 如果只传入一个可迭代的对象，product函数产出的是一系列只有一个元素的元组，没啥意义
# [('A',), ('B',), ('C',)]
print(list(itertools.product('ABC', repeat=2)))  # repeat关键字参数用于重复处理可迭代对象
# [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]


''' 用于扩展的生成器函数：从一个元素中产出多个值，扩展输入的可迭代对象
   模块                       函数                                                        说明
itertools           combinations(it, out_len)                      把it产出的out_len个元素组合在一起，然后产出
itertools           combinations_with_replacement(it, out_len)     把it产出的out_len个元素组合在一起，然后产出，包含相同元素的组合
itertools           count(start=0, step=1)                         从start开始不断产出数字，按step指定的步幅增加
itertools           cycle(it)                                      从it中产出各个元素，存储各个元素的副本，然后按顺序重复不断地产出各个元素
itertools           permutations(it, out_len=None)                 把out_len个it产出的元素排列在一起，然后产出这些排列；out_len的默认值等于len(list(it))
itertools           repeat(item, [times])                          重复不断地产出指定的元素，除非提供times，指定次数    
'''
ct = itertools.count()  # 构建生成器ct
print(next(ct))  # 获取ct中的第一个元素
# 0
print(next(ct), next(ct), next(ct))  # 特别注意，不能使用ct构建列表，因为ct是无穷的
# 1, 2, 3
print(list(itertools.islice(itertools.count(1, .3), 3)))  # 可以使用islice和takewhile做限制来构建列表
# [1, 1.3, 1.6]

cy = itertools.cycle('ABC')
print(next(cy))
# A
print(list(itertools.islice(cy, 7)))  # 只有受到islice函数的限制，才能构建列表
# ['B', 'C', 'A', 'B', 'C', 'A', 'B']

rp = itertools.repeat(7)  # 始终产出数字7
print(next(rp), next(rp))
# 7 7
print(list(itertools.repeat(8, 4)))  # 使用times参数限制产出
# [8, 8, 8, 8]
print(list(map(operator.mul, range(11), itertools.repeat(5))))  # repeat生成器函数的常见用途：为map函数提供固定参数，这里提供乘数5
# [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

# combinations、combinations_with_replacement、permutations以及product函数，称为组合学生成器
print(list(itertools.combinations('ABC', 2)))  # 每2个元素的各种组合，元素顺序无关紧要
# [('A', 'B'), ('A', 'C'), ('B', 'C')]
print(list(itertools.combinations_with_replacement('ABC', 2)))  # # 每2个元素的各种组合，包含相同元素的组合
# [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
print(list(itertools.permutations('ABC', 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]  # 每2个元素的各种组合，元素顺序有重要意义


''' 用于重新排列元素的生成器函数：产出输入的可迭代对象中的全部元素，不过会以某种方式重新排列
   模块                       函数                                                        说明
itertools              groupby(it, key=None)                  产出由两个元素组成的元素，形式为(key, group），其中key是分组标准，group是生成器，用于产出分组里的元素
(内置)                  reversed(seq)                          从后向前，倒序产出seq中的元素；seq必须是序列，或者是实现了__reversed__特殊方法的对象
itertools              tree(it, n=2)                          产出一个由n个生成器组成的元组，每个生成器用于单独产出输入的可迭代对象中的元素
'''
print(list(itertools.groupby('LLLLAAGGG')))  # 产出(key, group_generator)形式的元组
# [('L', <itertools._grouper object at 0x000002AEEEABACC0>), ('A', <itertools._grouper object at 0x000002AEEEABAC50>), ('G', <itertools._grouper object at 0x000002AEEEABACF8>)]
for char, group in itertools.groupby('LLLLAAGGG'):  # 处理groupby函数返回的生成器要嵌套迭代：这里外层使用for循环
    print(char, '->', list(group))  # 内层使用列表推导
# L -> ['L', 'L', 'L', 'L']
# A -> ['A', 'A']
# G -> ['G', 'G', 'G']

animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear', 'bat', 'dolphin', 'shark', 'lion']
animals.sort(key=len)  # 就地排序，为了使用groupby函数，要排序输入，这里按照单词的长度排序
print(animals)
# ['rat', 'bat', 'duck', 'bear', 'lion', 'eagle', 'shark', 'giraffe', 'dolphin']
for length, group in itertools.groupby(animals, len):
    print(length, '->', list(group))
# 3 -> ['rat', 'bat']
# 4 -> ['duck', 'bear', 'lion']
# 5 -> ['eagle', 'shark']
# 7 -> ['giraffe', 'dolphin']

for length, group in itertools.groupby(reversed(animals), len):  # 使用reversed函数反向迭代animals
    print(length, '->', list(group))
# 7 -> ['dolphin', 'giraffe']
# 5 -> ['shark', 'eagle']
# 4 -> ['lion', 'bear', 'duck']
# 3 -> ['bat', 'rat']

g1, g2 = itertools.tee('ABC')  # tee函数只有一个作用：从输入的一个可迭代对象中产出多个生成器，每个生成器都可以产出输入的各个元素
print(list(g1), list(g2))
# ['A', 'B', 'C'] ['A', 'B', 'C']
print(list(zip(*itertools.tee('ABC'))))
# [('A', 'A'), ('B', 'B'), ('C', 'C')]
