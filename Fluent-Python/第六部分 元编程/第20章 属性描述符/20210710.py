# 描述符是对多个属性运用相同存取逻辑的一种方式。例如，Django ORM和SQL Alchemy等ORM中的字段类型是描述符，把数据库记录中字段里的数据与Python对象的属性对应起来。
# 描述符是实现了特定协议的类，这个协议包括__get__、__set__和__delete__方法。property类实现了完整的描述符协议。通常，可以只实现部分协议（__get__和__set__）。
# 描述符是python的独有特征，不仅在应用层中使用，在语言的基础设施中也有用到。除了特性之外，使用描述符的Python功能还有方法以及classmethod和staticmethod装饰器

"""1、描述符示例：验证属性"""
import sre_parse

''' LineItem类第3版：一个简单的描述符
实现了__get__、__set__或__delete__方法的类是描述符。描述符的作用：创建一个实例，作为另一个类的类属性

定义：
    描述符类：实现描述符协议的类。本例中是Quantity类
    托管类：把描述符实例声明为类属性的类。本例中是LineItem类
    描述符实例：描述符类的各个实例，声明为托管类的类属性。
    托管实例：托管类的实例。本例中是LineItem实例
    储存属性：托管实例中存储自身托管属性的属性。LineItem实例的weight和price属性是存储属性。这种属性与描述符实例不同，描述符实例都是类属性
    托管属性：托管类中由描述符实例处理的公开属性，值存储在储存属性中。也就是说，描述符实例和储存属性为托管属性建立了基础
'''
class Quantity:  # 描述符基于协议实现，无需创建子类
    def __init__(self, storage_name):
        self.storage_name = storage_name  # 托管实例中存储值的属性的名称

    def __set__(self, instance, value):  # 尝试为托管属性赋值时，会调用__set__方法。这里，self是描述符实例（即LineItem.weight或LineItem.price），instance是托管实例（LineItem实例），value是要设定的值
        if value > 0:
            instance.__dict__[self.storage_name] = value  # 必须直接处理托管实例的__dict__属性；如果使用内置的setattr函数，会再次触发__set__方法，导致无限递归
        else:
            raise ValueError('value must be > 0')

class LineItem:
    weight = Quantity('weight')  # 第一个描述符实例绑定给weight属性
    price = Quantity('price')  # 第二个描述符实例绑定给price属性

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


''' LineItem类第4版：自动获取储存属性的名称 '''
class Quantity:
    __counter = 0  # Quantity类的类属性，统计Quantity实例的数量

    def __init__(self):
        cls = self.__class__  # Quantity类的引用
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)  # 每个描述符实例的storage_name属性都是独一无二的，因为其值由描述符类的名称和__counter属性的当前值构成，例如_Quantity#0
        cls.__counter += 1  # 递增__counter属性的值，保证每个描述符实例都不同

    def __get__(self, instance, owner):  # 实现__get__方法，因为托管属性的名称与storage_name不同，owner参数是托管类的引用（LineItem）,通过描述符从托管类中获取属性时用得到
        if instance is None:
            return self  # 如果不是通过实例调用，返回描述符自身
        else:  # 否则返回托管属性的值
            return getattr(instance, self.storage_name)  # 使用内置的getattr函数从instance中获取储存属性的值

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)  # 使用内置函数setattr把值存储在instance中
        else:
            raise ValueError('value must be > 0')

class LineItem:
    weight = Quantity()  # 不用把托管属性的名称传给Quantity构造方法
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

# 测试
coconuts = LineItem('Brazilian cocount', 20, 17.95)
print(coconuts.weight, coconuts.price)
# 20 17.95
print(getattr(coconuts, '_Quantity#0'), getattr(coconuts, '_Quantity#1'))
# 20 17.95


''' LineItem类第5版：一种新型描述符 '''
import abc

class AutoStorage:  # 自动管理储存属性的描述符类
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)

class Validated(abc.ABC, AutoStorage):  # 扩展AutoStorage类的抽象子类，覆盖__set__方法，调用必须由子类实现的validate方法
    def __set__(self, instance, value):
        value = self.validate(instance, value)  # 验证操作委托给validate方法
        super().__set__(instance, value)  # 返回的value值传给超类的__set__方法，存储值

    @abc.abstractmethod
    def validate(self, instance, value):  # 抽象方法
        """ return validated value or raise ValueError """

class Quantity(Validated):  # 继承Validated类
    """ a number greater than zero """
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value

class NonBlank(Validated):
    """ a string at least one non-space character """
    def validate(self, instance, value):
        value = value.strip()  # 去掉首位空格
        if len(value) == 0:  # 检查是否空行
            raise ValueError('value connot be empty or blank')
        return value  # 返回去掉首位空格的value
