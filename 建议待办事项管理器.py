# 1.初始化一个空待办事项列表
todo_list = []
print("---欢迎使用简易待办事项管理器---")

# 2.添加功能：使用 for 循环让用户可以连续输入三次待办事项
for i in range(3):
    # input() 用于获取用户输入
    new_todo = input(f"请输入第{i+1}个待办事项：")
    # .append() 将新增的待办事项添加到列表末尾
    todo_list.append(new_todo)

print("\n---太棒了！所有待办事项已经全部添加成功。---")

# 3. 显示功能：打印当前的所有待办事项
# 使用一个循环和 f-string 来格式化输出
print("\n---您当前待办的事项有---")
# enumerate()是一个很酷的函数，可以同时得到索引和元素
for index, item in enumerate(todo_list):
    print(f"{index+1}.{item}")

# 4. 完成功能：让用户标记一个已完成的事项
print("\n---请标记已完成的事项---")

# 使用 while 循环，直到用户输入有效数字为止
while True:
    # 获取用户输入的要完成的事项的编号
    completed_num_str = input("请输入您已完成的事项的编号；")

    try:
        # 尝试将用户输入的字符串编号转化为整型
        num_str = int(completed_num_str)
        # 检查编号是否在规定范围之中（1到列表长度之间）
        if 1 <= num_str <len (todo_list):
            # 将编号转化为索引（-1）
            #.pop() 会将指定位置元素删除并且返回它
            completed_item = todo_list.pop(num_str - 1)
            print(f'\n恭喜您！已完成事项：{completed_item}')
            # 输入有效，跳出循环
            break
        else:
            # 输入的数字超出了范围
            print(f"\n输出的数字无效，请输入 1 到 {len(todo_list)} 之间的数字")

    except ValueError:
        # int() 转换失败，则说明输入的并非纯数字编号
        print("\n输入无效，请输入一个数字编号")

# 5. 最终显示：显示出剩余的待办事项
print("\n---您剩余的待办事项有---")
# 判断是否全部完成
if len(todo_list) == 0 :
    print("太棒了！您已完成所有待办事项！请再接再厉！")
else:
    for index,item in enumerate(todo_list):
        print(f"{index + 1}. {item}")

print("\n---程序结束---")





