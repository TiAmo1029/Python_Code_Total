import pandas as pd

# -- 准备数据 --
order_data = {
    'order_id' : range(1,11),
    'timestamp' : pd.to_datetime([
        '2025-10-01 08:15', '2025-10-01 09:30', '2025-10-01 09:45',
        '2025-10-01 14:20', '2025-10-01 15:05', '2025-10-01 18:10',
        '2025-10-01 19:00', '2025-10-01 21:25', '2025-10-01 22:10',
        '2025-10-01 22:55'
    ]),
    'district_id' : ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
    'price' : [12.5, 20.0, 8.0, 15.5, 30.0, 25.0, 18.0, 40.0, 10.0, 22.0]
}
orders_df = pd.DataFrame(order_data)

# --- 任务a：特征工程 ---

# 1. 定义“纯函数”
def get_time_period(timestamp):
    """
    根据输入的时间戳，判断其所属的时间段。
    :param timestamp: 一个 pandas的 Timestamp对象。
    :return:一个表示时间段的字符串。
    """

    # 从 Timestamp 对象中提取小时（hour属性）
    hour = timestamp.hour

    if 7 <= hour <= 9:
        return "早高峰"
    elif 18 <= hour <= 20:
        return "晚高峰"
    elif hour >= 21:
        return "深夜"
    else:
        return "日间"

# 2. 使用.apply()方法，将函数应用到列上
orders_df['time_period'] = orders_df['timestamp'].apply(get_time_period)

print("--- 特征工程完成后的DataFrame ---")
print(orders_df)

# 1. 使用 .groupby() 按两个维度进行分组
grouped_stats = orders_df.groupby(['district_id', 'time_period'])

# 2. 使用 .agg() 进行多种聚合操作，并重命名列
final_agg_df = grouped_stats.agg(
    order_count=('order_id', 'count'),
    total_revenue=('price', 'sum')
)
print("\n--- 分组聚合完成后的结果 ---")
print(final_agg_df)

# 区域信息表
district_data = {
    'district_id' : ['A', 'B', 'C', 'D'],
    'district_name' : ['中心商务区', '科教创新区', '滨海旅游区', '老城区'],
    'area_sqkm' : [20.5, 35.2, 50.1, 15.8]
}
districts_df = pd.DataFrame(district_data)

# --- 任务a: 合并数据 (`.merge()`) ---

# 1. 首先，我们需要将 final_agg_df 的多级索引转换回普通列
#    .reset_index() 可以做到这一点
analysis_df = final_agg_df.reset_index()
print("--- reset_index后的分析表 ---")
print(analysis_df)

# 2. 使用 .merge() 进行左连接
#    'on' 参数指定了用哪个列作为连接的“钥匙”
#    'how' 参数指定了连接的方式
merged_df = pd.merge(
    analysis_df,
    districts_df,
    how='left',
    on='district_id'
)
print("\n--- merge完成后的合并表 ---")
print(merged_df)

# --- 任务b: 再次计算 ---

# 1. 直接用列与列的运算，创建新列
#    Pandas会自动地按行进行计算
merged_df['order_density'] = merged_df['order_count'] / merged_df['area_sqkm']
print("\n--- 计算出最终结果的完整分析表 ---")
# 为了美观，我们可以用 .round(2) 保留两位小数
print(merged_df.round(2))
