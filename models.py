from sqlalchemy import orm

from database import Base
from app import db


class Users(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.Integer)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


class PlayList(Base):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<User %r>' % (self.name)


class Video(Base):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(50))
    playlist_id = db.Column(db.Integer, db.ForeignKey(PlayList.id))

    playlist = db.relationship(PlayList, backref='playlist', lazy='joined')

    def __init__(self, url=None, playlist=None):
        self.url = url
        self.playlist = playlist

    def __repr__(self):
        return '<User %r>' % self.url



