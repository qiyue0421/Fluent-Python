"""1、运算符重载基础"""
''' Python对运算符重载的限制
* 不能重载内置类型的运算符
* 不能新建运算符，只能重载现有的
* 某些运算符不能重载————is、and、or和not（不过位运算符&、|和~可以）
'''


"""2、一元运算符"""
''' 三个一元运算符：
- (__neg__) 一元取负算术运算符。如果x是-2，那么-x == 2
+ (__pos__) 一元取正算术运算符。通常，x == +x。
~ (__invert__) 对整数按位取反，定义为 ~x == -(x+1)。如果x是2，那么 ~x == -3
'''


"""3、重载向量加法运算符+"""
''' 向量加法运算的几个场景
# 两个向量相加
>>> v1 = Vector([3, 4, 5])
>>> v2 = Vector([6, 7, 8])
>>> v1 + v2
Vector([9.0, 11.0, 13.0])
>>> v1 + v2 == Vector([3+6, 4+7, 5+8])
True

# 将两个长度不同的Vector实例加在一起，最好使用零填充较短的那个向量
>>> v1 = Vector([3, 4, 5, 6])
>>> v3 = Vector([1, 2])
>>> v1 + v3
Vector([4.0, 6.0, 5.0, 6.0])
'''

''' Python为中缀运算符特殊方法提供了特殊的分派机制，对表达式 a + b 来说，解释器会执行以下几步操作
①、如果a有__add__方法，而且返回值不是NotImplemented，调用a.__add__(b)，然后返回结果
②、如果a没有__add__方法，或者调用__add__方法返回NotImplemented，检查b有没有__radd__方法，如果有，而且没有返回NotImplemented，调用b.__radd__(a)，然后返回结果
③、如果b没有__radd__方法，或者调用__radd__方法返回NotImplemented，抛出TypeError，并在错误消息中指明操作数类型不支持
'''


"""4、重载标量乘法运算符*"""
''' 向量乘法运算的几个场景
# 元素级乘法————各个分量都会乘以x
>>> v1 = Vector([1, 2, 3])
>>> v1 * 10
Vector([10.0, 20.0, 30.0])
>>> 11 * v1
Vector([11.0, 22.0, 33.0])

# 点积运算符@————python3.5版本引入
@运算符由特殊方法__matmul__、__rmatmul__和__imatmul__提供支持
>>> va = Vector([1, 2, 3])
>>> vz = Vector([5, 6, 7])
>>> va @ vz == 38.0  # 1*5 + 2*6 + 3*7
True
>>> [10, 20, 30] @ vz
380.0
'''


"""5、众多比较运算符"""
''' Python解释器对比较运算符的处理：
①、正向和反向调用使用的是同一系列方法。例如，对==来说，正向和反向调用都是__eq__方法，只是把参数对调了；而正向的__gt__方法调用的是反向的__lt__方法，并把参数对调
②、对==和!=来说，如果反向调用失败，Python会比较对象的ID，而不抛出TypeError

众多比较运算符：正向方法返回NotImplemented的话，调用反向方法
分组        中缀运算符       正向方法调用        反向方法调用            后备机制
相等性       a == b         a.__eq__(b)       b.__eq__(a)       返回id(a) == id(b) 
            a != b         a.__ne__(b)       b.__ne__(a)       返回not(a == b)
排序        a > b          a.__gt__(b)       b.__lt__(a)       抛出TypeError
            a < b          a.__lt__(b)       b.__gt__(a)       抛出TypeError
            a >= b         a.__ge__(b)       b.__le__(a)       抛出TypeError
            a <= b         a.__le__(b)       b.__ge__(a)       抛出TypeError
'''


"""6、增量赋值运算符"""
# 增量赋值不会修改不可变目标，而是新建实例，然后重新绑定
''' 增量赋值运算的几个场景
# +=和*=
>>> v1 = Vector([1, 2, 3])
>>> v1_alias = v1  # 复制一份，供后面审查
>>> id(v1)
4302860128
>>> v1 += Vector([4, 5, 6])  # 增量加法运算
>>> v1
Vector([5.0, 7.0, 9.0])
>>> id(v1)  # 审查发现，创建了新的Vector实例
4302859904
>>> v1_alias  # 原来的Vector实例没被修改
Vector([1.0, 2.0, 3.0])

>>> v1 *= 11  # 增量乘法运算
>>> v1
Vector([55.0, 77.0, 99.0])
>>> id(v1)  # 同样创建了新的Vector实例
4302858336


'''


# 在Vector类上实现运算符重载
from array import array
import reprlib
import math
import functools
import operator
import numbers
import itertools

class Vector:
    """ Vector类 """
    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __neg__(self):  # 计算 -v
        return Vector(-x for x in self)  # 构建一个新Vector实例，把self的每个分量都取反

    def __pos__(self):  # 计算 +v
        return Vector(self)  # 构建一个新Vector实例，传入self的各个分量

    def __add__(self, other):  # 运算符+
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)  # pairs是个生成器，它会生成（a, b）形式的元组，其中a来自self，b来自other。如果self和other的长度不同，使用fillvalue填充较短的那个可迭代对象
            return Vector(a + b for a, b in pairs)
        except TypeError:  # 捕获TypeError异常
            return NotImplemented  # 如果由于类型不兼容而导致运算符特殊方法无法返回有效的结果，那么应该返回NotImplemented，此时另一个操作数所属的类型还有机会执行运算，即Python会尝试调用反向方法

    def __radd__(self, other):  # __add__的反向版本
        return self + other  # 直接委托给 __add__ 方法

    def __mul__(self, other):  # 标量乘法
        if isinstance(other, numbers.Real):  # 检查类型
            return Vector(n * other for n in self)
        else:
            return NotImplemented  # 返回NotImplemented，尝试在other操作数上调用__rmul__方法

    def __rmul__(self, other):  # __mul__的反向版本
        return self * other  # 委托给__mul__

    def __matmul__(self, other):  # 点积运算符@
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other

    def __eq__(self, other):  # 运算符==
        if isinstance(other, Vector):  # 如果other操作数是Vector实例，正常比较
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented  # 否则返回NotImplemented

    def __ne__(self, other):  # 运算符!=
        eq_result = self == other
        if eq_result is NotImplemented:
            return NotImplemented
        else:
            return not eq_result

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            # noinspection PyTypeChecker
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attributes {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self), self.angles()])
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)































