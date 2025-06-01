# api/liveness_baidu.py

from flask import Blueprint, request, jsonify
import base64, json, requests

baidu_bp = Blueprint('baidu_bp', __name__)

API_KEY = ""
SECRET_KEY = ""

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")


@baidu_bp.route('/baidu', methods=['POST'])
def liveness_baidu():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    access_token = get_access_token()

    url = f"https://aip.baidubce.com/rest/2.0/face/v3/faceverify?access_token={access_token}"
    payload = json.dumps([{
        "image": image_base64,
        "image_type": "BASE64",
        "liveness_control": "HIGH"
    }])
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, headers=headers, data=payload.encode('utf-8')).json()

    score = resp.get("result", {}).get("face_liveness", 0)
    passed = score >= 0.5

    return jsonify({
        "liveness_passed": passed,
        "face_liveness": score,
        "raw_response": resp
    })
