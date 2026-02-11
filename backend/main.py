from flask import jsonify
from __init__ import app, socketio

# 注册蓝图
from api.product import product_bp

app.register_blueprint(product_bp)

@app.route('/')
def root():
    return {"message": "比赛平台API"}


@socketio.on('connect')
def handle_connect():
    print('客户端已连接')


@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=8000, allow_unsafe_werkzeug=True)
