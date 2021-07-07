''' 使用shelve模块调整OSCON数据源的结构
shelve模块提供了pickle存储方式。shelve.open高阶函数返回一个shelve.Shelf实例，这是简单的键值对象数据库，背后由dbm模块支持，具有下述特点：
    * shelve.Shelf是abc.MutableMapping的子类，因此提供了处理映射类型的重要方法
    * 此外，shelve.Shelf类还提供了几个管理I/O的方法，如sync和close；它也是一个上下文管理器
    * 只要把新值赋予键，就会保存键和值
    * 键必须是字符串
    * 值必须是pickle模块能够处理的对象
'''
import json
import os
import shelve
from urllib.request import urlopen

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


import warnings
import shelve

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # 更新实例的__dict__属性，把值设为一个映射，能快速地在实例中创建一堆属性


def load_db(db):
    raw_data = load()  # 如果本地没有副本，从网上下载JSON数据源
    warnings.warn('loading' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():  # 迭代集合
        record_type = collection[:-1]  # 去掉尾部的's'
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])  # 使用record_type和'serial'字段构成key
            record['serial'] = key  # 把'serial'字段的值设为完整的键
            db[key] = Record(**record)  # 构建Record实例，存储在数据库中的key键名下


db = shelve.open(DB_NAME)  # 打开现有的数据库文件，或者新建一个
if CONFERENCE not in db:  # 检查已知的键是否存在
    load_db(db)  # 数据库是空的，就调用load_db加载数据

speaker = db['speaker.3471']  # 从数据库中获取一条记录
print(type(speaker))  # Record类的实例
# <class '__main__.Record'>
print(speaker.name, speaker.twitter)  # 各个Record实例都有一系列自定义的属性，对应于底层JSON记录里的字段
db.close()  # 关闭shelve.Shelf对象
