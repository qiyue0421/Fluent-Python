"""2、覆盖型与非覆盖型描述符对比"""
# Python存储属性的方式特别不对等，通过实例读取属性时，通常返回的是实例中定义的属性；但是，如果实例中没有指定的属性，那么会获取类属性。而为实例中的属性赋值时，通常会在实例中创建属性，根本不影响类。

# 几个辅助类
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))

def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


class Overriding:  # 有__get__和__set__方法的典型覆盖性描述符
    """也称数据描述符或强制描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # 没有__get__方法的覆盖型描述符
    """没有__get__方法的覆盖型描述符"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # 没有__set__方法，所以这是非覆盖型描述符
    """也称非数据描述符或遮盖型描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:  # 托管类，使用各个描述符类的一个实例
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))


''' 覆盖型描述符
实现__set__方法的描述符属于覆盖型描述符，因为虽然描述符是类属性，但是实现__set__方法的话，会覆盖对实例属性的赋值操作。
'''
obj = Managed()  # 创建供测试使用的Managed对象
print(obj.over)  # 触发描述符的__get__方法，第二个参数的值是托管实例obj
# -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
print(Managed.over)  # 触发描述符的__get__方法，第二个参数（instance）的值是None
# -> Overriding.__get__(<Overriding object>, None, <class Managed>)

obj.over = 7  # 为obj.over赋值，触发描述符的__set__方法，最后一个参数的值是7
# -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
print(obj.over)  # 读取obj.over，仍会触发描述符的__get__方法
# -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

obj.__dict__['over'] = 8  # 跳过描述符，直接通过obj.__dict__属性设值
print(vars(obj))
# {'over': 8}
print(obj.over)  # 即使是名为over的实例属性，Managed.over描述符仍会覆盖读取obj.over这个操作
# -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)


''' 没有__get__方法的覆盖型描述符 
通常，覆盖型描述符既会实现__set__方法，也会实现__get__方法，不过也可以只实现__set__方法。此时，只有写操作由描述符处理。通过实例读取描述符会返回描述符对象本身，因为没有处理读取操作的__get__方法。
如果直接通过实例的__dict__属性创建同名实例属性，以后再设置那个属性时，仍会由__set__方法插手接管，但是读取那个属性的话，就会直接从实例中返回新赋予的值，而不会返回描述符对象，也就是说，实例属性会遮盖描述符，不过只有读取操作是如此
'''
print(obj.over_no_get)  # 这个覆盖型描述符没有__get__方法，因此，obj.over_no_get从类中获取描述符实例
# <__main__.OverridingNoGet object at 0x0000015BD6EA27B8>
print(Managed.over_no_get)  # 直接从托管类中读取描述符实例也是如此
# <__main__.OverridingNoGet object at 0x0000015BD6EA27B8>

obj.over_no_get = 7  # 赋值操作会触发描述符的__set__方法
# -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
print(obj.over_no_get)  # 因为__set__方法没有修改属性，所以在此读取的obj.over_no_get获取的仍是托管类中的描述符实例
# <__main__.OverridingNoGet object at 0x0000015BD6EA27B8>


obj.__dict__['over_no_get'] = 9  # 通过实例的__dict__属性设置名为over_no_get的实例属性
print(obj.over_no_get)  # 此时over_no_get实例属性会遮盖描述符，但是只有读操作是如此
# 9

obj.over_no_get = 7  # 为obj.over_no_get赋值，仍然经过描述符的__set__方法处理
# -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
print(obj.over_no_get)  # 但是读取时，只要有同名的实例属性，描述符就会被遮盖
# 9


''' 非覆盖型描述符 
没有实现__set__方法的描述符是非覆盖型描述符。如果设置了同名的实例属性，描述符会被覆盖，致使描述符无法处理那个实例的那个属性。方法是以非覆盖型描述符实现的。
'''
obj = Managed()
print(obj.non_over)  # 触发描述符的__get__方法，第二个参数的值是obj
# -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)

obj.non_over = 7  # Managed.non_over是非覆盖型描述符，因此没有干涉赋值操作的__set__方法
print(obj.non_over)  # obj有个名为non_over的实例属性，把Managed类的同名描述符属性遮盖掉
# 7
print(Managed.non_over)  # Managed.non_over描述符依然存在，会通过类截获这次访问
# -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)

del obj.non_over  # 如果删除了non_over实例属性
print(obj.non_over)  # 读取obj.non_over时，会触发类中描述符的__get__方法，第二个参数的值是托管实例
# -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)


''' 在类中覆盖描述符 
不管描述符是不是覆盖型，为类属性赋值都能覆盖描述符。这是一种猴子补丁技术
'''
obj = Managed()
Managed.over = 1  # 覆盖描述符属性
Managed.over_no_get = 2
Managed.non_over = 3
print(obj.over, obj.over_no_get, obj.non_over)
# 1 2 3


"""3、方法是描述符"""
# 在类中定义的函数属于绑定方法（bound method），因为用户定义的函数都有__get__方法，所以依附到类上时，就相当于描述符
obj = Managed()
print(obj.spam)  # obj.spam获取的是绑定方法对象
# <bound method Managed.spam of <__main__.Managed object at 0x000001DC6A7D34E0>>
print(Managed.spam)  # Managed.spam获取的是函数

obj.spam = 7  # 为obj.spam赋值，会遮盖类属性，导致无法通过obj实例访问spam方法
print(obj.spam)  # 函数没有实现__set__方法，因此是非覆盖型描述符

# 通过托管类访问时，函数的__get__方法会返回自身的引用；但是，通过实例访问时，函数的__get__方法返回的是绑定方法对象：一种可调用的对象，里面包装着函数，并把托管实例（例如obj）绑定给函数的第一个参数（即self）

''' 测试一个方法 
import collections

class Text(collections.UserString):
    def __repr__(self):
        return 'Text({!r})'.format(self.data)  # 返回一个类似Text构造方法调用的字符串，可用于创建相同的实例

    def reverse(self):
        return self[::-1]

>>> word = Text('forward')
>>> word
Text('forward')
>>> word.reverse()
Text('drawrof')  # 返回反向拼写的单词
>>> Text.reverse(Text('backward'))  # 在类上调用方法相当于调用函数
Text('drawkcab') 

>>> type(Text.reverse), type(word.reverse)  # 注意类型是不同的，一个是function，一个是method
(<class 'function'>, <class 'method'>)

>>> list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))  # Text.reverse相当于函数，甚至可以处理Text实例之外的其他对象
['diaper', (30, 20, 10), Text('desserts')]

>>> Text.reverse.__get__(word)  # 函数都是非覆盖型描述符，在函数上调用__get__方法时传入实例，得到的是绑定到那个实例上的方法
<bound method Text.reverse of Text('forward')>
>>> Text.reverse.__get__(None, Text)  # 调用函数的__get__方法时，如果instance参数的值是None，那么得到的是函数本身
<function Text.reverse at 0x0000016363CF1730>

>>> word.reverse  # 实际上调用Text.reverse.__get__(word)，返回对应的绑定方法
<bound method Text.reverse of Text('forward')>
>>> word.reverse.__self__  # 绑定方法对象有个__self__属性，其值是调用
forward
>>> word.reverse.__func__ is Text.reverse  # 绑定方法的__func__属性是依附在托管类上那个原始函数的引用
True
'''


"""4、描述符用法建议
①、使用特性以保持简单
内置的property类创建的其实是覆盖型描述符，__set__方法和__get__方法都实现了，即便不定义设值方法也是如此。





"""


