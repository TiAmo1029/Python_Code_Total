import pandas as pd

traffic_data = {
    'intersection_id': ['A', 'A', 'A', 'B', 'B', 'B', 'A', 'B'],
    'timestamp': pd.to_datetime([
        '2023-10-01 08:00', '2023-10-01 09:00', '2023-10-01 10:00',
        '2023-10-01 08:00', '2023-10-01 09:00', '2023-10-01 10:00',
        '2023-10-02 08:00', '2023-10-02 09:00'
    ]),
    'flow': [300, 500, 450, 600, 800, 750, 320, 850]
}

traffic_df = pd.DataFrame(traffic_data)
# 添加一个小时列，用来统计
traffic_df['hour'] = traffic_df['timestamp'].dt.hour

traffic_df['hourly_avg_flow'] = traffic_df.groupby(['intersection_id', 'hour'])['flow'].transform('mean')

# grouped_traffic_df = traffic_df.groupby(['intersection_id', 'hour'])

# traffic_df['hourly_avg_flow'] = grouped_traffic_df['flow'].transform('mean')

print("--- 步骤a完成后，带有同期平均流量的DataFrame ---")
print(traffic_df)

traffic_df['is_anomaly'] = traffic_df['flow'] > (traffic_df['hourly_avg_flow'] * 1.2)

print("\n--- 步骤b完成后，带有异常标记的DataFrame ---")
print(traffic_df)

# --- 步骤c: 筛选并展示结果 ---

# 1. 使用布尔索引，筛选出所有 is_anomaly 为 True 的行
anomaly_df = traffic_df[traffic_df['is_anomaly'] == True]

print("\n--- 最终筛选出的“早高峰异常流量”记录 ---")
print(anomaly_df)



