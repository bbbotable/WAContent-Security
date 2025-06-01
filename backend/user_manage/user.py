from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == '123456':
        return jsonify({"token": "fake-jwt-token"})
    else:
        return jsonify({"message": "用户名或密码错误"}), 401