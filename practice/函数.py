# r1 = 5.2
# r2 = 3.7
# r3 = 4.6
# s1 = 3.14 * r1 * r1
# s2 = 3.14 * r2 * r2
# s3 = 3.14 * r3 * r3
# print("圆1的面积是：", s1)
# print("圆2的面积是：", s2)
# print("圆3的面积是：", s3)
# import numpy as np
#
#
# def square(r):
#     return np.pi * r ** 2
#
#
# square(5.2) #调用函数的时候，必须知道函数名和函数的参数是什么，参数的类型是什么，参数的顺序是什么。
# square(3.7)
# square(4.6)
# print(square(5.2))
# print(square(3.7))
# print(square(4.6))
# def power(x,y=2):     #默认参数放在必须参数的最后  默认参数一般设置是该参数不常用的
#     s=1
#     while y>0:
#         s*=x
#         y-=1
#     return s
# print(power(2))
#


# def power(*args):   #可变参数适用于传参不确定的情况
#     sum = 0
#     for b in args:
#         sum = sum + b * b
#     return sum


# print(power(2, 3))

def person(name, age, **kw):
    print(name, age, kw)

print(person(name="张三", age=18, city="北京",job="engineer"))
#限制用户只能额外传city和job这两个参数
def person2(name, age, *,city,job):  #传入的参数必须是city和job，且是参数名=值的形式，其他参数不允许传入
    print(name, age, city,job)
person2("李四", 24, city="东京",job="worker")
#如果有可变参数的话，则命名关键字参数不需要在写 *号了
def person3(name, age, *args, city, job):
    print(name, age, args, city, job)
person3("王五", 30, "python", "java", city="上海", job="teacher")