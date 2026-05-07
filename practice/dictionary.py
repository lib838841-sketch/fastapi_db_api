# 字典是键值对结构，用 {} 包裹，格式：{键: 值, 键: 值}
# 键 key：相当于索引，唯一、不能重复值 value：存放数据，可以重复。
# dict1 = {"name": "张三", "age": 20, "gender": "男"}
# print(dict1)
# print(dict1["name"])
# print(dict1["age"])
# print(dict1["gender"])
# # 字典的增删改查
# # 增加
# dict1["address"] = "北京市"
# print(dict1)
# print(dict1.keys())  # 获取所有键
# print(dict1.values())  # 获取所有值
# print(dict1.items()) # 获取所有键值对
# for key, value in dict1.items():
#     print(f"{key}: {value}")
# # 修改
# dict1["age"] = 21
# print(dict1)
# # 删除
# del dict1["gender"]
# print(dict1)
# # 查询
# print(dict1["name"])
# dict3={} #空字典
# dict2=dict()   #空字典
# print(type(dict1))
# print(dict1)
# if "dog" in dict1:   # in 默认只判断键 (key)，不判断值 (value)
#     print("键 dog 存在")
# else:
#     print("键 dog 不存在")
# name = dict1.pop("age")  # 删除键 age 和对应的值
# print(name)
# if 21 in dict1.values():  #判断值是否在字典里，要用 值 in 字典.values()
#     print("值21在value中")
# else:
#     print("值21不在value中")
# name1 = dict1.pop("name")
# print(name1)
# print(dict1)
# dict1["country"] = "CHINA"
# print(dict1)
# dict1.popitem()    # 删除最后一个键值对
# print(dict1)
# del dict1
# print(dict1)
# dict4 = dict1.copy()
# print(dict4)
# name2 = dict1.get("name")  # 获取键 name 对应的值
# print(name2)
# dict1.get("name1", "默认值")  # 获取键 name1 对应的值，如果不存在则返回默认值
# print(dict1)
child1={"name": "李四", "age": 20, "gender": "男"}
child2={"name": "王五", "age": 21, "gender": "女"}
child3={"name": "刘六", "age": 22, "gender": "女"}
family1={"child1": child1, "child2": child2, "child3": child3}
print(family1)
dict6= dict(brand= "Porche",country="China")
print(dict6)