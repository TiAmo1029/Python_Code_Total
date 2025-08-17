import math

# --- 全局辅助函数 ---

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
    核心几何函数：计算两条无限长直线的交点。
    思路：使用标准的线段交点公式求解。
    """
    # 暂时返回None，表示无法计算
    return None


# --- 解答区 ---
def rotate_point(px, py, cx, cy, angle_rad):
    """
    步骤：1.坐标平移 2.应用旋转公式 3.坐标移回
    """
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    p_translated_x = px - cx
    p_translated_y = py - cy
    p_rotated_x = p_translated_x * cos_angle - p_translated_y * sin_angle
    p_rotated_y = p_translated_x * sin_angle + p_translated_y * cos_angle
    final_x = p_rotated_x + cx
    final_y = p_rotated_y + cy
    return [final_x, final_y]


def solve_q1(data):
    """
    摆正旋转框。
    """
    result = {"rotate_box": {}}
    for group_id, box_info_list in data['box'].items():
        box_coords, rot = box_info_list
        x1, y1, x2, y2 = box_coords
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        corners = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]

        # 反向旋转，所以角度为-rot
        angle_rad_to_unrotate = math.radians(-rot)

        unrotated_corners = []
        for px, py in corners:
            new_corner = rotate_point(px, py, cx, cy, angle_rad_to_unrotate)
            unrotated_corners.append(new_corner)
        result["rotate_box"][group_id] = unrotated_corners

    return result


def solve_q2(data):
    """
    第二问：筛选完美线段。
    """
    result = {"perfect_line": {}}
    print("问(2)的逻辑已设计，待具体实现。")
    return result


def solve_q3(perfect_lines_data, original_data):
    """
    第三问：计算延长线与旋转框的交点。
    """
    result = []
    print("问(3)的逻辑已设计，待具体实现。")
    return result


# --- 主函数入口（展示你懂得如何组织代码）---
if __name__ == "__main__":
    # 模拟一份输入数据
    mock_data = {
        "box": {"1": [[100, 100, 200, 150], 30.0]},
        "lines": {"1": [[110, 110, 180, 250]]}
    }

    print("开始执行解题方案...")

    # 执行第一问
    q1_result = solve_q1(mock_data)
    print(q1_result)

    # 执行第二问
    q2_result = solve_q2(mock_data)
    print(q2_result)

    # 执行第三问
    q3_result = solve_q3(q2_result, mock_data)
    print(q3_result)

    print("\n解题代码结构已完成。")
