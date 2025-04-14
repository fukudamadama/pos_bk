#-----------------------------------------------------------------
#必要なライブラリのインポート
#-----------------------------------------------------------------

import os
from openai import OpenAI
from datetime import datetime
import json
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
import pytz
from dotenv import load_dotenv
import requests

#-----------------------------------------------------------------
#環境変数の設定
#-----------------------------------------------------------------

# API設定
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

#-----------------------------------------------------------------
#定義された関数群
#-----------------------------------------------------------------

# お題と写真の合致度を点数化し、フィードバックコメントを返す関数
def diagnostic_kamo(hageLevel):
    #OpenAI APIに対するプロンプト
    prompt = f"""
    ユーザーのハゲレベルは「{hageLevel} 」です。
    以下の{hageLevel}ごとの記載内容に基づいて、以下のパターンで文章にアレンジを加えながら
    専門家かつ親しいコーチのように温かみのあるコメントで100文字程度の診断結果を返してください。
    語尾は「カモ」をつけて可愛らしさを演出してください。
    
    {hageLevel}のバリエーション
    1. 「fusafusa」は非常に頭皮・頭髪が生き生きとしており、ハゲてしまう心配がない状態です。
        このユーザーに対しては、良好な現状を褒め、今後も継続できるようなフィードバックをお願いします。
    2. 「hagekamo」はやや地肌が見えており、確実にハゲているわけではないが、少しハゲる危険がある状態です。
        このユーザーに対しては、頭皮・頭髪のケアを進め、心配であれば専門機関を頼ることも視野にフィードバックをお願いします。
    3. 「hagedane」は潔いハゲです。
        ユーザーの内面を褒め、生きていることこそが素晴らしいことであると前向きになれるフィードバックをお願いします。
        専門機関を頼ることで改善可能であることも視野にフィードバックをお願いします。
    
    
    回答は以下のJSON形式で返してください:
    {{"score": 数値, "feedback": "メッセージ"}}
    """

    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは頭髪診療の名医です。"},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )

    return response.choices[0].message.content.strip()