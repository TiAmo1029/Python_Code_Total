import requests
from parsel import Selector
import pandas as pd
import time
import re

def scrape_douban_top250():
    """
    爬取豆瓣读书 Top 250的所有书籍信息。
    :return: .csv
    """
    base_url = "https://book.douban.com/top250?start={}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    all_books_data = []


    # 1.（进阶）翻页爬取
    for i in range(0, 10):
        start_num = i * 25
        url = base_url.format(start_num)
        print(f"正在爬取页面：{url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # 如果状态码不是200，会抛出异常

            selector = Selector(text=response.text)

            # 2. 定位到每一个书籍信息的“大盒子”
            items = selector.css('tr.item')

            # 3. 在每个“大盒子”内部，分别提取信息
            for item in items:
                title = item.css('.p12 a::attr(title)').get()
                # 作者信息比较乱，可能包含很多换行和空格，需要清洗
                author_info = item.css('p.pl::text').get()
                author = author_info.strip().split('/')[0].strip() if author_info else 'N/A'

                rating = item.css('.rating_nums::text').get()
                # 简介可能不存在
                quote = item.css('.inq::text').get()
                comment = item.css('span.pl::text').get()
                if comment:
                    # 使用正则表达式，将一个或多个连续的空白字符(\s+)替换为空
                    cleaned_comment = re.sub(r'\s+', '', comment)
                else:
                    cleaned_comment = 'N/A'

                book_data = {
                    'Title': title,
                    'Author': author,
                    'Rating': rating,
                    'Comment': cleaned_comment,
                    'Quote': quote
                }
                all_books_data.append(book_data)

            # 友好爬虫：每次请求后休息一下
            time.sleep(1)
        except requests.RequestException as e:
            print(f"请求页面失败：{e}")
            continue
    # 4. 使用Pandas存储数据
    df = pd.DataFrame(all_books_data)
    df.to_csv('douban_top250_books.csv', index=False, encoding='utf-8-sig')
    print("\n爬取完成！数据已保存到 douban_top250_books.csv")


if __name__ == '__main__':
    scrape_douban_top250()
