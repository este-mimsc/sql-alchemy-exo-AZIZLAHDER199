"""Database models for the blog assignment.

The attributes are left intentionally light so students can practice
adding the proper columns, relationships, and helper methods.
"""
<<<<<<< HEAD
from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True)
    posts = db.relationship('Post', backref='user', lazy=True)
=======
from app import db


class User(db.Model):
    """Represents a user who can author posts."""

    __tablename__ = "users"

    # TODO: Add id primary key, username (unique + required), and
    # a relationship to ``Post`` named ``posts``.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)  # Students should customize constraints
>>>>>>> 13d4e0b49c89a211ed69c57b7d44aa1c1316bff1

    def __repr__(self):  # pragma: no cover - convenience repr
        return f"<User {getattr(self, 'username', None)}>"


class Post(db.Model):
    """Represents a blog post written by a user."""

    __tablename__ = "posts"

<<<<<<< HEAD
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
=======
    # TODO: Add id primary key, title, content, foreign key to users.id,
    # and a relationship back to the ``User`` model.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer)
>>>>>>> 13d4e0b49c89a211ed69c57b7d44aa1c1316bff1

    def __repr__(self):  # pragma: no cover - convenience repr
        return f"<Post {getattr(self, 'title', None)}>"
