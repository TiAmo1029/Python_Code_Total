import psycopg2
from typing import Dict  # 引入类型提示


def get_city_list_with_province_total(db_config: Dict) -> Dict[str, int]:
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
        COUNT(*) OVER(PARTITION BY province_name) AS total_cities_in_provinces
    FROM
        city_province_join
    ORDER BY
        province_name, city_name;
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

        # 直接返回数据库查询出的所有行
        rows = cur.fetchall()

        if rows:
            print(f"DEBUG: 数据库返回的第一行数据是: {rows[0]}")
            print(f"DEBUG: 第一行数据有 {len(rows[0])} 个元素。")
        return rows  # rows本身就是 [(province, city, total_count), ...] 格式

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

    # 1. 调用新的函数
    city_list = get_city_list_with_province_total(DB_CONFIG)

    # 2. 对返回结果进行处理和展示
    if city_list:
        print("\n--- 各省份城市列表及省内总数 ---")

        # --- 核心修改：数据重组 ---
        # 创建一个空字典，用来按省份组织数据
        provinces_data = {}
        for province, city, total_count in city_list:
            # 如果这个省份还没在字典里，就先为它创建一个键
            if province not in provinces_data:
                # 键是省份名，值是另一部字典，包含总数和一个空的城市列表
                provinces_data[province] = {
                    'total_count': total_count,
                    'cities': []
                }
            # 将当前城市添加到对应省份的城市列表中
            provinces_data[province]['cities'].append(city)

        # 经过重组，provinces_data 的格式会是：
        # {
        #   'Anhui': {'total_count': 17, 'cities': ['Anqing', 'Bengbu', ...]},
        #   'Beijing': {'total_count': 1, 'cities': ['Beijing']}
        # }

        # --- 核心修改：排序 ---
        # 我们可以按省份的城市数量（total_count）来排序
        # provinces_data.items() -> [('Anhui', {'total_count': 17, ...}), ...]
        sorted_provinces = sorted(
            provinces_data.items(),
            key=lambda item: item[1]['total_count'],  # 按每个省份字典里的total_count值来排序
            reverse=True  # 降序
        )

        # --- 核心修改：格式化输出 ---
        # 用 enumerate 为排序后的省份列表添加序号
        for province_index, (province_name, province_info) in enumerate(sorted_provinces, start=1):
            # 打印省份标题
            print(f"\n--- {province_index}. {province_name} (共 {province_info['total_count']} 个城市) ---")

            # 遍历并打印该省份下的城市列表，并为城市添加序号
            for city_index, city_name in enumerate(province_info['cities'], start=1):
                print(f"  {city_index}. {city_name}")

    else:
        print("未能获取到统计结果或处理过程中发生错误。")

    print("\n--- 分析结束 ---")