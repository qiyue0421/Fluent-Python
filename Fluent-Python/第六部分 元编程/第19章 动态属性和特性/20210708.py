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
"""
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


''' 特性会覆盖实例属性
# 特性都是类属性，但是特性管理的其实是实例属性的存取，如果实例和所属的类有同名数据属性，那么实例属性会覆盖类属性

'''