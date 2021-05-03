# 实现一个简单的二维向量类
from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):  # 将实例对象用字符串形式表达出来
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self):  # 取模运算
        return hypot(self.x, self.y)

    def __bool__(self):  # 布尔值
        return bool(abs(self))
        # return bool(self.x or self.y)  # 更高效的实现

    def __add__(self, other):  # 加运算
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)  # 返回值是一个新的向量对象

    def __mul__(self, other):  # 乘运算
        return Vector(self.x * other, self.y * other)  # 返回值是一个新的向量对象