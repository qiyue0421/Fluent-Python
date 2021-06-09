"""1、Vector类：用户定义的序列类型"""
# 使用组合模式实现Vector类，而不使用继承。向量的分量存储在浮点数组中，而且还将实现不可变扁平序列所需的方法。
import itertools
import numbers

"""2、Vector类第1版：与Vector2d类兼容"""
from array import array
import reprlib
import math
import functools
import operator


class Vector:
    """ Vector类 """
    typecode = 'd'  # 类属性，在类实例和字节序列之间转换时使用
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)  # self._components是“受保护的”实例属性，把Vector的分量保存在一个数组中

    def __iter__(self):  # 将实例变成可迭代对象，这样才能拆包，比如 x, y = my_vector，这里使用生成器表达式一个接一个产出分量
        return iter(self._components)  # 构建一个迭代器

    def __repr__(self):
        components = reprlib.repr(self._components)  # 使用reprlib.repr()函数获取self.components的有限长度表现形式（如 array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])）
        components = components[components.find('['):-1]  # 去掉前面的 array('d' 和后面的 )，保留[]内的内容（包括一堆方括号）
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))  # 得到一个元组，显示为一个有序对

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)  # 直接使用self._components构建bytes对象

    def __eq__(self, other):
        """ 使用zip()函数提高比较效率
        if len(self) != len(other):  # 如果两个对象的长度不一样，那么它们不相等
            return False
        for a, b in zip(self, other):  # 提高比较效率，使用zip函数生成一个由元组构成的生成器，元组中的元素来自参数传入的各个可迭代对象
            if a != b:  # 只要有分量不同，返回False
                return False
        return True
        """
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))  # 用all()函数比较所有分量的结果都是True，首先要检查两个操作数长度是否相同，因为zip()函数会在最短的那个操作数耗尽时停止

    def __hash__(self):
        hashes = (hash(x) for x in self._components)  # 创建一个生成器表达式，惰性计算各个分量的散列值，得到一个可迭代对象
        # hashes = map(hash, self._components)  # 也可以使用map()函数，将函数应用到各个元素上，生成一个新序列
        return functools.reduce(operator.xor, hashes, 0)  # 使用xor函数计算聚合的散列值，第三个参数0是初始值

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))  # 首先计算各分量的平方之和，然后再使用sqrt方法开平方

    def __bool__(self):
        return bool(abs(self))  # 使用abs()计算模，然后把结果转换成布尔值，因此0.0是False，非零值是True

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):  # 处理切片
        cls = type(self)  # 获取实例所属的类（即Vector），供后面使用
        if isinstance(index, slice):  # 如果index参数的值是slice对象
            return cls(self._components[index])  # 调用类的构造方法，使用_components数组的切片构建一个新的Vector实例
        elif isinstance(index, numbers.Integral):  # 如果index参数是int或其他整数类型
            # noinspection PyTypeChecker
            return self._components[index]  # 返回数组中相应的元素
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))  # 否则抛出异常

    def __getattr__(self, name):  # 动态存取属性，通过单个字母访问前几个分量
        cls = type(self)  # 获取实例所属的类（即Vector）
        if len(name) == 1:  # 如果属性名只有一个字母，那么可能是shortcut_names中的一个
            pos = cls.shortcut_names.find(name)  # 查找字母的位置
            if 0 <= pos < len(self._components):  # 如果位置落在范围内，返回数组中对应的元素
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):  # 禁止对实例属性赋值
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attributes {attr_name!r}'  # 设置错误信息
            elif name.islower():  # 如果name是小写字母，为所有小写字母设置一个错误消息
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)  # 抛出异常
        super().__setattr__(name, value)  # 默认情况：在超类上调用__setattr__方法，提供标准行为

    def angle(self, n):  # 使用“n维球体”词条中的公式计算某个角坐标
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):  # 创建生成器表达式，按需计算所有角坐标
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):  # 格式化函数
        if format_spec.endswith('h'):  # 超球面坐标
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self), self.angles()])  # 使用itertools.chain函数生成生成器表达式，无缝迭代向量的模和各个角坐标
            outer_fmt = '<{}>'  # 使用尖括号显示球面坐标
        else:
            coords = self
            outer_fmt = '({})'  # 使用圆括号显示笛卡尔坐标
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    # 从字节序列转换成Vector实例
    @classmethod
    def frombytes(cls, octets):  # 不用传入self参数，相反需要通过cls传入类本身
        typecode = chr(octets[0])  # 从第一个字节中读取typecode
        memv = memoryview(octets[1:]).cast(typecode)  # 使用传入的octets字节序列创建一个memoryview
        return cls(memv)  # 直接把memoryview传给构造方法，无需拆包


# 测试
print(Vector([3.1, 4.2]))
# (3.1, 4.2)
print(Vector((3, 4, 5)))
# (3.0, 4.0, 5.0)
print(Vector(range(10)))


"""3、切片原理"""
# 了解__getitem__和切片的行为
class MySeq:
    def __getitem__(self, index):
        return index  # 直接返回传给它的值

s = MySeq()
print(s[1])  # 单个索引
# 1
print(s[1:4])
# slice(1, 4, None)  # 1:4表示法变成了slice(1, 4, None)
print(s[1:4:2])
# slice(1, 4, 2)  # 从1开始，到4结束，步幅为2
print(s[1:4:2, 9])
# (slice(1, 4, 2), 9)  # 如果[]中有逗号，那么__getitem__收到的是元组
print(s[1:4:2, 7:9])
# (slice(1, 4, 2), slice(7, 9, None))  # 元组中甚至也可以有多个切片对象

# 审查内置类型slice
print(dir(slice))  # 发现它有start、stop和step数据属性，以及indices方法
'''

['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', 
'__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']

s.indices(len) -> (start, stop, stride)
    给定长度为len的序列，计算S表示的扩展切片的起始和结尾索引，以及步幅。超出边界的索引会被截掉，这与常规切片的处理方式一样。主要用于优雅的处理缺失索引和复数索引，
    以及长度超过目标序列的切片，这个方法会“整顿”元组，把start、stop和stride都变成非负数，而且都落在指定长度序列的边界内。
    
假设有个长度为5的序列，例如'ABCDE':
>>> slice(None, 10, 2).indices(5)
(0, 5, 2)
'ABCDE'[:10:2] 等同于 'ABCDE'[0:5:2]

>>> slice(-3, None, None).indices(5)
(2, 5, 1)
'ABCDE'[-3:] 等同于 'ABCDE'[2:5:1]
    
'''
v7 = Vector(range(7))
print(v7[-1])
# 6.0
print(v7[1:4])  # 切片索引创建一个新的Vector实例
# (1.0, 2.0, 3.0)


"""4、动态存取属性"""
'''对 my_obj.x 表达式，Python会进行如下查找：
①、首先检查my_obj实例有没有名为x的属性
②、到类（my_obj.__class__）中找
③、顺着继承树继续查找
④、调用my_obj所属类中定义的__getattr__方法，传入self和属性名称的字符串形式（如'x'）

'''
v = Vector(range(5))
print(v)
# (0.0, 1.0, 2.0, 3.0, 4.0)
print(v.x)  # 获取第一个元素
# 0.0

''' __getattr__运作机制：
仅当对象没有指定名称的属性时，Python才会调用那个方法，这是一种后备机制。v.x=10这样赋值之后，v对象有x属性了，因此使用v.x获取x属性时的值不会调用__getattr__方法，解释器直接返回绑定到v.x上的值
>>> v.x = 10  # 为v.x赋值
>>> print(v.x)  # 读取v.x，得到的是新值
10
>>> print(v)  # 可是，向量的分量没有变
(0.0, 1.0, 2.0, 3.0, 4.0)

'''


"""5、散列和快速等值测试"""
'''reduce()函数原理
* 函数体：reduce(function, iterable, initializer)
* 关键思想：把一系列值归约成单个值
* 说明：reduce()函数的第一个参数是接受两个参数的函数，第二个参数是一个可迭代的对象。假如有个接受两个参数的fn函数和一个lst列表。调用reduce(fn, lst)时，fn会应用到第一对元素上，即fn(lst[0], lst[1])，
生成第一个结果r1。然后，fn会应用到r1和下一个元素上，即fn(r1, lst[2])，生成第二个结果r2。接着调用fn(r2, lst[3])，生成r3...直到最后一个元素，返回最后得到的结果rN。
* 注意：使用reduce()函数时，最好提供第三个参数，这样能够避免异常：TypeError:reduce() of empty sequence with no inital value，如果序列为空，initializer是返回的结果；否则，在归约中使用它作为第一个参数，
因此应该是恒等值。比如，对+、|和^来说，应该是0；而对*和&来说，应该是1

# 示例
import functools

functools.reduce(lambda a,b: a*b, range(1, 6))  # 计算5的阶乘
# 120
'''
