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

'''为任意对象做深复制和浅复制

'''













