# 在Python中，数据的属性和处理数据的方法统称为属性（attribute）。其实，方法只是可调用的属性。除了这二者之外，我们还可以创建特性（property），在不改变类接口的前提下，使用存取方法（即读值方法和设值方法）修改数据属性
# 除了特性，Python还提供了丰富的API，用于控制属性的访问权限，以及实现动态属性。使用点号访问属性时（如obj.attr），Python解释器会调用特殊的方法（如__getattr__和__setattr__）计算属性。
# 用户自定义的类可以通过__getattr__方法实现“虚拟属性”，当访问不存在的属性时（如obj.no_such_attribute），即时计算属性的值

"""1、使用动态属性转换数据"""
# 下载osconfeed.json文件
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
























