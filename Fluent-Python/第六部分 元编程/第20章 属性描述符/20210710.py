# 描述符是对多个属性运用相同存取逻辑的一种方式。例如，Django ORM和SQL Alchemy等ORM中的字段类型是描述符，把数据库记录中字段里的数据与Python对象的属性对应起来。
# 描述符是实现了特定协议的类，这个协议包括__get__、__set__和__delete__方法。property类实现了完整的描述符协议。通常，可以只实现部分协议（__get__和__set__）。
# 描述符是python的独有特征，不仅在应用层中使用，在语言的基础设施中也有用到。除了特性之外，使用描述符的Python功能还有方法以及classmethod和staticmethod装饰器

"""1、描述符示例：验证属性"""
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

















