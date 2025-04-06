import os
import requests
import time
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("ADFI_API_URL")
API_KEY = os.getenv("ADFI_API_KEY")
MODEL_ID = os.getenv("ADFI_MODEL_ID")
MODEL_TYPE = os.getenv("ADFI_MODEL_TYPE")


def classify_hair(image_path: str) -> dict:
    img = Image.open(image_path).convert("RGB")
    MAX_SIZE = 1200
    img = img.resize((min(img.width, MAX_SIZE), min(img.height, MAX_SIZE)), Image.LANCZOS)
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    files = {"image_data": (image_path, img_bytes, "image/png")}
    data = {
        "api_key": API_KEY,
        "aimodel_id": MODEL_ID,
        "model_type": MODEL_TYPE,
        "method": "image"
    }

    res = requests.post(API_URL, files=files, data=data)
    if res.status_code != 200:
        time.sleep(1)
        res = requests.post(API_URL, files=files, data=data)

    token = res.json().get("token")

    data_result = {
        "api_key": API_KEY,
        "aimodel_id": MODEL_ID,
        "model_type": MODEL_TYPE,
        "method": "result",
        "token": token
    }

    for _ in range(10):
        result_res = requests.post(API_URL, data=data_result)
        result_json = result_res.json()
        if not result_json.get("is_processing"):
            break
        time.sleep(1)

# アドバイスを定義
    advice_map = {
    "fusafusa": "頭髪の状態は安定しているようです。このまま、無理のないケアを続けていきましょう🌿",
    "hagekamo": "髪にやさしい習慣を意識してみてください🌷頭皮を優しくマッサージするのもおすすめです",
    "hagedane": "頭髪がお疲れ気味かも。まずは、自分に合ったケアを探すことからはじめてみるのもおすすめです"
    }

    # 整形して返す
    return {
        "result": result_json["top_class_result"]["category_name"],
        "score": round(result_json["top_class_result"]["score"], 3),
        "advice": advice_map.get(result_json["top_class_result"]["category_name"], "診断結果が不明です")
    }