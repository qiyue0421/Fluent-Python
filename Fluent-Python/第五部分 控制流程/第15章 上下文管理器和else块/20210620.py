""" 不常见的一些流程控制特性
* with语句和上下文管理器
* for、while和try语句的else子句

with语句会设置一个临时的上下文，交给上下文管理器对象控制，并且负责清理上下文。这样做能避免错误并减少样板代码，因此API更安全，而且更易于使用。除了自动关闭文件之外，with块还有很多用途
"""


"""2、先做这个，再做那个：if语句之外的else块"""
# else子句不仅能在if语句中使用，还能在for、while和try语句中使用

''' else子句行为：
①、for
    仅当for循环运行完毕时（即for循环没有被break语句中止）才运行else块
    
for item in my_list:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('No banana flavor found!')    

②、while
    仅当while循环因为条件为假值而退出时（即while循环没有被break语句中止）才运行else块
    
③、try
    仅当try块中没有异常抛出时才运行else块，else子句抛出的异常不会由前面的except子句处理
    
try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()  # 只有try块不抛出异常，才会执行after_call()
'''


"""2、上下文管理器和with块"""
''' 上下文管理器 
* 上下文管理器对象存在的目的是管理with语句，就像迭代器的存在是为了管理for语句一样
* with语句目的：简化try/finally模式，这种模式用于保证一段代码运行完毕后执行某项操作，即便那段代码由于异常、return语句或sys.exit()调用而中止，也会执行指定的操作。finally子句中代码通常用于释放重要的资源，或者还原临时变更的状态
* 上下文管理器协议包含__enter__和__exit__两个方法，with语句开始运行时，会在上下文管理器对象上调用__enter__方法。with语句运行结束后，会在上下文管理器对象上调用__exit__方法，以此扮演finally子句的角色
'''
with open('example.txt', encoding='utf-8') as fp:  # fp绑定到打开的文件上，因为文件的__enter__方法返回self
    src = fp.read(60)

print(len(src))
print(fp)  # fp变量仍然可用
# <_io.TextIOWrapper name='example.txt' mode='r' encoding='utf-8'>
print(fp.closed, fp.encoding)  # 可以读取fp对象的属性
# True utf-8
'''
fp.read(60)  # 不能在fp上执行I/O操作，因为在with块的末尾，调用TextIOWrapper.__exit__方法把文件关闭了
Traceback (most recent call last):
    ...
    fp.read(60)
ValueError: I/O operation on closed file.
'''

class LookingGlass:
    def __enter__(self):  # 除了self参数外，不会传入任何参数
        import sys
        self.original_write = sys.stdout.write  # 保存原来的sys.stdout.write方法到一个实例属性中，后面再使用
        sys.stdout.write = self.reverse_write  # 替换sys.stdout.write为自己编写的方法
        return 'JABBERWOCKY'  # 返回字符串

    def reverse_write(self, text):  # 将text内容反转
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):  # 一切正常的话，这三个参数应该都是None
        """
        exc_type：异常类（例如ZeroDivisionError）
        exc_val：异常实例。有时会有参数传给异常构造方法，例如错误消息，这些参数可以使用exc_val.args获取
        exc_tb：trackback对象
        """
        import sys  # 重复导入模块不会消耗很多资源，因为Python会缓存导入的模块
        sys.stdout.write = self.original_write  # 还原原来的方法
        if exc_type is ZeroDivisionError:  # 如果有异常，且是ZeroDivisionError类型，打印消息
            print('Please DO NOT divide by zero!')
            return True  # 返回True，表示异常已处理


with LookingGlass() as what:  # 上下文管理器是LookingGlass类的实例；Python在上下文管理器上调用__enter__方法，把返回结果绑定到what上
    print('Alice, Kitty and Snowdrop')
    print(what)

# 打印出的内容是反向的
# pordwonS dna yttiK ,ecilA
# YKCOWREBBAJ

print(what)  # with块已经执行完毕，输出不再是反向的
# JABBERWOCKY


# 在with块之外使用LookingGlass类
manager = LookingGlass()  # 实例化并审查manager实例
print(manager)
# <__main__.LookingGlass object at 0x0000023D0A417D30>

monster = manager.__enter__()  # 调用__enter__()方法，将结果存储在monster中
print(monster == 'JABBERWOCKY')  # 打印出的True标识符都是反向的，因为stdout的所有输出都经过了__enter__方法中打补丁的write方法处理
# eurT
print(monster)
# YKCOWREBBAJ
print(manager)
# >07B7C9F15D100000x0 ta tcejbo ssalGgnikooL.__niam__<

manager.__exit__(None, None, None)  # 调用__exit__方法，还原之前的stdout.write
print(monster)
# JABBERWOCKY


"""3、contextlib模块中的实用工具"""
'''
closing
    如果对象提供了close()方法，但没有实现__enter__/__exit__协议，那么可以使用这个函数构建上下文管理器
    
suppress
    构建临时忽略指定异常的上下文管理器
    
@contextmanager（用途最广泛）
    这个装饰器把简单的生成器函数变成上下文管理器，这样就不用创建类去实现管理器协议了
    
ContextDecorator
    这是个基类，用于定义基于类的上下文管理器。这种上下文管理器也能用于装饰函数，在受管理的上下文中运行整个函数
    
ExitStack
    这个上下文管理器能进入多个上下文管理器。with块结束时，ExitStack按照后进先出的顺序调用栈中各个上下文管理器的__exit__方法。如果事先不知道with块要进入多少个上下文管理器，可以使用这个类。例如，同时打开任意一个文件列表中的所有文件
'''


"""4、使用@contextmanager"""
'''
①、@contextmanager装饰器能减少创建上下文管理器的样板代码量，因为不用编写一个完整的类，定义__enter__和__exit__方法，而只需实现一个yield语句的生成器，生成想让__enter__方法返回的值。

②、在使用@contextmanager装饰的生成器中，yield语句的作用是把函数的定义体分成两部分：yield语句前面的所有代码在with块开始时（即调用__enter__方法时）执行，yield语句后面的代码在with块结束时（即调用__exit__方法时）执行

③、contextlib.contextmanager装饰器会把函数包装成实现了__enter__和__exit__方法的类
__enter__方法作用：
    * 调用生成器函数，保存生成器对象（这里称为gen）
    * 调用next(gen)，执行到yield关键字所在的位置
    * 返回next(gen)产出的值，以便把产出的值绑定到with/as语句中的目标变量上
    
with块终止时，__exit__方法会做以下几件事：
    * 检查有没有把异常传给exc_type；如果有，调用gen.throw(exception)，在生成器函数定义体中包含yield关键字的那一行抛出异常
    * 否则，调用next(gen)，继续执行生成器函数定义体中yield语句之后的代码
'''
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'  # 产出一个值，这个值会绑定到with语句中as子句的目标变量上。执行with块中的代码时，这个函数会在这一点暂停
    except ZeroDivisionError:  # 处理ZeroDivisionError异常，设置一个错误消息
        msg = 'Plase DO NOT divide by zero'
    finally:
        sys.stdout.write = original_write  # 控制权一旦跳出with块，继续执行yield语句之后的代码，这里是恢复成原来的sys.stdout.write方法
        if msg:
            print(msg)

with looking_glass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)
# pordwonS dna yttiK ,ecilA
# YKCOWREBBAJ
