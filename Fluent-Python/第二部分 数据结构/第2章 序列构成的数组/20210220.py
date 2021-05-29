import array
from collections import namedtuple

"""1、内置序列类型概览"""
# python标准库用C实现了丰富的序列类型
# 按照存放数据类型的不同
# 容器序列：list、tuple和collections.deque，这些序列能存放不同类型的数据，实际存放的是它们所包含的任意类型的对象的引用
# 扁平序列：str、bytes、bytearray、memoryview和array.array，这类序列只能容纳一种类型，实际存放的是值而不是引用（一段连续的内存空间）

# 按照能否被修改，序列可分为：
# 可变序列：list、bytearray、array.array、collections.deque和memoryview
# 不可变序列：tuple、str和bytes


"""2、列表推导式"""
# 列表推导式是构建列表的快捷方式，增强可读性
# 使用原则为：只用列表推导来创建新的列表，并且尽量保持简短
symbols = 'qiyue'
codes = [ord(symbol) for symbol in symbols]
print(codes)

# 使用列表推导计算笛卡尔积
# 笛卡尔积：两个或以上的列表中的元素对构成元组，这些元组构建的列表就是笛卡尔积，列表长度等于输入变量的长度的乘积
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
# tshirts = [(color, size) for size in sizes for color in colors]  # 调整从句顺序按照size大小排序
print(tshirts)


"""3、生成器表达式"""
# 生成器表达式遵守了迭代器的协议，可以逐个产出元素，而不是先建立一个完整的列表，然后再把这个列表传递到某个构造函数里，可以节省内存
# 生成器初始化元组
symbols = 'qiyue'
codes = tuple(ord(symbol) for symbol in symbols)
print(codes)

# 生成器初始化数组
print(array.array('I', (ord(symbol) for symbol in symbols)))  # 第一个参数指定了数组中数字的存储方式

for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):  # 生成器会逐个产生元素
    print(tshirt)


"""4、元组"""
# 元组是对数据的记录：元组中的每个元素都存放了记录中一个字段的数据，外加这个字段的位置
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
for passport in sorted(traveler_ids):  # 在迭代过程中，passport被绑定到每个元组上
    print('%s %s' % passport)  # %格式运算符能被匹配到对应的元组元素上

for country, _ in traveler_ids:  # for循环可以分别提取元组里的元素，也叫做拆包。没有用的第二个元素可以赋值给 "_" 占位符
    print(country)

# 元组拆包可以应用到任何可迭代对象上，唯一的硬性要求是：被可迭代对象中的元素数量必须要跟接受这些元素的元组的空挡一致
# *运算符把一个可迭代对象拆开作为函数的参数
t = (20, 8)
quotient, remainder = divmod(*t)
print(quotient, remainder)


# 嵌套元组拆包
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35, 139)),
    ('Delhi NCR', 'IN', 21.935, (28, 77)),
    ('Mexico City', 'MX', 20, (19, -99)),
    ('New York-Newark', 'US', 20, (40, -74)),
    ('Sao Paulo', 'BR', 19, (-23, -46))
]

print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:
    if longitude <= 0:
        print(fmt.format(name, latitude, longitude))


# 具名元组，collections.namedtuple是一个工厂函数，可以用来构建一个带字段名的元组和一个有名字的类
# 创建具名元组需要两个参数，一个是类名，另一个是类的各个字段的名字，后者可以是由数个字符串组成的可迭代对象，或者是由空格分隔开的字段名组成的字符串
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35, 139))
print(tokyo)
print(tokyo.population)  # 通过字段名获取信息
print(tokyo[1])  # 通过字段位置获取信息

print(City._fields)  # _fields属性是一个包含这个类所有字段名称的元组
delhi_data = ('Delhi NCR', 'IN', 21.935, (28, 77))
delhi = City._make(delhi_data)  # make()通过接受一个可迭代对象来生成类的实例，等同于City(*delhi_data)
print(delhi._asdict())  # _asdict()把具名元组的信息以更友好的方式呈现出来


"""5、切片"""
# 在切片和区间操作里不包含区间范围的最后一个元素，这样带来的好处有以下几点：
# ①、当只有最后一个位置信息时，也可以快速看出切片和区间里有几个元素，比如range(3)、my_list[:3]都返回3个元素
# ②、当起止位置信息都可见时，可以快速计算出切片和区间的长度，用后一个数减去第一个下标（stop - start）即可
# ③、可以利用任意一个下标来把序列分割成不重叠的两部分，只要写成 my_list[:x] 和 my_list[:x] 即可

# 对对象进行切片，s[a:b:c]对s在a和b之间以c为间隔取值
s = 'bicycle'
print(s[::3])
print(s[::-1])
print(s[::-2])

# 给切片赋值，如果赋值对象是一个切片，那么赋值语句的右侧必须是个可迭代对象。即便只有单独的一个值，也要把它转换成可迭代的序列
l = [0, 1, 2, 3, 4, 5]
l[2:5] = [100]
print(l)


"""6、对序列使用+和*"""
# 通常+号两侧的序列由相同类型的数据所构成，在拼接的过程中，两个被操作的序列都不会被修改，python会新建一个包含同样类型数据的序列来作为拼接的结果
# 如果想要把一个序列复制几份然后再拼接起来，更快捷的做法是把这个序列乘以一个整数，+和*都遵循这个规律，不修改原有的操作对象，而是构建一个全新的序列
l = [1, 2, 3]
print(l * 5)

# 建立由列表组成的列表——采用列表推导式
board = [["_"] * 3 for i in range(3)]
print(board)
board[1][2] = 'X'
print(board)
'''等同于如下操作
board = []
for i in range(3):
    row = ['_'] * 3  # 每次都新建了一个列表
    board.append(row)
'''

error_board = [["_"] * 3] * 3  # 外边的列表其实包含3个指向同一个列表的引用
print(error_board)
error_board[1][2] = 'O'
print(error_board)
'''等同于如下操作
row = ['_'] * 3
board = []
for i in range(3):
    board.append(row)  # 追加同一个对象(row)3次到board
'''


"""7、序列的增量赋值"""
# 增量赋值运算符+=和*=的表现取决于它们的第一个操作对象
# +=背后的特殊方法是 __iadd__(用于“就地加法”)，但是如果一个类没有实现这个方法的话，python会退一步调用__add__
a = 0
b = 1
a += b  # 如果没有实现__iadd__的话，首先计算a+b，得到一个新对象，然后赋值给a。变量名会不会被关联到新的对象，完全取决于这个类型有没有实现__iadd__方法
print(a)
# 同样的，*=对应的是__imul__方法

# 一个关于+=的谜题：
t = (1, 2, [30, 40])
t[2] += [50, 60]
print(t)
# 结果为：t变成(第5章 一等函数, 2, [30, 40, 50, 60])，并且因为tuple不支持对它的元素赋值，所以会抛出TypeError异常
# 得到启示：不要把可变对象放在元组里面；增量赋值不是一个原子操作（虽然抛出了异常，但是还是完成了操作）


"""8、list.sort方法和内置函数sorted"""
# list.sort方法会就地排序列表，也就是说不会把原列表复制一份，返回值为None（Python惯例：如果一个函数或者方法对对象进行的是就地改动，那它就应该返回None，例如random、shuffle函数）
# 与list.sort相反的是内置函数sorted，它会新建一个列表作为返回值，方法接受任何形式的可迭代对象作为参数，甚至包括不可变序列或生成器，最后返回一个列表
# 关键字参数：
# ①、reversed: 如果被设定为True，被排序的序列里的元素会以降序输出，默认值为False
# ②、key: 一个只有一个参数的函数，这个函数会被用在序列里的每个元素上，所产生的结果将是排序算法依赖的对比关键字。比如说，在对一些字符串排序时，可以用key=str.lower实现忽略大小写的排序
#         或者是用key=len进行基于字符串长度的排序。参数默认值为恒等函数，也就是默认用元素自己的值来排序
