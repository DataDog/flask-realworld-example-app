# 可作为独立模块：把此文件中的 blueprint 注册到你的主 app 中（示例在 docs）
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200
