"""3、导入时和运行时比较
在导入时，解释器会从上到下一次性解析完.py模块的源码，然后生成用于执行的字节码。如果句法有错误，就在此时报告。如果本地的__pycache__文件夹中有最新的.pyc文件，解释器会跳过上述步骤，因为已经有运行所需的字节码
编译肯定是导入时的活动，不过那个时期还会做其他事，因为Python中的语句几乎都是可执行的，也就是说语句可能会运行用户代码，修改用户程序的状态。尤其是import语句，它不只是声明，在进行中首次导入模块时，还会运行所导入模块中的全部顶层代码
以后导入相同的模块则使用缓存，只做名称绑定。那些顶层代码可以做任何事情，包括通常在“运行时”做的事，例如连接数据库。因此，“导入时”与“运行时”之间的界线是模糊的：import语句可以触发任何“运行时”行为

对于函数来说：
    解释器会编译函数的定义体（首次导入模块时），把函数对象绑定到对应的全局名称上，但是显然解释器不会执行函数的定义体。通常这意味着解释器在导入时定义顶层函数，但是仅当在运行时调用函数时才会执行函数的定义体

对类来说：
    在导入时，解释器会执行每个类的定义体，甚至会执行嵌套类的定义体。执行类定义体的结果是，定义了类的属性和方法，并构建了类对象。从这个意义上理解，类的定义体属于“顶层代码”，因为它在导入时运行
"""
from evalsupport import deco_alpha

print('<[1]> evaltime module start')

class ClassOne:
    print('<[2]> ClassOne body')

    def __init__(self):
        print('<[3]> ClassOne.__init__')

    def __del__(self):
        print('<[4]> ClassOne.__del__')

    def method_x(self):
        print('<[5]> ClassOne.method_x')

    class ClassTwo(object):
        print('<[6]> ClassTwo body')


@deco_alpha
class ClassThree:
    print('<[7]> ClassThree body')

    def method_y(self):
        print('<[8]> ClassThree.method_y')


class ClassFour(ClassThree):  # 类装饰器（ClassThree的deco_alpha）对子类没有影响
    print('<[9]> ClassFour body')

    def method_y(self):
        print('<[10]> ClassFour.method_y')


if __name__ == '__main__':
    print('<11> ClassOne tests', 30 * '.')
    one = ClassOne()
    one.method_x()
    print('<[12]> ClassThree tests', 30 * '.')
    three = ClassThree()
    three.method_y()
    print('<[13]> ClassFour tests', 30 * '.')
    four = ClassFour()
    four.method_y()

print('<[14]> evaltime module end')


""" 在python控制台运行 import evaltime 导入模块时输出如下：
<[100]> evalsupport module start  # evalsupport模块中的所有顶层代码在导入模块时运行；解释器会编译deco_alpha函数，但是不会执行定义体
<[400]> MetaAleph body  # MetaAleph类的定义体运行了
<[700]> evalsupport module end
<[1]> evaltime module start
<[2]> ClassOne body  # 每个类的定义体都执行了
<[6]> ClassTwo body
<[7]> ClassThree body
<[200]> deco_alpha  # 先计算被装饰的类ClassThree的定义体，然后运行装饰器函数
<[9]> ClassFour body
[14]> evaltime module end  # 在这个场景中，evaltime模块是导入的，因此不会运行 if __name__ == '__main__': 块
"""


""" 在python命令行运行 python3 evaltime.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime module start
<[2]> ClassOne body
<[6]> ClassTwo body
<[7]> ClassThree body
<[200]> deco_alpha
<[9]> ClassFour body  # 到这里为止都跟上面输出相同
<11> ClassOne tests ..............................
<[3]> ClassOne.__init__  # 类的标准行为
<[5]> ClassOne.method_x
<[12]> ClassThree tests ..............................
<[300]> deco_alpha:inner_1  # deco_alpha装饰器修改了ClassThree.method_y方法，因此调用three.method_y()时会运行inner_1函数定义体
<[13]> ClassFour tests ..............................
<[10]> ClassFour.method_y
<[14]> evaltime module end
<[4]> ClassOne.__del__   # 只有程序结束时，绑定在全局变量one上的ClassOne实例才会被垃圾回收程序回收
"""
