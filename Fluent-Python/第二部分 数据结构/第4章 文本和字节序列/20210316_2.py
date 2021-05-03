"""6、为了正确比较而规范化Unicode字符串"""
# 因为Unicode有组合字符（变音符号和附加到前一个字符上的记号，打印时作为一个整体），所以字符串比较起来很复杂
s1 = 'café'  # 4个码位
s2 = 'cafe\u0301'  # 5个码位，U+0301是COMBINING ACUTE ACCENT，加在”e“后面得到”é“
print(s1, s2)  # 在Unicode标准中，'é'和'e\u0301'这样的序列叫做”标准等价物“，应用程序应该把它们视作相同的字符
print(len(s1), len(s2))
print(s1 == s2)  # python看到的是不同的码位序列，因此判定二者不相等

# 这个问题的解决方案是使用 unicodedata.normalize 函数提供的Unicode规范化，这个函数的第一个参数是这4个字符串中的一个：'NFC'、'NFD'、'NFKC'和'NFKD'
# 'NFC'使用最少的码位构成等价的字符串，而'NFD'把组合字符分解成基字符和单独的组合字符，这两种规范化方法都能让比较行为符合预期
from unicodedata import normalize

print(len(normalize('NFC', s1)), len(normalize('NFC', s2)))
print(len(normalize('NFD', s1)), len(normalize('NFD', s2)))
print(normalize('NFC', s1) == normalize('NFC', s2))
print(normalize('NFD', s2) == normalize('NFD', s2))


# 大小写折叠：把所有文本变成小写，再做些其他转换，这个功能由 str.casefold()方法支持（Python 3.3新增）
# 对于只包含latin1字符的字符串s，s.casefold()得到的结果与s.lower()一样
print('A'.casefold() == 'a'.casefold())


# 规范化文本匹配使用函数：如果要处理多语言文本，工具箱中应该有该函数
from unicodedata import normalize


def nfc_equal(str1, str2):  # 处理Unicode规范化
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):  # 处理大小写折叠
    return normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold()


''' 极端”规范化“：去掉变音符号 '''
import unicodedata


def shave_marks(text):
    norm_text = unicodedata.normalize('NFD', text)  # 采用'NFD'把所有字符分解成基字符和组合记号
    shaved = ''.join(c for c in norm_text if not unicodedata.combining(c))  # 过滤掉所有组合记号
    return unicodedata.normalize('NFC', shaved)  # 重组所有字符
