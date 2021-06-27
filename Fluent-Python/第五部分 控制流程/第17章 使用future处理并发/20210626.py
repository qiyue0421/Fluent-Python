"""1、示例：网络下载的三种风格"""
''' 依序下载的脚本 '''
import os
import time
import sys
import requests

POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'

def save_flag(img, filename):  # 把img（字节序列）保存到DEST_DIR目录中，命名为filename
    pass
    # path = os.path.join(DEST_DIR, filename)
    # with open(path, 'wb') as fp:
    #     fp.write(img)

def get_flag(cc):  # 构建URL，然后下载图像，返回响应中的二进制内容
    # noinspection PyStringFormat
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

def show(text):  # 显示一个字符串，然后刷新sys.stdout，这样能在一行消息中看到进度（默认换行才会刷新stdout缓冲）
    print(text, end=' ')
    sys.stdout.flush()

def download_many(cc_list):  # 下载程序
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
    return len(cc_list)

def main(download_many):  # 运行并报告download_many函数的耗时
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags download in {:.2f}s'
    print(msg.format(count, elapsed))


main(download_many)
# BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
# 20 flags download in 19.87s


''' 使用concurrent.futures模块下载 '''
# concurrent.futures模块的主要特色是ThreadPoolExecutor和ProcessPoolExecutor类，这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护着一个工作线程或进程池，以及要执行的任务队列

from concurrent import futures

MAX_WORKERS = 20  # 设定ThreadPoolExecutor类最多使用几个线程

def download_one(cc):  # 下载一个图像的函数，这是在各个线程中执行的函数
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # 设定工作线程数：使用允许的最大值与要处理的数量之间较小的那个值，以免创建多余的线程
    with futures.ThreadPoolExecutor(workers) as executor:  # 使用工作线程数实例化ThreadPoolExecutor类；executor.__exit__方法会调用executor.shutdown(wait=True)方法，它会在所有线程都执行完毕前阻塞线程
        res = executor.map(download_one, sorted(cc_list))  # map方法返回一个生成器，因此可以迭代，获取各个函数返回的值
    return len(list(res))  # 返回获取的结果数量；如果有线程抛出异常，异常会在这里抛出，这与隐式调用next()函数从迭代器中获取相应的返回值一样

main(download_many)  # 调用main函数，传入download_many函数的增强版
# EG CN NG FR IN ID IR US PH TR VN ET JP BR DE CD MX BD RU PK
# 20 flags download in 1.07s


"""2、阻塞型I/O和GIL"""
''' GIL
CPython解释器本身就不是线程安全的，因此有全局解释器锁（GIL），一次只允许使用一个线程执行Python字节码。因此，一个Python进程通常不能同时使用多个CPU核心。

编写Python代码时无法控制GIL，不过执行耗时的任务时，可以使用一个内置的函数或一个使用C语言编写的扩展释放GIL。然而，标准库中所有执行阻塞型I/O操作的函数，在等待操作系统返回结果时都会释放GIL，允许其他线程运行。
这意味着在Python语言这个层次上可以使用多线程，而I/O密集型Python程序能从中收益：一个Python线程等待网络响应时，阻塞型I/O函数会释放GIL，再运行一个线程
'''


"""3、使用concurrent.futures模块启动进程"""
''' concurrent.futures————实现的是真正的并行计算
ProcessPoolExecutor：CPU密集型作业，实现了通用Executor接口，__init__方法的max_workers参数是可选的，而且大多数情况下不使用，默认值是os.cpu_count()函数返回的CPU数量
ThreadPoolExecutor：I/O密集型作业，实现了通用Executor接口，__init__方法需要max_workers参数，指定线程池中线程的数量

def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor: 

def download_many(cc_list):
    with futures.ProcessPoolExecutor() as executor: 
'''


"""4、实验Executor.map方法————并发运行多个可调用的对象"""
from time import sleep, strftime
from concurrent import futures

def display(*args):  # 打印传入的参数，并加上固定格式的时间戳
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))  # 使用制表符缩进，缩进的量由n的值确定
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  # 创建ThreadPoolExecutor实例，有3个线程
    results = executor.map(loiter, range(5))  # 把5个任务交给executor（因为只有3个线程，所以只有3个任务立即开始），这是非阻塞调用
    display('results:', results)  # 立即显示调用executor.map方法的结果：一个生成器
    display('Waiting for individual results:')
    for i, result in enumerate(results):  # enumerate函数会隐式调用next(results)，这个函数又会在（内部）表示第一个任务（loiter(0)）的_f future上调用_f.result()方法。result方法会阻塞，直到future运行结束，因此这个循环每次迭代时都要等待下一个结果做好准备
        display('result {}: {}'.format(i, result))

main()
''' 运行过程：
[15:25:41] Script starting.  # 41秒开始
[15:25:41] loiter(0): doing nothing for 0s...  # loiter(0)开始运行
[15:25:41] loiter(0): done.  # 甚至会在第二个线程开始前运行完成
[15:25:41] 	loiter(1): doing nothing for 1s...  # loiter(1)和loiter(2)立即开始，可以并发三个线程
[15:25:41] 		loiter(2): doing nothing for 2s...
[15:25:41] results: <generator object Executor.map.<locals>.result_iterator at 0x0000024E4F638DE0>  # executor.map返回的是生成器
[15:25:41] Waiting for individual results:
[15:25:41] 			loiter(3): doing nothing for 3s...  # 因为loiter(0)已经运行完了，第一个职程可以启动第四个线程

[15:25:41] result 0: 0  # 此时执行过程可能阻塞，具体情况取决于传给loiter函数的参数：results生成器的__next__方法必须等待第一个future运行结束。此时不会阻塞，因为loiter(0)在循环开始前结束，此时是41秒
[15:25:42] 	loiter(1): done.  # 42秒时，loiter(1)运行完毕，这个线程闲置，可以开始运行loiter(4)
[15:25:42] 				loiter(4): doing nothing for 4s... 
[15:25:42] result 1: 10  # 现在for循环会阻塞，等待loiter(2)的结果

[15:25:43] 		loiter(2): done.  # loiter(2)运行结束，显示结果
[15:25:43] result 2: 20    # 现在for循环会阻塞，等待loiter(3)的结果
[15:25:44] 			loiter(3): done.
[15:25:44] result 3: 30
[15:25:46] 				loiter(4): done.
[15:25:46] result 4: 40
'''
