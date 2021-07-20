# 类元编程是指在运行时创建或定制类的技艺，在python中，类是一等对象，因此任何时候都可以使用函数新建类，而无需使用class关键字。
# 类装饰器也是函数，不过能够审查、修改，甚至把被装饰的类替换成其它类
# 元类是类元编程最高级的工具：使用元类可以创建具有某种特质的全新类种，例如抽象基类

"""1、类工厂函数"""
''' 标准库中的类工厂函数——collections.namedtuple
把一个类名和几个属性名传给这个函数，它会创建一个tuple的子类，其中的元素通过名称获取，还为调试提供了友好的字符串表示形式__repr__
'''
def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:  # 不能调用replace和split方法，抛出异常
        pass  # 假定field_names本就是标识符组成的序列
    field_names = tuple(field_names)