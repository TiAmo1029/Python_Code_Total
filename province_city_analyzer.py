import psycopg2
from typing import Dict  # 引入类型提示


def get_city_counts_by_province(db_config: Dict) -> Dict[str, int]:
    """
    连接数据库，统计每个省份的城市数量。
    :param db_config: 包含数据库连接信息的字典。
    :return: 一个以省份名为键，城市数量为值的字典；如果出错则返回一个空字典。
    """
    # 注意：请将 SQL 中的表名和列名替换为你自己的
    sql_query = """
    WITH city_province_join AS (
        SELECT
            p."name_1" AS province_name,
            c."name_2" AS city_name
        FROM
            public.gadm41_chn_1_1 AS p
        JOIN
            public.gadm41_2 AS c ON ST_Contains(p.geom, c.geom)
    )
    SELECT
        province_name,
        city_name,
        COUNT(*) OVER(PARTITION BY province_name) AS total_cities_in_provinces,
        COUNT(*) AS city_count
    FROM
        city_province_join
    GROUP BY
        province_name,
        city_name
    ORDER BY
        province_name, city_name, city_count;
    """

    results_dict = {}
    conn = None
    cur = None
    try:
        print("--- 正在连接数据库... ---")
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        print("--- 正在执行SQL查询... ---")
        cur.execute(sql_query)
        rows = cur.fetchall()

        for row in rows:
            results_dict[row[0]] = row[2]

        print("--- 数据处理成功！ ---")
        return results_dict

    except psycopg2.Error as e:
        print(f"!!! 数据库错误: {e} !!!")
        return {}

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
        print("--- 数据库连接已关闭。 ---")


if __name__ == "__main__":
    # 1. 定义数据库连接配置
    DB_CONFIG = {
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "123456",  # <--- 在这里替换成你的密码
        "dbname": "gisdb"
    }

    print("--- 开始执行省份城市数量分析 ---")

    # 2. 调用函数，并接收返回的字典
    province_stats = get_city_counts_by_province(DB_CONFIG)

    # --- 核心修改在这里 ---
    # 1. 因为字典本身是无序的（在老版本Python中），我们最好先把它转换成一个列表来排序。
    #    province_stats.items() 会得到 [('广东省', 21), ('山东省', 17), ...]
    #    我们用一个 lambda 函数作为 key，告诉 sorted() 按元组的第二个元素（数量）来降序排序。
    sorted_province_stats = sorted(province_stats.items(), key=lambda item: item[1], reverse=True)

    # 2. 使用 enumerate() 函数来自动生成序号
    #    enumerate(sorted_stats, start=1) 的意思是，从1开始编号
    for index, (province, count) in enumerate(sorted_province_stats, start=1):
        print(f"{index}. {province}: {count} 个城市")

else:
    print("未能获取到统计结果或处理过程中发生错误。")

    # 3. 对返回结果进行处理和展示
    # if province_stats:
    #     print("\n--- 各省份城市数量统计结果 ---")
    #     for province, count in province_stats.items():
    #         print(f"- {province}: {count} 个城市")
    # else:
    #     print("未能获取到统计结果或处理过程中发生错误。")
    #
    # print("\n--- 分析结束 ---")