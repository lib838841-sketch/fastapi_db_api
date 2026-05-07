from fastapi import FastAPI
import pandas as pd
import psycopg2

app = FastAPI()

# 数据库连接函数
def get_conn():

    conn = psycopg2.connect(
        host="10.0.0.133",
        port=5432,
        user="root",
        password="Gauss@123",
        database="finance"
    )

    return conn


# 首页测试
@app.get("/")
def home():

    return {
        "msg": "FastAPI openGauss OK"
    }


# 查询客户接口
@app.get("/client")
def get_client():

    conn = get_conn()

    sql = """
    select *
    from client
    limit 5
    """

    # SQL结果导入Pandas
    df = pd.read_sql(sql, conn)

    conn.close()

    # Pandas分析
    row_count = len(df)

    # 转JSON
    result = {
        "total": row_count,
        "data": df.to_dict(orient="records")
    }

    return result