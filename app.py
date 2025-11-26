"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import User, Post
from config import Config

# Shared DB extension instance
from database import db

migrate = Migrate()


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure models are imported so SQLAlchemy knows about them
    import models  # noqa: F401

    @app.route("/users", methods=["GET", "POST"])
    def users():
        if request.method == "GET":
            users = User.query.all()
            return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users]), 200

        data = request.get_json() or {}
        username = data.get("username")
        email = data.get("email")
        if not username:
            return jsonify({"message": "Username is required"}), 400

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"id": new_user.id, "username": new_user.username, "email": new_user.email}), 201

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        if request.method == "GET":
            posts = Post.query.all()
            return jsonify([
                {"id": p.id, "title": p.title, "content": p.content, "user_id": p.user_id, "username": p.user.username if p.user else None}
                for p in posts
            ]), 200

        data = request.get_json() or {}
        title = data.get("title")
        content = data.get("content")
        user_id = data.get("user_id")
        if not title or not content or not user_id:
            return jsonify({"message": "Title, content, and user_id are required"}), 400

        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"message": "User not found"}), 400

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({"id": new_post.id, "title": new_post.title, "content": new_post.content, "user_id": new_post.user_id, "username": new_post.user.username}), 201

    return app


# expose db and app at module level
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
