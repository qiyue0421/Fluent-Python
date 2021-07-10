"""4、定义一个特性工厂函数"""
# quantity特性工厂函数
def quantity(storage_name):  # storage_name参数确定各个特性的数据存储在哪儿；对weight特性来说，存储的名称是'weight'
    def qty_getter(instance):  # instance指代要把属性存储其中的LineItem实例
        return instance.__dict__[storage_name]  # 引用了storage_name，把它保存在这个函数的闭包里；值直接从instance.__dict__中获取，为的是跳过特性，防止无限递归

    def qty_setter(instance, value):  # 定义qty_setter函数，第一个参数也是instance
        if value > 0:
            instance.__dict__[storage_name] = value  # 值直接存到instance.__dict__中，这也是为了跳过特性
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)  # 构建一个自定义的特性对象，然后将其返回

class LineItem:
    weight = quantity('weight')  # 使用工厂函数把第一个自定义的特性weight定义为类属性
    price = quantity('price')  # 构建另一个自定义的特性price

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 激活特性，确保不能把weight设为负数或零
        self.price = price

    def subtotal(self):
        return self.weight * self.price  # 使用特性获取实例中存储的值

nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
print(nutmeg.weight, nutmeg.price)  # 通过特性读取weight和price，这会遮盖同名实例属性
# 8 13.95
print(sorted(vars(nutmeg).items()))  # 查看存储值的实例属性
# [('description', 'Moluccan nutmeg'), ('price', 13.95), ('weight', 8)]


"""5、处理属性删除操作
对象的属性可以使用del语句删除：

    del my_object.an_attribute

定义特性时，可以使用@my_property.deleter装饰器包装一个方法，负责删除特性管理的属性

在不使用装饰器的经典调用句法中，fdel参数用于设置删值函数：

    member = property(member_getter, fdel=member+deleter)

"""

class Blackknight:
    def __init__(self):
        self.members = ['an arm', 'another arm', 'a leg', 'another leg']
        self.phrases = ["'Tis but a scratch.", "It's just a flesh wound.", "I'm invincible!", "All right, we'll call it a draw."]

    @property
    def member(self):
        print('next member is:')
        return self.members[0]

    @member.deleter
    def member(self):
        text = 'BLACK KNIGHT (loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))

knight = Blackknight()
print(knight.member)
# next member is:
# an arm
del knight.member  # 删除member特性管理的属性
# BLACK KNIGHT (loses an arm)
# -- 'Tis but a scratch.
del knight.member
# BLACK KNIGHT (loses another arm)
# -- It's just a flesh wound.
del knight.member
# BLACK KNIGHT (loses a leg)
# -- I'm invincible!
del knight.member
# BLACK KNIGHT (loses another leg)
# -- All right, we'll call it a draw.






