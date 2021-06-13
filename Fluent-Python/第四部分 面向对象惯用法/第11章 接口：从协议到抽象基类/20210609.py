"""1、Python文化中的接口和协议"""
'''接口在动态类型语言中是怎么运作的？

Python语言没有interface关键字，而且除了抽象基类，每个类都有接口：类实现或者继承的公开属性（方法或数据属性），包括特殊方法，如__getitem__或__add__

'''

"""2、定义抽象基类的子类"""
import collections.abc

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(collections.abc.MutableSequence):  # 将FrenchDeck2声明为collections.MutableSequence的子类
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value

    def __delitem__(self, position):
        del self._cards[position]

    def insert(self, position: int, value) -> None:
        self._cards.insert(position, value)


"""3、标准库中的抽象基类"""
''' collections.abc模块中的抽象基类

collections.abc模块中定义了16个抽象基类：
①、Iterable、Container和Sized
    各个集合应该继承这三个抽象基类，或者至少实现兼容的协议。Iterable通过__iter__方法支持迭代，Container通过__contains__方法支持in运算符，Sized通过__len__方法支持len()函数
    
②、Sequence、Mapping和Set
    这三个是主要的不可变集合类型，而且各自都有可变的子类。

③、MutableSequence、MutableMapping和MutableSet
    是上面三中类型的可变子类
    
④、MappingView
    映射方法：items()、keys()和.value()

⑤、ItemsView、KeysView和ValuesView
    MappingView的三个方法返回的对象分别是ItemsView、KeysView和ValuesView的实例
    
⑥、Callable和Hashable
    这两个抽象基类的主要作用是为内置函数isinstance提供支持，以一种安全的方式判断对象能不能调用或散列

⑦、Iterator
    是Iterable的子类

'''


''' 抽象基类的数字塔
numbers包定义的是“数字塔”————各个抽象基类的层次结构是线性的，其中Number是位于最顶端的超类，随后是Complex子类，依次往下，最低端是Integral类：
* Number
* Complex
* Real
* Rational
* Integral

因此，如果检查一个数是不是整数，可以用 isinstance(x, numbers.Integral)；与之类似，如果一个值可能是浮点数类型，可以使用 isinstance(x, numbers.Real)检查
'''


"""4、定义并使用一个抽象基类"""
''' 抽象基类Tombola
两个抽象方法：
    load(...)：把元素放入容器
    pick()：从容器中随机拿出一个元素，返回选中的元素
    
两个具体方法：
    loaded()：如果容器中至少有一个元素，返回True
    inspect()：返回一个有序元组，由容器中的现有元素构成，不会修改容器的内容（内部的顺序不保留）
'''
import abc

class Tombola(abc.ABC):  # 自己定义的抽象基类要继承abc.ABC

    @abc.abstractmethod
    def load(self, iterable):  # 抽象方法使用@abc.abstractmethod装饰器标记，而且定义体中通常只有文档字符串
        """ 从可迭代对象中添加元素 """

    @abc.abstractmethod
    def pick(self):  # 根据文档字符串，如果没有元素可选，应该抛出LookupError
        """ 随机删除元素，然后将其返回。如果实例为空，这个方法应该抛出LookupError异常 """

    def loaded(self):  # 抽象基类可以包含具体方法
        """ 如果至少有一个元素，返回True；否则返回False """
        return bool(self.inspect())  # 抽象基类中的具体方法只能依赖抽象基类定义的接口————只能使用抽象基类中的其他具体方法、抽象方法或特性

    def inspect(self):
        """ 返回一个有序元组，由当前元素构成 """
        items = []
        while True:  # 不断调用pick()方法，把Tombola清空————不知道子类如何存储元素
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # 使用load()把元素放回去
        return tuple(sorted(items))


# 不符合Tombola要求的子类
class Fake(Tombola):
    def pick(self):
        return 13

print(Fake)  # 创建Fake类
# <class '__main__.Fake'>
# f = Fake()  # 尝试实例化Fake时抛出了TypeError，Python认为Fake是抽象类，因为它没有实现load方法，这是Tombola抽象基类声明的抽象方法之一
# TypeError: Can't instantiate abstract class Fake with abstract methods load

''' 抽象基类句法详解
声明抽象基类最简单的方式是继承abc.ABC或其他抽象基类。abc.ABC是Python3.4新增的类，用旧版Python时必须在class语句中使用metaclass=关键字，把值设为abc.ABCMeta，例如：

class Tombola(metaclass=abc.ABCMeta):
    # ...
    
metaclass=关键字参数是Python3引入的，在Python2中必须使用 __metaclass__ 类属性：

class Tombola(object):  # Python2.0
    __metaclass__ = abc.ABCMeta
    # ...
    
'''


''' 定义Tombola抽象基类的子类 '''
# BingoCage子类使用了更还的随即发生器，实现了所需的抽象方法load和pick，从Tombola中继承了loaded方法，覆盖了inspect方法，还增加了__call__方法
import random

class BingoCage(Tombola):
    def __init__(self, items):
        self._randomizer = random.SystemRandom()  # 生成”适合用于加密“的随机字节序列
        self._items = []
        self.load(items)  # 委托load()方法实现初始加载

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)  # 使用SystemRandom实例的shuffle()方法

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()  # bingo.pick()的快捷方式是bingo()


# LotteryBlower子类打乱”数字球“后没有取出最后一个，而是取出一个随机位置上的球
class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)  # 初始化时接受任何可迭代对象，把参数构建成列表

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))  # 如果范围为空
        except ValueError:  # 捕获ValueError异常
            raise LookupError('pick from empty LotteryBlower')  # 兼容Tombola，捕获ValueError，抛出LookupError
        return self._balls.pop(position)

    def loaded(self):  # 覆盖loaded方法，避免调用inspect方法
        return bool(self._balls)  # 直接处理self._balls而不必构建整个有序元组，从而提升速度

    def inspect(self):  # 使用一行代码覆盖inspect方法
        return tuple(sorted(self._balls))


''' 使用register方法声明虚拟子类 '''
# 注册虚拟子类的方式是在抽象基类上调用register方法，这么做了后，注册的类会变成抽象基类的虚拟子类，而且issubclass和isinstance等函数都能识别，但是注册的类不会从抽象基类中继承任何方法或属性

# noinspection PyUnresolvedReferences
@Tombola.register  # 把TomboList注册为Tombola的虚拟子类
class TomboList(list):  # 扩展list，TomboList是list的真实子类
    def pick(self):
        if self:  # 从list中继承__bool__方法，列表不为空时返回True
            position = random.randrange(len(self))
            return self.pop(position)  # 调用继承自list的self.pop方法，传入一个随机的元素索引
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend  # TomboList.load与list.extend一样

    def loaded(self):
        return bool(self)  # loaded方法委托bool函数

    def inspect(self):
        return tuple(sorted(self))


print(issubclass(TomboList, Tombola))  # 判断TomboList是不是Tombola的子类
# True
t = TomboList(range(100))
print(isinstance(t, Tombola))
# True
