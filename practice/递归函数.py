#递归函数就是函数自己调用自己   需要设置一个出口  否则就会死循环。有递归条件和终止条件。
# def fact(n):
#     if n == 0:
#         return 1
#     else:
#         return n * fact(n-1)
# print(fact(6))
# pthon lambda函数 限制（必记）
# 只能有一个表达式
# 不能用 for、while、if多行、def、return
# 只适合简单计算，复杂逻辑老老实实写 def 函数
# 一句话总结
# lambda = 一行匿名小函数，不用起名、不用 return，适合临时简单逻辑。
#
import os
print(os.path.abspath('.'))