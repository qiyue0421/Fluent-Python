"""第5章 一等函数、字符问题"""
# “字符串的概念”——一个字符串是一个字符序列，“字符”的最佳定义是Unicode字符，因此从python3的str对象中获取的元素是Unicode字符。
# Unicode标准把字符的标识和具体的字节表述进行了区分：
# ①、字符的标识，即码位，是0~1114111的数字（十进制），在Unicode标准中以4~6个十六进制数字表示，而且加前缀“U+”。
'''
例如，字母A的码位是U+0041，欧元符号的码位是U+20AC，
'''

# ②、字符的具体表述取决于所用的编码。编码是在码位和字节序列之间转换时使用的算法。把码位转换成字节序列的过程是编码；把字节序列转换成码位的过程是解码
'''
在UTF-8编码中，A(U+0041)的码位编码成单个字节 \x41，而在UTF-16LE编码中，编码成两个字节 \x41\x00；欧元符号(u+20AC)在UTF-8编码中是三个字节——\xe2\x82\xac，
而在UTF-16LE中编码成两个字节：\xac\x20
'''

s = 'café'
print(len(s))  # 有4个Unicode字符
b = s.encode('utf8')  # 使用UTF-8把str对象编码成bytes对象
print(b)  # 字节类型bytes字面量以b开头
print(len(b))  # 字节序列b有5个字节（最后一位的码位编码是两个字节）
print(b.decode('utf8'))  # 使用UTF-8把bytes对象解码成str对象


"""2、字节概要"""
# python内置了两种基本的二进制序列类型：Python 3引入的不可变bytes类型和Python 2.6添加的可变bytearray类型。bytes或bytearray对象的各个元素是介于0~255之间的整数，然而二进制
# 序列的切片始终是同一类型的二进制序列
cafe = bytes('café', encoding='utf_8')  # bytes对象可以从str对象使用给定的编码构建
print(cafe)
print(cafe[0])  # 各个元素都是range(256)内的整数
print(cafe[:1])  # bytes对象的切片还是bytes对象，即使是只有一个字节的切片

cafe_arr = bytearray(cafe)
print(cafe_arr)  # bytearray对象没有字面量句法，而是以bytearray()和字节序列字面量参数的形式显示
print(cafe_arr[-1:])  # bytearray对象的切片还是bytearray对象

''' 字节值的三种不同的显示方式 
第5章 一等函数）、可打印的ASCII范围内的字节（从空格到~），使用ASCII字符本身
2）、制表符、换行符、回车符和 \ 对应的字节，使用转义序列 \t、\n、\r和\\
3）、其他字节的值，使用十六进制转义序列，例如，\x00是空字节
'''

''' 构建bytes或bytearray 
第5章 一等函数）、一个str对象和一个encoding关键字参数
2）、一个可迭代对象，提供0~255之间的数值
3）、一个整数，使用空字节创建对应长度的二进制序列（该方法已过时，在python 3.6中已删除）
4）、一个实现了缓冲协议的对象（如bytes、bytearray、memoryview、array.array）；此时，把源对象中的字节序列复制到新建的二进制序列中
'''

# 使用缓冲类对象构建二进制序列，涉及类型转换
import array

numbers = array.array('h', [-2, -1, 0, 1, 2])  # 指定类型码代码 h，创建一个短整数（16位）数组
octets = bytes(numbers)  # numbers字节序列的副本
print(octets)


# 结构体和内存视图
# struct模块提供了一些函数，把打包的字节序列转换成不同类型字段组成的元组，该模块能处理bytes、bytearray和memoryview对象
# 使用memoryview和struct查看一个GIF图像的首部
import struct

fmt = '<3s3sHH'  # 结构体的格式：< 是小字节序，3s3s是两个3字节序列，HH是两个16位二进制整数
with open('filter.gif', 'rb') as fp:
    img = memoryview(fp.read())  # 使用内存中的文件内容创建一个memoryview对象

header = img[:10]  # 用切片操作再获得一个memoryview对象，并且不会复制字节序列
print(header)
print(bytes(header))  # 转换为字节序列——便于显示

struct_msg = struct.unpack(fmt, header)  # 拆包memoryview对象，得到一个元组。元组中包含类型、版本、宽度和高度
print(struct_msg)  # (b'GIF', b'89a', 800, 600)

del header  # 删除引用，释放memoryview实例所占的内存
del img


"""3、基本的编解码器"""
# Python自带了超过100种编解码器，用于在文本和字节之间相互转换，每个编解码器都有一个名称，如'utf_8'，而且经常有几个别名，如'utf8'、utf-8'和'U8'
for codec in ['latin_1', 'utf_8', 'utf_16']:
    print(codec, 'El Niño'.encode(codec), sep='\t')

''' 一些典型的编码 '''
# latin1(即iso8859_1)
# cp1252
# cp437
# gb2312
# utf-8
# utf-16le
