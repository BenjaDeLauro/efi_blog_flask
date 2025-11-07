from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from decorators.roles_required import roles_required
from models.category import Category
from app import db

class CategoryAPI(MethodView):
    def get(self):
        cats = Category.query.all()
        return jsonify([c.serialize() for c in cats])

    @jwt_required()
    @roles_required("moderator", "admin")
    def post(self):
        data = request.get_json()
        category = Category(name=data["name"], description=data.get("description"))
        db.session.add(category)
        db.session.commit()
        return jsonify({"message": "Categoría creada"})

    @jwt_required()
    @roles_required("moderator", "admin")
    def put(self, category_id):
        cat = Category.query.get_or_404(category_id)
        data = request.get_json()
        cat.name = data.get("name", cat.name)
        cat.description = data.get("description", cat.description)
        db.session.commit()
        return jsonify({"message": "Categoría actualizada"})

    @jwt_required()
    @roles_required("admin")
    def delete(self, category_id):
        cat = Category.query.get_or_404(category_id)
        db.session.delete(cat)
        db.session.commit()
        return jsonify({"message": "Categoría eliminada"})
