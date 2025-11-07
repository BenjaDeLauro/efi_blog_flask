from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators.roles_required import roles_required
from models.user import User
from app import db

class UserAPI(MethodView):
    @jwt_required()
    @roles_required("admin")
    def get(self):
        users = User.query.all()
        return jsonify([u.serialize() for u in users])

    @jwt_required()
    def get(self, user_id):
        user = get_jwt_identity()
        target = User.query.get_or_404(user_id)
        if user["id"] != user_id and user["role"] != "admin":
            return jsonify({"error": "No autorizado"}), 403
        return jsonify(target.serialize())

    @jwt_required()
    @roles_required("admin")
    def patch(self, user_id):
        target = User.query.get_or_404(user_id)
        data = request.get_json()
        target.role = data.get("role", target.role)
        db.session.commit()
        return jsonify({"message": "Rol actualizado"})

    @jwt_required()
    @roles_required("admin")
    def delete(self, user_id):
        target = User.query.get_or_404(user_id)
        target.is_active = False
        db.session.commit()
        return jsonify({"message": "Usuario desactivado"})
