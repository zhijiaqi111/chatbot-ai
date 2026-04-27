from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

api_key = os.environ.get("DASHSCOPE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI 聊天机器人</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #a8e6cf 0%, #d4fc79 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .chat-container {
            width: 500px;
            max-width: 100%;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .chat-header {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-header h1 {
            font-size: 1.5rem;
        }
        .chat-header p {
            font-size: 0.8rem;
            opacity: 0.9;
        }
        .chat-box {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f0fff4;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
        }
        .user-message {
            justify-content: flex-end;
        }
        .ai-message {
            justify-content: flex-start;
        }
        .message-content {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 20px;
            word-wrap: break-word;
        }
        .user-message .message-content {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }
        .ai-message .message-content {
            background: white;
            color: #2c3e50;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border: 1px solid #d4fc79;
        }
        .input-area {
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        .input-area input {
            flex: 1;
            padding: 12px;
            border: 2px solid #d4fc79;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
        }
        .input-area input:focus {
            border-color: #2ecc71;
        }
        .input-area button {
            margin-left: 10px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
        }
        .input-area button:hover {
            transform: scale(1.02);
        }
        .chat-box::-webkit-scrollbar {
            width: 6px;
        }
        .chat-box::-webkit-scrollbar-track {
            background: #e0e0e0;
            border-radius: 10px;
        }
        .chat-box::-webkit-scrollbar-thumb {
            background: #2ecc71;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🌿 AI 聊天机器人</h1>
            <p>基于阿里云百炼 · qwen-turbo</p>
        </div>
        <div class="chat-box" id="chat-box">
            <div class="message ai-message">
                <div class="message-content">🌱 你好！我是 AI 助手，有什么可以帮你的吗？</div>
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="输入你的问题..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">发送 ✨</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += '<div class="message user-message"><div class="message-content">' + escapeHtml(message) + '</div></div>';
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            const loadingId = Date.now();
            chatBox.innerHTML += '<div class="message ai-message" id="loading-' + loadingId + '"><div class="message-content">🌱 思考中...</div></div>';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                document.getElementById('loading-' + loadingId).remove();
                chatBox.innerHTML += '<div class="message ai-message"><div class="message-content">' + escapeHtml(data.reply) + '</div></div>';
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (error) {
                document.getElementById('loading-' + loadingId).remove();
                chatBox.innerHTML += '<div class="message ai-message"><div class="message-content">❌ 出错了，请重试</div></div>';
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
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
        return jsonify({"reply": f"服务器错误: {str(e)}"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)