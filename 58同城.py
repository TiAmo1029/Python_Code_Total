import requests
import pandas as pd
import time
import json


def scrape_58_rent():
    # 使用你侦察到的、有效的API URL
    api_url = "https://m.58.com/esf-ajax/property/info/list/?city_id=10097&reform=pcfront&PGTID=0d100000-008d-293d-8d40-b47029548e50&ClickID=8&is_default=1&identity=a3c5c4b1c6f4bce0b41675474bf41476&page=2&page_size=25&is_ax_partition=0"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://sz.58.com/ershoufang/',
    }

    all_houses = []

    # 先只爬取前5页进行测试
    for page_num in range(1, 6):
        params = {
            'page': page_num,
        }

        print(f"正在爬取第 {page_num} 页的数据...")

        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            house_list = data.get('data', {}).get('list', [])

            if not house_list:
                print("本页没有数据或已到达末尾，停止爬取。")
                break

            for house in house_list:
                # --- 核心修复：使用全新的、正确的寻宝路线！---

                # 1. 增加一个更严格的“安检”，确保是房源而不是广告
                #    真正的房源，list_type是'1'
                if house.get('list_type') != '1' or 'info' not in house:
                    continue

                info = house['info']

                # 2. 从 'info' 中分别提取 'property' 和 'attribute'
                property_info = info.get('property', {})
                attribute_info = property_info.get('attribute', {})

                # 3. 从各自的区域里，精准地提取数据
                room_num = attribute_info.get('room_num', '?')
                hall_num = attribute_info.get('hall_num', '?')

                house_data = {
                    'Title': property_info.get('title', 'N/A'),
                    'Price': attribute_info.get('price', 'N/A'),
                    'RoomType': f"{room_num}室{hall_num}厅" if room_num != '?' else 'N/A',
                    'Area': attribute_info.get('area_num', 'N/A'),
                    'AvgPrice': attribute_info.get('avg_price', 'N/A'),
                    'HouseAge': attribute_info.get('house_age', 'N/A')
                }
                all_houses.append(house_data)

            time.sleep(2)

        except Exception as e:
            print(f"请求或处理第 {page_num} 页时发生错误: {e}")
            break

    # 保存数据
    if all_houses:
        df = pd.DataFrame(all_houses)
        df.to_csv('58_ershoufang_shenzhen_SUCCESS.csv', index=False, encoding='utf-8-sig')
        print("\n爬取完成！数据已保存到 58_ershoufang_shenzhen_SUCCESS.csv")
    else:
        print("\n未能爬取到任何数据。请检查API的URL和参数是否已更新。")


if __name__ == '__main__':
    scrape_58_rent()