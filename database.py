from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    xp = db.Column(
        db.Integer,
        default=0
    )

    level = db.Column(
        db.String(50),
        default="Beginner"
    )

    profile_picture = db.Column(
        db.String(200),
        default="default.png"
    )

    def __repr__(self):
        return f"<User {self.username}>"