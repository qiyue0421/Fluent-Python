"""4、元类基础知识
# 元类是制造类的工厂，不过不是函数，而是类
# 根据Python对象模型，类是对象，因此类肯定是另外某个类的实例。默认情况下，Python中的类是type类的实例，也就是说，type是大多数内置的类和用户定义的类的元类：
>>> 'spam'.__class__
<class 'str'>
>>> str.__class__
<class 'type'>
>>> type.__call__  # 为了避免无限回溯，type是其自身的实例
<class 'type'>
# object类和type类之间的关系很独特：object是type的实例，而type是object的子类。

# 所有类都直接或间接的是type的实例，不过只有元类同时也是type的子类。若想理解元类，一定要知道这种关系：元类从type类继承了构建类的能力
>>> import collections
>>> collections.Iterable.__class__  # collections.Iterable所属的类是abc.ABCMeta
<class 'abc.ABCMeta'>
>>> import abc
>>> abc.ABCMeta.__class__  # ABCMeta最终所属的类也是type
<class 'type'>
>>> abc.ABCMeta.__mro__
(<class 'abc.ABCMeta'>, <class 'type'>, <class 'object'>)
"""
