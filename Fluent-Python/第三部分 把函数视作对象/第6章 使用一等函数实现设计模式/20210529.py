"""1、案例分析：重构“策略”模式"""

'''经典的“策略”模式
“策略”模式定义：定义一系列算法，把它们一一封装起来，并且使它们可以相互替换。本模式使得算法可以独立于使用它的客户而变化

相关概念：
    * 上下文：把一些计算委托给实现不同算法的可互换组件，它提供服务
    * 策略：实现不同算法的组件共同的接口。
    * 具体策略：“策略”的具体子类。
'''

'''电商领域有个功能明显可以使用“策略”模式，即根据客户的属性或订单中的商品计算折扣。
假如一个网店制定了下述折扣规则：
    * 有1000或以上积分的顾客，每个订单享5%折扣
    * 同一订单中，单个商品的数量达到了20个或以上，享10%折扣
    * 订单中的不同商品达到10个或以上，享受7%折扣
'''

'''
# 实现Order类，支持插入式折扣策略
from abc import ABC, abstractmethod
from collections import namedtuple

# 顾客类
Customer = namedtuple('Customer', 'name fidelity')  # 具名元组包含名字和积分两个字段


# 订单商品类
class LineItem:
    def __init__(self, product, quantity, price):  # 商品名、数量、单价
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # 上下文
    def __init__(self, customer, cart, promotion=None):  # 客户、订单列表、策略折扣
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.__total = 0

    # 总价
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    # 打折后的价格
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # 策略：抽象基类
    @abstractmethod  # 装饰器，明确表明所用的模式
    def discount(self, order):
        """返回折扣金额（正值）"""


class FidelityPromo(Promotion):  # 第一个具体策略：为积分为1000或以上的顾客提供5%折扣
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # 第二个具体策略：单个商品为20个或以上时提供10%折扣
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):  # 第三个具体策略：订单中的不同商品达到10个或以上时提供7%折扣
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0


# 两个顾客：joe的积分是0，ann的积分是1100
joe = Customer('Johe Doe', 0)
ann = Customer('Ann Smith', 1100)

# 订单列表
cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]

print(Order(joe, cart, FidelityPromo()))  # 没有折扣
# <Order total: 42.00 due: 42.00>
print(Order(ann, cart, FidelityPromo()))  # 有第一种折扣
# <Order total: 42.00 due: 39.90>

banana_cart = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
print(Order(joe, banana_cart, BulkItemPromo()))  # 拥有第二种折扣
# <Order total: 30.00 due: 28.50>

long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order, LargeOrderPromo()))  # 拥有第三种折扣
# <Order total: 10.00 due: 9.30>

'''


"""使用函数实现“策略”模式
上面每个具体策略都是一个类，而且都只定义了一个方法，即discount。此外，策略实例没有状态（没有实例属性）
重构上述代码，把具体策略换成了简单的函数，而且去掉了Pormo抽象类
"""

# Order类和使用函数实现的折扣策略
from collections import namedtuple

# 顾客类
Customer = namedtuple('Customer', 'name fidelity')  # 具名元组包含名字和积分两个字段

# 订单商品类
class LineItem:
    def __init__(self, product, quantity, price):  # 商品名、数量、单价
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

class Order:  # 上下文
    def __init__(self, customer, cart, promotion=None):  # 客户、订单列表、策略折扣
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
        self.__total = 0

    # 总价
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    # 打折后的价格
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)  # 计算折扣只需调用 self.promotion() 函数，各个策略都是函数
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

# 第一个具体策略：为积分为1000或以上的顾客提供5%折扣
def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

# 第二个具体策略：单个商品为20个或以上时提供10%折扣
def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

# 第三个具体策略：订单中的不同商品达到10个或以上时提供7%折扣
def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


# 两个顾客：joe的积分是0，ann的积分是1100
joe = Customer('Johe Doe', 0)
ann = Customer('Ann Smith', 1100)

# 订单列表
cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]

# 将函数作为参数传入
print(Order(joe, cart, fidelity_promo))  # 没有折扣
# <Order total: 42.00 due: 42.00>
print(Order(ann, cart, fidelity_promo))  # 有第一种折扣
# <Order total: 42.00 due: 39.90>

banana_cart = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
print(Order(joe, banana_cart, bulk_item_promo))  # 拥有第二种折扣
# <Order total: 30.00 due: 28.50>

long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order, large_order_promo))  # 拥有第三种折扣
# <Order total: 10.00 due: 9.30>


"""选择最佳策略：简单的方式"""
promos = [fidelity_promo, bulk_item_promo, large_order_promo]  # 策略函数列表

def best_promo(order):
    # 选择可用的最佳折扣
    return max(promo(order) for promo in promos)  # 使用生成器表达式把order传给promos列表中的各个函数，返回计算出的最大折扣额度


print(Order(joe, long_order, best_promo))
# <Order total: 10.00 due: 9.30>
print(Order(joe, banana_cart, best_promo))
# <Order total: 30.00 due: 28.50>
print(Order(ann, cart, best_promo))
# <Order total: 42.00 due: 39.90>


"""缺陷：若想添加新的促销策略，要定义相应的函数，还要记得把它添加到promos列表中；否则，当新促销函数显式地作为参数传给Order时，它是可用的但是best_promo不会考虑它

找出模块中的全部策略:
    * 方法1：使用内置函数globals()
    * 方法2：在一个单独的模块中保存所有的策略函数，把best_promo排除在外

"""

'''内省模块的全局命名空间，构建promos列表

在Python中，模块也是一等对象，而且标准库提供了几个处理模块的函数:
globals() 
    函数返回一个字典，表示当前的全局符号表。这个符号表始终针对当前模块（对函数或方法来说，是指定于它们的模块，而不是调用它们的模块）


promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']

def best_promo(order):
    # 选择可用的最佳折扣
    return max(promo(order) for promo in promos)
'''

'''内省单独的promotions模块，构建promos列表

promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction())]  # promotions为模块，使用时需要导入
# inspect.getmembers 函数用于获取对象（即promotions模块）的属性，第二个参数是可选的判断条件（布尔函数）

def best_promo(order):
    # 选择可用的最佳折扣
    return max(promo(order) for promo in promos)

'''


"""2、“命令”模式"""
# “命令”模式的目的是解耦调用操作的对象（调用者）和提供实现的对象（接收者）。例如，调用者是图形应用程序中的菜单项，而接收者是被编辑的文档或应用程序自身
# 这个模式的做法是：在二者之间放一个Command对象，让它实现只有一个方法（execute）的接口，调用接收者中的方法执行所需的操作。这样，调用者无需了解接收者的接口，而且不同的接收者可以适应不同的Command子类。
# 调用者有一个具体的命令，通过调用execute方法执行。

class MacroCommand:
    # 一个执行一组命令的命令
    def __init__(self, commands):
        self.commands = list(commands)  # 使用commands参数构建一个列表，确保参数是可迭代对象

    def __call__(self, *args, **kwargs):
        for command in self.commands:  # 调用MacroCommand实例时，self.commands中的各个命令依序执行
            command()
