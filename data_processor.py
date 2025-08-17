import psycopg2
import json
import pandas as pd
from tqdm import tqdm  # 一个漂亮的进度条库，pip install tqdm

# --- 数据库连接配置 ---
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "123456",  # 替换成你的密码
    "dbname": "gisdb"
}

# --- 表名和列名配置 (请根据你的真实情况修改！) ---
PROVINCE_TABLE = 'provinces_of_china'
PROVINCE_NAME_COL = 'name'

CITY_TABLE = 'cities_of_china'
CITY_NAME_COL = 'name'


def process_data():
    """
    连接PostGIS，统计每个省份内的城市名称和面积，并保存为JSON。
    """
    conn = None
    all_province_stats = {}

    try:
        # 1. 建立数据库连接
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("数据库连接成功！")

        # 2. 首先，获取所有省份的列表
        cur.execute(f'SELECT "{PROVINCE_NAME_COL}" FROM public."{PROVINCE_TABLE}";')
        provinces = [row[0] for row in cur.fetchall()]
        print(f"共找到 {len(provinces)} 个省份。")

        # 3. (核心) 循环遍历每一个省份，去查询它内部的城市
        print("开始逐个省份查询城市面积...")
        for province_name in tqdm(provinces, desc="处理进度"):

            sql_query = f"""
                SELECT 
                    c."{CITY_NAME_COL}" as city_name,
                    ST_Area(c.geom::geography) as area_sqm
                FROM 
                    public."{CITY_TABLE}" AS c
                JOIN 
                    public."{PROVINCE_TABLE}" AS p ON ST_Intersects(p.geom, c.geom)
                WHERE 
                    p."{PROVINCE_NAME_COL}" = %s;
            """

            cur.execute(sql_query, (province_name,))
            rows = cur.fetchall()

            city_stats = []
            if rows:
                colnames = [desc[0] for desc in cur.description]
                for row in rows:
                    city_stats.append(dict(zip(colnames, row)))

            all_province_stats[province_name] = city_stats

        # 4. 将最终结果写入JSON文件
        output_path = 'E:/NearTerm_Target/Vue_Projects/my-first-app/public/province_city_stats.json'  # 注意路径
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_province_stats, f, ensure_ascii=False, indent=4)

        print(f"\n处理完成！数据已成功写入到: {output_path}")

    except psycopg2.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭。")


if __name__ == '__main__':
    process_data()