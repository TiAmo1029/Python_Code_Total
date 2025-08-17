import requests

# ---最佳实践：将不会改变的配置信息作为全局常量---
# 替换成你自己的高德 Key
GAODE_API_KEY = "25a753e0c05dbd60a1c2bfa2323e9937"
GEOCODE_API_URL = "https://restapi.amap.com/v3/geocode/geo"
REVERSE_GEOCODE_API_URL = "https://restapi.amap.com/v3/geocode/regeo"

def geocode(address: str) -> dict or None:
    """
    使用高德API将地址转换为经纬度坐标（地理编码）。
    :param address: 要查询的地址字符串
    :return: 如果成功返回一个包含地址和坐标的字典；否则则返回 None

    """
# 1. 准备请求参数（填写申请表）：
    param = {
        'key': GAODE_API_KEY,
        'address': address
    }

    try:
        # 2. 发送HTTP GET请求，并设置5秒超时
        response = requests.get(GEOCODE_API_URL, params=param, timeout = 5)
        # 检查 HTTP 状态码，如果不是2xx，会抛出异常
        response.raise_for_status()

        # 3. 解析JSON响应
        result = response.json()

        # 4. 检查API业务状态码，并提取数据
        if result['status'] == '1' and int(result['count']) > 0:
            geocode_info = result['geocodes'][0]
            # 提取我们需要的信息
            formatted_address = geocode_info['formatted_address']
            location = geocode_info['location']

            # 返回一个结构清晰的字典
            return {
                'formatted_address' : formatted_address,
                'location' : location
            }

        else:
            # API返回失败或没有找到结果
            print(f"地理编码失败：{result.get('info', '未知错误')}")
            return None

    except requests.exceptions.RequestException as e:
        # 捕获所有requests相关的网络异常
        print(f"网络请求服务：{e}")
        return None

def reverse_geocode(location: str) -> dict or None:
    """
    使用高德API将经纬度坐标转换为地址（逆地理编码）
    :param location: 经纬度字符串，格式为 “lon, lat” 。
    :return: 如果成功，返回一个包含地址的字典，否则返回 None 。
    """

    param = {
        "key": GAODE_API_KEY,
        "location": location
    }

    try:
        response = requests.get(REVERSE_GEOCODE_API_URL, params=param, timeout=5)
        response.raise_for_status()
        result = response.json()

        if result['status'] == '1':
            regeocode_info = result['regeocode']
            formatted_address = regeocode_info['formatted_address']
            return {
                'formatted_address': formatted_address
            }
        else:
            print(f"逆地理编码失败：{result.get('info', '未知错误')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"网络请求错误：{e}")
        return None


# --- 测试代码块 ---
# if __name__ == "__main__" 是一个Python脚本的良好习惯
# 意思是：只有当这个文件被直接运行时，才执行下面的代码
# 如果它被其他文件导入(import)，下面的代码不会执行
if __name__ == "__main__":
    # 测试地理编码
    address_to_check = "杭州市西湖区浙江大学"
    print(f"---正在查询地址：’{address_to_check}'---")
    location_info = geocode(address_to_check)
    if location_info:
        print(f"查询成功！")
        print(f" 格式化地址：{location_info['formatted_address']}")
        print(f" 经纬度：{location_info['location']}")
    else:
        print("查询失败或未找到结果。")

    print("\n" + "=" * 30 + "\n")

    # 测试逆地理编码
    location_to_check = "120.089982, 30.292932"
    print(f"--- 正在查询坐标：‘{location_to_check}'---")
    address_info = reverse_geocode(location_to_check)
    if address_info:
        print("查询成功！")
        print(f" 格式化地址：{address_info['formatted_address']}")
    else:
        print("查询失败或未找到结果。")





