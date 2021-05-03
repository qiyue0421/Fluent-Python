# 散列表是字典类型性能出众的根本原因，跟字典有关的内置函数都在 __builtins__.__dict__ 模块中

"""第5章 一等函数、泛映射类型"""
# collections.abc 模块中有 Mapping 和 MutableMapping 这两个抽象基类，它的作用是为dict和其他类似的类型定义形式接口，作为形式化的文档定义了构建一个映射类型所需要的最基本的接口，
# 可以跟 isinstance 一起被用来判断某个数据是不是广义上的映射类型：
from collections import abc

my_dict = {}
print(isinstance(my_dict, abc.Mapping))

# 标准库里的所有映射类型都是利用dict来实现的，因此它们有个共同的限制——只有可散列的数据类型才能用作这些映射里的键（值不需要是可散列的）
'''
可散列类型定义：
    ①、如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现__hash__()方法
    ②、可散列对象还要有__eq__()方法，这样才能跟其他键做比较，如果两个可散列对象是相等的，那么它们的散列值一定是一样的

原子不可变数据类型（str、bytes和数值类型）都是可散列类型，frozenset也是可散列的。元组的话，只有当一个元组包含的所有元素都是可散列类型的情况下，它才是可散列的
'''

# 创建字典的不同方式
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))  # zip()内置函数将可迭代对象作为参数，将对象中对应的元素打包成一个个元组，返回由元组组成的列表
d = dict([('two', 2), ('one', 1), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})
print(a == b == c == d == e)


"""2、字典推导"""
# 字典推导可以从任何以键值对作为元素的可迭代对象中构建出字典
DIAL_CODES = [(86, 'China'), (91, 'India'), (1, 'United States'), (62, 'Indonesia'), (55, 'Brazil'), (92, 'Pakistan')]
contry_code = {country: code for code, country in DIAL_CODES}
print(contry_code)


"""3、常见的映射方法"""
# 用setdefault处理找不到的键
my_dict = {'runoob': '菜鸟教程', 'google': 'Google 搜索'}

print("Value : %s" % my_dict.setdefault('runo0b', None))  # 如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。


"""4、映射的弹性键查询"""
# 如果某个键在映射里不存在，但是希望读取这个键时能得到一个默认值，实现的两种方法：
# ①、通过defaultdict类型实现：
'''
比如新建了字典 dd = defaultdict(list)，如果键 'new-key' 在dd中还不存在的话，表达式dd['new-key']会按照以下步骤行事：
第5章 一等函数)、调用list()来建立一个新列表
2)、把这个新列表作为值，'new-key'作为它的键，放到dd中
3)、返回这个列表的引用
'''

from collections import defaultdict

index = defaultdict(list)
print(index['pp'])

# ②、特殊方法 __missing__
# 所有映射类型在处理找不到的键时都会牵扯到__missing__方法，该方法只会被__getitem__调用


class StrKeyDict0(dict):  # 继承dict基类
    def __missing__(self, key):
        if isinstance(key, str):  # 没有这个测试，代码会陷入无限递归
            raise KeyError(key)  # 如果找不到的键本身就是字符串，那就抛出KeyError异常
        return self[str(key)]  # 如果找不到的键不是字符串，那么把它转换成字符串再进行查找——调用__getitem__

    def get(self, key, default=None):
        try:
            return self[key]  # get()方法把查找工作用self[key]的形式委托给__getitem__，这样在查找失败之前可以通过__missing__再给某个键一个机会
        except KeyError:
            return default  # 如果抛出KeyError，那么说明__missing__也失败了，返回default

    def __contains__(self, item):  # 实现 k in d 操作，保证一致性
        return item in self.keys() or str(item) in self.keys()


"""5、字典的变种"""
# ①、collections.OrderedDict: 这个类型在添加键的时候会保持顺序，因此键的迭代次序总是一致的。popitem方法默认删除并返回的是字典的最后一个元素，但是如果像
# my_odict.popitem(last=False) 这样调用它，那么它删除并返回第一个被添加进去的元素

# ②、collections.ChainMap: 该类型可以容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到为止
from collections import ChainMap
import builtins

pylookup = ChainMap(locals(), globals(), vars(builtins))
print(pylookup['max'])

# ③、collections.Counter: 这个映射类型会给键准备一个整数计数器。每次更新一个键的时候都会增加这个计数器。Counter实现了 + 和 - 运算符用来合并记录，还有 most_common([n]) 方法，
# 该方法会按照次序返回映射里最常见的n个键和它们的计数

from collections import Counter

words = 'abracadavra'
ct = Counter(words)
print(ct)
# Counter({'a': 5, 'r': 2, 'b': 第5章 一等函数, 'c': 第5章 一等函数, 'd': 第5章 一等函数, 'v': 第5章 一等函数})

ct.update('aaaaazzz')
print(ct)
# Counter({'a': 10, 'z': 3, 'r': 2, 'b': 第5章 一等函数, 'c': 第5章 一等函数, 'd': 第5章 一等函数, 'v': 第5章 一等函数})

print(ct.most_common(2))
# [('a', 10), ('z', 3)]

# ④、collections.UserDict: 这个类就是把标准dict用纯Python又实现了一遍，是用于让用户继承写子类的（前面三种是开箱即用型）。
