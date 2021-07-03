# asyncio包：这个包使用事件循环驱动的协程实现并发

"""1、线程与协程对比"""
''' 通过线程以动画形式显示文本式旋转指针 spinner_thread.py
import threading
import itertools
import time
import sys

class Signal:  # 定义一个简单的可变对象
    go = True  # go属性用于从外部控制线程


def spain(msg, signal):  # 在单独的线程中运行，signal参数用来关闭线程
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # 无限循环，itertools.cycle用于从指定序列中反复不断的生成元素
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # 关键所在：使用退格符（\x08）把光标移回来，原理上相当于 len(status) 长度的\b退格键，覆盖了原来的 Len(status) 长度字符，退格符相当于键盘上的backspace
        time.sleep(.1)
        if not signal.go:  # 如果go的属性不是true了，就跳出循环
            break
    write(' ' * len(status) + '\x08' * len(status))  # 使用退格键清空状态消息，把光标移回开头


def slow_function():  # 执行阻塞型I/O操作
    time.sleep(3)  # 调用sleep函数会阻塞主线程，不过一定要这样做，以便释放GIL，创建从属线程
    return 42


def supervisor():  # 这个函数设置从属线程，显示线程对象，运行耗时的计算，最后杀死线程
    signal = Signal()
    spinner = threading.Thread(target=spain, args=('thinking!', signal))
    print('spinner object:', spinner)  # 显示从属线程对象
    spinner.start()  # 启动从属线程
    result = slow_function()  # 运行slow_function函数，阻塞主线程，同时，从属线程以动画形式显示旋转指针
    signal.go = False  # 改变signal状态，这回终止spin函数中的那个for循环
    spinner.join()  # 等待spinner线程结束
    return result


def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
    
# 运行方式为：
# python3 spinner_thread.py
'''


''' 通过协程以动画形式显示文本式旋转指针 spinner_asyncio.py
import asyncio
import itertools
import sys

@asyncio.coroutine  # 打算交给asyncio处理的协程要使用 @asyncio.coroutine 装饰，这不是强制要求，因为这样能够在一众普通函数中将协程凸显出来，也有助于调试：如果还没从中产出值，
# 协程就被垃圾回收了（意味着有操作未完成，因此有可能是个缺陷），那样就可以发出警告，这个装饰器不会预激协程
def spin(msg):  # 无需signal参数来关闭线程
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)  # 代替time.sleep(.1)，这样的休眠不会阻塞事件循环
        except asyncio.CancelledError:  # spin函数苏醒后抛出asyncio.CancelledError异常，其原因是发出了取消请求，因此退出循环
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():  # 协程，在用休眠假装进行I/O操作时，使用yield from继续执行事件循环
    yield from asyncio.sleep(3)  # 把控制权交给主循环，在休眠结束后恢复这个协程
    return 42


@asyncio.coroutine
def supervisor():  # 也是协程，可以用yield from驱动slow_function函数
    spinner = asyncio.ensure_future(spin('thinking!'))  # asyncio.ensure_future()函数排定spin协程的运行时间，使用一个Task对象包装spin协程，并立即返回
    print('spinner object:', spinner)  # 显示Task对象
    result = yield from slow_function()  # 驱动slow_function函数，结束后获取返回值。同时，事件循环继续运行，因为slow_function最后使用yield from asyncio.sleep(3)表达式把控制权交回给了主循环
    spinner.cancel()  # Task对象可以取消，取消后会在协程当前暂停的yield处抛出asyncio.CannelledError异常，协程可以捕获这个异常，也可以延迟取消，甚至拒绝取消
    return result


def main():
    loop = asyncio.get_event_loop()  # 获取事件循环的引用
    result = loop.run_until_complete(supervisor())  # 驱动supervisor协程，让它运行完毕，这个协程的返回值是这次调用的返回值
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
    
# 运行方式为：
# python3 spinner_asyncio.py
'''


''' 对比两个supervisor函数
# 线程版supervisor函数
def supervisor():  # 这个函数设置从属线程，显示线程对象，运行耗时的计算，最后杀死线程
    signal = Signal()
    spinner = threading.Thread(target=spain, args=('thinking!', signal))
    print('spinner object:', spinner)  # 显示从属线程对象
    spinner.start()  # 启动从属线程
    result = slow_function()  # 运行slow_function函数，阻塞主线程，同时，从属线程以动画形式显示旋转指针
    signal.go = False  # 改变signal状态，这回终止spin函数中的那个for循环
    spinner.join()  # 等待spinner线程结束
    return result

# 异步版supervisor协程
@asyncio.coroutine
def supervisor():  # 也是协程，可以用yield from驱动slow_function函数
    spinner = asyncio.ensure_future(spin('thinking!'))  # asyncio.ensure_future()函数排定spin协程的运行时间，使用一个Task对象包装spin协程，并立即返回
    print('spinner object:', spinner)  # 显示Task对象
    result = yield from slow_function()  # 驱动slow_function函数，结束后获取返回值。同时，事件循环继续运行，因为slow_function最后使用yield from asyncio.sleep(3)表达式把控制权交回给了主循环
    spinner.cancel()  # Task对象可以取消，取消后会在协程当前暂停的yield处抛出asyncio.CannelledError异常，协程可以捕获这个异常，也可以延迟取消，甚至拒绝取消
    return result

主要区别如下：
- asyncio.Task对象差不多与threading.Thread对象等效

'''

