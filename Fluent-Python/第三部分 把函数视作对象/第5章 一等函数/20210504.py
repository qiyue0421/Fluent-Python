""" 在Python中，函数是一等对象，定义为：
1、在运行时创建
2、能赋值给变量或数据结构中的元素
3、能作为参数传给函数
4、能作为函数的返回结果
在Python中，整数、字符串和字典都是一等对象。
"""

"""1、把函数视作对象"""


# 创建并测试一个函数，然后读取它的__doc__属性，再检查它的类型


def factorial(n):
    """returns n!"""
    return 1 if n < 2 else n * factorial(n - 1)


print(factorial(42))
print(factorial.__doc__)  # __doc__是函数对象众多属性中的一个，用于生成对象的帮助文本
print(type(factorial))  # factorial是function类的实例

# 通过别的名称使用函数，再把函数作为参数传递
fact = factorial  # 将函数赋值给变量
print(fact)
print(fact(5))  # 120
map(factorial, range(11))  # 函数作为参数传给另一个函数
# map函数返回一个可迭代对象，里面的元素是把第一个参数（一个函数）应用到第二个参数（一个可迭代对象，这里是range(11)）中各个元素上得到的结果
print(list(map(factorial, range(11))))

"""2、高阶函数"""
# 接受函数为参数，或者把函数作为结果返回的函数是高阶函数。比如map、filter、reduce、sorted等函数

# 根据单词长度给一个列表排序
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=len))  # 可选的key参数用于提供一个函数，它会应用到各个元素上进行排序


# ['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']


# 根据反向拼写给一个单词列表排序
def reverse(word):
    return word[::-1]


print(reverse('testing'))  # gnitset
print(sorted(fruits, key=reverse))
# ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']


# map、filter和reduce的现代替代品
# 函数式语言通常会提供map、filter和reduce三个高阶函数。在Python 3中，map和filter还是内置函数，但是由于引入了列表推导式和生成器表达式，它们变得没那么重要了。
# 列表推导或生成器表达式具有map和filter两个函数的功能，而且易于阅读。

# 计算阶乘列表：map和filter与列表推导比较
print(list(map(fact, range(6))))  # 使用map函数构建一个阶乘列表
print([fact(n) for n in range(6)])  # 使用列表推导执行相同的操作

print(list(map(factorial, filter(lambda n: n % 2, range(6)))))  # 获得奇数阶乘列表，为了使用高阶函数，有时创建一次性的小型函数更便利——lambda匿名函数
print([factorial(n) for n in range(6) if n % 2])  # 使用列表推导替换掉map和filter

# 使用reduce和sum计算0~99之和
from functools import reduce  # 从python 3.0开始，reduce不再是内置函数
from operator import add  # 导入add，以免创建一个专求两数之和的函数

print(reduce(add, range(100)))
print(sum(range(100)))  # 使用sum做相同的求和，无需导入或创建求和函数
# sum和reduce的通用思想是把某个操作连续应用到序列的元素上，累计之前的结果，把一系列值归约成一个值
# all和any也是内置的规约函数
# all(iterable)：如果iterable的每个元素都是真值，返回True；all([])返回True
# any(iterable)：只要iterable中有元素是真值，就返回True；any([])返回False


"""3、匿名函数"""
# lambda关键字在Python表达式内创建匿名函数，lambda函数的定义体中不能赋值，也不能使用while和try等语句，只能使用纯表达式

print(sorted(fruits, key=lambda word: word[::-1]))  # 使用lambda表达式反转拼写，然后依此给单词列表排序
# lambda句法只是语法糖：与def语句一样，lambda表达式会创建函数对象，这是python中几种可调用对象的一种。


"""4、可调用对象"""
# 除了用户定义的函数，调用运算符（即()）还可以应用到其他对象上。如果想判断对象能否调用，可以使用内置的callable()函数。

# Python数据模型文档中的7种可调用对象：
## 用户定义的函数：使用def语句或lambda表达式创建
## 内置函数：使用C语言（CPython）实现的函数，如len或time.strftime
## 内置方法：使用C语言实现的方法，如dict,get
## 方法：在类的定义体中定义的函数
## 类：调用类时会运行类的__new__方法创建一个实例，然后运行__init__方法，初始化实例，最后把实例返回给调用方。因为python没有new操作符，所以调用类相当于调用函数
## 类的实例：如果类定义了__call__方法，那么它的实例可以作为函数调用
## 生成器函数：使用yield关键字的函数或方法。调用生成器函数返回的是生成器对象


"""5、用户定义的可调用类型"""
# 不仅Python函数是真正的对象，任何Python对象都可以表现得像函数。为此，只需要实现实例方法__call__
import random


class BingoCage:  # 该类的实例使用任何可迭代对象构建，而且会在内部存储一个随机顺序排列的列表，调用该实例会取出一个元素
    def __init__(self, items):  # 接受任何可迭代对象
        self._items = list(items)  # 在本地构建一个副本，防止列表参数的意外副作用
        random.shuffle(self._items)  # 随机打乱列表中的元素

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')  # 抛出异常，设定错误消息

    def __call__(self, *args, **kwargs):  # bingo.pick()的快捷方式是bingo()
        return self.pick()


bingo = BingoCage(range(3))
print(bingo.pick())
print(bingo())  # bingo实例可以作为函数调用
print(callable(bingo))  # True

"""6、函数内省"""
# 除了__doc__，函数对象还有很多属性。使用dir函数可以探知factorial具有下述属性：
print(dir(factorial))
'''
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
'__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', 
'__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', 
'__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
'''


# 计算两个属性集合的差集能够得到函数专有属性列表（函数专有而用户定义的一般对象没有的属性）
class C: pass  # 创建一个空的用户定义的类


obj = C()  # 创建一个类的实例


def func(): pass  # 创建一个空函数


print(sorted(set(dir(func)) - set(dir(obj))))  # 计算差集，然后排序，得到函数有的而类的实例没有的属性列表
# ['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']


"""7、从定位参数到仅限关键字参数"""


# python提供了极为灵活的参数处理机制，python3进一步提供了仅限关键字参数（keyword-only argument）
def tag(name, *content, cls=None, **attrs):
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


print(tag('br'))  # 传入单个定位参数，生成一个指定名称的空标签
# <br />
print(tag('p', 'hello'))  # 第一个参数后面的任意个参数会被*content捕获，存入一个元组
# <p>hello</p>
print(tag('p', 'hello', 'world'))
# <p>hello</p>
# <p>world</p>
print(tag('p', 'hello', id=33))  # 没有明确指定名称的关键字参数（比如id=33）会被**attrs捕获，存入一个字典
# <p id="33">hello</p>
print(tag('p', 'hello', 'world', cls='sidebar'))  # cls参数只能作为关键字参数传入
# <p class="sidebar">hello</p>
# <p class="sidebar">world</p>
print(tag(content='tesing', name="img"))  # 第一个定位参数也能作为关键字参数传入
# <img content="tesing" />
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
print(tag(**my_tag))  # 在my_tag前面加上 **，字典中的所有元素作为单个参数传入，同名键会绑定到对应的具名参数上，余下的则被 **attrs捕获
# <img class="framed" src="sunset.jpg" title="Sunset Boulevard" />


"""8、获取关于参数的信息"""
import bobo  # HTTP微框架


@bobo.query('/')  # 把一个普通的函数与框架的请求处理机制集成起来，Bobo会内省hello函数，发现它需要一个名为person的参数，然后从请求中获取那个名称对应的参数，将其传给hello函数
def hello(person):
    return 'Hello %s!' % person


# 函数对象有个 __defaults__ 属性，它的值是一个元组，里面保存着定位参数和关键字参数的默认值。仅限关键字参数的默认值在 __kwdefaults__ 属性中。然而，参数的名称在__code__属性中，
# 它的值是一个code对象的引用，自身也有很多属性
def clip(text, max_len=80):
    """在max_len前面或后面的第一个空格处截断文本"""
    end = None  # 截断点
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)  # 往前找
        if space_before >= 0:  # 查找空格（范围从0到max_len），返回字符串最后一次出现的位置，如果没有匹配项则返回-1
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)  # 往后找
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()  # 返回截断的文本


print(clip.__defaults__)  # 参数的默认值只能通过参数在 __defaults__ 元组中的位置确定，因此要从后向前扫描才能把参数和默认值对应起来
# (80,)
print(clip.__code__)
# <code object clip at 0x0...
print(clip.__code__.co_varnames)  # 参数名称在 __code__.co_varnames 中，不过里面有包含函数定义体中创建的局部变量，因此，参数名称是前N个字符串
# ('text', 'max_len', 'end', 'space_before', 'space_afer')，前2个字符是 text和max_len，其中一个有默认值，即80，因此它必然属于最后一个参数，即max_len
print(clip.__code__.co_argcount)  # N的值由 __code__.co_argcount 确定
# 2


# 使用inspect模块：提取函数的签名
from inspect import signature

# signatrue对象，它有一个parameters属性，这是一个有序映射，把参数名和inspect.Parameter对象对应起来
sig = signature(clip)
print(sig)
for name, param in sig.parameters.items():
    print(param.kind, ":", name, "=", param.default)
# POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
# POSITIONAL_OR_KEYWORD : max_len = 80

# 各个Parameter属性也有自己的属性，例如name、default和kind。特殊的inspect._empty值表示没有默认值，kind属性的值是_ParameterKind类中的5个值之一，列举如下：
# POSITIONAL_OR_KEYWORD：可以通过定位参数和关键字参数传入的形参（多数python函数的参数属于此类）
# VAR_POSITIONAL：定位参数元组
# VAR_KEYWORD：关键字参数字典
# KEYWORD_ONLY：仅限关键字参数
# POSITIONAL_ONLY：仅限定位参数

# inspect.Signatrue对象有个bind方法，可以把任意个参数绑定到签名中的形参上，所用的规则与实参到形参的匹配方式一样
import inspect

sig = inspect.signature(tag)  # 获取tag函数的签名
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
bound_args = sig.bind(**my_tag)  # 把一个字典参数传给bind()方法
print(bound_args)  # 得到一个BoundArguments对象
# <BoundArguments (name='img', cls='framed', attrs={'title': 'Sunset Boulevard', 'src': 'sunset.jpg'})>
for name, value in bound_args.arguments.items():  # 迭代
    print(name, '=', value)  # 显示参数名称和值
'''
del my_tag['name']  # 尝试将必须指定的参数name从my_tag中删除
bound_args = sig.bind(**my_tag)  # TypeError: missing a required argument: 'name'
'''


"""9、函数注解"""
# python3提供了一种句法，用于为函数声明中的参数和返回值附加元数据。函数声明中的各个参数可以在 : 之后增加注解表达式。
# 如果参数有默认值，注解放在参数名和 = 号之间
# 如果想注解返回值，在 ) 和函数声明末尾的 : 之间添加 -> 和一个表达式（可以是任何类型）
# 注解中最常用的类型是类（如str或int）和字符串（如'int > 0'），如此例的max_len
def clip(text: str, max_len: 'int > 0' = 80) -> str:
    """在max_len前面或后面的第一个空格处截断文本"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()

# 注解不会做任何处理，只是存储在函数的 __annotations__ 属性（一个字典）中，换句话说，注解对python解释器没有任何意义，注解只是元数据，可以供IDE、框架和装饰器等工具使用
print(clip.__annotations__)  # {'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}

# 从函数签名中提取注解
sig = signature(clip)  # signature函数返回一个Signature对象，它有一个return_annotation属性和一个parameters属性，后者是一个字典，把参数名映射到Parameter对象上
print(sig.return_annotation)  # <class 'str'>
for param in sig.parameters.values():
    note = repr(param.annotation).ljust(13)  # 每个Parameter对象自己也有annotation属性
    print(note, ':', param.name, '=', param.default)
'''
<class 'str'> : text = <class 'inspect._empty'>
'int > 0'     : max_len = 80
'''


"""10、支持函数式编程的包"""
## operator模块：为多个算术运算符提供了对应的函数
# 使用reduce函数和一个匿名函数计算阶乘
def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))

# 使用reduce和operator.mul函数计算阶乘
from functools import reduce
from operator import mul

def fact_1(n):
    return reduce(mul, range(1, n+1))

# operator模块中还有一类函数，能替代从序列中取出元素或读取对象属性的lambda表达式：itemgetter和attrgetter会自行构建函数
# 使用itemgetter排序一个元组列表，itemgetter的常见用途：根据元组的某个字段给元组列表排序
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35, 139)),
    ('Delhi NCR', 'IN', 21.935, (28, 77)),
    ('Mexico City', 'MX', 20, (19, -99)),
    ('New York-Newark', 'US', 20, (40, -74)),
    ('Sao Paulo', 'BR', 19, (-23, -46))
]

from operator import itemgetter

for city in sorted(metro_areas, key=itemgetter(1)):  # itemgetter(1)的作用与lambda fields: fields[1] 一样：创建一个接受集合的函数，返回索引位1上的元素
    print(city)
'''
('Sao Paulo', 'BR', 19, (-23, -46))
('Delhi NCR', 'IN', 21.935, (28, 77))
('Tokyo', 'JP', 36.933, (35, 139))
('Mexico City', 'MX', 20, (19, -99))
('New York-Newark', 'US', 20, (40, -74))
'''

# 如果把多个参数传给itemgetter，它构建的函数会返回提取的值构成的元组
cc_name = itemgetter(1, 0)
for city in metro_areas:
    print(cc_name(city))
'''
('JP', 'Tokyo')
('IN', 'Delhi NCR')
('MX', 'Mexico City')
('US', 'New York-Newark')
('BR', 'Sao Paulo')
'''

# attrgetter创建的函数根据名称提取对象的属性。如果把多个属性名传给attrgetter，它也会返回提取的值构成的元组。此外，如果参数名中包含 .（点号），attrgetter还会深入嵌套对象，获取指定属性
from collections import namedtuple

LatLong = namedtuple('LatLong', 'lat long')  # 使用namedtuple定义LatLong
Metropolis = namedtuple('Metropolis', 'name cc pop coord')  # 使用namedtuple定义Metropolis
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_areas]  # 使用Metropolis实例构建metro_areas列表
print(metro_areas[0])
# Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35, long=139))
print(metro_areas[0].coord.lat)  # 深入metro_areas，获取metro_areas的纬度

from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat')  # 定义一个attrgetter，获取name属性和嵌套的coord.lat属性
for city in sorted(metro_areas, key=attrgetter('coord.lat')):  # 使用attrgetter获取纬度排序城市列表
    print(name_lat(city))  # 使用之前定义的attrgetter，只显示城市名和纬度
    '''
    ('Sao Paulo', -23)
    ('Mexico City', 19)
    ('Delhi NCR', 28)
    ('Tokyo', 35)
    ('New York-Newark', 40)
    '''

# operator模块中的methodcaller函数：在对象上调用参数指定的方法
from operator import methodcaller

s = 'The time has come'
upcase = methodcaller('upper')
print(upcase(s))
# THE TIME HAS COME

hiphenate = methodcaller('replace', ' ', '-')
print(hiphenate(s))
# The-time-has-come


## functools模块提供了一系列高阶函数，除了reduce外，最有用的是partial及其变体，partialmethod
# functools.partial这个高阶函数用于部分应用一个函数，部分应用是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。
# 使用这个函数可以把接受一个或多个参数的函数改编成需要回调的API，这样参数更少
from operator import mul
from functools import partial

triple = partial(mul, 3)  # 固定参数3
print(triple(7))  # 测试 7 x 3
print(list(map(triple, range(1, 10))))  # 在map中使用triple
# [3, 6, 9, 12, 15, 18, 21, 24, 27]

picture = partial(tag, 'img', cls='pic-frame')  # 固定tag函数中的第一个位置参数为img，把cls关键字参数固定为 'pic-frame'
print(picture(src='wumpus.jpg'))
# <img class="pic-frame" src="wumpus.jpg" />
print(picture.func)  # 访问原函数
print(picture.args, picture.keywords)  # 访问位置参数及关键字参数
