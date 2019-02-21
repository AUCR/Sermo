"""AUCR Chat plugin database table model handler."""
#  coding=utf-8
import udatetime
from aucr_app import db


class Rooms(db.Model):
    """Chat Database Table."""

    __tablename__ = "chat_rooms"
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(64), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """AUCR chat plugin return messages."""
        return '<ChatRooms {}>'.format(self.room_name)


class Chat(db.Model):
    """Chat Database Table."""

    __searchable__ = ['id', 'author', 'message', 'room', 'timestamp']
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), db.ForeignKey('user.username'))
    message = db.Column(db.String(512), index=True)
    room_name = db.Column(db.String(64), db.ForeignKey('chat_rooms.room_name'))
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """AUCR chat plugin return messages."""
        return '<Chat {}>'.format(self.message)
