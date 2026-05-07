import pandas as pd
import psycopg2
import argparse
import json


# 建立连接
def get_conn(host, port, user, password, database):

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    return conn


# 执行查询
def query_data(conn, table, limit):

    sql = f"""
    select *
    from {table}
    limit {limit}
    """

    df = pd.read_sql(sql, conn)

    return df


# 主程序
def main():

    parser = argparse.ArgumentParser(description="openGauss 数据查询工具")

    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=5432)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", required=True)

    parser.add_argument("--table", required=True)
    parser.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()

    # 建立连接
    conn = get_conn(
        args.host,
        args.port,
        args.user,
        args.password,
        args.database
    )

    try:

        df = query_data(conn, args.table, args.limit)

        # 分析
        result = {
            "total": len(df),
            "data": df.to_dict(orient="records")
        }

        # 输出JSON
        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        conn.close()


if __name__ == "__main__":
    main()