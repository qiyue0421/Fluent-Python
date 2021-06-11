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

'''
