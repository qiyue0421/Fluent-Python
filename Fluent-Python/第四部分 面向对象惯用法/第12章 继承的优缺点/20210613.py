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

































