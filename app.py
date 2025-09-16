app.py
import os
import requests
import json
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)

# Zoom Meeting SDK認証情報
ZOOM_MEETING_SDK_KEY = os.getenv("ZOOM_MEETING_SDK_KEY")
ZOOM_MEETING_SDK_SECRET = os.getenv("ZOOM_MEETING_SDK_SECRET")
if not ZOOM_MEETING_SDK_KEY or not ZOOM_MEETING_SDK_SECRET:
    # 本番では詳細を出力しない
    print("[WARN] Zoom Meeting SDK credentials are not set.")

# --- ルート定義 ---

@app.route("/")
def index():
    """
    Meeting SDKのウェブページを表示する
    """
    return render_template("meeting.html")

@app.route("/meeting_sdk_token", methods=["POST"])
def generate_meeting_sdk_token():
    """
    クライアント側が使用するためのMeeting SDKトークンを生成する
    """
    # ここはテスト用です。実際にはクライアント側からパラメータを受け取ります。
    meeting_number = "1234567890"  # 参加する会議のID
    role = 0  # 1:ホスト, 0:参加者

    payload = {
        "sdkKey": ZOOM_MEETING_SDK_KEY,
        "mn": meeting_number,
        "role": role,
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()),
        "tokenExp": int((datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp())
    }
    
    try:
        token = jwt.encode(payload, ZOOM_MEETING_SDK_SECRET, algorithm="HS256")
        return jsonify({"token": token, "meeting_number": meeting_number, "sdkKey": ZOOM_MEETING_SDK_KEY})
    except Exception as e:
        print(f"トークン生成エラー: {e}")
        return jsonify({"error": "Failed to generate token"}), 500

# Vercel用のエントリーポイント
def handler(request):
    return app(request.environ, request.start_response)

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')