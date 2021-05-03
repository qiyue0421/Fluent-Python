"""9、用bisect来管理已排序的序列"""
# bisect模块包含两个主要函数，bisect和insort，两个函数都利用二分查找算法来在有序序列中查找或插入元素

# 用bisect来搜索
# bisect(haystack, needle)在haystack里搜索needle的位置，该位置满足的条件是——把needle插入这个位置之后，haystack还能保持升序，haystack必须是一个有序的序列
import bisect
import sys

HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLE = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

ROW_FMT = '{0:2d} @ {第5章 一等函数:2d}    {2}{0:<2d}'


def demo(bisect_fn):
    for needle in reversed(NEEDLE):
        position = bisect_fn(HAYSTACK, needle)  # 用特定的bisect函数来计算元素应该出现的位置
        offset = position * '  |'  # 利用该位置计算需要几个分隔符号
        print(ROW_FMT.format(needle, position, offset))  # 打印出元素及其应该出现的位置


if __name__ == '__main__':
    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left  # 相等元素的前面
    else:
        bisect_fn = bisect.bisect  # 相等元素的后面

    print('DEMO:', bisect_fn.__name__)
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)


# bisect还可以用来建立一个用数字作为索引的查询表格
def grade(socre, breakpoints=(60, 70, 80, 90), grades='FDCBA'):  # 根据一个分数，找出它所对应的成绩
    i = bisect.bisect(breakpoints, socre)
    return grades[i]


print([grade(score) for score in [33, 99, 77, 70, 89, 90, 100]])

# 用bisect.insort插入新元素，insort(seq, item)把变量item插入到序列seq中，并能保持seq的升序顺序。
import random

SIZE = 7
random.seed(1729)  # 当seed()有参数时，每次生成的随机数是一样的

my_lists = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_lists, new_item)
    print('%2d ->' % new_item, my_lists)


"""10、当列表不是首选时"""
# 数组
# 如果需要一个只包含数字的列表，那么array.array比list更高效，数组支持所有跟可变序列有关的操作，包括.pop、.insert和.extend；另外，数组还提供从文件读取和存入文件的更快的方法，如：
# .frombytes和.tofile。创建数组需要一个类型码，这个类型码用来表示在底层的C语言应该存放怎样的数据类型，例如b类型码代表的是有符号的字符，因此arrag('b')创建出的数组就只能存放一个字节
# 大小的整数，范围从-128到127
from array import array
from random import random
floats = array('d', (random() for i in range(10**7)))  # 双精度浮点数组，类型码为'd'
print(floats[-1])
fp = open('floats.bin', 'wb')
floats.tofile(fp)  # 存入一个二进制文件
fp.close()

floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)  # 把1000万个浮点数从二进制文件中读取出来，只需要0.1秒
fp.close()
print(floats2[-1])
print(floats == floats2)


# 内存视图
# memoryview是一个内置类，它能让用户在不复制内容的情况下操作同一个数组的不同切片，memoryview.cast能用不同的方式读写同一块内存数据，而且内容字节不会随意移动
numbers = array('h', [-2, -1, 0, 1, 2])  # 5个短整型有符号整数的数组（类型码为'h'）
memv = memoryview(numbers)  # 创建一个memoryview，memv里的5个元素跟数组里的没有区别
print(len(memv))
print(memv[0])

memv_oct = memv.cast('B')  # 创建一个memv_oct，将memv的内容转换成'B'类型，即无符号字符
print(memv_oct.tolist())  # 以列表的形式查看memv_oct的内容
memv_oct[5] = 4  # 把位于位置5的字节赋值成4
print(numbers)  # 把占2个字节的整数高位字节改成了4，所以这个有符号整数的值就变成了1024


# NumPy和SciPy
# NumPy实现了多维同质数组和矩阵，这些数据结构不但能处理数字，还能存放其他由用户定义的记录
# SciPy是基于NumPy的另一个库，它提供了很多跟科学计算有关的算法，专门为线性代数、数值积分和统计学而设计

# 对numpy.ndarray的行和列进行基本操作
import numpy

a = numpy.arange(12)  # 新建一个0~11的整数的numpy.ndarray
print(a, type(a))
print(a.shape)  # 查看数组维度，是一个一维的含有12个元素的数组

a.shape = 3, 4  # 将数组变成二维的
print(a)
print(a[2])  # 打印第二行
print(a[2, 1])  # 打印第二行第一列
print(a[:, 1])  # 打印第一列
print(a.transpose())  # 交换行列，得到一个新的数组


# 双向队列和其他形式的队列
# collections.deque类（双向队列）是一个线程安全、可以快速从两端添加或者删除元素的数据类型
# 双向队列有一些缺陷，从队列中间删除元素的操作会慢一些，因为它只对在头尾的操作进行了优化
from collections import deque

dq = deque(range(10), maxlen=10)  # maxlen参数是一个可选参数，代表这个队列可以容纳的元素的数量，一旦设定就不能修改了
print(dq)  # deque([0, 第5章 一等函数, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)

dq.rotate(3)  # 循环右移3位
print(dq)  # deque([7, 8, 9, 0, 第5章 一等函数, 2, 3, 4, 5, 6], maxlen=10)

dq.rotate(-4)  # 循环左移4位
print(dq)  # deque([第5章 一等函数, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)

dq.appendleft(-1)  # 头部添加-第5章 一等函数，当试图对一个已满的队列头部添加元素时，它的尾部元素会被删除掉
print(dq)  # deque([-第5章 一等函数, 第5章 一等函数, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)

dq.extend([11, 22, 33])  # 在尾部添加3个元素，头部元素会被挤掉
print(dq)  # deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)

dq.extendleft([10, 20, 30, 40])  # 把迭代器里的元素逐个添加到双向队列的左边，元素会逆序出现在队列里
print(dq)  # deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)











