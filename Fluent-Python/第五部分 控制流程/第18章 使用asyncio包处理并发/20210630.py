# asyncio包：这个包使用事件循环驱动的协程实现并发

"""1、线程与协程对比"""
''' 通过线程以动画形式显示文本式旋转指针 spinner_thread.py
import threading
import itertools
import time
import sys

class Signal:  # 定义一个简单的可变对象
    go = True  # go属性用于从外部控制线程


def spain(msg, signal):  # 在单独的线程中运行
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # 无限循环，itertools.cycle用于从指定序列中反复不断的生成元素
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # 关键所在：使用退格符（\x08）把光标移回来，原理上相当于 len(status) 长度的\b退格键，覆盖了原来的 Len(status) 长度字符，退格符相当于键盘上的backspace
        time.sleep(.1)
        if not signal.go:  # 如果go的属性不是true了跳出循环
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



