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


















































