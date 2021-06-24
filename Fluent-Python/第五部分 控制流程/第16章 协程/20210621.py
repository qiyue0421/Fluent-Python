"""6、让协程返回值"""
from collections import namedtuple

Result = namedtuple('Result', 'count average')


def average():
    total = 0.0
    count = 0
    avg = None
    while True:
        term = yield  # 每次激活协程时不会产出移动平均值
        if term is None:
            break  # 为了返回值，协程必须正常终止，这里通过条件判断退出循环
        total += term
        count += 1
        avg = total / count
    return Result(count, avg)  # 在最后返回一个值，通常是某种累计值。注意，return表达式的值会偷偷传给调用方，赋值给StopIteration异常的一个属性，总的来说这么做还是不太合理的


''' average的行为
>>> coro_avg = average()
>>> next(coro_avg)
>>> coro_avg.send(10)
>>> coro_avg.send(20)
>>> coro_avg.send(30)
>>> coro_avg.send(None)  # 发送None会终止循环，导致协程结束，返回结果。生成器对象会抛出StopIteration异常，异常对象的value属性保存着返回的值
Traceback (most recent call last):
  ...
StopIteration: Result(count=3, average=20.0)
'''

''' 捕获异常，获取返回值
>>> coro_avg = average()
>>> next(coro_avg)
>>> coro_avg.send(10)
>>> coro_avg.send(20)
>>> coro_avg.send(30)
>>> try:
...    coro_avg.send(None)
... except StopIteration as exc:
...    result = exc.value
...
>>> result
Result(count=3, average=20.0)
'''

"""7、使用yield from"""
''' 示例
# yield from 可用于简化for循环中的yield表达式
def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i

def gen():  # 改写
    yield from 'AB'
    yield from range(1, 3)    
    
    
# 使用yield from链接可迭代对象
def chain(*iterables):
    for it in iterables:
        yield from it

s = 'ABC'
t = tuple(range(3))
print(list(chain(s, t)))
['A', 'B', 'C', 0, 1, 2]


在生成器gen中使用yield from subgen()时，subgen会获得控制权，把产出的值传给gen的调用方，即调用方可以直接控制subgen。与此同时，gen会阻塞，等待subgen终止。
yield from x 表达式对x对象所做的第一件事是，调用iter(x)，从中获取迭代器。因此，x可以是任意可迭代的对象。
yield from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的样板代码

一些术语：
* 委派审生成器：包含yield from <iterable> 表达式的生成器函数
* 子生成器：从yield from 表达式中<iterable>部分获取的生成器
* 调用方：调用委派生成器的客户端代码
'''
from collections import namedtuple

Result = namedtuple('Result', 'count avg')


# 子生成器
def averager():
    total = 0.0
    count = 0
    avg = None
    while True:
        term = yield  # 客户端发送的所有值都绑定到term变量上
        if term is None:  # 终止条件，如果不这么做，使用yield from调用这个协程的生成器会永远阻塞
            break
        total += term
        count += 1
        avg = total / count
    return Result(count, avg)  # 返回的Result会成为grouper函数中 yield from 表达式的值


# 委派生成器
def grouper(results, key):
    while True:  # 每次循环迭代都会新建averager实例，每个实例都是作为协程使用的生成器对象
        results[key] = yield from averager()  # grouper发送的每个值都会经过yield from处理，通过管道传给averager实例。grouper会在yield from 处暂停，等待averager实例处理客户端发来的值，
        # averager实例运行完毕后，返回的值绑定到results[key]上


# 客户端代码
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)  # 生成器对象（作为协程使用），第一个参数results用于收集结果；第二个参数是某个键
        next(group)  # 预激协程
        for value in values:
            group.send(value)  # 把valuees一个一个传给grouper，传入的值最终到达averager函数中 term = yield 这行
        group.send(None)  # 传入None，终止当前的averager实例，也让grouper继续运行，再创建一个averager实例，处理下一组值
    report(results)


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.avg, unit))


data = {
    'girls;kg': [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m': [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg': [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m': [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

main(data)  # 运行程序
''' 
# 运行结果：
 9 boys  averaging 40.42kg
 9 boys  averaging 1.39m
10 girls averaging 42.04kg
10 girls averaging 1.43m

# 运行方式：
①、外层for循环每次迭代会新建一个grouper实例，赋值给group变量；group是委派生成器
②、调用next(group)，预激委派生成器grouper，此时进入while True循环，调用子生成器averager后，在yield from表达式处暂停
③、内层for循环调用group.send(value)，直接把值传给子生成器averager。同时，当前的grouper实例（group）在yield from表达式处暂停
④、内层循环结束后，group实例依旧在yield from表达式处暂停，因此，grouper函数定义体中为results[key]赋值的语句还没有执行
⑤、如果外层for循环的末尾没有group.send(None)，那么averager子生成器永远不会终止，委派生成器group永远不会再次激活，因此永远不会为results[key]赋值
⑥、外层for循环重新迭代时会新建一个grouper实例，然后绑定到group变量上。前一个grouper实例以及它创建的尚未终止的averager子生成器实例被垃圾回收程序回收
'''
