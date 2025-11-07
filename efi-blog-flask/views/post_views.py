from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators.roles_required import roles_required
from models.post import Post
from app import db

class PostAPI(MethodView):
    @jwt_required(optional=True)
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get_or_404(post_id)
            return jsonify(post.serialize())
        posts = Post.query.filter_by(is_published=True).all()
        return jsonify([p.serialize() for p in posts])

    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        data = request.get_json()
        new_post = Post(
            title=data["title"],
            content=data["content"],
            user_id=user["id"],
            category_id=data.get("category_id")
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "Post creado", "id": new_post.id}), 201

    @jwt_required()
    def put(self, post_id):
        user = get_jwt_identity()
        post = Post.query.get_or_404(post_id)
        if post.user_id != user["id"] and user["role"] != "admin":
            return jsonify({"error": "No autorizado"}), 403
        data = request.get_json()
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        db.session.commit()
        return jsonify({"message": "Post actualizado"})

    @jwt_required()
    def delete(self, post_id):
        user = get_jwt_identity()
        post = Post.query.get_or_404(post_id)
        if user["role"] != "admin" and post.user_id != user["id"]:
            return jsonify({"error": "No autorizado"}), 403
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post eliminado"})
