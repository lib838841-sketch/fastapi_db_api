import numpy as np

# print(np.__version__)
# a = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])  # 2D array 必须元素数量一致
# print(a.shape)
# print(a.ndim)
# print(a[1])
# print(a[:,0:2])  #0到2 不包含2
# # b = np.array([6, 7, 8, 9, 10])
# # c = a * b
# # print(c)
# d = np.array([[2, 3], [4, 5],[6,7],[8,9],[10,11]])
# print(a @ d)
# print(a *2)

# image = np.array([
#     [255,128,64],
#     [0,32,200]
# ])
# print(image)

# x = np.array([1,2,3])
#
# w = np.array([0.2,0.5,0.8])
#
# y = x @ w
#
# print(y)

a = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
print(a[1:,1:])
print(a[:,:])