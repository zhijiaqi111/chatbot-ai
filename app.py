from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# 从环境变量中获取 API Key (Railway 上已经设置好了)
client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 最简单的 HTML 界面
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI 聊天机器人</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; background: #a8e6cf; padding: 20px; }
        .chat-box { max-width: 500px; margin: auto; background: white; border-radius: 10px; padding: 20px; }
        .message { margin: 10px 0; }
        .user { text-align: right; color: blue; }
        .ai { text-align: left; color: green; }
        textarea { width: 80%; }
    </style>
</head>
<body>
    <div class="chat-box">
        <h2>AI 聊天机器人</h2>
        <div id="chat-log">
            <div class="ai">你好！有什么可以帮你的吗？</div>
        </div>
        <textarea id="user-input" rows="2" placeholder="输入你的问题..."></textarea>
        <button onclick="send()">发送</button>
    </div>
    <script>
        async function send() {
            let input = document.getElementById('user-input');
            let msg = input.value;
            if (!msg) return;

            let chatLog = document.getElementById('chat-log');
            chatLog.innerHTML += '<div class="user">' + msg + '</div>';
            input.value = '';

            let response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            });
            let data = await response.json();
            chatLog.innerHTML += '<div class="ai">' + data.reply + '</div>';
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return HTML


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"错误: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))