# 类元编程是指在运行时创建或定制类的技艺，在python中，类是一等对象，因此任何时候都可以使用函数新建类，而无需使用class关键字。
# 类装饰器也是函数，不过能够审查、修改，甚至把被装饰的类替换成其它类
# 元类是类元编程最高级的工具：使用元类可以创建具有某种特质的全新类种，例如抽象基类

"""1、类工厂函数"""
''' 标准库中的类工厂函数——collections.namedtuple
把一个类名和几个属性名传给这个函数，它会创建一个tuple的子类，其中的元素通过名称获取，还为调试提供了友好的字符串表示形式__repr__

type通常被视作函数，因为我们像函数那样使用它，例如，调用type(my_object)获取对象所属的类————作用与my_object.__class__相同。然而，type是一个类。当成类使用时，传入三个参数可以新建一个类：

    MyClass = type('MyClass', (MySuperClass, MyMixin), {'x': 42, 'x2': lambda self: self.x * 2})

type的三个参数分别是name、bases和dict，最后一个参数是一个映射，指定新类的属性名和值，上述代码等同于下述代码：

    class MyClass(MySuperClass, MyMixin):
        x = 42
        
        def x2(self):
            return self.x * 2
'''
def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()  # 鸭子类型：尝试在逗号或空格处拆分field_names；如果失败，那么假定field_names本就是可迭代的对象，一个元素对应一个属性名
    except AttributeError:  # 不能调用replace和split方法，抛出异常
        pass  # 假定field_names本就是标识符组成的序列
    field_names = tuple(field_names)  # 使用属性名构建元组，这将成为新建类的__slots__属性；此外，这么做还设定了拆包和字符串表示形式中各字段的顺序

    def __init__(self, *args, **kwargs):  # 此函数将成为新建类的__init__方法，参数有位置参数和关键字参数
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):  # 实现__iter__函数，把类的实例变成可迭代的对象；按照__slots__设定的顺序产出字段值
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):  # 迭代__slots__和self，生成友好的字符串表现形式
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__=field_names, __init__=__init__, __iter__=__iter__, __repr__=__repr__)  # 组建类属性字典

    return type(cls_name, (object,), cls_attrs)  # 调用type构造方法，构建新类，然后将其返回


Dog = record_factory('Dog', 'name weight owner')  # 工厂函数：先写类名，后面跟着写在一个字符串里的多个属性名，使用空格或逗号分号
rex = Dog('Rex', 30, 'Bob')
print(rex)  # 返回字符串表示形式
# Dog(name='Rex', weight=30, owner='Bob')

name, weight, _ = rex  # 实例是可迭代的对象，因此赋值时可以便利的拆包
print(name, weight)
# Rex 30

print("{2}'s dog weights {1}kg".format(*rex))  # 传给format等函数也可以拆包
# Bob's dog weights 30kg
rex.weight = 32  # 记录实例是可变的对象
print(rex)
# Dog(name='Rex', weight=32, owner='Bob')
print(Dog.__mro__)  # 新建的类继承自object，与我们的工厂函数没有关系
# (<class '__main__.Dog'>, <class 'object'>)


"""2、定制描述符的类装饰器"""
# 类装饰器与函数装饰器非常类似，是参数为类对象的函数，返回原来的类或修改后的类
# 类装饰器还有一个重大缺点：只对直接依附的类有效，这意味着，被装饰的类的子类可能继承也可能不继承装饰器所作的改动，具体情况视改动的方式而定

import model_v6 as model

@model.entity
class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


print(LineItem.weight.storage_name, LineItem.description.storage_name)
# _Quantity#weight _NonBlank#description
raisins = LineItem('Golden raisins', 10, 6.95)
print(dir(raisins)[:3])
# ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
print(raisins.description)
# Golden raisins
print(getattr(raisins, '_NonBlank#description'))
# Golden raisins
