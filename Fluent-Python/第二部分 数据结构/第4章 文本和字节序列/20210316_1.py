"""4、了解编解码问题"""
# Unicode异常类型主要分为两种：
# UnicodeEncodeError异常：把字符串转换成二进制序列时，如果目标编码种没有定义某个字符，那就会抛出该异常，除非把errors参数传给编码方法或函数，对错误进行特殊处理
# UnicodeDecodeError异常，把二进制序列转换成字符串时，遇到无法转换的字节序列时抛出该异常

# 处理UnicodeEncodeError
city = 'São Paulo'
print(city.encode('utf-8'))  # utf_? 编码能够处理任何字符串
print(city.encode('utf-16'))
# print(city.encode('cp437'))  # 报错，因为cp437无法编码其中的一个字符，默认抛出异常UnicodeEncodeError
print(city.encode('cp437', errors='ignore'))  # 跳过无法编码的字符（不推荐）
print(city.encode('cp437', errors='replace'))  # 将未识别的字符替换为 "?"
print(city.encode('cp437', errors='xmlcharrefreplace'))  # 把无法编码的字符替换成XML实体

# 处理UnicodeDecodeError
octets = b'Montr\xe9al'  # 该字节序列使用latin1编码的 'Montréal'
print(octets.decode('cp1252'))  # 使用 'cp1252' 解码，因为它是latin1的有效超集
print(octets.decode('iso8859_7'))  # ISO-8859-7用于编码希腊文，因此无法正确解释其中某个字节，而且没有抛出错误
print(octets.decode('koi8_r'))  # KOI8-R用于编码俄文
# print(octets.decode('utf-8'))  # 报错，检测到不是有效的utf-8字符，排除异常
print(octets.decode('utf-8', errors='replace'))  # 使用 'replace' 错误处理方式，\xe9替换成了 "�"(码位是U+FFFD)，这是官方指定的替换字符，表示未知字符

# 使用预期之外的编码加载模块时抛出的 SyntaxError
# Python3默认使用UTF-8编码，Python2则默认使用ASCII。如果加载的.py模块中包含UTF-8之外的数据，而且没有声明编码，会得到SyntaxError异常，为了修正这个问题，
# 可以在文件顶部添加一个神奇的coding注释
# coding: cp1252

print('Olá, mundo!')  # “你好，世界”的葡萄牙语班


''' BOM：有用的鬼符 '''
u16 = 'El Niño'.encode('utf-16')  # UTF-16编码的序列开头有几个额外的字节
print(u16)  # b'\xff\xfe'，即BOM——字节序标记，指明编码时使用Intel CPU的小字节序
# b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'

# 在小字节序设备中，各个码位的最低有效字节在前面：字母'E'的码位是U+0045（十进制数69），在字节偏移的第2位和第3位编码为69和0
print(list(u16))  # [255, 254, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]

# 在大字节序CPU中，编码顺序是相反的；'E'的编码为0和69。为了避免混淆，UTF-16编码在要编码的文本前面加上特殊的不可见字符（U+FEFF）。在小字节序系统中，这个字符编码为b'\xff\xfe'，
# 十进制数为(255, 254)。

# UTF-16有两个变种：UTF-16LE，显式指明使用小字节序；UTF-16BE，显式指明使用大字节序。如果使用这两个变种，不会生成BOM
u16le = 'El Niño'.encode('utf-16le')
u16be = 'El Niño'.encode('utf-16be')
print(list(u16le))  # [69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]
print(list(u16be))  # [0, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111]


"""5、处理文本文件"""
# 处理文本的最佳实践是”Unicode三明治“。意思是，要尽早把输入（例如读取文件时）的字节序列解码成字符串，这种三明治的”肉片“是程序的业务逻辑，在这里只能处理字符串对象。在其他处理程序中，
# 一定不能编码或解码。对输出来说，则要尽量晚的把字符串编码成字节序列。

open('cafe.txt', 'w', encoding='utf-8').write('café')  # 内置open函数会在读取文件时做必要的解码
readlines = open('cafe.txt').read()  # 读取文件时没有指定编码，使用的是系统默认的编码（Windows 1252）
print(readlines)  # cafÃ©

fp = open('cafe.txt', 'w', encoding='utf-8')  # 默认情况下，open函数采用文本模式，返回一个TextIOWrapper对象
print(fp)  # <_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf-8'>
# 在TextIOWrapper对象上调用write方法返回写入的Unicode字符数
fp.write('café')  # 4
fp.close()

import os
# os.stat报告文件中有5个字节
print(os.stat('cafe.txt').st_size)  # 5

fp2 = open('cafe.txt')  # 打开文本文件时没有显式指定编码，返回一个TextIOWrapper对象，编码是区域设置中的默认值
print(fp2)  # <_io.TextIOWrapper name='cafe.txt' mode='r' encoding='cp936'>，注意此处的编码是cp936
print(fp2.encoding)  # cp936
print(fp2.read())  # cafÃ©

fp3 = open('cafe.txt', encoding='utf-8')  # 使用正确的编码打开文本文件
print(fp3)  # <_io.TextIOWrapper name='cafe.txt' mode='r' encoding='utf-8'>
print(fp3.read())  # café

fp4 = open('cafe.txt', 'rb')  # 'rb'标志指明在二进制模式中读取文件
print(fp4)  # <_io.BufferedReader name='cafe.txt'>，返回的是BufferedReader对象，而不是TextIOWrapper对象
print(fp4.read())  # b'caf\xc3\xa9'


# 编码默认值：一团糟
import sys
import locale

expressions = '''
    locale.getpreferredencoding()
    type(my_file)
    my_file.encoding
    sys.stdout.isatty()
    sys.stdout.encoding
    sys.stdin.isatty()
    sys.stdin.encoding
    sys.stderr.isatty()
    sys.stderr.encoding
    sys.getdefaultencoding()
    sys.getfilesystemencoding()
'''

my_file = open('dummy', 'w')

for expression in expressions.split():
    value = eval(expression)  # 内置函数eval()执行字符串表达式，并返回表达式的值
    print(expression.rjust(30), '->', repr(value))  # 内置函数repr()将对象转化为供解释器读取的形式
# 综上，locale.getpreferredencoding() 返回的编码是最重要的：这是打开文件的默认编码，也是重定向到文件的 sys.stdout/stdin/stderr 的默认编码
