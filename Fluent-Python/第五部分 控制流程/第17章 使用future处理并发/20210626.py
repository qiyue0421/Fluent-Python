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

