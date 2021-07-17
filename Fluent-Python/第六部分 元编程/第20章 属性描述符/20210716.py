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







