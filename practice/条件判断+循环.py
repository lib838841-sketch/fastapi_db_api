# age = 30  #if条件判断
# if age >= 18:
#     print("成年人")
# elif age >= 7:
#     print("少年")
# else:
#     print("儿童")
# while age<35:
#     age+=1
#     print(age)
# i = 0
# while i<6:
#
#     if i ==3:
#         break
#     print(i)
#     i +=1
# while i<6:
#     i += 1
#     if i ==3:
#         continue
#     print(i)

# list =["apple","banana","cherry"]
# for item in list:
#     print(item)
#
# for i in range (0,10,2):  #0-10 左闭右开  步长是2
#     print(i)
#嵌套循环
fruits=("apple","banana","cherry")
adj=("red","bleu","yellow")
for a in fruits:
    for b in adj:
        print(a,b)
for c in range(0,10,2):
    pass
# pass 1. 核心作用pass 是空语句，什么都不做，只用来占位。
# 就是：占个位置、凑语法、不报错、不执行任何代码。
# 2. 为什么需要 pass？
# Python 的 if、while、for、函数、类，冒号后面必须有代码块，
# 如果暂时没想好写什么，空着会报错，加个 pass 就不报错