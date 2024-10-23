from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LINE_TOKEN = "UKbyHQKiPLZA3+s6jcUWO8S3lNpLrX97T1nMULS1asZn6C/ImazRC9BcyfAYiUwP05IJGdD+ntZBH7nH0XDmG+XGSuDfypOt9cVaA9cICLEmk1snoGWy8MFPYEoi4r7F2jbJU/x61eR70ZqEOAWX4QdB04t89/1O/w1cDnyilFU="
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1298550454736781312/M1oB9ddkCpn0ET1jBuepmGzLxGngIBHHLbBLJrjZic_ddUQF4C8fISx9UP5h7hXW570A"

# 接收來自 LINE 的 Webhook 請求
@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.json
    # 確認有接收到 LINE 的事件
    if 'events' in data:
        event = data['events'][0]
        if event['type'] == 'message' and 'text' in event['message']:
            message = event['message']['text']
            # 傳送訊息至 Discord
            send_to_discord(message)
    return jsonify({'status': 'success'})

# 將收到的 LINE 訊息發送到 Discord
def send_to_discord(message):
    data = {
        "content": f"LINE 訊息：{message}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print('訊息已成功傳送至 Discord!')
    else:
        print(f"傳送失敗，狀態碼：{response.status_code}")

if __name__ == "__main__":
    # 本地測試時使用，執行伺服器
    app.run(debug=True, port=5000)