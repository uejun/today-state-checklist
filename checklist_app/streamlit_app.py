import streamlit as st
import datetime

import gspread
from google.oauth2.service_account import Credentials

# --- Google Sheets 設定 ---
SPREADSHEET_NAME = "Flavor_Today_State_Checklist"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

MEASUREMENT_SLOTS = [
    "3/23（月）10:45（事務所会場）",
    "3/23（月）12:05（事務所会場）",
    "3/23（月）13:25（事務所会場）",
    "3/23（月）14:45（事務所会場）",
    "3/23（月）16:05（事務所会場）",
    "3/24（火）10:00（逗子会場）",
    "3/24（火）11:20（逗子会場）",
    "3/24（火）13:30（逗子会場）",
    "3/24（火）14:50（逗子会場）",
    "3/24（火）16:10（逗子会場）",
    "3/24（火）17:30（逗子会場）",
    "3/25（水）10:00（逗子会場）",
    "3/25（水）11:20（逗子会場）",
    "3/25（水）13:30（逗子会場）",
    "3/25（水）14:50（逗子会場）",
    "3/25（水）16:10（逗子会場）",
    "3/25（水）17:30（逗子会場）",
    "3/26（木）10:00（事務所会場）",
    "3/26（木）11:20（事務所会場）",
    "3/26（木）13:00（事務所会場）",
    "3/26（木）14:20（事務所会場）",
    "3/26（木）15:40（事務所会場）",
    "3/26（木）17:00（事務所会場）",
]

HEADER = [
    "timestamp",
    "email",
    "名前またはID",
    "計測日時",
    "前日の睡眠時間",
    "昨夜の就寝時刻",
    "今朝の起床時刻",
    "前日のアルコール摂取",
    "前日の運動",
    "本日の朝食",
    "本日のカフェイン摂取",
    "本日の喫煙",
    "本日の入浴・サウナ",
    "計測直前の体調",
    "計測直前の症状",
    "本日の服薬",
    "服薬の内容",
    "本日の香り製品の使用",
    "衣類の香り",
    "その他",
]


@st.cache_resource
def get_gspread_client():
    """Streamlit Secrets からサービスアカウント認証情報を読み取り gspread クライアントを返す"""
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )
    return gspread.authorize(creds)


def save_response(data):
    """回答を Google スプレッドシートに追記"""
    client = get_gspread_client()
    sh = client.open(SPREADSHEET_NAME)
    worksheet = sh.sheet1

    # シートが空ならヘッダ行を追加
    if not worksheet.get_all_values():
        worksheet.append_row(HEADER)

    worksheet.append_row(data)


# --- メインUI ---
st.set_page_config(
    page_title="当日の状態確認チェックシート",
    page_icon="📝",
    layout="centered",
)
st.title("香り評価計測　当日の状態確認チェックシート")
st.markdown(
    "本研究では、香りによる心理・生理反応をできるだけ正確に解析するため、"
    "計測当日の生活状況や体調について確認させていただいております。"
)
st.markdown(
    "ご回答いただいた内容は、計測結果の解析の参考情報としてのみ使用いたします。"
)
st.markdown("所要時間：約1〜2分")

st.divider()

# 回答者ID入力（メールアドレスまたは被験者ID）
email = st.text_input(
    "回答者IDを入力してください（メールアドレスまたは被験者ID）",
    placeholder="例：example@email.com または S001",
)

if not email:
    st.warning("メールアドレスまたは被験者IDを入力してから回答を開始してください。")
    st.stop()

# --- セクション1：基本情報 ---
st.header("基本情報")

name_or_id = st.text_input(
    "お名前 または IDナンバー",
    help="一般参加者の方：お名前　／　ロクシタンジャポン社員の方：事前にお知らせしているIDナンバー",
)

measurement_slot = st.selectbox(
    "計測日時",
    options=["選択してください"] + MEASUREMENT_SLOTS,
    help="ご参加いただいた計測日時を選択してください。",
)

# --- セクション2：前日の状態 ---
st.header("前日の状態")

sleep_duration = st.radio(
    "前日の睡眠時間：昨夜の睡眠時間を教えてください。",
    options=["3時間未満", "3〜5時間", "5〜6時間", "6〜7時間", "7〜8時間", "8時間以上"],
    horizontal=True,
)

bedtime = st.text_input(
    "昨夜の就寝時刻",
    placeholder="例：23:30",
)

wakeup_time = st.text_input(
    "今朝の起床時刻",
    placeholder="例：7:00",
)

alcohol = st.radio(
    "前日のアルコール摂取：昨日、アルコールを飲みましたか。",
    options=["飲んでいない", "少量飲んだ", "通常量飲んだ", "多めに飲んだ"],
    horizontal=True,
)

exercise = st.radio(
    "前日の運動：昨日、運動をしましたか。",
    options=[
        "運動していない",
        "軽い運動（散歩・ストレッチなど）",
        "中程度の運動",
        "激しい運動（息が上がる運動）",
    ],
)

# --- セクション3：当日の状態 ---
st.header("当日の状態")

breakfast = st.radio(
    "本日の朝食：今日は朝食を食べましたか。",
    options=["食べていない", "軽めに食べた", "普段どおり食べた"],
    horizontal=True,
)

caffeine = st.radio(
    "本日のカフェイン摂取：本日、カフェインを摂取しましたか。",
    options=[
        "摂取していない",
        "摂取した（計測4時間以上前）",
        "摂取した（計測4時間以内）",
    ],
    help="コーヒー・エナジードリンク・濃いお茶、カフェイン錠など",
)

smoking = st.radio(
    "本日の喫煙：本日、喫煙しましたか。",
    options=[
        "喫煙していない",
        "計測1時間以上前に喫煙した",
        "計測1時間以内に喫煙した",
    ],
)

bathing = st.radio(
    "本日の入浴・サウナ：本日、入浴またはサウナを利用しましたか。",
    options=[
        "入浴していない",
        "入浴した（計測2時間以上前）",
        "入浴した（計測2時間以内）",
        "サウナを利用した",
    ],
)

# --- セクション4：体調 ---
st.header("体調")

condition = st.radio(
    "計測直前の体調：計測直前の体調について教えてください。",
    options=["とても良い", "良い", "普通", "少し不調", "不調"],
    horizontal=True,
)

symptoms = st.multiselect(
    "計測直前の症状：気になる症状があれば選択してください。",
    options=["特になし", "風邪気味", "頭痛", "花粉症・鼻づまり", "倦怠感", "その他"],
    default=["特になし"],
)

medication = st.radio(
    "本日の服薬：本日、薬を服用しましたか。",
    options=["服薬なし", "常用薬のみ服用", "本日追加で薬を服用した"],
)

medication_detail = ""
if medication != "服薬なし":
    medication_detail = st.text_input(
        "服薬の内容：服用した薬があれば教えてください。",
        placeholder="例：頭痛薬、花粉症薬など",
    )

# --- セクション5：香りに関する確認 ---
st.header("香りに関する確認")

fragrance_products = st.multiselect(
    "本日の香り製品の使用：本日使用した香り製品があれば選択してください。",
    options=[
        "使用していない",
        "香水",
        "整髪料",
        "ボディミスト",
        "香りの強いハンドクリーム",
        "香りの強いボディクリーム",
        "その他",
    ],
    default=["使用していない"],
)

clothing_fragrance = st.radio(
    "衣類の香り（柔軟剤・洗剤）：衣類の香りについて教えてください。",
    options=["無香料または弱い香り", "香りあり", "わからない"],
    horizontal=True,
)

# --- セクション6：その他 ---
st.header("その他")

other_notes = st.text_area(
    "その他、通常と異なる体調や状況があればご記入ください。",
    placeholder="例：寝不足、強い花粉症、薬の服用　など",
)

# --- 送信 ---
st.divider()

# バリデーション
can_submit = True
errors = []

if not name_or_id:
    errors.append("お名前またはIDナンバーを入力してください。")
    can_submit = False

if measurement_slot == "選択してください":
    errors.append("計測日時を選択してください。")
    can_submit = False

if errors:
    for e in errors:
        st.warning(e)

if st.button("回答を送信", type="primary", disabled=not can_submit):
    row = [
        datetime.datetime.now().isoformat(),
        email,
        name_or_id,
        measurement_slot,
        sleep_duration,
        bedtime,
        wakeup_time,
        alcohol,
        exercise,
        breakfast,
        caffeine,
        smoking,
        bathing,
        condition,
        ", ".join(symptoms),
        medication,
        medication_detail,
        ", ".join(fragrance_products),
        clothing_fragrance,
        other_notes,
    ]
    try:
        save_response(row)
        st.success("回答を送信しました。ご協力ありがとうございました！")
        st.balloons()
    except Exception as e:
        st.error(f"保存中にエラーが発生しました: {e}")
