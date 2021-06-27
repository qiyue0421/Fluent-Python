# 基于futures.ThreadPoolExecutor类实现的HTTP并发客户端，演示如何处理错误，以及集成进度条
import collections
import requests
import tqdm

from concurrent import futures
from flags2_common import main, HTTPStatue
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000

def download_many(cc_list, base_url, verbose, concur_req):
    pass


