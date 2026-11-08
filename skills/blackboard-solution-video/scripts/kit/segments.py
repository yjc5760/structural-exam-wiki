# 講稿（唯一改稿處）：動畫、配音、字幕都讀這個檔。
# 講稿是逐字稿：TTS 一字不漏唸出。為了讓 TTS 讀對：
#   - 數字寫國字（五百、零點二七、百分之七十），字幕端 make_srt.py 會轉回阿拉伯數字
#   - 符號寫成念法（V s、e max、伽瑪 d），再在 SUB_SYMBOLS 設定字幕要顯示成什麼
#   - 停頓標籤 <short pause>／<long pause> 可插在句中，字幕會自動濾掉
# CHAPTERS：黑板左上角章名；BOARD：每段黑板要出現的東西（給寫動畫的人看，不唸）

PROBLEM_ID = "XX-YYYY-N"          # 題號，例：SM-2020-3
TOPIC = "主題"                      # 例：相對密度

# ── 配音 ──
GEMINI_MODEL = "gemini-3.8-flash-tts"       # 省錢可改 gemini-3.8-flash-lite-tts
GEMINI_VOICE = "Charon"                     # 先 python tts_gemini.py --audition A,B,C 試聽再定
GEMINI_STYLE = "patient teacher explaining at a blackboard, clear and steady, medium pace"
AZURE_VOICE = "zh-TW-YunJheNeural"          # 備用
AZURE_RATE = "+0%"

# ── 字幕 ──
# (念法, 顯示) —— 長的放前面
SUB_SYMBOLS = [
    # ("伽瑪 d max", "γd,max"), ("伽瑪 d", "γd"), ("e max", "e_max"), ("V s", "Vs"),
]
# 含數字但不是數值的詞，字幕不要轉成阿拉伯數字（內建已含第一、一樣、三個…，這裡補題目專屬的）
SUB_KEEP = [
    # "兩成七", "三根",
]
# 單位念法 → 顯示（數字後面的單位才會換）
SUB_UNITS = [("毫升", "ml"), ("克", "g")]

CHAPTERS = [
    ("c0", "題目", ["s01"]),
    ("c1", "解法", ["s02", "s03"]),
    ("c2", "總結", ["s04"]),
]

SEGMENTS = [
    ("s01", "這題給了……問的是……"),
    ("s02", "……"),
    ("s03", "……"),
    ("s04", "整理一下。……<short pause> 答案是……"),
]

BOARD = {
    "s01": "題目原文逐句寫出，已知數字圈黃；最後寫「求 …」並框起",
    "s02": "",
    "s03": "",
    "s04": "重點條列逐條寫出，最後答案大字黃框",
}
