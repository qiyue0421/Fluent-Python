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
