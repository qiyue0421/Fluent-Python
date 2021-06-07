"""1、Vector类：用户定义的序列类型"""
# 使用组合模式实现Vector类，而不使用继承。向量的分量存储在浮点数组中，而且还将实现不可变扁平序列所需的方法。


"""2、Vector类第1版：与Vector2d类兼容"""
from array import array
import reprlib
import math


class Vector:
    """ Vector类 """
    typecode = 'd'  # 类属性，在类实例和字节序列之间转换时使用

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
        return tuple(self) == tuple(other)  # 构建元组进行比较

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))  # 首先计算各分量的平方之和，然后再使用sqrt方法开平方

    def __bool__(self):
        return bool(abs(self))  # 使用abs()计算模，然后把结果转换成布尔值，因此0.0是False，非零值是True

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]  # 支持迭代，只需实现__getitem__方法

    # 从字节序列转换成Vector2d实例
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

'''


















