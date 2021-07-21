import abc

class AutoStorage:  # 自动管理储存属性的描述符类
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):  # 扩展AutoStorage类的抽象子类，覆盖__set__方法，调用必须由子类实现的validate方法
    def __set__(self, instance, value):
        value = self.validate(instance, value)  # 验证操作委托给validate方法
        super().__set__(instance, value)  # 返回的value值传给超类的__set__方法，存储值

    @abc.abstractmethod
    def validate(self, instance, value):  # 抽象方法
        """ return validated value or raise ValueError """


class Quantity(Validated):  # 继承Validated类
    """ a number greater than zero """
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """ a string at least one non-space character """
    def validate(self, instance, value):
        value = value.strip()  # 去掉首位空格
        if len(value) == 0:  # 检查是否空行
            raise ValueError('value connot be empty or blank')
        return value  # 返回去掉首位空格的value


def entity(cls):  # 类装饰器与函数装饰器非常类似，是参数为类对象的函数，返回原来的类或修改后的类
    for key, attr in cls.__dict__.items():  # 迭代存储类属性的字典
        if isinstance(attr, Validated):  # 如果属性是Validated描述符的实例
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)  # 使用描述符类的名称和托管属性的名称命名storage_name
    return cls  # 返回修改后的类
