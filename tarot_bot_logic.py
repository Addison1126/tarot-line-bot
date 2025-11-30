import random
import time
from datetime import datetime

# --- 圖片生成器 (修正版) ---
def get_card_image(name_en):
    # [修正] 改用 dummyimage.com，這個服務對 LINE 機器人比較穩定
    # 格式：https://dummyimage.com/寬x高/背景色/文字色.png&text=文字
    clean = name_en.replace(" ", "+")
    return f"https://dummyimage.com/300x500/000000/ffffff.png&text={clean}"

# --- 塔羅牌資料 (完整 22 張大阿爾克那) ---
TAROT_DECK = [
    {"name": "0. 愚者", "score": 0, "name_en": "The Fool", "image_url": get_card_image("The Fool"), "desc_up": "大膽嘗試，踏上新旅程。", "desc_rev": "過於魯莽，計畫不周。"},
    {"name": "I. 魔術師", "score": 1, "name_en": "The Magician", "image_url": get_card_image("The Magician"), "desc_up": "資源俱備，展現能力。", "desc_rev": "缺乏意志，易受欺騙。"},
    {"name": "II. 女祭司", "score": 0, "name_en": "The High Priestess", "image_url": get_card_image("The High Priestess"), "desc_up": "相信直覺，靜心觀察。", "desc_rev": "情緒不穩，封閉內心。"},
    {"name": "III. 皇后", "score": 1, "name_en": "The Empress", "image_url": get_card_image("The Empress"), "desc_up": "豐盛富足，享受生活。", "desc_rev": "過度揮霍，依賴他人。"},
    {"name": "IV. 皇帝", "score": 1, "name_en": "The Emperor", "image_url": get_card_image("The Emperor"), "desc_up": "掌控局勢，建立秩序。", "desc_rev": "固執己見，濫用權力。"},
    {"name": "V. 教皇", "score": 1, "name_en": "The Hierophant", "image_url": get_card_image("The Hierophant"), "desc_up": "貴人相助，心靈指引。", "desc_rev": "過度保守，盲目迷信。"},
    {"name": "VI. 戀人", "score": 1, "name_en": "The Lovers", "image_url": get_card_image("The Lovers"), "desc_up": "重要抉擇，甜蜜結合。", "desc_rev": "關係破裂，溝通不良。"},
    {"name": "VII. 戰車", "score": 1, "name_en": "The Chariot", "image_url": get_card_image("The Chariot"), "desc_up": "克服障礙，衝刺勝利。", "desc_rev": "魯莽失敗，失去方向。"},
    {"name": "VIII. 力量", "score": 1, "name_en": "Strength", "image_url": get_card_image("Strength"), "desc_up": "以柔克剛，內在勇氣。", "desc_rev": "失去信心，軟弱退縮。"},
    {"name": "IX. 隱士", "score": 0, "name_en": "The Hermit", "image_url": get_card_image("The Hermit"), "desc_up": "獨處內省，尋找真理。", "desc_rev": "孤僻逃避，拒絕溝通。"},
    {"name": "X. 命運之輪", "score": 1, "name_en": "Wheel of Fortune", "image_url": get_card_image("Wheel of Fortune"), "desc_up": "順勢而為，轉機已到。", "desc_rev": "時運不濟，錯失良機。"},
    {"name": "XI. 正義", "score": 0, "name_en": "Justice", "image_url": get_card_image("Justice"), "desc_up": "公平公正，理性判斷。", "desc_rev": "不公平待遇，偏見誤判。"},
    {"name": "XII. 吊人", "score": -1, "name_en": "The Hanged Man", "image_url": get_card_image("The Hanged Man"), "desc_up": "換位思考，暫時等待。", "desc_rev": "無謂犧牲，鑽牛角尖。"},
    {"name": "XIII. 死神", "score": -1, "name_en": "Death", "image_url": get_card_image("Death"), "desc_up": "告別過去，迎接新生。", "desc_rev": "抗拒改變，痛苦延長。"},
    {"name": "XIV. 節制", "score": 1, "name_en": "Temperance", "image_url": get_card_image("Temperance"), "desc_up": "平衡協調，自我療癒。", "desc_rev": "失去平衡，過度極端。"},
    {"name": "XV. 惡魔", "score": -1, "name_en": "The Devil", "image_url": get_card_image("The Devil"), "desc_up": "面對慾望，掙脫束縛。", "desc_rev": "沈迷誘惑，無法自拔。"},
    {"name": "XVI. 高塔", "score": -1, "name_en": "The Tower", "image_url": get_card_image("The Tower"), "desc_up": "驟變衝擊，破除假象。", "desc_rev": "勉強支撐，內部崩壞。"},
    {"name": "XVII. 星星", "score": 1, "name_en": "The Star", "image_url": get_card_image("The Star"), "desc_up": "充滿希望，靈感湧現。", "desc_rev": "好高騖遠，失去信心。"},
    {"name": "XVIII. 月亮", "score": -1, "name_en": "The Moon", "image_url": get_card_image("The Moon"), "desc_up": "直覺敏銳，探索潛意識。", "desc_rev": "不安恐懼，受騙上當。"},
    {"name": "XIX. 太陽", "score": 1, "name_en": "The Sun", "image_url": get_card_image("The Sun"), "desc_up": "熱情活力，成功在望。", "desc_rev": "熱度消退，過度自信。"},
    {"name": "XX. 審判", "score": 0, "name_en": "Judgement", "image_url": get_card_image("Judgement"), "desc_up": "重大決定，覺醒時刻。", "desc_rev": "逃避責任，猶豫不決。"},
    {"name": "XXI. 世界", "score": 1, "name_en": "The World", "image_url": get_card_image("The World"), "desc_up": "達成目標，圓滿結局。", "desc_rev": "尚未完成，缺乏臨門一腳。"},
]

# 占卜師設定
TELLERS = {
    "1": {"name": "月光女士", "intro": "親愛的 {name}，讓我們看看「{topic}」的指引...", "style": "healing"},
    "2": {"name": "星辰大師", "intro": "哼，{name}，看清楚「{topic}」的現實吧。", "style": "direct"},
    "3": {"name": "貓咪塔羅", "intro": "喵！{name} 想問「{topic}」？肉球感應中～", "style": "cute"}
}

VALID_ZODIACS = ["牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座"]
user_db = {}
STATE_IDLE = 'IDLE' 
STATE_WAIT_NAME = 'WAIT_NAME'
STATE_WAIT_GENDER = 'WAIT_GENDER'
STATE_WAIT_BIRTHDAY = 'WAIT_BIRTHDAY'
STATE_WAIT_ZODIAC = 'WAIT_ZODIAC'
STATE_WAIT_TELLER = 'WAIT_TELLER' 
STATE_WAIT_TOPIC = 'WAIT_TOPIC'   

class TarotBotLogic:
    def __init__(self):
        pass

    def get_user(self, user_id):
        if user_id not in user_db:
            user_db[user_id] = {'state': STATE_IDLE, 'profile': {}, 'temp_data': {}}
        return user_db[user_id]

    def handle_message(self, user_id, message):
        user = self.get_user(user_id)
        state = user['state']
        text = message.strip()

        # 按鈕指令對應 (模擬 Rich Menu)
        if text == "🔮 開始占卜": text = "占卜"
        elif text == "📖 查看資料": text = "查看資料"
        elif text == "⚙️ 重新註冊": text = "開始註冊"
        elif text == "❓ 使用說明": text = "說明"

        if text in ["取消", "退出"]:
            user['state'] = STATE_IDLE
            user['temp_data'] = {}
            return ["已取消，回到待命狀態。"]

        # --- 狀態機流程：註冊 ---
        if state == STATE_WAIT_NAME:
            user['temp_data']['name'] = text
            user['state'] = STATE_WAIT_GENDER
            return [f"好的 {text}，請問您的性別是？(男/女/其他)"]
        elif state == STATE_WAIT_GENDER:
            user['temp_data']['gender'] = text
            user['state'] = STATE_WAIT_BIRTHDAY
            return ["了解。請輸入您的出生年月日 (格式：YYYY-MM-DD)"]
        elif state == STATE_WAIT_BIRTHDAY:
            try:
                datetime.strptime(text, "%Y-%m-%d")
                user['temp_data']['birthday'] = text
                user['state'] = STATE_WAIT_ZODIAC
                return ["收到。請問您的星座是？"]
            except ValueError:
                return ["日期格式錯誤囉！請依照 YYYY-MM-DD 格式輸入。"]
        elif state == STATE_WAIT_ZODIAC:
            clean_text = text.replace(" ", "")
            if clean_text not in VALID_ZODIACS:
                 if clean_text + "座" in VALID_ZODIACS: clean_text += "座"
                 else: return [f"請輸入正確的星座，如：{random.choice(VALID_ZODIACS)}"]
            user['temp_data']['zodiac'] = clean_text
            user['state'] = STATE_WAIT_TELLER 
            return ["最後，請輸入 1~3 選擇占卜師：\n1. 月光女士\n2. 星辰大師\n3. 貓咪塔羅"]
        elif state == STATE_WAIT_TELLER:
            if text not in TELLERS: return ["請輸入 1, 2 或 3。"]
            user['temp_data']['teller_id'] = text
            user['profile'] = user['temp_data'].copy()
            user['temp_data'] = {}
            user['state'] = STATE_IDLE
            return [f"設定完成！由「{TELLERS[text]['name']}」為您服務。\n請輸入「占卜」開始。"]
        
        # --- 狀態機流程：占卜 ---
        elif state == STATE_WAIT_TOPIC:
            user['state'] = STATE_IDLE
            topic = text if text in ["愛情", "工作", "學業", "健康"] else "整體運勢"
            return self._perform_divination(user, topic)

        # --- IDLE 狀態指令 ---
        if text == "開始註冊":
            user['state'] = STATE_WAIT_NAME
            return ["沒問題，請告訴我，我該如何稱呼您？"]
        elif text == "查看資料":
            p = user['profile']
            if not p: return ["尚未設定資料，請輸入「開始註冊」。"]
            return [f"姓名: {p['name']}\n星座: {p['zodiac']}"]
        elif text in ["占卜", "抽牌"]:
            if not user['profile']: return ["請先輸入「開始註冊」設定資料。"]
            user['state'] = STATE_WAIT_TOPIC
            return ["請輸入您想詢問的方向：\n(愛情 / 工作 / 學業 / 整體運勢)"]
        elif text == "說明":
            return ["請輸入：占卜、查看資料、或開始註冊。"]
        
        return ["我不明白您的意思，請輸入「占卜」或「說明」。"]

    def _perform_divination(self, user, topic):
        p = user['profile']
        teller = TELLERS[p.get('teller_id', "1")]
        
        # 抽 3 張牌
        cards = random.sample(TAROT_DECK, 3)
        results = []
        for card in cards:
            is_rev = random.choice([True, False]) # 50%機率逆位
            name = f"{card['name']} ({'逆' if is_rev else '正'})"
            desc = card['desc_rev'] if is_rev else card['desc_up']
            results.append({"card": card, "name": name, "desc": desc, "rev": is_rev})

        # 組合回覆 List (確保 app.py 能看懂)
        response_data = []

        # 1. 開場白 (Text)
        response_data.append(teller['intro'].format(name=p['name'], topic=topic))

        # 2, 3, 4. 三張圖片 (Image Dict)
        for res in results:
            response_data.append({"type": "image", "url": res['card']['image_url']})

        # 5. 總結分析 (Text)
        # 把三張牌的解釋合併成一則長文字，避免觸發 LINE 的 5 則訊息上限
        summary = f"📊 {topic}運勢分析\n"
        summary += f"──────────\n"
        summary += f"1️⃣ 過去：{results[0]['name']}\n   📝 {results[0]['desc']}\n\n"
        summary += f"2️⃣ 現在：{results[1]['name']}\n   📝 {results[1]['desc']}\n\n"
        summary += f"3️⃣ 未來：{results[2]['name']}\n   📝 {results[2]['desc']}\n"
        summary += f"──────────\n"
        
        # 根據正逆位給予不同建議
        score = sum([-1 if r['rev'] else 1 for r in results])
        if score > 0:
            summary += f"💡 {teller['name']} 建議：\n運勢看起來不錯！保持自信，大膽行動吧！"
        else:
            summary += f"💡 {teller['name']} 建議：\n目前稍有波折，建議放慢腳步，多聽聽朋友意見喔。"

        response_data.append(summary)

        return response_data