# 基于futures.ThreadPoolExecutor类实现的HTTP并发客户端，演示如何处理错误，以及集成进度条
import collections
import requests
import tqdm  # 导入显示进度条的库

from concurrent import futures
from flags2_common import main, HTTPStatus
from flags2_sequential import download_one  # 重用flags2_sequential模块的download_one函数

DEFAULT_CONCUR_REQ = 30  # 没有在命令行中指定 -m/--max_req 选项，使用这个值作为并发请求数的最大值，也就是线程池的大小
MAX_CONCUR_REQ = 1000  # 安全措施，并发请求数无论如何都不会超过这个数

def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:  # concur_req的值为以下三个值中最小的那个值：MAX_CONCUR_REQ、cc_list的长度、-m/--max_req命令行选项的值
        to_do_map = {}  # 将future实例映射到相应的国家代码上，在处理错误时使用
        for cc in sorted(cc_list):  # 按字母顺序迭代国家代码列表i
            future = executor.submit(download_one, cc, base_url, verbose)  # 每次调用executor.submit方法排定一个可调用对象的执行时间，然后返回一个Future实例，第一个参数是可调用的对象，其余参数是传给可调用对象的参数
            to_do_map[future] = cc  # 将返回的future和国家代码存储在字典中
        done_iter = futures.as_completed(to_do_map)  # 返回一个迭代器（包含已经运行结束的future），在future运行结束后产出future
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))  # 显示进度条，传入长度total，tqdm才能预计剩余工作量
        for future in done_iter:  # 迭代运行结束后的future
            try:
                res = future.result()  # 要么返回可调用对象的返回值，要么抛出可调用的对象在执行过程中捕获的异常。这个方法可能阻塞，等待确定结果；不过，这里不会阻塞，因为as_completed函数只返回已经运行结束的future
            except requests.exceptions.HTTPError as exc:  # 处理可能的异常
                error_msg = 'HTTP error {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:  # 如果没有异常，从download_one函数返回的namedtuple中获取status
                error_msg = ''
                status = res.status
            if error_msg:
                status = HTTPStatus.error  # 如果有错误，将局部变量status设置为相应的状态
            counter[status] += 1  # status作为键，增加计数器
            if verbose and error_msg:
                cc = to_do_map[future]
                print('*** Error for {}: {}'.format(cc, error_msg))  # 如果是详细模式而且有错误，显示带有当前国家代码的错误信息
        return counter  # 返回counter，以便main函数能够在最终的报告中显示数量

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
