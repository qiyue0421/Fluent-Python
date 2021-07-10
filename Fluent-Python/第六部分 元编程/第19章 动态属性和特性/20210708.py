"""2、使用特性验证属性"""
''' LineItem类第一版：表示订单中商品的类
# 假设有个销售散装有机食物的电商应用，客户可以按重量订购坚果、干果或杂粮。在这个系统中，每个订单中都有一系列商品，而每个商品都可以使用下面定义的类表示：
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        
    def subtotal(self):
        return self.weight * self.price

>>> raisins = LineItem('Golden raisins', 10, 6.95)
>>> raisins.subtotal()
69.5
>>> raisins.weight = -20  #  无效输入
>>> raisins.subtotal()  # 无效输出
-139
针对这个问题，需要修改LineItem类的接口，使用读值方法和设值方法管理weight属性，此时符合Python风格的做法是：把数据属性换成特性
'''


""" LineItem类第2版：能验证值的特性
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 此处已经使用了特性的设值方法了，确保所创建实例的weight属性不能为负值
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property  # 装饰读值方法
    def weight(self):  # 实现特性的方法，其名称都与公开属性的名称一样
        return self.__weight  # 真正的值存储在私有属性self.__weight中

    @weight.setter  # 被装饰的读值方法有个.setter属性，这个属性也是装饰器；这个装饰器把读值方法和设值方法绑定在一起
    def weight(self, value):
        if value > 0:
            self.__weight = value  # 如果值大于0，设置私有属性__weight
        else:
            raise ValueError('value must be > 0')  # 抛出ValueError异常


>>> walnuts = LineItem('walnuts', 0, 10.00)
Traceback (most recent call last):
  ...
ValueError: value must be > 0
"""


"""3、特性全解析
虽然内置的property经常用作装饰器，但它其实是个类，构造方法的完整签名如下：

    property(fget=None, fset=None, fdel=None, doc=None)

所有参数都是可选的，如果没有把函数传给某个参数，那么得到的特性对象就不允许执行相应的操作

class LineItem:  # 不使用装饰器的版本
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):  # 普通的读值方法
        return self.weight * self.price

    def get_weight(self):  # 普通的设值方法
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight, set_weight)  # 构建property对象，然后赋值给公开的类属性
"""


""" 特性会覆盖实例属性
# 特性都是类属性，但是特性管理的其实是实例属性的存取，如果实例和所属的类有同名数据属性，那么实例属性会覆盖类属性

"""
class Class:  # Class类，有两个类属性：data数据属性和prop特性
    data = 'the class data attr'

    @property
    def prop(self):
        return 'the prop value'

''' 实例属性遮盖类的数据属性 '''
obj = Class()
print(vars(obj))  # 返回obj的__dict__属性，表明没有实例属性
# {}
print(obj.data)  # 读取obj.data，获取的其实是Class.data的值
# the class data attr

obj.data = 'bar'  # 为obj.data赋值，创建一个实例属性
print(vars(obj))  # 审查实例，查看实例属性
# {'data': 'bar'}
print(obj.data)  # 现在读取obj.data，获取的是实例属性的值，从obj实例中读取属性时，实例属性data会遮盖类属性data
# bar
print(Class.data)  # 类属性的值完好无损
# the class data attr

''' 实例属性不会遮盖类特性 '''
print(Class.prop)  # 直接从Class中读取prop特性，获取的是特性对象本身，不会运行特性的读值方法
# <property object at 0x00000239B70DC908>
print(obj.prop)  # 读取obj.prop会执行特性的读值方法
# the prop value

# obj.prop = 'foo'  # 尝试设置prop实例属性，结果失败
# Traceback (most recent call last):
#   ...
# AttributeError: can't set attribute

obj.__dict__['prop'] = 'foo'  # 直接把'prop'存入obj.__dict__
print(vars(obj))  # obj有两个实例属性：data和prop
# {'data': 'bar', 'prop': 'foo'}
print(obj.prop)  # 读取obj.prop时仍然会运行特性的读值方法，特性没有被实例属性遮盖
# the prop value
# noinspection PyPropertyAccess
Class.prop = 'baz'  # 直接覆盖Class.prop特性，销毁特性对象
print(obj.prop)  # 现在obj.prop获取的是实例属性，Class.prop不是特性了，因此不会再遮盖obj.prop
# foo

''' 新添加的类特性遮盖现有的实例属性 '''
print(obj.data)  # 实例属性
# bar
print(Class.data)  # 类属性
# the class data attr

Class.data = property(lambda self: 'the "data" prop value')  # 使用新特性覆盖类属性Class.data
print(obj.data)  # 现在，obj.data被Class.data特性遮盖了
# the "data" prop value
del Class.data  # 删除特性
print(obj.data)  # 现在恢复原样，obj.data获取的是实例属性data
# bar

''' 特性的文档
控制台中的help()函数或IDE等工具需要显示特性的文档时，会从特性的__doc__属性中提取信息。如果使用经典调用句法，为property对象设置文档字符串的方法是传入doc参数：

    weight = property(get_weight, set_weight, doc='weight in kilograms')

使用装饰器创建property对象时，读值方法（有@property装饰器的方法）的文档字符串作为一个整体，变成特性的文档
'''
class Foo:
    @property
    def bar(self):
        # noinspection PySingleQuotedDocstring
        '''The bar attribute'''
        return self.__dict__['bar']

    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value

print(help(Foo))
''' 
Help on class Foo in module __main__:

class Foo(builtins.object)
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  bar
 |      The bar attribute

None
'''

print(help(Foo.bar))
''' 输出结果
Help on property:

    The bar attribute

None
'''


