import bobo  # HTTP微框架

@bobo.query('/')  # 把一个普通的函数与框架的请求处理机制集成起来，Bobo会内省hello函数，发现它需要一个名为person的参数，然后从请求中获取那个名称对应的参数，将其传给hello函数
def hello(person):
    return r'Hello %s!' % person

# bobo -f test.py
# curl http://localhost:8080/?person=qiyue
