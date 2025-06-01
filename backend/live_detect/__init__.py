
from flask import Blueprint
from .baidu import baidu_bp
from .local import local_bp

liveness_bp = Blueprint('liveness_bp', __name__, url_prefix='/liveness')

# 注册子路由
liveness_bp.register_blueprint(baidu_bp)
liveness_bp.register_blueprint(local_bp)