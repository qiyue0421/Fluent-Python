"""1、子类化内置类型很麻烦"""
# 在Python2.2之前，内置类型（如list或dict）不能子类化。在Python2.2之后，内置类型可以子类化了，但是有个重要的注意事项：内置类型（使用C语言编写）不会调用用户定义的类覆盖的特殊方法
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)  # 重复存入的值，委托给超类


dd = DoppelDict(one=1)  # 继承自dict的__init__方法显然忽略了自定义覆盖的__setitem__方法
print(dd)
# {'one': 1}  # one的值没有重复

dd['two'] = 2  # []运算符会调用自定义的__setitem__方法，按照预期那样工作
print(dd)
# {'one': 1, 'two': [2, 2]}  # two对应的是两个重复的值

dd.update(three=3)  # 继承自dict的update方法也不使用自定义覆盖的__setitem__方法，three的值没有重复
print(dd)
# {'one': 1, 'two': [2, 2], 'three': 3}
# 原生类型的这种行为违背了面向对象编程的一个基本原则：始终应该从实例（self）所属的类开始搜索方法，即使在超类实现的类中调用也是如此

class AnswerDict(dict):
    def __getitem__(self, key):  # 不管传入什么键，AnswerDict.__getitem__方法始终返回42
        return 42

ad = AnswerDict(a='foo')  # ad是AnswerDict的实例，进行初始化赋值
print(ad['a'])  # 返回42，与预期相符合
# 42

d = {}  # d是内置类型dict的实例
d.update(ad)  # 使用ad的值更新d
print(d['a'])  # dict.update方法忽略了AnswerDict.__getitem__方法
# foo


"""2、多重继承和方法解析顺序"""
# 任何实现多重继承的语言都要处理潜在的命名冲突，这种冲突由不相关的祖先类实现同名方法引起
class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong:', self)  # pong


class C(A):
    def pong(self):
        print('PONG:', self)  # PONG


class D(B, C):
    def ping(self):
        super().ping()
        # A.ping()  # 绕过方法解析，直接调用某个超类的方法
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)


d = D()
print(d.ping())  # D类的ping方法做了两次调用
# ping: <__main__.D object at 0x00000223328BAE10>  # 第一个调用是super().ping()：super函数把ping调用委托给A类；这一行由A.ping输出
# post-ping: <__main__.D object at 0x00000223328BAE10>  # 第二个调用是print('post-ping:', self)，输出的是这一行

print(d.pong())  # 直接调用d.pong()运行的是B类中的版本
# pong: <__main__.D object at 0x000001C6C618AEB8>
print(C.pong(d))  # 超类中的方法都可以直接调用，此时要把实例作为显式参数传入
# PONG: <__main__.D object at 0x000002BB870DAEB8>

# Python能区分d.pong()调用的是哪个方法，是因为Python会按照特定的顺序遍历继承图。这个顺序叫做方法解析顺序（Method Resolution Order, MRO）。类都有一个名为__mro__的属性，
# 它的值是一个元组，按照方法解析顺序列出各个超累，从当前类一直向上，直到object类。方法解析顺序不仅考虑继承图，还考虑子类声明中列出超类的顺序。如果把D类声明为class D(C, B)，那么会先搜索C类，再搜索B类
print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

print(d.pingpong())  # pingpong()方法的5个调用
# ping: <__main__.D object at 0x0000019C25B3AEB8>  # 第一个调用是self.ping()，运行的是D类的ping方法，输出本行和下一行
# post-ping: <__main__.D object at 0x0000019C25B3AEB8>
# ping: <__main__.D object at 0x0000019C25B3AEB8>  # 第二个调用是super().ping()，跳过D类的ping方法，找到A类的ping方法
# pong: <__main__.D object at 0x0000019C25B3AEB8>  # 第三个调用是self.pong()，根据__mro__，找到的是B类实现的pong方法
# pong: <__main__.D object at 0x0000019C25B3AEB8>  # 第四个调用是super().pong，也是根据__mro__，找到B类实现的pong方法
# PONG: <__main__.D object at 0x0000019C25B3AEB8>  # 第五个调用是C.pong(self)，忽略__mro__，找到的是C类实现的pong方法


''' 查看几个类的__mro__属性 '''
print(bool.__mro__)
# (<class 'bool'>, <class 'int'>, <class 'object'>)  # bool从int和object中继承方法和属性

def print_mro(cls):
    print(', '.join(c.__name__ for c in cls.__mro__))

import numbers
print(print_mro(numbers.Integral))  # 输出numbers模块提供的几个数字类
# Integral, Rational, Real, Complex, Number, object

import io  # io模块，open()返回的对象属于这些类型
print(print_mro(io.BytesIO))
# BytesIO, _BufferedIOBase, _IOBase, object
print(print_mro(io.TextIOWrapper))
# TextIOWrapper, _TextIOBase, _IOBase, object

import tkinter  # GUI工具包
print(print_mro(tkinter.Text))
# Text, Widget, BaseWidget, Misc, Pack, Place, Grid, XView, YView, object


"""3、处理多重继承"""
''' ①、把接口继承和实现继承区分开
使用多重继承时，一定要明确一开始为什么创建子类，主要原因可能有：
    * 继承接口，创建子类型，实现”是什么“关系
    * 继承实现，通过重用避免代码重复
通过继承重用代码是实现细节，通常可以换用组合和委托模式，而接口继承则是框架的支柱
'''

''' ②、使用抽象基类显式表示接口
如果类的作用是定义接口，应该明确把它定义为抽象基类
'''

''' ③、通过混入重用代码
如果一个类的作用是为多个不相关的子类提供方法实现，从而实现重用，但不体现”是什么“关系，应该把那个类明确的定义为混入类（mixin class）。从概念上将，混入不定义新类型，只是打包方法，便于重用。
混入类绝对不能实例化，而且具体类不能只继承混入类。混入类应该提供某方面的特定行为，只实现少量关系非常紧密的方法。
'''

''' ④、在名称中明确指明混入
在Python中没有把类声明为混入的正规方式，所以强烈推荐在名称中加入 __Mixin 后缀
'''

''' ⑤、抽象基类可以作为混入，反过来则不成立
抽象基类可以实现具体方法，因此也可以作为混入使用。不过，抽象基类会定义类型，而混入做不到。此外，抽象基类可以作为其他类的唯一基类，而混入绝不能作为唯一的超类，除非继承另一个更具体的混入。

抽象基类有个局限是混入没有的：抽象基类中实现的具体方法只能与抽象基类及其超类中的方法协作。这表明，抽象基类中的具体方法只是一种便利措施，因为这些方法所作的一切，用户调用抽象基类中的其他方法也能做到
'''

''' ⑥、不要子类化多个具体类
具体类可以没有，或最多只有一个具体超类。也就是说具体类的超类中除了这一具体超类之外，其余的都是抽象基类或混入。

class MyConcreteClass(Alpha, Beta, Gamma):  # 如果Alpha是具体类，那么Beta和Gamma必须是抽象基类或混入
    # ...
'''

''' ⑦、为用户提供聚合类
如果抽象基类或混入的组合对客户代码非常有用，那就提供一个类，使用易于理解的方式把它们结合起来，这种类称为聚合类

class Widget(BaseWidget, Pack, Place, Grid):  # Widget类的定义体是空的，但是这个类提供了有用的服务：把四个超类结合在一起
    pass
'''

''' ⑧、优先使用对象组合，而不是类继承
优先使用组合能让设计更灵活
'''
