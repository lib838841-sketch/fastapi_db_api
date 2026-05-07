#元组是有序且不可修改的集合。元组一旦创建，不能改、不能加、不能删。
# 使用场景：数据固定不变，不让别人修改（比如坐标、配置、常量
tuple =('cat','dog','lion')
print(tuple.count('dog'))  # 指定元素在元组出现的次数
print(tuple.index('dog')) #指定元组在元组中第一次出现的位置
# print(tuple)
# print(len(tuple))
# print(tuple[1])
# print(tuple[0])
# print(tuple[0:2])
# t1=('apple','banana')
# t2= ('pear','orange')
# t3 = t1 + t2
# print(t3)
# 单个元素必须加逗号！重点
# t3 = (5,)   # 是元组
# print(type(t3))
# t4 = 5  # 只是整数，不是元组
# print(type(t4))
# del t4 #可以删除整个元组，但不能删除元组里面的元素。
# print(t4)