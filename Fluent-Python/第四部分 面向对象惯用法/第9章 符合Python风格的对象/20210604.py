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
    # __slots__ = ('__x', '__y')  # 使用__slots__类属性节省空间

    typecode = 'd'  # 类属性，在类实例和字节序列之间转换时使用

    def __init__(self, x, y):
        self.__x = float(x)  # 转换成浮点数
        self.__y = float(y)  # 使用两个前导下划线，把属性标记为私有的

    @property  # 装饰器把读值方法标记为特性
    def x(self):  # 读值方法与公开属性同名，都是x
        return self.__x  # 直接返回self.__x

    @property
    def y(self):
        return self.__y

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

    def angle(self):
        return math.atan2(self.x, self.y)  # 计算角度

    def __format__(self, format_spec=''):
        if format_spec.endswith('p'):  # 如果格式以'p'结尾，使用极坐标
            format_spec = format_spec[:-1]  # 删除'p'后缀
            coords = (abs(self), self.angle())  # 构建一个元组，表示极坐标
            outer_fmt = '<{}, {}>'  # 格式为尖括号
        else:  # 构建直角坐标
            coords = self
            outer_fmt = '({}, {})'  # 格式为圆括号
        components = (format(c, format_spec) for c in coords)  # 使用各个分量生成可迭代的对象，构成格式化字符串
        return outer_fmt.format(*components)  # 把格式化字符串代入外层格式

    def __hash__(self):  # 使向量变成可散列的
        return hash(self.x) ^ hash(self.y)

    # 从字节序列转换成Vector2d实例
    @classmethod
    def frombytes(cls, octets):  # 不用传入self参数，相反需要通过cls传入类本身
        typecode = chr(octets[0])  # 从第一个字节中读取typecode
        memv = memoryview(octets[1:]).cast(typecode)  # 使用传入的octets字节序列创建一个memoryview
        return cls(*memv)  # 拆包转换后的memoryview，得到构造方法所需的一对参数


# 测试
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
print(format(Vector2d(1, 1), 'p'))  # format函数会调用__format__方法
# <1.4142135623730951, 0.7853981633974483>
print(format(Vector2d(1, 1), '0.5fp'))
# <1.41421, 0.78540>


"""4、classmethod与staticmethod"""
# 定义操作类，而不是操作实例的方法。classmethod改变了调用方法的方式，因此类方法的第一个参数是类本身，而不是实例
# classmethod最常见的用途是定义备选构造方法
# staticmethod装饰器也会改变方法的调用方式，但是第一个参数不是特殊的值。其实，静态方法就是普通的函数，只是碰巧在类的定义体中，而不是在模块层定义·

'''比较classmethod和staticmethod的行为
class Demo:
    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def statmeth(*args):
        return args

print(Demo.klassmeth())
# (<class '__main__.Demo'>,)
print(Demo.klassmeth('spam'))
# (<class '__main__.Demo'>, 'spam')  # 不管怎么调用Demo.klassmeth，它的第一个参数始终是Demo类

print(Demo.statmeth())
# ()
print(Demo.statmeth('spam'))  # Demo.statmeth的行为与普通的函数相似
# ('spam',)
'''


"""5、格式化显示"""
# 内置的format()函数和str.format()方法把各个类型的格式化方法委托给相应的__format__(format_spec)方法
# format_spec是格式化说明符，可以是format(my_obj, format_spec)的第二个参数，或者是str.format()方法的格式字符串，{}里代换字段中冒号后面的部分

print(format(1/2.43, '0.4f'))  # 格式说明符是'0.4f'
# 0.4115
print('1 BRL = {rate:0.2f} USD'.format(rate=1/2.43))  # 格式说明符是0.2f，冒号左边的是代换字段句法中的字段名，冒号右边是格式说明符
# 1 BRL = 0.41 USD

'''格式规范微语言为一些内置类型提供了专用的表示代码
b——二进制int类型
x——十六进制int类型
f——小数形式的float类型
%——百分形式
'''


"""7、Python的私有属性和“受保护的”属性"""
'''例子：
有人编写了一个名为Dog的类，这个类的内部用到了mood实例属性，但是没有将其开放。现在，创建了Dog类的子类：Beagle。在你不知情的情况下又创建了名为mood的实例属性，那么在继承的方法中就会把Dog类
的mood属性覆盖掉，这是个难以调试的问题。

为了避免上述这种情况，如果以__mood的形式（两个前导下划线，尾部没有或最多有一个下划线）命名实例属性，Python会把属性名存入实例的__dict__属性中，而且会在前面加上一个下划线和类名。因此，
对Dog类来说，__mood会变成_Dog__mood；对Beagle类来说，会变成_Beagle_mood。这个语言特性叫做名称改写（name mangling）

名称改写是一种安全措施，不能保证万无一失：它的目的是避免意外访问，不能防止故意做错事。
'''

v1 = Vector2d(3, 4)
print(v1.__dict__)
# {'_Vector2d__x': 3.0, '_Vector2d__y': 4.0}
print(v1._Vector2d__x)  # 只要知道改写私有属性名的机制，任何人都能直接读取私有属性，只要编写 v1._Vector2d__x = 7 这样的代码，就能轻松修改私有分量
# 3.0


"""8、使用__slots__类属性节省空间"""
# 默认情况下，Python在各个实例中名为__dict__的字典里存储实例属性，为了使用底层的散列表提升访问速度，字典会消耗大量内存
# 可以通过__slots__类属性，能节省大量内存，方法是让解释器在元组中存储实例属性，而不用字典

'''定义__slots__：
创建一个类属性，使用__slots__这个名字，并把它的值设为一个字符串构成的可迭代对象，其中各个元素表示各个实例属性

clss Vector2d:
    __slots__ = ('__x', '__y')
    
    typecode = 'd'

'''

'''__slots__的问题：
1、每个子类都要定义__slots__属性，因为解释器会忽略继承的__slots__属性
2、实例只能拥有__slots__中列出的属性，除非把'__dict__'加入__slots__中（这样做就失去了节省内存的功效）
3、如果不把'__weakref__'加入__slots__，实例就不能作为弱引用的目标
'''


"""9、覆盖类属性"""
'''Python独特的特性：类属性可用于为实例属性提供默认值
上述向量类中有一个typecode类属性，__bytes__方法两次用到了它，而且都故意使用 self.typecode 读取它的值。因为实例本身没有typecode属性，所以，self.typecode 默认获取
的是 Vector2d.typecode类属性的值。但是，如果为不存在的实例属性赋值，会新建实例属性。假如为typecode实例属性赋值，那么同名类属性不受影响。然而，自此之后，实例读取
的 self.typecode 是实例属性typecode，也就是把同名类属性遮盖了。借助这一特性，可以为各个实例的typecode属性定制不同的值
'''
v1 = Vector2d(1.1, 2.2)
dumpd = bytes(v1)
print(dumpd, len(dumpd))
# b'd\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@' 17
v1.typecode = 'f'  # 将实例的typecode属性设为'f'
dumpf = bytes(v1)
print(dumpf, len(dumpf))
# b'f\xcd\xcc\x8c?\xcd\xcc\x0c@' 9
print(Vector2d.typecode)  # Vector2d.typecode属性的值不变，只有v1实例的typecode属性使用了'f'
# d

'''修改类属性的值'''
# 如果想修改类属性的值，必须直接在类上修改，不能通过实例修改
# Vector2d.typecode = 'f'

# 另外一种更好的方法是：创建一个子类，类属性是公开的，因此会被子类继承
class ShortVector2d(Vector2d):
    typecode = 'f'
