import os
from flask import Flask, request, jsonify
import requests
from threading import Thread

app = Flask(__name__)

LINE_TOKEN = "UKbyHQKiPLZA3+s6jcUWO8S3lNpLrX97T1nMULS1asZn6C/ImazRC9BcyfAYiUwP05IJGdD+ntZBH7nH0XDmG+XGSuDfypOt9cVaA9cICLEmk1snoGWy8MFPYEoi4r7F2jbJU/x61eR70ZqEOAWX4QdB04t89/1O/w1cDnyilFU="
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1298550454736781312/M1oB9ddkCpn0ET1jBuepmGzLxGngIBHHLbBLJrjZic_ddUQF4C8fISx9UP5h7hXW570A"

# 用來請求 LINE 用戶資料的函式
def get_line_user_profile(user_id, group_id=None, room_id=None):
    if group_id:
        url = f"https://api.line.me/v2/bot/group/{group_id}/member/{user_id}"
    elif room_id:
        url = f"https://api.line.me/v2/bot/room/{room_id}/member/{user_id}"
    else:
        url = f"https://api.line.me/v2/bot/profile/{user_id}"
    
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # 返回用戶資料，包含 'displayName'
    else:
        print(f"無法獲取用戶資料，狀態碼: {response.status_code}")
        return None

# 接收來自 LINE 的 Webhook 請求
@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.json
    print("接收到的 LINE 資料:", data)

    if 'events' in data and len(data['events']) > 0:
        event = data['events'][0]
        if event['type'] == 'message' and 'text' in event['message']:
            message = event['message']['text']
            user_id = event['source']['userId']
            group_id = event['source'].get('groupId')
            room_id = event['source'].get('roomId')
            
            print(f"接收到的訊息: {message}, 發送者 ID: {user_id}, 群組 ID: {group_id}, 聊天室 ID: {room_id}")

            # 啟動新執行緒，獲取用戶資料並發送至 Discord
            Thread(target=handle_message, args=(message, user_id, group_id, room_id)).start()

    # 立即返回 200 OK
    return jsonify({'status': 'success'}), 200

# 處理訊息並將訊息發送到 Discord
def handle_message(message, user_id, group_id=None, room_id=None):
    user_profile = get_line_user_profile(user_id, group_id, room_id)
    if user_profile:
        user_name = user_profile['displayName']
        if group_id:
            content = f"來自群組 {group_id} 的 {user_name} ：{message}"
        elif room_id:
            content = f"來自聊天室的 {user_name} ：{message}"
        else:
            content = f"來自 {user_name} ：{message}"
    else:
        content = f"來自未知用戶：{message}"
    
    send_to_discord(content)

# 將處理後的訊息發送到 Discord
def send_to_discord(content):
    data = {
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print('訊息已成功傳送至 Discord!')
    else:
        print(f"傳送失敗，狀態碼：{response.status_code}, 回應內容：{response.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
