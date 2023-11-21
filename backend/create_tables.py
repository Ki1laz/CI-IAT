#!usr/bin/python3
# -*- coding UTF-8 -*-

from __init import app, db

# 创建所有表格
with app.app_context():
    db.create_all()
