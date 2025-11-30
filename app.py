import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# 引用你的塔羅牌邏輯核心
from tarot_bot_logic import TarotBotLogic

app = Flask(__name__)

# 從環境變數取得 LINE 的設定 (等一下會在 Render 設定)
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

# 初始化塔羅牌機器人邏輯
logic_bot = TarotBotLogic()

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 表頭
    signature = request.headers['X-Line-Signature']
    # 取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽章並處理事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_msg = event.message.text
    
    # 1. 呼叫你的邏輯核心處理訊息
    #這會回傳一個 list，例如 ["正在洗牌...", "結果是..."]
    reply_list = logic_bot.handle_message(user_id, user_msg)
    
    # 2. 轉換回應格式 (把文字轉成 LINE 的訊息物件)
    line_messages = []
    
    for text_res in reply_list:
        # 簡單的判斷：如果是圖片連結 (根據你的邏輯檔格式)
        if "[🖼️ 圖片]:" in text_res:
            # 提取網址 (這是一個簡易做法，對應你的邏輯輸出)
            # 格式: [🖼️ 圖片]: https://...
            try:
                img_url = text_res.split(": ")[1].strip()
                # 圖片與預覽圖都用同一個
                line_messages.append(ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
            except:
                pass # 解析失敗就跳過
        else:
            # 一般文字訊息
            line_messages.append(TextSendMessage(text=text_res))
            
    # LINE 一次最多只能回覆 5 則訊息，做個保護
    if len(line_messages) > 5:
        line_messages = line_messages[:5]

    # 3. 回覆給使用者
    line_bot_api.reply_message(event.reply_token, line_messages)

if __name__ == "__main__":
    app.run()