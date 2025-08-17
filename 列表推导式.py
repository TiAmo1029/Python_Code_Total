prices = [120, 99, 250, 43, 88]
# 将所有价格除以 255.0 进行归一化，并过滤掉太小的价格
normalized_prices = [p / 255.0 for p in prices if p > 50]
print(normalized_prices) # [0.470..., 0.388..., 0.980..., 0.345...]