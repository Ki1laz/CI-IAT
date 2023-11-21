#!usr/bin/python3
# -*- coding UTF-8 -*-


from datetime import datetime
from flask_login import UserMixin
from __init import db


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    created_rooms = db.relationship('Room', backref='creator', lazy=True)
    sent_chats = db.relationship('Chat', backref='sender', lazy=True)
    unread_chats = db.relationship('UnreadChat', backref='receiver', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Room(db.Model):
    __tablename__ = 'Room'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(128), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    creator_name = db.Column(db.String(64), nullable=False)
    members = db.relationship('User', secondary='room_members', lazy='subquery',
                              backref=db.backref('rooms', lazy=True))
    create_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_message_time = db.Column(db.DateTime, nullable=True)

    chats = db.relationship('Chat', backref='room', lazy=True)
    unread_chats = db.relationship('UnreadChat', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.room_name}>'


# 添加一个关联表来存储 Room 和 User 之间的关系
room_members = db.Table('room_members',
                        db.Column('room_id', db.Integer, db.ForeignKey('Room.id'), primary_key=True),
                        db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True))


class Chat(db.Model):
    __tablename__ = 'Chat'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    sender_name = db.relationship('User', foreign_keys=[sender_id], backref='sent_chats_relationship')
    room_id = db.Column(db.Integer, db.ForeignKey('Room.id'), nullable=False)
    send_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'sender_id': self.sender_id,
            'sender_name': self.sender_name.username,
            'room_id': self.room_id,
            'send_time': self.send_time.isoformat(),
        }

    def __repr__(self):
        return f'<Chat {self.type}>'


class UnreadChat(db.Model):
    __tablename__ = 'UnreadChat'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    sender_name = db.relationship('User', foreign_keys=[sender_id], backref='unread_chats_relationship')
    room_id = db.Column(db.Integer, db.ForeignKey('Room.id'), nullable=False)
    receive_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'sender_id': self.sender_id,
            'sender_name': self.sender_name.username,
            'room_id': self.room_id,
            'receive_time': self.receive_time.isoformat(),
        }

    def __repr__(self):
        return f'<UnreadChat {self.type}>'
