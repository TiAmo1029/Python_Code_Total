import pandas as pd

# 宽格式数据
wide_df = pd.DataFrame({
    'City': ['北京', '上海'],
    'GDP_2023': [38000, 42000],
    'GDP_2024': [40000, 45000]
})
print("--- 原始宽表 ---")
print(wide_df)

# 使用.melt()进行逆透视
long_df = wide_df.melt(
    id_vars=['City'],              # 保持不变的“ID列”
    value_vars=['GDP_2023', 'GDP_2024'], # 需要被“融化”的列
    var_name='Year_Indicator',       # 新的“变量名”列的名称
    value_name='GDP'               # 新的“值”列的名称
)
print("\n--- 融化后的长表 ---")
print(long_df)

# (进阶) 我们可以再对'Year_Indicator'列进行处理，提取出年份
long_df['Year'] = long_df['Year_Indicator'].str.replace('GDP_', '')
print("\n--- 清洗后的最终长表 ---")
print(long_df)