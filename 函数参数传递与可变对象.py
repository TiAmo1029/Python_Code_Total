def modify_list(some_list):
    print(f"  函数内部，接收到的列表 ID: {id(some_list)}")
    some_list.append(100)
    print(f"  函数内部，修改后的列表: {some_list}")

my_list = [1, 2, 3]
print(f"函数调用前，我的列表: {my_list}")
print(f"函数调用前，我的列表 ID: {id(my_list)}")

modify_list(my_list)

print(f"函数调用后，我的列表: {my_list}")
print(f"函数调用后，我的列表 ID: {id(my_list)}")

# ---- 对比不可变对象的例子 ----
def modify_string(some_string):
    print(f"  函数内部，接收到的字符串 ID: {id(some_string)}")
    some_string = "new_string" # 重新赋值会创建一个新对象
    print(f"  函数内部，新字符串 ID: {id(some_string)}")

my_string = "original_string"
print(f"\n函数调用前，我的字符串 ID: {id(my_string)}")
modify_string(my_string)
print(f"函数调用后，我的字符串: {my_string}") # 外部的字符串不会变