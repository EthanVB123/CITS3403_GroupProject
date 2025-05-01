from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    passwordHash = db.Column(db.String(256), nullable=False)
    userScore = db.Column(db.Integer, nullable=False, default=0)


class Friends(db.Model):
    __tablename__ = 'friends'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    