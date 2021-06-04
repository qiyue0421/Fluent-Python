"""1、对象表示形式"""
'''
# 获取对象的字符串表示形式，两种方式：
repr()
    以便于开发者理解的方式返回对象的字符串表示形式
    
str()
    以便于用户理解的方式返回对象的字符串表示形式

# 特殊方法：
__repr__
    为repr()提供支持

__str__
    为str()提供支持

__bytes__
    bytes()函数调用它获取对象的字节序列表示形式

__format__
    被内置format()函数和str.format()方法调用，使用特殊的格式代码显示对象的字符串表示形式
'''


"""2、再谈向量类"""
from array import array
import math

class Vector2d:
    typecode = 'd'  # 类属性，在类实例和字节序列之间转换时使用

    def __init__(self, x, y):
        self.x = float(x)  # 转换成浮点数
        self.y = float(y)

    def __iter__(self):  # 将实例变成可迭代对象，这样才能拆包，比如 x, y = my_vector，这里使用生成器表达式一个接一个产出分量
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)  # 使用{!r}获取各分量的表现形式，然后插值，构成一个字符串，能用 *self 是因为实例是可迭代对象

    def __str__(self):
        return str(tuple(self))  # 得到一个元组，显示为一个有序对

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))  # 把typecode转换成字节序列，然后迭代实例，得到一个数组，再把数组转换成字节序列

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # 构建元组进行比较

    def __abs__(self):
        return math.hypot(self.x, self.y)  # 计算模

    def __bool__(self):
        return bool(abs(self))  # 使用abs()计算模，然后把结果转换成布尔值，因此0.0是False，非零值是True


v1 = Vector2d(3, 4)
print(v1.x, v1.y)  # 直接通过属性访问
x, y = v1  # 可以拆包

'''
>>> v1              # __repr__()方法
Vector2d(3.0, 4.0)
'''

print(v1)           # print()函数会调用str函数，输出的是一个有序对
# (3.0, 4.0)
v1_clone = eval(repr(v1))  # 使用eval函数，表明repr函数调用Vector2d实例得到的是对构造方法的准确表达
print(v1 == v1_clone)  # 支持 == 比较
octets = bytes(v1)  # bytes函数会调用__bytes__方法，生成实例的二进制表示形式
print(octets)
# b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
print(abs(v1))  # abs函数会调用__abs__方法
print(bool(v1))  # bool函数会调用__bool__方法


"""3、备选构造方法"""
''' 从字节序列转换成Vector2d实例

@classmethod
def frombytes(cls, octets):  # 不用传入self参数，相反需要通过cls传入类本身
    typecode = chr(octets[0])  # 从第一个字节中读取typecode
    memv = memoryview(octets[1:]).cast(typecode)  # 使用传入的octets字节序列创建一个memoryview
    return cls(*memv)  # 拆包转换后的memoryview，得到构造方法所需的一对参数
    
'''


























