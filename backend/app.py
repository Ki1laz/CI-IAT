#!usr/bin/python3
# -*- coding UTF-8 -*-
import datetime
import os
import uuid

from concurrent.futures import ThreadPoolExecutor

from flask import request, jsonify, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import join_room, send, emit
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

from __init import app, db, socketio, login_manager
from models import Room, User, Chat, UnreadChat


Threadpool = ThreadPoolExecutor(max_workers=10)


# 设置首页
@app.route("/")
def index():
    return jsonify({"message": "welcome to CI-IAT"})


# 设置注册页
@app.route("/register", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def register():
    if request.method == "GET":
        return "hello"
    else:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirmpasswd = data.get('confirmpasswd')
        duplicate_user = User.query.filter_by(username=username).first()
        # 检验输入用户名和密码是否为空
        if not username or not password:
            return jsonify({"message": "please input username and password"})
        # 查找数据库中是否存在同名用户
        elif duplicate_user:
            return jsonify({"message": "the username has been used"})
        # 判断用户注册信息是否合法
        elif isinstance(username, str) and not isinstance(password, str):
            if len(username) < 6 or len(username) > 12:
                return jsonify({"message": "The username is invalid"})
            elif len(password) < 6 or len(password) > 20:
                return jsonify({"message": "the password is invalid"})
        elif confirmpasswd != password:
            return jsonify({"message": "confirmpasswd must be same as password"})
        else:
            hashed_password = generate_password_hash(password, method='scrypt')
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return jsonify({"message": "User has registered successfully"})


# 回调函数,根据id加载用户对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# 设置登录页
@app.route("/login", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def login():
    if request.method == "GET":
        return "hello"
    else:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # 检验输入用户名和密码是否为空
        if not username or not password:
            return jsonify({"message": "Please input your username and password"})
        # 查找数据库中是否存在该用户
        registered_user = User.query.filter_by(username=username).first()
        if registered_user and check_password_hash(registered_user.password_hash, password):
            login_user(registered_user)
            return jsonify({"message": "Login successfully"})
        else:
            return jsonify({"message": "The user does not exist"})


# 获取登录用户信息
@app.route("/get_info")
@cross_origin(supports_credentials=True)
@login_required
def get_info():
    user = User.query.filter_by(id=current_user.id).first()
    if user:
        user_info = {
            'id': user.id,
            'username': user.username
        }
        return jsonify(user_info)
    else:
        return jsonify({'message': 'User not found'})


# 设置注销页
@app.route("/logout", methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required
def logout():
    logout_user()
    return jsonify({"message": "return to index page"})


# 设置头像修改页
def allowed_avatar(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_avatar(file, filename):
    unique_filename = uuid.uuid4().hex + '_' + filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
    return unique_filename


def save_avatar_async(file, filename):
    return Threadpool.submit(save_avatar, file, filename).result()


@app.route("/modify_avatar", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def modify_avatar():
    if "file" not in request.files:
        flash("No file part")
    file = request.files.get('file')
    if file is None or file.filename == '':
        return jsonify({"message": "No selected file"})
    if file and allowed_avatar(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = save_avatar_async(file, filename)
        user = User.query.filter_by(username=current_user.username).first()
        user.avatar = unique_filename
        db.session.commit()
        return jsonify({"message": "Upload avatar successfully"})
    else:
        return jsonify({"message": "Invalid file type"})


# 获取用户头像
@app.route("/get_avatar")
@cross_origin(supports_credentials=True)
@login_required
def get_avatar():
    if current_user.avatar:
        avatar_url = url_for("static", filename=f"uploads/{current_user.avatar}")
        return jsonify({"avatar": avatar_url})
    else:
        return jsonify({"message": "User does not have an avatar"})


# 获取用户加入聊天室
@app.route("/room_list")
@cross_origin(supports_credentials=True)
@login_required
def room_list():
    chatroom_list = current_user.rooms
    chatrooms = [{"id": room.id, "room_name": room.room_name} for room in chatroom_list]
    return jsonify(chatrooms)


# 创建聊天室
@app.route("/create_room", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def create_room():
    if request.method == "POST":
        data = request.get_json()
        room_name = data.get("room_name")
        if not room_name:
            return jsonify({"message": "please input room name"})
        else:
            creator_id = current_user.id
            creator_name = current_user.username
            new_room = Room(room_name=room_name, creator_id=creator_id, creator_name=creator_name)
            new_room.members.append(current_user)
            db.session.add(new_room)
            db.session.commit()
            return jsonify({"message": "Create chatroom successfully"})


# 删除聊天室
@app.route("/delete_room", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def delete_room():
    if request.method == "POST":
        data = request.get_json()
        room_id = data.get("room_id")
        room_name = data.get("room_name")
        room = Room.query.filter_by(id=room_id, room_name=room_name).first()
        if room:
            if current_user.id == room.creator_id and current_user.username == room.creator_name:
                db.session.delete(room)
                db.session.commit()
                return jsonify({"message": "Chatroom has been deleted successfully"})
            else:
                return jsonify({"message": "Only the Chatroom creator can delete Chatroom"})
        else:
            return jsonify({"message": "The chatroom does not exist"})


# 加入聊天室
@app.route("/join_room", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required
def join():
    data = request.get_json()
    room_name = data.get("room_name")
    # 获取聊天室对象
    room = Room.query.filter_by(room_name=room_name).first()
    if room and current_user not in room.members:
        # 将用户添加到聊天室的成员列表
        room.members.append(current_user)
        db.session.commit()
        join_room(room)
        send(f'{current_user.username} has entered the room.', to=room)
        return jsonify({"message": "Joined the room successfully"})
    else:
        return jsonify({"message": "The room does not exist or you are already a member"})


# 发送聊天信息
def handle_message(message, room_id, sender_id):
    try:
        print(message)
        print(sender_id)
        print(room_id)
        with app.app_context():
            chat = Chat(type='text', content=message, sender_id=sender_id, room_id=room_id)
            db.session.add(chat)
            db.session.commit()
            serialized_message = chat.serialize()
            socketio.emit("response", {"message": serialized_message})
    except Exception as e:
        print(f"Error handling message: {e}")


@socketio.on("message")
def send_message(data):
    message = data["message"]
    room_id = data["room_id"]
    sender_id = data["sender_id"]
    Threadpool.submit(lambda: handle_message(message, room_id, sender_id))


# 查看聊天记录
@socketio.on("check")
def check_chat(data):
    room_id = data.get("room_id")
    chat_history = Chat.query.filter_by(room_id=room_id).order_by(Chat.send_time).all()
    serialized_history = [chat.serialize() for chat in chat_history]
    socketio.emit('chat_history', {'room_id': room_id, 'history': serialized_history})
