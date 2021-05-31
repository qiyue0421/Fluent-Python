"""5、闭包"""
# 闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。

# 计算移动平均值
import functools

'''使用类实现'''

class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)


avg = Averager()
print(avg(10))
print(avg(11))
print(avg(12))


'''使用函数式实现'''
# 调用make_averager时，返回一个averager函数对象。每次调用averager时，它会把参数添加到系列值中，然后计算当前平均值
def make_averager():
    series = []  # 在make_averager函数中，series是局部变量

    def averager(new_value):
        series.append(new_value)  # 在averager函数中，series是自由变量，指未在本地作用域中绑定的变量
        total = sum(series)
        return total/len(series)
    return averager


avg = make_averager()
print(avg(10))  # 调用avg(10)时，make_averager函数已经返回了，而它的本地作用域也没了
print(avg(11))
print(avg(12))

# 审查averager对象，python在__code__属性（表示编译后的函数定义体）中保存局部变量和自由变量的名称
print(avg.__code__.co_varnames)  # 局部变量
# ('new_value', 'total')
print(avg.__code__.co_freevars)  # 自由变量
# ('series',)

# series的绑定在返回的avg函数的__closure__属性中。avg.__closure__中的各个元素对应于avg.__code__.co_freevars中的一个名称，这些元素都是cell对象，有个cell_contents属性，保存着真正的值
print(avg.__closure__)
# (<cell at 0x0000020A021547C8: list object at 0x0000020A01F56288>,)  # 这里只有一个元素
print(avg.__closure__[0].cell_contents)
# [10, 11, 12]


"""5、nonlocal声明"""
# 计算移动平均值的高阶函数，不保存所有历史值
def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total  # 将变量标记为自由变量，即使在函数中为变量赋予新值了，也会变成自由变量
        count += 1  # 只存储目前的总值
        total += new_value  # 只存储目前的元素个数
        return total / count
    return averager


"""7、实现一个简单的装饰器"""
# 定义一个简单的装饰器，它会在每次调用被装饰的函数时计时，然后把经过的时间、传入的参数和调用的结果打印出来
import time

def clock(func):
    def clocked(*args):  # 定义内部函数clocked，接受任意个位置参数
        t0 = time.perf_counter()  # 返回系统运行时间的精确值
        result = func(*args)  # clocked的闭包中包含自由变量func
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ','.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked  # 返回内部函数，取代被装饰的函数

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorail(n):
    return 1 if n < 2 else n*factorail(n-1)


print('*' * 40, 'Calling snooze(.123)')
snooze(.123)
print('*' * 40, 'Calling factorail(6)')
print('6! =', factorail(6))

'''
**************************************** Calling snooze(.123)
[0.12978890s] snooze(0.123) -> None
**************************************** Calling factorail(6)
[0.00000190s] factorail(1) -> 1
[0.00005650s] factorail(2) -> 2
[0.00008580s] factorail(3) -> 6
[0.00011150s] factorail(4) -> 24
[0.00013770s] factorail(5) -> 120
[0.00016750s] factorail(6) -> 720
6! = 720
'''
# 装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外的操作


'''改进后的clock装饰器，能够正确处理关键字参数
def clock(func):
    @functools.wraps(func)  # 将相关属性从func复制到clocked，比如__name__、__doc__属性
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(','.join(pairs))
        arg_str = ','.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name , arg_str, result))
        return result
    return clocked
'''


"""8、标准库中的装饰器"""
# Python内置了三个用于装饰方法的函数：property、classmethod和staticmethod

'''使用functools.lru_cache做备忘'''
# functools.lru_cache实现了备忘功能，它把耗时的函数的结果保存起来，避免传入相同的参数时重复计算，一段时间不用的缓存条目会被扔掉（表明缓存不会无限增长）

# N个斐波那契数(递归方式)
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

print(fibonacci(6))
'''输出如下
[0.00000020s] fibonacci(0) -> 0
[0.00000030s] fibonacci(1) -> 1
[0.00001130s] fibonacci(2) -> 1
[0.00000010s] fibonacci(1) -> 1
[0.00000010s] fibonacci(0) -> 0
[0.00000020s] fibonacci(1) -> 1
[0.00000990s] fibonacci(2) -> 1
[0.00001960s] fibonacci(3) -> 2
[0.00004220s] fibonacci(4) -> 3
[0.00000020s] fibonacci(1) -> 1
[0.00000020s] fibonacci(0) -> 0
[0.00000020s] fibonacci(1) -> 1
[0.00000960s] fibonacci(2) -> 1
[0.00001980s] fibonacci(3) -> 2
[0.00000010s] fibonacci(0) -> 0
[0.00000020s] fibonacci(1) -> 1
[0.00000980s] fibonacci(2) -> 1
[0.00000020s] fibonacci(1) -> 1
[0.00000020s] fibonacci(0) -> 0
[0.00000020s] fibonacci(1) -> 1
[0.00001010s] fibonacci(2) -> 1
[0.00001970s] fibonacci(3) -> 2
[0.00003970s] fibonacci(4) -> 3
[0.00007010s] fibonacci(5) -> 5
[0.00012230s] fibonacci(6) -> 8
8
'''
# 可见，fibonacci(1)调用了8次，fibonacci(2)调用了5次，性能损耗严重

# 使用缓存实现
@functools.lru_cache()  # 像常规函数那样调用lru_cache，因为lru_cache可以接受配置参数
@clock  # 叠放装饰器
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

print(fibonacci(6))
'''输出如下
[0.00000090s] fibonacci(0) -> 0
[0.00000090s] fibonacci(1) -> 1
[0.00007210s] fibonacci(2) -> 1
[0.00000300s] fibonacci(3) -> 2
[0.00012510s] fibonacci(4) -> 3
[0.00000220s] fibonacci(5) -> 5
[0.00017890s] fibonacci(6) -> 8
8
'''
# 执行时间少了一半，而且n的每个值只调用一次函数


'''lru_cache可以使用两个可选参数配置
functools.lru_cache(maxsize=128, typed=False)

maxsize参数指定存储多少个调用的结果，缓存满了之后，旧的结果会被扔掉，腾出空间，为了得到最佳性能，maxsize应该设为2的幂
typed参数如果设为True，把不同参数类型得到的结果分开保存，即把通常认为相等的浮点数和整数参数（如1和1.0）区分开
lru_cache使用字典存储结果，而且键根据调用时传入的定位参数和关键字参数创建，所有被lru_cache装饰的函数，它的所有参数都必须是可散列的

'''


"""9、叠放装饰器
# 下述代码

@d1
@d2
def f():
    print('f')

# 等同于

def f():
    print('f')

f = d1(d2(f))
"""


"""10、参数化装饰器"""
'''让装饰器接受其他参数'''
registry = set()  # set对象，添加和删除很快

def register(active=True):  # 装饰器工厂函数，接受一个可选的关键字参数，调用它会返回真正的装饰器
    def decorate(func):  # 真正的装饰器，它的参数是一个函数
        print('running register(active=%s) -> decorate(%s)' % (active, func))
        if active:
            registry.add(func)  # active为真时，注册func
        else:
            registry.discard(func)  # 如果active不为真，而且func在registry中，那么把它删除
        return func  # 返回一个函数
    return decorate  # 返回装饰器


@register(active=False)  # 工厂函数必须作为函数调用，并且传入所需的参数
def f1():
    # running register(active=False) -> decorate(<function f1 at 0x000001D32530D840>)
    print('running f1()')

@register()  # 即使不传入参数，也必须作为函数调用
def f2():
    # running register(active=True) -> decorate(<function f2 at 0x000001D32530D9D8>)
    print('running f2()')

def f3():
    print('running f3()')

print(registry)  # 只有f2函数在registry中，f1不在其中
# {<function f2 at 0x00000244A931D9D8>}


'''参数化clock装饰器，添加功能：让用户传入一个格式字符串，控制被装饰函数的输出'''
DEAFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEAFAULT_FMT):  # 参数化装饰器工厂函数
    def decorate(func):  # 真正的装饰器
        def clocked(*_args):  # 包装被装饰的函数
            t0 = time.time()
            _result = func(*_args)  # 被装饰的函数返回的真正结果
            elapsed = time.time() - t0
            name = func.__name__
            args = ','.join(repr(arg) for arg in _args)  # _args是clocked的参数，args是用于显示的字符串
            result = repr(_result)  # 字符串表现形式，用于显示
            print(fmt.format(**locals()))  # **locals()是为了在fmt中引用clocked的局部变量
            return _result  # clocked会替换被装饰的函数，因此应该返回被装饰的函数返回的值
        return clocked  # decorate返回clocked
    return decorate  # 返回装饰器


@clock()
def snooze(seconds):
    time.sleep(seconds)

for i in range(3):
    snooze(.123)
'''输出结果
[0.12468410s] snooze(0.123) -> None
[0.12522125s] snooze(0.123) -> None
[0.12492847s] snooze(0.123) -> None
'''

@clock('{name}: {elapsed}s')
def snooze(seconds):
    time.sleep(seconds)

for i in range(3):
    snooze(.123)
'''输出结果
snooze: 0.12455487251281738s
snooze: 0.12527012825012207s
snooze: 0.12454485893249512s
'''

@clock('{name}({args}) dt={elapsed:0.3f}s')
def snooze(seconds):
    time.sleep(seconds)

for i in range(3):
    snooze(.123)
'''输出结果
snooze(0.123) dt=0.125s
snooze(0.123) dt=0.125s
snooze(0.123) dt=0.126s
'''
