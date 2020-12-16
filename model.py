from app import db, bcrypt

# alembic revision --autogenerate -m "initial"


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

    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = db.relationship(User, backref="playlists", lazy="joined")

    def __repr__(self):
        return f"Playlist(name = {name}, owner_id = {owner_id}, owner = {owner})"


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100))

    playlist_id = db.Column(db.Integer, db.ForeignKey(PlayList.id))
    playlist = db.relationship(PlayList, backref="videos", lazy="joined")

    def __repr__(self):
        return f"Video(id = {id}, url = {url}, playlist_id = {playlist_id})"

