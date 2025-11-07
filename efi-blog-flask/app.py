from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

# Inicialización de extensiones
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # 🔹 Configuración base
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "supersecretkey"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    db.init_app(app)
    jwt.init_app(app)

    # 🔹 Importar modelos para crear tablas
    from models import user, post, comment, category
    with app.app_context():
        db.create_all()

    # 🔹 Importar vistas
    from views.auth_views import RegisterAPI, LoginAPI
    from views.post_views import PostAPI
    from views.comment_views import CommentAPI
    from views.category_views import CategoryAPI
    from views.user_views import UserAPI
    from views.stats_views import StatsAPI

    # 🔹 Registrar endpoints
    app.add_url_rule("/api/register", view_func=RegisterAPI.as_view("register"))
    app.add_url_rule("/api/login", view_func=LoginAPI.as_view("login"))

    app.add_url_rule("/api/posts", view_func=PostAPI.as_view("posts"), methods=["GET", "POST"])
    app.add_url_rule("/api/posts/<int:post_id>", view_func=PostAPI.as_view("post_detail"), methods=["GET", "PUT", "DELETE"])

    app.add_url_rule("/api/posts/<int:post_id>/comments", view_func=CommentAPI.as_view("comments"), methods=["GET", "POST"])
    app.add_url_rule("/api/comments/<int:comment_id>", view_func=CommentAPI.as_view("comment_detail"), methods=["DELETE"])

    app.add_url_rule("/api/categories", view_func=CategoryAPI.as_view("categories"), methods=["GET", "POST"])
    app.add_url_rule("/api/categories/<int:category_id>", view_func=CategoryAPI.as_view("category_detail"), methods=["PUT", "DELETE"])

    app.add_url_rule("/api/users", view_func=UserAPI.as_view("users"), methods=["GET"])
    app.add_url_rule("/api/users/<int:user_id>", view_func=UserAPI.as_view("user_detail"), methods=["GET", "PATCH", "DELETE"])

    app.add_url_rule("/api/stats", view_func=StatsAPI.as_view("stats"), methods=["GET"])

    # 🔹 Ruta base
    @app.route("/")
    def home():
        return jsonify({"message": "✅ EFI Blog Flask funcionando correctamente"})

    return app


# 🔹 Punto de entrada
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
