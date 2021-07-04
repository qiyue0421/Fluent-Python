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
- Task对象用于驱动协程，Thread对象用于调用可调用的对象
- Task对象不由自己动手实例化，而是通过把协程传给asyncio.ensure_future(...)函数或loop.create_task(...)方法获取
- 获取的Task对象已经排定了运行时间（例如，由asyncio.ensure_future函数排定）；Thread实例则必须调用start方法，明确告知让它运行
- 在线程版supervisor函数中，slow_function函数是普通的函数，直接由线程调用。在异步版supervisor函数中，slow_function函数是协程，由yield from驱动
- 没有API能从外部终止线程，因为线程随时可能被中断，导致系统处于无效状态。如果想终止任务，可以使用Task.cancel()实例方法，在协程内部抛出CancelledError异常。协程可以在暂停的yield处捕获这个异常，处理终止请求
- supervisor协程必须在main函数中由loop.run_until_complete方法执行


如果使用线程做过重要的编程，就知道写出程序有多么困难，因为调度程序任何时候都能中断线程。必须记住保留锁，去保护程序中的重要部分，防止多步操作在执行的过程中中断，防止数据处于无效状态。
而协程默认会做好全方位保护，以防止中断。必须显式产出才能让程序的余下部分运行。对协程来说，无需保留锁，在多个线程之间同步操作，协程自身就会同步，因为在任意时刻只有一个协程运行。要想交出控制权，可以使用yield或yield from把控制权交还调度程序
'''


"""2、使用asyncio和aiohttp包下载"""
# 从Python3.4起，asyncio包只直接支持TCP和UDP。如果想使用HTTP或其他协程，那么要借助第三方包。当下，使用asyncio实现HTTP客户端和服务器时，使用的似乎都是aiohttp包

''' 使用asyncio和aiohttp包实现的异步下载脚本：
import asyncio
import aiohttp
import os
import sys
import time

BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'
POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()


def save_flag(img, filename):  # 把img（字节序列）保存到DEST_DIR目录中，命名为filename
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def show(text):  # 显示一个字符串，然后刷新sys.stdout，这样能在一行消息中看到进度（默认换行才会刷新stdout缓冲）
    print(text, end=' ')
    sys.stdout.flush()


@asyncio.coroutine  # 协程使用@asyncio.coroutine装饰
def get_flag(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)  # 阻塞的操作使用协程实现，客户代码通过yield from把职责委托给协程，以便异步运行协程
    image = yield from resp.read()  # 读取响应内容是一项单独的异步操作
    return image


@asyncio.coroutine
def download_one(cc):  # 也是协程
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()  # 获取事件循环底层实现的引用
    to_do = [download_one(cc) for cc in sorted(cc_list)]  # 调用download_one函数获取各个国旗，然后构建一个协程对象列表
    wait_coro = asyncio.wait(to_do)  # wait是一个协程，等传给它的所有协程运行完毕后结束
    res, _ = loop.run_until_complete(wait_coro)  # 驱动协程，执行事件循环，直到wait_coro运行结束；事件循环运行的过程中，这个脚本会在这里阻塞
    loop.close()  # 关闭事件循环
    return len(res)


def main(download_many):  # 运行并报告download_many函数的耗时
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags download in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
'''

''' 原理
asyncio.wait(...)协程的参数是一个由future或协程构成的可迭代对象；wait会分别把各个协程包装进一个Task对象。最终的结果是，wait处理的所有对象都通过某种方式变成Future类的实例。
wait是协程函数，因此返回的是一个协程或生成器对象；wait_coro变量中存储的正是这种对象

loop.run_until_complete方法的参数是一个future或协程。如果是协程，run_until_complete方法与wait函数一样，把协程包装进一个Task对象中。协程、future和任务都能由yield from驱动，这正是run_until_complete方法对wait函数返回的
wait_coro对象所做的事。wait_coro运行结束后返回一个元组，第一个元素是一系列结束的future，第二个元素是一系列未结束的future

以这个协程为例：
@asyncio.coroutine
def get_flag(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    image = yield from resp.read()
    return image

假设上述函数与下述函数的作用相同，只不过协程版从不阻塞
def get_flag(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

yield from foo 句法能防止阻塞，是因为当前协程（即包含yield from代码的委派生成器）暂停后，控制权回到事件循环手中，再去驱动其他协程；foo future或协程运行完毕后，把结果返回给暂停的协程，将其恢复
- 使用yield from链接的多个协程最终必须由不是协程的调用方驱动，调用方显式或隐式（例如在for循环中）在最外层委派生成器上调用next(...)函数或.send(...)方法
- 链条中最内层的子生成器必须是简单的生成器（只使用yield）或可迭代的对象
- 编写的协程链条始终通过把最外层委派生成器传给asyncio包API中的某个函数（如loop.run_until_complete(...)）驱动。也就是说，使用asyncio包时，编写的代码不通过调用next(...)函数或.send(...)方法驱动协程————这一点由asyncio包实现的事件循环去做
- 编写的协程链条最终通过yield from把职责委托给asyncio包中的某个协程函数或协程方法（yield from asyncio.sleep(...)），或者其他库中实现高层协议的协程（resp = yield from aiohttp.request('GET', url)）。
也就是说，最内层的子生成器是库中真正执行I/O操作的函数，而不是自己编写的函数

概况起来就是：使用asyncio包时，我们编写的异步代码中包含由asyncio本身驱动的协程（即委派生成器），而生成器最终把职责委托给asyncio包或第三方库（如aiohttp）中的协程。这种处理方式相当于架起了管道，
让asyncio事件循环（通过自己编写的协程）驱动执行低层异步I/O操作的库函数
'''
