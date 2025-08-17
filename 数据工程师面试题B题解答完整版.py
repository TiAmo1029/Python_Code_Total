import math


# --- 1. 全局辅助函数 ---
# 这些函数是解决问题的基础工具，提取出来方便复用

def rotate_point(px, py, cx, cy, angle_rad):
    """
    将点(px, py)围绕中心(cx, cy)旋转 angle_rad 弧度。
    angle_rad > 0 为逆时针（数学常规）。
    """
    # 步骤1: 将坐标系平移，使旋转中心成为原点
    p_translated_x = px - cx
    p_translated_y = py - cy

    # 步骤2: 应用标准旋转公式
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    p_rotated_x = p_translated_x * cos_angle - p_translated_y * sin_angle
    p_rotated_y = p_translated_x * sin_angle + p_translated_y * cos_angle

    # 步骤3: 将坐标系平移回去
    final_x = p_rotated_x + cx
    final_y = p_rotated_y + cy

    return [final_x, final_y]


def get_line_intersection(p1, p2, p3, p4):
    """
    计算两条无限长直线 L1(p1,p2) 和 L2(p3,p4) 的交点。
    返回交点坐标 [x, y] 或者在平行/共线时返回 None。
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9:  # 使用一个小的容差来判断是否为0，避免浮点数问题
        return None  # 直线平行或共线

    t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = t_num / den

    ix = x1 + t * (x2 - x1)
    iy = y1 + t * (y2 - y1)

    return [ix, iy]


# --- 2. 模拟输入数据 ---
# 根据题目截图创建一个可用的输入数据样本
mock_data = {
    "size": [1920, 1080],  # [height, width] -> [y, x] or [w,h]? Assume [w,h]
    "box": {
        "1": [
            [100, 100, 200, 150],  # [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
            30.0  # rot in degrees
        ]
    },
    "lines": {
        "1": [
            # 这条线一个端点在框内，且长度>30，应该被选中
            [110, 110, 180, 250],
            # 这条线长度<30，不应该被选中
            [50, 50, 60, 60],
            # 这条线两个端点都在框外，不应该被选中
            [0, 0, 500, 500]
        ]
    }
}


# --- 3. 分步解答 ---

def solve_q1(data):
    """
    问(1): 旋转Box使其“摆正”，输出四个顶点坐标。
    实现：围绕Box中心点，进行 `-rot` 度的反向旋转。
    """
    result = {"rotate_box": {}}

    for group_id, box_info_list in data['box'].items():
        box_coords = box_info_list[0]
        rot = box_info_list[1]

        x1, y1, x2, y2 = box_coords

        # 计算旋转前Box的中心点
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # 确定旋转前的四个顶点 (TL, TR, BR, BL)
        corners = [
            [x1, y1], [x2, y1], [x2, y2], [x1, y2]
        ]

        # "摆正"需要反向旋转，角度为 -rot
        # 将角度转为弧度
        angle_rad_to_unrotate = math.radians(-rot)

        unrotated_corners = []
        for px, py in corners:
            new_corner = rotate_point(px, py, cx, cy, angle_rad_to_unrotate)
            unrotated_corners.append(new_corner)

        result["rotate_box"][group_id] = unrotated_corners

    return result


def solve_q2(data):
    """
    问(2): 筛选"完美线段"。
    条件1: 线段任一端点在对应组的原始旋转框内。
    条件2: 线段长度 > 30。
    """
    result = {"perfect_line": {}}

    for group_id, lines_list in data['lines'].items():
        if group_id not in data['box']:
            continue

        box_info = data['box'][group_id]
        box_coords, rot = box_info
        x1, y1, x2, y2 = box_coords
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        angle_rad_to_unrotate = math.radians(-rot)

        perfect_lines_for_group = []
        for line in lines_list:
            p1 = [line[0], line[1]]
            p2 = [line[2], line[3]]

            # 条件2：检查长度
            if math.hypot(p2[0] - p1[0], p2[1] - p1[1]) <= 30:
                continue

            # 条件1：检查端点是否在旋转框内
            # 策略：反向旋转端点，看是否在原始轴对齐框内
            p1_unrotated = rotate_point(p1[0], p1[1], cx, cy, angle_rad_to_unrotate)
            p2_unrotated = rotate_point(p2[0], p2[1], cx, cy, angle_rad_to_unrotate)

            epsilon = 1e-9  # 浮点数容差

            is_p1_in = (x1 - epsilon <= p1_unrotated[0] <= x2 + epsilon) and \
                       (y1 - epsilon <= p1_unrotated[1] <= y2 + epsilon)

            is_p2_in = (x1 - epsilon <= p2_unrotated[0] <= x2 + epsilon) and \
                       (y1 - epsilon <= p2_unrotated[1] <= y2 + epsilon)

            if is_p1_in or is_p2_in:
                perfect_lines_for_group.append(line)

        if perfect_lines_for_group:
            result["perfect_line"][group_id] = perfect_lines_for_group

    return result


def solve_q3(perfect_lines_data, original_data):
    """
    问(3): 计算完美线段延长后，与旋转框边的交点。
    """
    # 题目输出格式是一个大列表，我们按这个格式组织
    result = []

    if "perfect_line" not in perfect_lines_data:
        return []

    for group_id, perfect_lines in perfect_lines_data["perfect_line"].items():
        # 获取对应组的原始Box信息
        box_info = original_data['box'][group_id]
        box_coords, rot = box_info
        x1, y1, x2, y2 = box_coords

        # 步骤1: 计算旋转框的4个实际顶点坐标（正向旋转）
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        angle_rad_to_rotate = math.radians(rot)

        original_corners = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        rotated_corners = [rotate_point(px, py, cx, cy, angle_rad_to_rotate) for px, py in original_corners]

        # 步骤2: 定义旋转框的四条边
        box_sides = [
            (rotated_corners[0], rotated_corners[1]),  # top side
            (rotated_corners[1], rotated_corners[2]),  # right side
            (rotated_corners[2], rotated_corners[3]),  # bottom side
            (rotated_corners[3], rotated_corners[0]),  # left side
        ]

        # 步骤3: 遍历该组的每一条完美线段
        for line in perfect_lines:
            line_p1 = [line[0], line[1]]
            line_p2 = [line[2], line[3]]

            intersections = []
            # 与旋转框的四条边求交点
            for side_p1, side_p2 in box_sides:
                intersection_point = get_line_intersection(line_p1, line_p2, side_p1, side_p2)
                if intersection_point:
                    intersections.append(intersection_point)

            # 按照题目截图中的格式（虽然不明确），我们输出一个包含所有信息的列表项
            # [组号，完美线段，[交点1, 交点2, ...]]
            if intersections:
                # 按照题目截图，它需要一个平铺的列表
                # 例如：[group_id, perfect_line_x1, y1, x2, y2, intersection_x, y]
                # 这里我们先按更结构化的方式展示，方便理解
                # 解释：一条线段和4条边最多有4个交点（通常是2个）
                result.append({
                    "group_id": group_id,
                    "perfect_line": line,
                    "intersections": intersections
                })

    return result


# --- 4. 运行并打印结果 ---

print("--- Question 1 Result ---")
q1_result = solve_q1(mock_data)
print(q1_result)
print("\n" + "=" * 30 + "\n")

print("--- Question 2 Result ---")
q2_result = solve_q2(mock_data)
print(q2_result)
print("\n" + "=" * 30 + "\n")

print("--- Question 3 Result ---")
# Q3依赖Q2的结果和原始数据
q3_result = solve_q3(q2_result, mock_data)
print(q3_result)
print("\n" + "=" * 30 + "\n")