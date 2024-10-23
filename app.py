import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LINE_TOKEN = "UKbyHQKiPLZA3+s6jcUWO8S3lNpLrX97T1nMULS1asZn6C/ImazRC9BcyfAYiUwP05IJGdD+ntZBH7nH0XDmG+XGSuDfypOt9cVaA9cICLEmk1snoGWy8MFPYEoi4r7F2jbJU/x61eR70ZqEOAWX4QdB04t89/1O/w1cDnyilFU="
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1298550454736781312/M1oB9ddkCpn0ET1jBuepmGzLxGngIBHHLbBLJrZic_ddUQF4C8fISx9UP5h7hXW570A"

# 接收來自 LINE 的 Webhook 請求
@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.json
    print("接收到的 LINE 資料:", data)  # 打印收到的 LINE 訊息
    
    # 檢查 data 中是否有 events 且 events 列表不為空
    if 'events' in data and len(data['events']) > 0:
        event = data['events'][0]
        if event['type'] == 'message' and 'text' in event['message']:
            message = event['message']['text']
            print(f"接收到的訊息: {message}")  # 打印接收到的訊息
            # 傳送訊息至 Discord
            send_to_discord(message)
        else:
            print("非文字訊息或未找到訊息內容")
    else:
        print("未接收到有效的 events")
    return jsonify({'status': 'success'}), 200  # 返回 200 狀態碼以避免 500 錯誤

# 將收到的 LINE 訊息發送到 Discord
def send_to_discord(message):
    data = {
        "content": f"LINE 訊息：{message}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print('訊息已成功傳送至 Discord!')
    else:
        print(f"傳送失敗，狀態碼：{response.status_code}, 回應內容：{response.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
