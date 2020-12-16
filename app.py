from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Resource, reqparse, abort, fields, marshal_with, Api
from flask_sqlalchemy import SQLAlchemy
from labapp.model import *


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/laba5'
db = SQLAlchemy(app)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("login", type=str, help="login of the user", required=True)
user_put_args.add_argument("hash_password", type=str, help="password of the user", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("login", type=str, help="login of the user")
user_update_args.add_argument("hash_password", type=str, help="password of the user")

user_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'hash_password': fields.String,
}

playlist_put_args = reqparse.RequestParser()
playlist_put_args.add_argument("name", type=str, help="name of the playlist", required=True)
playlist_put_args.add_argument("owner_id", type=int, help="owner of the playlist", required=True)

playlist_update_args = reqparse.RequestParser()
playlist_update_args.add_argument("name", type=str, help="name of the playlist")
playlist_update_args.add_argument("owner_id", type=int, help="owner of the playlist")

playlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'owner_id': fields.Integer,
}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("url", type=str, help="Url of the video", required=True)
video_put_args.add_argument("playlist_id", type=int, help="owner of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("url", type=str, help="name of the playlist")
video_update_args.add_argument("playlist_id", type=int, help="owner of the video")

video_fields = {
    'id': fields.Integer,
    'url': fields.String,
    'playlist_id': fields.Integer,
}


class UserView(Resource):
    @marshal_with(user_fields)
    def get(self):
        result = User.query.all()
        if not result:
            abort(404, message="Could not find user with that id")

        return result

    @marshal_with(user_fields)
    def post(self):
        args = user_put_args.parse_args()
        user = User(login=args['login'], hash_password=User.set_hash(args['hash_password']))

        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(404, message="Login is already exist")

        return user, 201


class UserDetailView(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        return result

    @marshal_with(user_fields)
    def post(self, user_id):
        args = user_put_args.parse_args()
        result = User.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User id taken...")

        user = User(id=user_id, login=args['login'], hash_password=User.set_hash(args['password']))

        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(404, message="Login is already exist")

        return user, 201

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_update_args.parse_args()
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            abort(404, message="User doesn't exist, cannot update")

        if args['login']:
            user.login = args['login']
        if args['hash_password']:
            user.hash_password = args['hash_password']

        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(404, message="Login is already exist")

        return user

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User doesn't exist")

        user = db.session.merge(user)
        db.session.delete(user)
        db.session.commit()

        return '', 204


class PlayListView(Resource):
    @marshal_with(playlist_fields)
    def get(self):
        playlists = PlayList.query.all()
        if not playlists:
            abort(404, message="Could not find playlist with that id")

        return playlists

    @marshal_with(playlist_fields)
    def post(self):
        args = playlist_put_args.parse_args()
        playlist = PlayList(name=args['name'], owner_id=args['owner_id'])

        try:
            db.session.add(playlist)
            db.session.commit()
        except:
            abort(404, message="Owner id doesn't exist")

        return playlist, 201


class PlayListDetailView(Resource):
    @marshal_with(playlist_fields)
    def get(self, playlist_id):
        playlist = PlayList.query.filter_by(id=playlist_id).first()
        if not playlist:
            abort(404, message="Could not find playlist with that id")
        return playlist

    @marshal_with(playlist_fields)
    def post(self, playlist_id):
        args = playlist_put_args.parse_args()
        playlist = User.query.filter_by(id=playlist_id).first()
        if playlist:
            abort(409, message="Playlist id taken...")

        playlist = PlayList(name=args['name'], owner_id=args['owner_id'])

        try:
            db.session.add(playlist)
            db.session.commit()
        except:
            abort(404, message="Owner id doesn't exist")

        return playlist, 201

    @marshal_with(playlist_fields)
    def put(self, playlist_id):
        args = playlist_update_args.parse_args()
        playlist = db.session.query(PlayList).filter_by(id=playlist_id).first()
        if not playlist:
            abort(404, message="Playlist doesn't exist, cannot update")

        if args['name']:
            playlist.name = args['name']
        if args['owner_id']:
            playlist.owner_id = args['owner_id']

        db.session.add(playlist)
        db.session.commit()

        return playlist, 201

    def delete(self, playlist_id):
        playlist = PlayList.query.filter_by(id=playlist_id).first()
        if not playlist:
            abort(404, message="Playlist doesn't exist")

        playlist = db.session.merge(playlist)
        db.session.delete(playlist)
        db.session.commit()

        return 'Deleted', 204


class VideoView(Resource):
    @marshal_with(video_fields)
    def get(self):
        videos = Video.query.all()
        if not videos:
            abort(404, message="Could not find video with that id")

        return videos

    @marshal_with(video_fields)
    def post(self):
        args = video_put_args.parse_args()
        video = Video(url=args['url'], playlist_id=args['playlist_id'])

        try:
            db.session.add(video)
            db.session.commit()
        except:
            abort(404, message="Owner id doesn't exist")

        return video, 201


class VideoDetailView(Resource):
    @marshal_with(video_fields)
    def get(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Could not find video with that id")
        return video

    @marshal_with(video_fields)
    def post(self, video_id):
        args = video_put_args.parse_args()
        video = User.query.filter_by(id=video_id).first()
        if video:
            abort(409, message="Video id taken...")

        video = Video(url=args['url'], playlist_id=args['playlist_id'])

        try:
            db.session.add(video)
            db.session.commit()
        except:
            abort(404, message="Owner id doesn't exist")

        return video, 201

    @marshal_with(video_fields)
    def put(self, video_id):
        args = video_update_args.parse_args()
        video = db.session.query(Video).filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesn't exist, cannot update")

        if args['url']:
            video.url = args['url']
        if args['playlist_id']:
            video.playlist_id = args['playlist_id']

        db.session.add(video)
        db.session.commit()

        return video, 201

    def delete(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesn't exist")

        video = db.session.merge(video)
        db.session.delete(video)
        db.session.commit()

        return 'Deleted', 204


api.add_resource(UserDetailView, "/user/<int:user_id>")
api.add_resource(UserView, "/user")

api.add_resource(PlayListDetailView, "/playlist/<int:playlist_id>")
api.add_resource(PlayListView, "/playlist")

api.add_resource(VideoDetailView, "/video/<int:video_id>")
api.add_resource(VideoView, "/video")

if __name__ == "__main__":
    app.run(debug=True)
