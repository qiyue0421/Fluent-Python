""" 使用特性获取链接的记录

Record：__init__方法与schedule1.py脚本中的一样；为了辅助测试，增加了__eq__方法
DbRecord：Record类的子类，添加了__db类属性，用于设置和获取__db属性的set_db和get_db静态方法，用于从数据库中获取记录的fetch类方法，以及辅助调试和测试的__repr__实例方法
Event：DbRecord类的子类，添加了用于获取所链接记录的venue和speakers属性，以及特殊的__repr__方法

"""
import warnings
import inspect
import json
import os
import shelve
from urllib.request import urlopen

URL = 'https://cdn.jsdelivr.net/gh/fluentpython/example-code@master/19-dyn-attr-prop/oscon/data/osconfeed.json'
JSON = 'data/osconfeed.josn'

DB_NAME = 'data/schedule2_db'
CONFERENCE = 'conference.115'


def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)  # 如果需要下载，就发出警告
        with urlopen(URL) as remote, open(JSON, 'wb') as local:  # with语句中使用两个上下文管理器，分别用于读取和保存远程文件
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)  # json.load函数解析JSON文件，返回Python原生对象。在这个数据源中有这几种数据类型：dict、list、str和int


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


class MissingDatabaseError(RuntimeError):  # 自定义的异常通常是标志类，没有定义体，直接写一个文档字符串说明异常的用途即可
    """需要数据库但没有指定数据库时抛出该异常"""


class DbRecord(Record):  # 扩展Record类
    __db = None  # 私有类属性，存储一个打开的shelve.Shelf数据库引用

    @staticmethod
    def set_db(db):  # 静态方法，强调不管调用多少次，效果始终一样
        DbRecord.__db = db  # 即使调用 Event.set_db(my_db)，__db属性仍在DbRecord类中设置

    @staticmethod
    def get_db():  # 也是静态方法，无论调用几次，返回值始终是 DbRecord.__db引用的对象
        return DbRecord.__db

    @classmethod  # 类方法
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]  # 从数据库中获取ident键对应的记录
        except TypeError:  # 捕获TypeError异常
            if db is None:  # db为空
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))  # 抛出异常，说明必须设置数据库
            else:
                raise  # 重新抛出TypeError异常

    def __repr__(self):
        if hasattr(self, 'serial'):  # 如果记录有'serial'属性，在字符串表现形式中使用
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  # 否则使用继承的__repr__方法


class Event(DbRecord):  # 扩展DbRecord类
    @property
    def venue(self):  # venue特性
        key = 'venue.{}'.format(self.venue_serial)  # 使用venue_serial属性构建key
        return self.__class__.fetch(key)  # 传给继承自DbRecord类的fetch类方法

    @property
    def speakers(self):  # speakers特性
        if not hasattr(self, '_speaker_objs'):  # 检查记录是否有_speaker_objs属性
            spkr_serials = self.__dict__['speakers']  # 如果没有，直接从__dict__实例属性中获取'speakers'属性的值，防止无限递归
            fetch = self.__class__.fetch  # 获取fetch类方法的引用
            self._speaker_objs = [fetch('speaker.{}'.format(key)) for key in spkr_serials]  # 获取speaker记录列表，赋值给self._speaker_objs
        return self._speaker_objs  # 返回列表

    def __repr__(self):
        if hasattr(self, 'name'):  # 如果记录有name属性，在字符串表现形式中使用
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:  # 否则调用继承的__repr__方法
            return super().__repr__()


def load_db(db):
    raw_data = load()  # 如果本地没有副本，从网上下载JSON数据源
    warnings.warn('loading' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():  # 迭代集合
        record_type = collection[:-1]  # 去掉尾部的's'
        cls_name = record_type.capitalize()  # 首字母大写，获取可能的类名
        cls = globals().get(cls_name, DbRecord)  # 从模块全局作用域获取名称对应的对象，找不到对象就使用DbRecord
        if inspect.isclass(cls) and issubclass(cls, DbRecord):  # 如果获取的对象是类，而且是DbRecord的子类
            factory = cls  # factory可能是DbRecord的任何一个子类，具体的类取决于record_type的值
        else:
            factory = DbRecord
        for record in rec_list:  # 创建key，并保存记录
            key = '{}.{}'.format(record_type, record['serial'])  # 使用record_type和'serial'字段构成key
            record['serial'] = key  # 把'serial'字段的值设为完整的键
            db[key] = factory(**record)  # 存储在数据库中的对象由factory构建，它可能是DbRecord类，也可能是根据record_type的值确定的某个子类


db = shelve.open(DB_NAME)  # 打开现有的数据库文件，或者新建一个
if CONFERENCE not in db:  # 检查已知的键是否存在
    load_db(db)  # 数据库是空的，就调用load_db加载数据

DbRecord.set_db(db)
event = DbRecord.fetch('event.33950')  # 获取任何类型的记录
print(event)  # event是Event类的实例，而Event类扩展DbRecord类
# <Event 'There *Will* Be Bugs'>
print(event.venue)  # 返回一个DbRecord实例
# <DbRecord serial='venue.1449'>
print(event.venue.name)  # 自动取值，找出event.venue的名称
# Portland 251
