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
        avg = total/count
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
















