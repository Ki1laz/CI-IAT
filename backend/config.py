#!usr/bin/python3
# -*- coding UTF-8 -*-

import os

# 设置密钥和数据库
SECRET_KEY = 'Killa'
SQLALCHEMY_DATABASE_URI = "mysql://root:ACEONE@localhost:3306/chatroom"
SQLALCHEMY_TRACK_MODIFICATIONS = True   # 追踪对象数据库的修改

# 设置用户上传头像的储存文件夹和上传类型
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SESSION_COOKIE_SECURE = 'True'
REMEMBER_COOKIE_SECURE = 'True'
SESSION_COOKIE_HTTPONLY = 'True'
REMEMBER_COOKIE_HTTPONLY = 'True'
SESSION_COOKIE_SAMESITE = 'None'
