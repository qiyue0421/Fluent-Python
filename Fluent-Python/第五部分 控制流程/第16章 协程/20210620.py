""" 协程
从句法来看，协程与生成器类似，都是定义体中包含yield关键字的函数。可是，在协程中，yield通常出现在表达式的右边（例如，datum = yield），可以产出值，也可以不产出————如果yield关键字后面没有表达式，那么生成器产出None。
协程可能会从调用方接收数据，不过调用方把数据提供给协程使用的是 .send(datum) 方法，而不是next(...)函数。通常，调用方会把值推送给协程。

yield关键字甚至还可以不接收或传出数据，不管数据如何流动，yield都是一种流程控制工具，使用它可以实现协作式多任务：协程可以把控制器让步给中心调度程序，从而激活其他协程。
"""
import inspect

"""1、生成器如何进化成协程"""
''' 协程的底层架构
yield关键字可以在表达式中使用，而且生成器API中增加了 .send(value) 方法，生成器的调用方可以使用.send(...)方法发送数据，发送的数据会成为生成器函数中yield表达式的值。因此，生成器可以作为协程使用。
协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值。除了send(...)方法，还添加了throw(...)和close(...)方法：前者的作用是让调用方抛出异常，在生成器中处理；后者的作用是终止生成器。
'''


"""2、用作协程的生成器的基本行为"""
''' 协程的四个状态————当前状态可以使用 inspect.getgeneratorstate(...) 函数确定，该函数会返回下述字符串中的一个
GEN_CREATED：等待开始执行
GEN_RUNNING：解释器正在执行
GEN_SUSPENDED：在yield表达式处暂停
GEN_CLOSED：执行结束
'''
def simple_coroutine():  # 协程使用生成器函数定义：定义体中有yield关键字
    print('-> coroutine started')
    x = yield  # 在表达式中使用yield，如果协程只需从客户那里接收数据，那么产出的值是None————这个值是隐式指定的，因为yield关键字右边没有表达式
    print('-> coroutine received:', x)

my_coro = simple_coroutine()  # 调用函数得到生成器对象
print(my_coro)
# <generator object simple_coroutine at 0x0000025939359A98>
print(next(my_coro))  # 首先要调用next(...)函数，因为生成器还没启动，没在yield语句处暂停，所以一开始无法发送数据
# -> coroutine started
# None
'''
my_coro.send(42)  # 调用send(...)方法后，协程定义体中的yield表达式会计算出42，现在，协程会恢复，一直运行到下一个yield表达式，或者终止
-> coroutine received: 42
Traceback (most recent call last):  # 控制权流动到协程定义体的末尾，导致生成器像往常一样抛出StopIteration异常
  ...
    my_coro.send(42)
StopIteration
'''


''' “预激”(prime)协程
因为send方法的参数会成为暂停的yield表达式的值，所以，仅当协程处于暂停状态时才能调用send方法，例如my_coro.send(42)。不过，如果协程还没有激活————即状态是GEN_CREATED，情况就不同。
因此，始终要调用next(my_coro)激活协程，也可以调用my_coro.send(None)，效果一样。最先调用next(my_coro)函数这一步通常称为“预激”(prime)协程————即让协程向前执行到第一个yield表达式，准备好作为活跃的协程使用
'''
my_coro1 = simple_coroutine()
'''
my_coro1.send(1729)  # 如果创建协程对象后立即把None之外的值发给它，会出现错误
Traceback (most recent call last):
  ...
    my_coro1.send(1729)
TypeError: can't send non-None value to a just-started generator
'''


# 产出两个值的协程
def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


''' 执行过程：
>>> my_coro2 = simple_coro2(14)
>>> inspect.getgeneratorstate(my_coro2)  # 此时处于GEN_CREATED状态————即协程未启动
GEN_CREATED
>>> next(my_coro2)  # 向前执行协程到第一个yield表达式，打印 -> Started: a = 14 消息，然后产出a的值，并且暂停，等待为b赋值
-> Started: a = 14
14
>>> inspect.getgeneratorstate(my_coro2)  # 此时处于GEN_SUSPENDED状态————即协程在yield表达式处暂停
GEN_SUSPENDED

>>> my_coro2.send(28)  # 发送数字28给暂停的协程，计算yield的值，得到28，然后把数绑定给b。打印 -> Received: b = 28 消息，产出 a + b 的值（42），然后协程暂停，等待为c赋值
-> Received: b = 28
42
>>> my_coro2.send(99)  # 发送数字99给暂停的协程，计算yield表达式，得到99，将数绑定给c。打印 -> Received: c = 99 消息，然后协程终止，导致生成器对象抛出StopIteration异常
-> Received: c = 99
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
>>> inspect.getgeneratorstate(my_coro2)  # 此时处于GEN_CLOSED状态————即协程执行结束
'GEN_CLOSED'

总结————simple_coro2协程的执行过程分为3个阶段：
1）、调用next(my_coro2)，打印第一个消息，然后执行yield a，产出数字14
2）、调用my_coro2.send(28)，把28赋值给b，打印第二个消息，然后执行yield a + b，产出数字42
3）、调用my_coro2.send(99)，把99赋值给c，打印第三个消息，协程终止
'''


"""3、示例：使用协程计算移动平均值"""
# 计算移动平均值的协程：好处是total和count声明为局部变量即可，无需使用实例属性或闭包在多次调用之间保持上下文
def averager():
    total = 0.0
    count = 0
    average = None
    while True:  # 无限循环表明，只要调用方不断把值发给这个协程，它就会一直接收值，然后生成结果。仅当调用方在协程上调用close()方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止
        term = yield average  # yield表达式用于暂停执行协程，把结果发送给调用方；还用于接收调用方后面发送给协程的值，恢复无限循环
        total += term
        count += 1
        average = total/count

''' 执行过程
>>> coro_avg = averager()  # 创建协程对象
>>> next(coro_avg)  # 预激协程
>>> coro_avg.send(10)  # 计算移动平均值
10.0
>>> coro_avg.send(30)
20.0
>>> coro_avg.send(5)
15.0
'''


"""4、预激协程的装饰器"""
# 如果不预激，那么协程没什么用，为了简化协程的用法，有时会使用一个预激装饰器
from functools import wraps

def coroutine(func):
    """ 装饰器：向前执行到第一个yield表达式，预激func """
    @wraps(func)
    def primer(*args, **kwargs):  # 将被装饰的生成器函数替换成primer函数；调用primer函数时，返回预激后的生成器
        gen = func(*args, **kwargs)  # 调用被装饰的函数，获取生成器对象
        next(gen)  # 预激生成器
        return gen  # 返回生成器
    return primer


@coroutine  # 使用装饰器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:  # 无限循环表明，只要调用方不断把值发给这个协程，它就会一直接收值，然后生成结果。仅当调用方在协程上调用close()方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止
        term = yield average  # yield表达式用于暂停执行协程，把结果发送给调用方；还用于接收调用方后面发送给协程的值，恢复无限循环
        total += term
        count += 1
        average = total/count

''' 执行过程：
>>> coro_avg = averager()  # 创建一个生成器对象，在coroutine装饰器的primer函数中已经预激了这个生成器
>>> inspect.getgeneratorstate(coro_avg)  # 当前处于GEN_SUSPENDED状态，因此这个协程已经准备好了，可以接收值了
'GEN_SUSPENDED'
>>> coro_avg.send(10)  # 立即开始把值发给coro_avg，计算移动平均值
10.0
>>> coro_avg.send(30)
20.0
>>> coro_avg.send(5)
15.0
'''








