# backend/face/views.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

from .reco import db, User

face_bp = Blueprint('face_bp', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'photo')

@face_bp.route('/list', methods=['GET'])
def list_users():
    print("来活了")
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'name': u.name,
            'student_id': u.student_id,
            'photo_path': f"/static/photo/{os.path.basename(u.photo_path)}"
        } for u in users
    ])

@face_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 删除数据库记录
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@face_bp.route('/upload', methods=['POST'])
def upload_user():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    photo = request.files.get('photo')

    if not all([name, student_id, photo]):
        return jsonify({'error': 'Missing fields'}), 400

    filename = secure_filename(f"{student_id}.png")
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    photo.save(save_path)

    # 存数据库
    user = User(name=name, student_id=student_id, photo_path=save_path)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User uploaded'})
