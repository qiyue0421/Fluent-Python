"""8、yield from 的意义"""
''' yield from 的行为
①、子生成器产出的值都直接传给委派生成器的调用方（即客户端代码）
②、使用send()方法发给委派生成器的值都直接传给子生成器。如果发送的值是None，那么会调用子生成器的__next__()方法。如果发送的值不是None，那么会调用子生成器的send()方法。如果调用的方法抛出StopIteration异常，那么委派生成器
恢复运行。任何其他异常都会向上冒泡，传给委托生成器
③、生成器退出时，生成器（或子生成器）中的return expr表达式会触发StopIteration(expr)异常抛出
④、yield from表达式的值是子生成器终止时传给StopIteration异常的第一个参数
⑤、传入委派生成器的异常，除了GeneratorExit之外都传给子生成器的throw()方法。如果调用throw()方法时抛出StopIteration异常，委派生成器恢复运行。StopIteration之外的异常会向上冒泡，传给委派生成器
⑥、如果把GeneratorExit异常传入委派生成器，或者在委派生成器上调用close()方法，那么在子生成器上调用close()方法，如果它有的话。如果调用close()方法导致异常抛出，那么异常会向上冒泡，传给委派生成器；
否则，委派生成器抛出GeneratorExit异常
'''

''' RESULT = yield from EXPR
# 简化的伪代码：不支持throw()和close()方法，且只处理StopIteration异常
_i = iter(EXPR)  # EXPR可以是任何可迭代的对象，因为获取迭代器_i(子生成器)使用的是iter()函数
try:
    _y = next(_i)  # 预激子生成器；结果保存在_y中，作为产出的第一个值
except StopIteration as _e:
    _r = _e.value  # 如果抛出StopIteration异常，获取异常对象的value属性，赋值给_r————这是最简单情况下的返回值
else:
    while 1:  # 运行这个循环时，委派生成器会阻塞，只作为调用方和子生成器之间的通道
        _s = yield _y  # 产出子生成器当前产出的元素；等待调用方发送_s中保存的值。注意，这个代码清单中只有这一个yield表达式
        try:
            _y = _i.send(_s)  # 尝试让子生成器向前执行，转发调用方发送的_s
        except StopIteration as _e:  # 如果子生成器抛出StopIteration异常，获取value属性的值，赋值给_r，然后退出循环，让委派生成器恢复运行
            _r = _e.value
            break            

RESULT = _r  # 返回的结果是_r，即整个yield from表达式的值
'''

''' RESULT = yield from EXPR
# 完整伪代码：支持处理throw()和close()方法
_i = iter(EXPR)  # EXPR可以是任何可迭代的对象，因为获取迭代器_i(子生成器)使用的是iter()函数
try:
    _y = next(_i)  # 预激子生成器；结果保存在_y中，作为产出的第一个值
except StopIteration as _e:
    _r = _e.value  # 如果抛出StopIteration异常，获取异常对象的value属性，赋值给_r————这是最简单情况下的返回值
else:
    while 1:  # 运行这个循环时，委派生成器会阻塞，只作为调用方和子生成器之间的通道
        try:
            _s = yield _y  # 产出子生成器当前产出的元素；等待调用方发送_s中保存的值。注意，这个代码清单中只有这一个yield表达式
        except GeneratorExit as _e:  # 这部分用于关闭委派生成器和子生成器。因为子生成器可以是任何可迭代的对象，所以可能没有close方法，需要处理子生成器没有close()方法的异常
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            raise _e
        except BaseException as _e:  # 这部分处理调用方通过throw()方法传入的异常。同样，子生成器可以是迭代器，从而没有throw方法可调用——-这种情况会导致委派生成器抛出异常
            _x = sys.exc_info()  # 保存调用方传入的值（异常）
            try:
                _m = _i.throw  # 子生成器是否有throw方法
            except AttributeError:  # 子生成器也可能不会处理，而是抛出相同的或不同的异常，向上冒泡，传给委派生成器
                raise _e
            else:  # 如果子生成器有throw方法，调用它并传入调用方发来的异常。子生成器可能会处理传入的异常（然后继续循环）
                try:
                    _y = _m(*_x)
                except StopIteration as _e:  # 可能抛出StopIteration异常（从中获取结果，赋值给_r，循环结束
                    _r = _e.value
                    break
        else:  # 如果产出值时没有异常
            try:  # 尝试让子生成器向前执行
                if _s is None:  # 如果调用方最后发送的值是None，在子生成器上调用next函数，否则调用send方法
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:  # 如果子生成器抛出StopIteration异常，获取value属性的值，赋值给_r，然后退出循环，让委派生成器恢复运行
                _r = _e.value
                break

RESULT = _r  # 返回的结果是_r，即整个yield from表达式的值
'''









