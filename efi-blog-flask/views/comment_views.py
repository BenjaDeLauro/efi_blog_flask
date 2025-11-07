from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators.roles_required import roles_required
from models.comment import Comment
from models.post import Post
from app import db

class CommentAPI(MethodView):
    @jwt_required(optional=True)
    def get(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id, is_visible=True).all()
        return jsonify([c.serialize() for c in comments])

    @jwt_required()
    def post(self, post_id):
        user = get_jwt_identity()
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        comment = Comment(content=data["content"], user_id=user["id"], post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        return jsonify({"message": "Comentario agregado"}), 201

    @jwt_required()
    def delete(self, comment_id):
        user = get_jwt_identity()
        comment = Comment.query.get_or_404(comment_id)
        if user["role"] in ["admin", "moderator"] or comment.user_id == user["id"]:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({"message": "Comentario eliminado"})
        return jsonify({"error": "No autorizado"}), 403
