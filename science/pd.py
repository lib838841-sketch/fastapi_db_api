import pandas as pd
import psycopg2
from sqlalchemy import create_engine
# print(pd.__version__)
# data = {
#     "姓名":["张三","李四","王五"],
#     "年龄":[28,35,30],
#     "工资":[12000,18000,15000]
# }
# df = pd.DataFrame(data)
# print(df)
# print(df["姓名"])
# print(df[df["工资"]>15000])
# print(
#     df[
#         (df["工资"] > 10000) &
#         (df["年龄"] > 30)
#     ]
# )
# df["年终奖"]=df["工资"]*2
# print(df)
# print(df["工资"].mean())
# print(df["工资"].max())
# print(df["工资"].min())
# print(df["年龄"].mean())
# print(df.describe())


# 建立连接
conn = psycopg2.connect(
    host="10.0.0.133",
    port=5432,
    user="root",
    password="Gauss@123",
    database="finance"
)

# SQL
sql = "select * from client limit 2"

# 导入Pandas
df = pd.read_sql(sql, conn)

# 输出
print(df)

# 关闭连接
conn.close()

df.to_excel("client.xlsx")
print(df.shape)
print(df.columns)
print(df.describe())
# df = pd.read_csv("user.csv")
# # print(df)
# df.to_csv("new_user.csv")