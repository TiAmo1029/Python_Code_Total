import requests

# 创建一个会话对象
s = requests.session()

# 第一次请求，比如登陆，服务器会返回一个cookie
# 这里用一个公共测试网站 httpbin.org 来模拟
s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')

# 第二次请求，用同一个 s 对象，它会自动带上刚才的 cookie
response = s.get('https://httpbin.org/cookies')

print(response.json())
# 输出会是: {"cookies": {"sessioncookie": "123456789"}}
# 证明cookie被成功保持和发送了