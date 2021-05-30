# 函数装饰器用于在源码中“标记”函数，以某种方式增强函数的行为

"""1、装饰器基础知识"""
# 装饰器是可调用的对象，其参数是另一个函数（被装饰的函数）。装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象。
# 两大特性：
#   * 将被装饰函数替换成其他函数
#   * 在加载模块时，装饰器立即执行

'''
假如有个名为decorate的装饰器：

@decorate
def target():
    print('running target()')
    
上述代码的效果与下述写法相同：

def target():
    print('running target()')
    
target = decorate(target)

两种写法的最终结果一样：上述两个代码片段执行完毕后得到的target不一定是原来的那个target函数，而是decorate(target)返回的函数
'''


# 装饰器通常把函数替换成另一个函数
def deco(func):
    def inner():
        print('running inner()')

    return inner  # 返回inner函数对象


@deco
def target():  # 使用deco装饰
    print('running target()')


target()  # 调用被装饰的target其实会运行inner()
# running inner()
print(target)  # 审查对象，发现target现在是inner的引用
# <function deco.<locals>.inner at 0x00000271ECA83D90>


"""2、Python何时执行装饰器"""
# 装饰器的一个关键特性是，它们在被装饰的函数定义之后立即运行，这通常是在导入时（即python加载模块时）

registry = []


def register(func):
    print('running register(%s)' % func)  # 显示被装饰的函数
    registry.append(func)
    return func  # 必须返回函数；这里返回的函数与通过参数传入的一样


@register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()
'''
输出如下：
running register(<function f1 at 0x0000012D73AED510>)  # 此处为register在其他所有函数之前运行
running register(<function f2 at 0x0000012D73AED598>)
running main()
registry -> [<function f1 at 0x0000012D73AED510>, <function f2 at 0x0000012D73AED598>]
running f1()
running f2()
running f3()
'''


"""3、使用装饰器改进“策略”模式"""
promos = []

def promotion(promo_func):  # 装饰器promotion把promo_func添加到promos列表中，然后原封不动的将其返回
    promos.append(promo_func)
    return promo_func

@promotion  # 所有被promotion装饰的函数都会添加到promos列表中
def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

@promotion
def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

def best_promo(order):
    return max(promo(order) for promo in promos)


"""4、变量作用域规则"""
# 定义并测试一个函数，读取两个变量的值：一个是局部变量a，是函数的参数；另一个是变量b，这个函数没有定义它。
'''
def f1(a):
    print(a)
    print(b)

f1(3)


# 报错：
Traceback (most recent call last):
  File "<stdin>", line 131, in <module>
    f1(3)
  File "<stdin>", line 129, in f1
    print(b)
NameError: name 'b' is not defined

如果先给全局变量b赋值，然后再调用f1，就不会出错：
b = 6
f1(3)

'''

'''
b = 6
def f2(a):
    print(a)
    print(b)  # Python编译函数的定义体时，它会首先判断b是局部变量，因为在函数中给它赋值了，就会报 UnboundLocalError 错误，即定义前使用错误
    b = 9

f2(3)


# 报错：
3
Traceback (most recent call last):
  File "<stdin>", line 131, in <module>
  File "<stdin>", line 129, in f2
UnboundLocalError: local variable 'b' referenced before assignment

'''
