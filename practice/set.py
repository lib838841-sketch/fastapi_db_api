'''
集合用 {} 包裹，和列表、元组不一样，关键三大特性
元素不能重复：自动去重
无序：每次打印顺序可能不一样，没有下标，不能用索引取值
元素必须是不可变类型：数字、字符串、元组可以；列表不能放进集合
'''
# set = {1,2,2,2,2,4,5,6,7,8,9,10}
#  print(set)
# print(len(set)) # 集合长度
# print(3 in set)
# for x in set:
#     print(x)  #遍历集合
#  set.add(11) # 添加元素
# set.update([12,13,14]) # 添加多个元素
# print(set)
# print(set)
# set.pop() # 随机删除一个元素  由于集合是无序的，所以每次删除的元素可能不一样。
# print(set)
# set.discard(11) # 删除指定元素，如果元素不存在，不会报错
# print(set)
# set.remove(2)  # remove(x) 删除指定元素，没有就报错
# print(set)
#集合最强功能：交集、并集、差集
a={1,2,3,4,5}
b={3,4,5,6,7}
print(a | b)  #并集
print(a & b)  #交集
print(a - b)  #差集
a.clear() #清空元组的元素
print(a)
