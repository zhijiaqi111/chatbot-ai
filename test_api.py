from dotenv import load_dotenv
import os
import dashscope
from dashscope import Generation

# 明确指定 .env 文件路径
load_dotenv(r"D:\PythonProject427\.env")

# 读取并设置 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
dashscope.api_key = api_key

# 验证是否读到（可选，测试用）
print(f"API Key: {api_key[:10]}...")  # 只打印前10位

messages = [
    {'role': 'user', 'content': '你好，请介绍一下你自己'}
]

response = Generation.call(
    model='qwen-turbo',
    messages=messages,
    result_format='message'
)

if response.status_code == 200:
    print("成功！回复：")
    print(response.output.choices[0].message.content)
else:
    print(f'失败：{response.message}')