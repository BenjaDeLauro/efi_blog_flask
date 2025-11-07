from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators.roles_required import roles_required
from models.post import Post
from models.comment import Comment
from models.user import User

class StatsAPI(MethodView):
    @jwt_required()
    @roles_required("moderator", "admin")
    def get(self):
        total_posts = Post.query.count()
        total_comments = Comment.query.count()
        total_users = User.query.count()
        data = {
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_users": total_users
        }
        user = get_jwt_identity()
        if user["role"] == "admin":
            data["posts_last_week"] = Post.query.limit(5).count()
        return jsonify(data)
