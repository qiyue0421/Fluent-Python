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
y = Gizmo() * 10
# Gizmo id: 2865192691640  # 此处表明，在尝试求积之前其实会创建一个新的Gizmo实例

print(dir())  # 不会创建变量y，因为在对赋值语句的右边进行求值时抛出了异常
# ['Gizmo', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'x']


































