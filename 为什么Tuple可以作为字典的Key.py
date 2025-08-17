my_dict = {}

# 使用 Tuple 作为 key (成功)
my_tuple = (1, 2)
my_dict[my_tuple] = "This works!"
print(my_dict)  # 输出: {(1, 2): 'This works!'}

# 尝试使用 List 作为 key (失败)
my_list = [1, 2]
try:
    my_dict[my_list] = "This will fail."
except TypeError as e:
    print(e)  # 输出: unhashable type: 'list'