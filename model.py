from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# alembic revision --autogenerate -m "initial"

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False, unique=True)
    hash_password = db.Column(db.String, nullable=False)

    def set_hash(password):
        return bcrypt.generate_password_hash(password)

    def __repr__(self):
        return f"User(login = {login}, password = {password})"


class PlayList(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    is_private = db.Column(db.Boolean)

    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = db.relationship(User, backref="playlists", lazy="joined")

    videos = db.relationship("Video", secondary="orders")

    def __repr__(self):
        return f"Playlist(name = {name}, owner_id = {owner_id}, owner = {owner})"


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100))

    playlists = db.relationship("PlayList", secondary="orders")

    def __repr__(self):
        return f"Video(id = {id}, url = {url})"


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))

    playlist = db.relationship(PlayList, backref=db.backref("orders", cascade="all, delete-orphan"))
    video = db.relationship(Video, backref=db.backref("orders", cascade="all, delete-orphan"))
