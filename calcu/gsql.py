import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="root",
    password="Gauss@123",
    host="10.0.0.133",
    port="5432",        # GaussDB 默认端口
    options="-c search_path=public"
)

# 查询
cur = conn.cursor()
cur.execute("SELECT current_database(), version();")
row = cur.fetchone()
print(row)

cur.close()
conn.close()