# 基于asyncio和aiohttp实现的HTTP并发客户端，演示如何处理错误，以及集成进度条
import asyncio
import aiohttp
import collections
from aiohttp import web
import tqdm
from flags2_common import main, HTTPStatus, Result, save_flag

# 默认设为较小的值，防止远程网站出错
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):  # 自定义的异常用于包装其他HTTP或网络异常，并获取country_code，以便报告错误
    def __init__(self, country_code):
        self.country_code = country_code


@asyncio.coroutine
def get_flag(base_url, cc):  # 协程有三种返回结果：返回下载得到的图像；HTTP响应码为404时，抛出web.HTTPNotFound异常；返回其他HTTP状态码时，抛出aiohttp.HttpProcessingError异常
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        image = yield from resp.read()
        return image
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
            code=resp.status, message=resp.reason,
            headers=resp.headers)


@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):  # semaphore参数是asyncio.Semaphore类的实例，Semaphore类是同步装置，用于限制并发请求数量
    try:
        with (yield from semaphore):  # 在yield from表达式中把semaphore当成上下文管理器使用，防止阻塞整个系统：如果semaphore计数器的值是所允许的最大值，只有这个协程会阻塞
            image = yield from get_flag(base_url, cc)  # 退出这个with语句后，semaphore计数器的值会递减，解除阻塞可能在等待同一个semaphore对象的其他协程实例
    except web.HTTPNotFound:  # 如果没有找到国旗，设置Result的状态
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:  # 其他异常当作FetchError抛出，传入国家代码
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)


@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)  # 创建一个asyncio.Semaphore实例，最多允许激活concur_req个使用这个计数器的协程
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in sorted(cc_list)]  # 多从调用download_one协程，创建一个协程对象列表
    to_do_iter = asyncio.as_completed(to_do)  # 获取一个迭代器，这个迭代器会在future运行结束后返回future
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:  # 迭代运行结束的future
        try:
            res = yield from future  # 获取asyncio.Future对象的结果，最简单的方法是使用yield from，而不是调用future.result()方法
        except FetchError as exc:  # download_one函数抛出的各个异常都包装在FetchError对象里，并且链接原来的异常
            country_code = exc.country_code  # 从FetchError异常中获取错误发生时的国家代码
            try:
                error_msg = exc.__cause__.args[0]  # 尝试从原来的异常（__cause__）中获取错误消息
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__  # 如果在原来的异常中找不到错误消息，使用所链接异常的类名作为错误消息
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status
        counter[status] += 1  # 记录结果
    return counter  # 返回计数器


def download_many(cc_list, base_url, verbose, concur_req):  # 实例化downloader_coro协程
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)  # 通过run_until_complete方法把它传给事件循环
    loop.close()  # 所有工作做完后，关闭事件循环，返回counts
    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
