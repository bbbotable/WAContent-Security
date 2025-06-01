from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from user_manage import user_bp
from live_detect import liveness_bp
from face import face_bp, init_db as init_face_db  # 导入初始化方法


import os
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # 设置数据库路径（相对于项目根目录）
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'dataset', 'face.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图前，注入 db
    with app.app_context():
        init_face_db(db)  # 给 face_bp 注入 db 并初始化模型表
        db.create_all()   # 确保表都创建了

    # 注册蓝图
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(face_bp, url_prefix='/face')
    app.register_blueprint(liveness_bp, url_prefix='/liveness')

    @app.route('/')
    def index():
        return 'Flask Server Running'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

