import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# 引用你的塔羅牌邏輯核心
from tarot_bot_logic import TarotBotLogic

app = Flask(__name__)

# 從環境變數取得 LINE 的設定
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
    
    # 1. 呼叫邏輯核心處理訊息
    # 這會回傳一個 list，裡面可能包含文字字串，或是 {'type': 'image', ...} 的字典
    reply_list = logic_bot.handle_message(user_id, user_msg)
    
    # 2. 轉換回應格式 (把邏輯端回傳的資料轉成 LINE 訊息物件)
    line_messages = []
    
    for content in reply_list:
        # 判斷是否為圖片字典格式 (來自新版 logic)
        # 格式範例: {'type': 'image', 'url': 'https://...'}
        if isinstance(content, dict) and 'type' in content and content['type'] == 'image':
            img_url = content['url']
            line_messages.append(
                ImageSendMessage(
                    original_content_url=img_url,
                    preview_image_url=img_url
                )
            )
        else:
            # 純文字訊息，強制轉成字串以防萬一
            line_messages.append(TextSendMessage(text=str(content)))
            
    # LINE 限制一次最多 5 則，超過會報錯，這裡做截斷保護
    if len(line_messages) > 5:
        line_messages = line_messages[:5]

    # 3. 回覆給使用者
    line_bot_api.reply_message(event.reply_token, line_messages)

if __name__ == "__main__":
    app.run()