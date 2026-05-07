# 创建类
class Person:
    #构造方法，创建对象时自动调用，用来初始化对象属性
    def __init__(self,name,age,gender):
        #给对象绑定属性
        self.name=name
        self.age=age
        self.gender=gender
    #定义方法
    def eat(self):
        print(self.name+"正在吃饭")
    def sleep(self):
        print(self.name+"正在睡觉")
    def play(self):
        print(self.name+"正在玩耍")
# 创建对象
p1=Person("张三",20,"男")
p2=Person("李四",18,"女")
#3.调用对象方法
p1.eat()
p1.sleep()
p1.play()
p2.eat()
p2.sleep()
p2.play()
# 修改属性
p1.age=27
p2.age=23
print(p1.age)
print(p2.age)
print(f"修改后的p1年龄是: {p1.age}")
print(f"修改后的p2年龄是: {p2.age}")
