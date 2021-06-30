# 能正确处理错误，以及显示进度条的HTTP依序下载客户端
import collections
import requests
import tqdm

from flags2_common import HTTPStatus, save_flag, Result, main

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:  # 没有处理错误，当HTTP响应代码不是200时，抛出异常
        resp.raise_for_status()
    return resp.content

def download_one(cc, base_url, verbose=False):  # 负责下载的基本函数
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:  # 捕获异常，这里专门处理HTTP 404错误，其他异常不管
        res = exc.response
        if res.status_code == 404:  # 处理HTTP 404错误
            status = HTTPStatus.not_found
            msg = 'not found'
        else:  # 重新抛出其他异常，向上冒泡传给调用方
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:  # 如果在命令行中设定了 -v/--verbose 选项，显示国家代码和状态消息（即详细模式）
        print(cc, msg)

    return Result(status, cc)  # 返回一个命名元组，其中有个status字段，其值是HTTPStatus.not_found或HTTPStatus.ok

def download_many(cc_list, base_url, verbose, max_req):  # 实现依序下载的download_many函数
    counter = collections.Counter()  # 计数器，用于统计不同的下载状态：HTTPStatus.ok、HTTPStatus.not_found、HTTPStatus.error
    cc_iter = sorted(cc_list)  # 按照顺序排列
    if not verbose:  # 如果不是详细模式，把cc_iter传给tqdm函数，返回一个迭代器，产出cc_iter中的元素，还会显示进度条动画
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:  # 迭代cc_iter
        try:
            res = download_one(cc, base_url, verbose)  # 不断调用download_one函数执行下载
        except requests.exceptions.HTTPError as exc:  # 处理调用download_one函数没有处理并抛出的异常（与HTTP相关）
            error_msg = 'HTTP error {res.status_code} - {res.reason}'
            error_msg = error_msg.format(res=exc.response)
        except requests.exceptions.ConnectionError as exc:  # 处理其他与网络有关的异常，其他异常会终止这个脚本（因为flags2_common.main主函数没有try/except块）
            error_msg = 'Connection error'
        else:  # 如果没有异常，从download_one函数返回的namedtuple中获取status
            error_msg = ''
            status = res.status

        if error_msg:
            status = HTTPStatus.error  # 如果有错误，将局部变量status设置为相应的状态
        counter[status] += 1  # status作为键，增加计数器
        if verbose and error_msg:
            print('*** Error for {}: {}'.format(cc, error_msg))  # 如果是详细模式而且有错误，显示带有当前国家代码的错误信息
    return counter  # 返回counter，以便main函数能够在最终的报告中显示数量

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
