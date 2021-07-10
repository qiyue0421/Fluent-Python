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


"""6、处理属性的重要属性和函数"""
''' 影响属性处理方式的特殊属性 
__class__
    对象所属类的引用（即obj.__class__与type(obj)的作用相同）。Python的某些特殊方法，例如__getattr__，只在对象的类中寻找，而不在实例中寻找

__dict__
    一个映射，存储对象或类的可写属性。有__dict__属性的对象，任何时候都能随意设置新属性。如果类有__slots__属性，它的实例可能没有__dict__属性
    
__slots__
    类可以定义这个属性，限制实例能有哪些属性。__slots__属性的值是一个字符串组成的元组，指明允许有的属性。如果__slots__中没有__dict__，那么该类的实例没有__dict__属性，实例只允许有指定名称的属性
'''

''' 处理属性的内置函数
dir([object])
    列出对象的大多数属性。dir函数的目的是交互式使用，因此没有提供完整的属性列表，只列出一组“重要的”属性名。dir函数能审查有或者没有__dict__属性的对象。dir函数不会列出__dict__属性本身，但会列出其中的键。
    dir函数也不会列出类的几个特殊属性，例如__mro__、__bases__和__name__。如果没有指定可选的object参数，dir函数会列出当前作用域中的名称。
    
getattr(object, name[, default])
    从object对象中获取name字符串对应的属性。获取的属性可能来自对象所属的类或超类。如果没有指定的属性，getattr函数抛出AttributeError异常，或者返回default参数的值（如果设定了这个参数的话）

hasattr(object, name)
    如果object对象中存在指定的属性，或者能以某种方式（例如继承）通过object对象获取指定的属性，返回True。
    
setattr(object, name, value)
    把object对象指定属性的值设为value，前提是object对象能接受那个值，这个函数可能会创建一个新属性，或者覆盖现有的属性。
    
vars([object])
    返回object对象的__dict__属性；如果实例所属的类定义了__slots__属性，实例没有__dict__属性，那么vars函数不能处理那个实例（相反，dir函数能够处理这种实例）。
    如果没有指定参数，那么vars()函数的作用与locals()函数一样：返回表示本地作用域的字典 
'''

