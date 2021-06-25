"""8、yield from 的意义"""
''' yield from 的行为
①、子生成器产出的值都直接传给委派生成器的调用方（即客户端代码）
②、使用send()方法发给委派生成器的值都直接传给子生成器。如果发送的值是None，那么会调用子生成器的__next__()方法。如果发送的值不是None，那么会调用子生成器的send()方法。如果调用的方法抛出StopIteration异常，那么委派生成器
恢复运行。任何其他异常都会向上冒泡，传给委托生成器
③、生成器退出时，生成器（或子生成器）中的return expr表达式会触发StopIteration(expr)异常抛出
④、yield from表达式的值是子生成器终止时传给StopIteration异常的第一个参数
⑤、传入委派生成器的异常，除了GeneratorExit之外都传给子生成器的throw()方法。如果调用throw()方法时抛出StopIteration异常，委派生成器恢复运行。StopIteration之外的异常会向上冒泡，传给委派生成器

'''