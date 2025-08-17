import psycopg2

# 1. 定义连接参数
# 最好把这些参数也放到配置文件中，而不是硬编码
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "123456",
    "dbname": "gisdb"
}

# 准备一个要执行的SQL查询
sql_query = 'SELECT "name_1", ST_AsText(ST_Centroid(geom)) FROM public.gadm41_chn_1_1 LIMIT 5;'

# ---使用try...except...finally 保证连接一定会被关闭---
conn = None
cur = None
try:
    # 2. 建立连接
    conn = psycopg2.connect(**DB_CONFIG) # **是Python的解包语法，将字典展开为关键字参数
    print("数据库连接成功！")

    # 3. 获取游标
    cur = conn.cursor()

    # 4. 执行SQL
    cur.execute(sql_query)
    print("SQL查询已执行。")

    # 5. 获取所有查询结果
    # fetchall() 返回的是一个列表，列表中的每一个元素是一个元组，代表一行记录
    rows = cur.fetchall()

    # 遍历并打印结果
    print("\n---查询结果---")
    for row in rows:
        province_name = row[0]
        centroid_wkt = row[1]
        print(f"省份：{province_name}，质心：{centroid_wkt}")


except psycopg2.Error as e:
    print(f"数据库错误：{e}")

finally:
    # 6. 关闭连接（无论是成功还是失败，finally块中的代码总会被执行）
    if cur is not None:
        cur.close()
        print("\n游标已关闭。")
    if conn is not None:
        conn.close()
        print("数据库连接已关闭。")

