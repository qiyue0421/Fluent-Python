"""1、变量不是盒子"""
# Python变量应该被理解为附加在对象上的标注，就好像便利贴一样。
# 为了理解Python中的赋值语句，应该始终先读右边。对象在右边创建或获取，在此之后左边的变量才会绑定到对象上，这就像为对象贴上标签。

a = [1, 2, 3]
b = a
a.append(4)
print(b)


'''创建对象之后才会把变量分配给对象，通常这样说：把变量s分配给对象seesaw'''
class Gizmo:
    def __init__(self):
        print('Gizmo id: %d' % id(self))

x = Gizmo()
# Gizmo id: 2865192691360
# noinspection PyTypeChecker
# y = Gizmo() * 10
# Gizmo id: 2865192691640  # 此处表明，在尝试求积之前其实会创建一个新的Gizmo实例

print(dir())  # 不会创建变量y，因为在对赋值语句的右边进行求值时抛出了异常
# ['Gizmo', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'x']


"""2、标识、相等性和别名"""
charles = {'name': 'Charles L. Dodgson', 'born': 1832}
lewis = charles  # lewis是charles的别名
print(lewis is charles)
# True
print(id(lewis), id(charles))
# 2115862235752 2115862235752
lewis['balance'] = 950  # 向lewis中添加一个元素相当于向charles中添加一个元素
print(charles)
# {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}

alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
print(alex == charles)  # 内容相等，== 比较值
print(id(alex))
print(alex is not charles)  # 不是相同的对象

'''在 == 和 is 之间选择
== 比较对象的值
is 比较对象的标识（内存中的地址），在变量和单例值之间比较时，应该使用is

通常使用is检查变量绑定的值是不是None
x is None
x is not None
'''

'''元组的相对不可变性
# 元组与多数Python集合（列表、字典、集合等等）一样，保存的是对象的引用。如果引用的元素是可变的，即便元组本身不可变，元素依然可变。也就是说，元组的不可变性其实是指tuple数据结构的物理内容，
# 即保存的引用不可变，与引用的对象无关。
'''
# 元组的值会随着引用的可变对象的变化而变，元组中不可变的是元素的标识
t1 = (1, 2, [30, 40])  # t1不可变，但是t1[-1]可变
t2 = (1, 2, [30, 40])  # 构建t2，元素与t1一样
print(t1 == t2)  # 不同对象，但是二者值相等
# True
print(id(t1[-1]))
# 2147470893704

t1[-1].append(99)  # 就地修改t1[-1]列表
print(t1)
print(id(t1[-1]))  # 标识没变
# 2147470893704
print(t1 == t2)  # 但是值变了
# False


"""3、默认做浅复制"""
# 复制列表（或多数内置的可变集合）最简单的方式是使用内置的类型构造方法
l1 = [3, [55, 44], (7, 8, 9)]
l2 = list(l1)
# l2 = l1[:]
print(l2 == l1)  # 副本与源列表相等
# True
print(l2 is l1)  # 二者指代的不是同一个对象
# False

# 构造方法或[:]默认做的是浅复制——即复制了最外层容器，副本中的元素是源容器中元素的引用。
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)  # l2是l1的浅复制副本
l1.append(100)  # 把100追加到l1中，对l2没有影响
l1[1].remove(55)  # 把内部的55删除，这对l2有影响，因为l2[1]绑定的列表与l1[1]是同一个
print('l1:', l1)
print('l2:', l2)
l2[1] += [33, 22]  # 对可变对象来说，如l2[1]引用的列表，+=运算符就地修改列表
l2[2] += (10, 11)  # 对于元组来说，+=运算符创建一个新元组，然后重新绑定给变量l2[2]
print('l1:', l1)
# l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
print('l2:', l2)
# l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]

'''为任意对象做深复制和浅复制'''
# 深复制——即副本不共享内部对象的引用，copy模块提供的deepcopy和copy函数能够为任意对象做深复制和浅复制

# 校车类，模拟乘客在途中上车和下车
import copy
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = Bus(['Alic', 'Bill', 'Claire', 'David'])
bus2 = copy.copy(bus1)  # 浅复制副本
bus3 = copy.deepcopy(bus1)  # 深复制副本
print(id(bus1), id(bus2), id(bus3))
# 1226700598800 1226700599024 1226700624728

bus1.drop('Bill')
print(bus2.passengers)  # bus1中的'Bill'下车后，bus2中也没有他了
# ['Alic', 'Claire', 'David']
print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))  # bus1和bus2共享同一个列表对象，因为bus2是bus1的浅复制副本
# 2020403581832 2020403581832 2020403512264
print(bus3.passengers)  # bus3的passengers属性指代另一个列表
# ['Alic', 'Bill', 'Claire', 'David']

'''循环引用'''
a = [10, 20]
b = [a, 30]  # b引用a
a.append(b)  # 追加b到a
print(a)
# [10, 20, [[...], 30]]

c = copy.deepcopy(a)  # deepcopy会想办法复制a
print(c)
# [10, 20, [[...], 30]]


"""4、函数的参数作为引用时"""
# python唯一支持的参数传递模式是共享传参（call by sharing）
# 共享传参：函数的各个形式参数获得实参中各个引用的副本。也就是说，函数内部的形参是实参的别名
# 函数可能会修改作为参数传入的可变对象，但是无法修改那些对象的标识（即不能把一个对象替换成另一个对象）
def f(c, d):
    c += d
    return c

m = 1
n = 2
print(f(m, n))
# 3
print(m, n)  # 数字m没有变
# 1 2

p = [1, 2]
q = [3, 4]
print(f(p, q))
# [1, 2, 3, 4]
print(p, q)  # 列表p被修改了
# [1, 2, 3, 4] [3, 4]

t = (10, 20)
u = (30, 40)
print(f(t, u))
# (10, 20, 30, 40)
print(t, u)  # 元组t没变
# (10, 20) (30, 40)

'''不要使用可变类型作为参数的默认值'''
# 可变默认值的危险
class HauntedBus:
    def __init__(self, passengers=[]):  # 默认绑定的列表对象为空列表
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


bus1 = HauntedBus(['Alice', 'Bill'])
print(bus1.passengers)
# ['Alice', 'Bill']
bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers)
# ['Bill', 'Charlie']

bus2 = HauntedBus()
bus2.pick('Carrie')
print(bus2.passengers)
# ['Carrie']

bus3 = HauntedBus()  # 一开始为空的
print(bus3.passengers)  # 但是默认列表不为空
# ['Carrie']
bus3.pick('Dave')
print(bus2.passengers)  # 登上bus3的'Dave'出现在了bus2中
# ['Carrie', 'Dave']
print(bus2.passengers is bus3.passengers)  # 指代的是同一个列表
# True
print(bus1.passengers)  # bus1.passengers是不同的列表
# ['Bill', 'Charlie']

# 问题在于：没有指定初始乘客的HauntedBus实例会共享同一个乘客列表

'''防御可变参数'''
class TwilightBus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers  # 赋值语句将self.passengers变成passengers的别名，而后者是传给__init__方法的实参的别名

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']  # 篮球队列表
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)  # 下车的学生从篮球队列表中消失了
# ['Sue', 'Maya', 'Diana']


class TwilightBus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)  # 创建passengers列表的副本；如果不是列表，就把它转换成列表

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']  # 篮球队列表
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)
# ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']


"""5、del和垃圾回收"""
# del语句删除名称，而不是对象。del命令可能会导致对象被当作垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时
# 在CPython中，垃圾回收使用的主要算法是引用计数。实际上，每个对象上都会统计有多少引用指向自己，当引用计数归零时，对象立即就被销毁：CPython会在对象上调用__del__方法，然后释放分配给对象的内存
import weakref

s1 = {1, 2, 3}
s2 = s1  # s1和s2是别名，指向同一个集合，{1, 2, 3}
def bye():
    print('Gone with the wind..')

ender = weakref.finalize(s1, bye)  # 在s1引用的对象上注册bye回调
print(ender.alive)  # 调用finalize对象之前，.alive属性的值为True
# True

del s1  # del不删除对象，而是删除引用
print(ender.alive)
# True

# noinspection PyRedeclaration
s2 = 'spam'  # 重新绑定最后一个引用s2，让{1, 2, 3}无法被获取，对象被销毁了
# Gone with the wind..
print(ender.alive)  # 调用bye回调
# False












