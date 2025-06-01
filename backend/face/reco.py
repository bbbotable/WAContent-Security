import os
import base64
import numpy as np
import tempfile
import faiss
import mimetypes
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import face_recognition
from werkzeug.utils import secure_filename

face_bp = Blueprint('face_bp', __name__)
db = None
User = None
SignInRecord = None
faiss_index = None
user_id_mapping = {}


def init_db(database):
    global db, User, SignInRecord
    db = database

    class _User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        student_id = db.Column(db.String(20), unique=True)
        face_encoding = db.Column(db.PickleType)
        photo = db.Column(db.LargeBinary)
        mime_type = db.Column(db.String(50))

    class _SignInRecord(db.Model):
        __tablename__ = 'sign_in_records'
        id = db.Column(db.Integer, primary_key=True)
        student_id = db.Column(db.String(20), nullable=True)
        name = db.Column(db.String(50), nullable=True)
        recognition_success = db.Column(db.Boolean, default=False)
        liveness_success = db.Column(db.Boolean, default=False)
        result = db.Column(db.String(100))
        time = db.Column(db.String(50))
        photo = db.Column(db.LargeBinary)
        mime_type = db.Column(db.String(50))

    User = _User
    SignInRecord = _SignInRecord
    db.create_all()
    build_faiss_index()


def build_faiss_index():
    global faiss_index, user_id_mapping
    users = User.query.all()
    face_vectors = []
    user_id_mapping.clear()

    for user in users:
        if user.face_encoding is not None:
            vec = np.array(user.face_encoding, dtype='float32')
            face_vectors.append(vec)
            user_id_mapping[len(face_vectors)-1] = user.id

    if face_vectors:
        face_vectors = np.stack(face_vectors).astype('float32')
        index = faiss.IndexFlatL2(128)
        index.add(face_vectors)
        faiss_index = index
    else:
        faiss_index = None


@face_bp.route('/recognition', methods=['POST'])
def recognition():
    print("\u2705 收到识别请求")
    if 'image' not in request.files:
        return jsonify({'state': 'fail', 'message': 'No image uploaded'})

    image_file = request.files['image']
    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, secure_filename(image_file.filename))
    image_file.save(image_path)

    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
    except Exception as e:
        os.remove(image_path)
        return jsonify({'state': False, 'message': f'Error processing image: {str(e)}'})

    if not face_encodings:
        os.remove(image_path)
        return jsonify({'state': False, 'message': '未识别到人脸'})

    input_encoding = face_encodings[0]
    input_vec = np.array(input_encoding, dtype='float32').reshape(1, -1)

    if faiss_index is None:
        os.remove(image_path)
        return jsonify({'state': False, 'message': 'No users in database'})

    D, I = faiss_index.search(input_vec, k=1)
    nearest_index = I[0][0]
    distance = D[0][0]

    print(f"FAISS最近距离: {distance}")

    if distance < 0.45:
        user_id = user_id_mapping[nearest_index]
        user = User.query.get(user_id)
        os.remove(image_path)
        return jsonify({
            'state': True,
            'message': 'Face recognized',
            'name': user.name,
            'student_id': user.student_id
        })
    else:
        os.remove(image_path)
        return jsonify({'state': False, 'message': 'Face not recognized'})


@face_bp.route('/upload', methods=['POST'])
def upload_user():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    photo = request.files.get('photo')

    if not all([name, student_id, photo]):
        return jsonify({'error': 'Missing fields'}), 400

    photo_bytes = photo.read()
    mime_type, _ = mimetypes.guess_type(photo.filename)
    if not mime_type:
        mime_type = 'application/octet-stream'

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(photo_bytes)
        temp_path = tmp.name

    image = face_recognition.load_image_file(temp_path)
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        return jsonify({'error': 'No face found in uploaded photo'}), 400

    face_encoding = face_encodings[0]

    user = User(
        name=name,
        student_id=student_id,
        face_encoding=face_encoding,
        photo=photo_bytes,
        mime_type=mime_type
    )
    db.session.add(user)
    db.session.commit()
    build_faiss_index()

    return jsonify({'message': 'User uploaded'})


@face_bp.route('/list', methods=['GET'])
def list_users():
    print(" 获取用户列表")
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'name': u.name,
            'student_id': u.student_id,
            'photo_base64': base64.b64encode(u.photo).decode('utf-8') if u.photo else None
        } for u in users
    ])


@face_bp.route('/signinrecord', methods=['GET'])
def list_signin():
    print(" 获取签到信息列表")
    signins = SignInRecord.query.all()
    return jsonify([
        {
            'id': signin.id,
            'name': signin.name,
            'student_id': signin.student_id,
            'photo_base64': base64.b64encode(signin.photo).decode('utf-8') if signin.photo else None,
            'recognition_success': signin.recognition_success,
            'liveness_success': signin.liveness_success,
            'result': signin.result,
            'time': signin.time,
            'mime_type': signin.mime_type
        } for signin in signins
    ])


@face_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    build_faiss_index()
    return jsonify({'message': 'User deleted'})


@face_bp.route('/deletesign/<int:user_id>', methods=['DELETE'])
def delete_sign(user_id):
    user = SignInRecord.query.get(user_id)
    if not user:
        return jsonify({'error': 'Sign not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Sign deleted'})


@face_bp.route('/record', methods=['POST'])
def save_signin_record():
    print(" 接收到签到记录")
    image = request.files.get('image')
    result = request.form.get('result', '')
    time = request.form.get('time', '')
    recognition_success = request.form.get('recognition_success', 'false') == 'true'
    liveness_success = request.form.get('liveness_success', 'false') == 'true'
    student_id = request.form.get('student_id')
    name = request.form.get('name')

    if not image or not result or not time:
        return jsonify({'error': '缺少必要字段'}), 400

    image_bytes = image.read()
    mime_type = image.mimetype or 'application/octet-stream'

    record = SignInRecord(
        student_id=student_id if recognition_success else None,
        name=name if recognition_success else None,
        recognition_success=recognition_success,
        liveness_success=liveness_success,
        result=result,
        time=time,
        photo=image_bytes,
        mime_type=mime_type
    )
    db.session.add(record)
    db.session.commit()
    print("签到记录已保存")
    return jsonify({'message': '签到记录已保存'})


@face_bp.route('/stats')
def stats_by_day():
    from datetime import datetime
    from collections import defaultdict

    stats = defaultdict(lambda: {
        'expected': 0,
        'actual_users': set(),
        'earliest_time': None,
        'earliest_name': None,
    })

    all_records = db.session.query(SignInRecord).all()

    for r in all_records:
        try:
            r_time = datetime.strptime(r.time, '%Y-%m-%d %H:%M:%S')
            day = r_time.strftime('%Y-%m-%d')
            if r.recognition_success:
                if r.student_id not in stats[day]['actual_users']:
                    stats[day]['actual_users'].add(r.student_id)
                    print(f"➕ 实到: {r.name} {r.student_id} @ {r_time}")
                if stats[day]['earliest_time'] is None or r_time < stats[day]['earliest_time']:
                    stats[day]['earliest_time'] = r_time
                    stats[day]['earliest_name'] = r.name
        except Exception as e:
            print(f"❌ 时间解析失败: {r.time} -> {e}")
            continue

    for day in stats:
        stats[day]['expected'] = 40

    print('✅ 获取成功，总天数:', len(stats))
    return jsonify([
        {
            'date': day,
            'expected': s['expected'],
            'actual': len(s['actual_users']),
            'earliest_time': s['earliest_name']
        }
        for day, s in sorted(stats.items())
    ])
