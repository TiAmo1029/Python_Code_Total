import pandas as pd

daily_sales_data = {
    'date': pd.to_datetime(['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05']),
    'revenue': [100, 150, 130, 200, 180]
}

sales_df = pd.DataFrame(daily_sales_data)

# 1. 计算累计总收入 (Cumulative Sum)
#    .cumsum() 是一个专门的窗口函数，计算从开始到当前行的累计和
sales_df['cumulative_revenue'] = sales_df['revenue'].cumsum()

# 2. 计算近3天的移动平均收入 (Moving Average)
#    .rolling(window=3) 定义了一个大小为3的“滑动窗口”
#    .mean() 对每个窗口内的数据求平均值
sales_df['3day_moving_avg'] = sales_df['revenue'].rolling(window=3).mean()

print(sales_df)