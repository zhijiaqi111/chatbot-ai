from dotenv import load_dotenv
import os
import dashscope
from dashscope import TextEmbedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 加载 .env 文件
load_dotenv()

# 设置 API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 定义三个句子
sentences = [
    "我喜欢吃苹果",
    "我爱吃水果",
    "今天天气真好"
]

# 调用 Embedding API
print("正在获取向量...")
response = TextEmbedding.call(
    model=TextEmbedding.Models.text_embedding_v3,
    input=sentences
)

# 提取向量
vectors = [item['embedding'] for item in response.output['embeddings']]

print(f"向量维度：{len(vectors[0])}")
print("-" * 50)

# 计算相似度矩阵
similarity_matrix = cosine_similarity(vectors)

# 打印结果
print("句子列表：")
for i, s in enumerate(sentences):
    print(f"{i+1}. {s}")

print("\n相似度矩阵：")
print("        句子1    句子2    句子3")
for i in range(3):
    print(f"句子{i+1} ", end="")
    for j in range(3):
        print(f"{similarity_matrix[i][j]:.4f}  ", end="")
    print()

# 单独计算
sim_12 = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
print(f"\n『{sentences[0]}』 和 『{sentences[1]}』 的相似度：{sim_12:.4f}")