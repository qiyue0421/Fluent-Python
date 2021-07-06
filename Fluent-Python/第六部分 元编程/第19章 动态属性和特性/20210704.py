# 在Python中，数据的属性和处理数据的方法统称为属性（attribute）。其实，方法只是可调用的属性。除了这二者之外，我们还可以创建特性（property），在不改变类接口的前提下，使用存取方法（即读值方法和设值方法）修改数据属性
# 除了特性，Python还提供了丰富的API，用于控制属性的访问权限，以及实现动态属性。使用点号访问属性时（如obj.attr），Python解释器会调用特殊的方法（如__getattr__和__setattr__）计算属性。
# 用户自定义的类可以通过__getattr__方法实现“虚拟属性”，当访问不存在的属性时（如obj.no_such_attribute），即时计算属性的值

"""1、使用动态属性转换数据"""
# 下载osconfeed.json文件
import keyword
from urllib.request import urlopen
import warnings
import os
import json

URL = 'https://cdn.jsdelivr.net/gh/fluentpython/example-code@master/19-dyn-attr-prop/oscon/data/osconfeed.json'
JSON = 'data/osconfeed.josn'

def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)  # 如果需要下载，就发出警告
        with urlopen(URL) as remote, open(JSON, 'wb') as local:  # with语句中使用两个上下文管理器，分别用于读取和保存远程文件
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)  # json.load函数解析JSON文件，返回Python原生对象。在这个数据源中有这几种数据类型：dict、list、str和int


feed = load()  # 一个字典，里面嵌套着字典和列表，存储着字符串和整数
print(sorted(feed['Schedule'].keys()))  # 列出"Schedule"键中的4个记录集合
# ['conferences', 'events', 'speakers', 'venues']
for key, value in sorted(feed['Schedule'].items()):  # 显示各个集合中的记录数量
    print('{:3} {}'.format(len(value), key))

print(feed['Schedule']['speakers'][-1]['name'])
print(feed['Schedule']['speakers'][-1]['serial'])


''' 使用动态属性访问JSON类数据'''
# feed['Schedule']['speakers'][-1]['name']) 语法过于冗长，可以使用 feed.Schedule.events[40].name 获取值
from collections import abc
import keyword

class FrozenJSON:
    # 一个只读接口，使用属性表示法访问JSON类对象
    def __init__(self, mapping):
        self.__data = {}  # 使用mapping参数构建一个字典，这么做有两个目录：一是确保传入的是字典（或者是能转换成字典的对象），二是安全起见，创建一个副本
        for key, value in mapping.items():  # 检查是否有关键字
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, item):  # 仅当没有指定名称（item）的属性时才调用此方法（即在实例、类或超类中找不到指定的属性）
        if hasattr(self.__data, item):  # 如果item是实例属性self.__data的属性时，返回这个属性，类似于keys方法
            return getattr(self.__data, item)
        else:  # 否则，从self.__data中获取item键对应的元素，返回调用FrozenJSON.build()方法得到的结果
            return FrozenJSON.build(self.__data[item])

    @classmethod
    def build(cls, obj):  # 将每一层嵌套转换成一个FrozenJSON实例
        if isinstance(obj, abc.Mapping):  # 如果obj是映射，那就构建一个FrozenJSON对象
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):  # 如果是MutableSequence对象，那必然是列表
            return [cls.build(item) for item in obj]  # 把obj中的每个元素递归地传给build方法，构建一个列表
        else:  # 既不是字典也不是列表，直接返回元素
            return obj


raw_feed = load()
feed = FrozenJSON(raw_feed)  # 传入嵌套的字典和列表组成的raw_feed，创建一个FrozenJSON实例
print(len(feed.Schedule.speakers))  # FrozenJSON实例可以使用属性表示法遍历嵌套的字典
# 357
print(sorted(feed.Schedule.keys()))  # 使用底层字典的方法，例如keys()
# ['conferences', 'events', 'speakers', 'venues']
for key, value in sorted(feed.Schedule.items()):
    print('{:3} {}'.format(len(value), key))


''' 处理无效属性名
FrozenJSON类有个缺陷：没有对名称为Python关键字的属性做特殊处理。比如说像下面这样构建一个对象：
>>> grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
>>> grad.class
    print(grad.class)
                   ^
SyntaxError: invalid syntax

此时无法读取grad.class的值，因为在python中class是保留字，也可以换一种方法：
>>> getattr(grad, 'class')

但是，FrozenJSON类的目的是为了便于访问数据，因此更好的方法是检查传给FrozenJSON.__init__方法的映射中是否有键的名称为关键字，如果是关键字，就在键名后面加上_，然后通过下面这种方式获取：
>>> grad.class_
'''


''' 使用__new__方法以灵活的方式创建对象
用于构建实例的是特殊方法__new__：这是个类方法（使用特殊方式处理，因此不必使用@classmethod装饰器），必须返回一个实例。返回的实例会作为第一个参数（即self）传给__init__方法。因为调用__init__方法时要传入实例，
                             而且禁止返回任何值，所以__init__方法其实是“初始化方法”。真正的构造方法是__new__。几乎不需要自己编写__new__方法，因为从object类继承的实现已经足够了

from collections import abc
import keyword

class FrozenJSON:  # FrozenJSON类的另一个版本，把之前在类方法build中的逻辑移到了__new__方法中
    # 一个只读接口，使用属性表示法访问JSON类对象
    def __new__(cls, arg):  # 类方法，第一个参数是类本身，余下的参数与__init__方法一样，只不过没有self
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)  # 默认的行为是委托给超类的__new__方法，这里调用的是object基类的__new__方法，把唯一的参数设为FrozenJSON
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}  # 使用mapping参数构建一个字典，这么做有两个目录：一是确保传入的是字典（或者是能转换成字典的对象），二是安全起见，创建一个副本
        for key, value in mapping.items():  # 检查是否有关键字
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, item):  # 仅当没有指定名称（item）的属性时才调用此方法（即在实例、类或超类中找不到指定的属性）
        if hasattr(self.__data, item):  # 如果item是实例属性self.__data的属性时，返回这个属性，类似于keys方法
            return getattr(self.__data, item)
        else:  # 否则，从self.__data中获取item键对应的元素，返回结果
            return FrozenJSON(self.__data[item])  # 现在只需要调用FrozenJSON构造方法
'''
