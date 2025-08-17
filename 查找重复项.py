def find_duplicates(data_list):
    """
    使用集合找出列表中所有元素
    :param data_list: 原始的列表
    :return: list(duplicate) （含有所有重复元素的列表）
    """

    seen = set() # 见过盘
    duplicate = set() # 重复盘
    # 用集合来存放元素可以自动去重
    for item in data_list:
        if item in seen:
            # 如果之间见过这个元素，则放入到重复盘之中
            duplicate.add(item)
        else:
            # 如果没见过就加入到见过盘之中
            seen.add(item)

    return list(duplicate)


data = [1,6,9,8,7,7,7,4,5,1,5,4,2,3]
duplicate_data = find_duplicates(data)
print(f"以下重复元素是：{duplicate_data}")
# * 操作符会把列表（或任何可迭代对象）“解包”成独立的元素，然后作为单独的参数传递给 print 函数。
print(*duplicate_data)
# 通过 sep 参数来指定分隔符。
print(*duplicate_data, sep='\n')



