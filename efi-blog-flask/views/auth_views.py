from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from app import db

class RegisterAPI(MethodView):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email ya registrado"}), 400
        user = User(name=data["name"], email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario creado", "user_id": user.id}), 201

class LoginAPI(MethodView):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return jsonify({"error": "Credenciales inválidas"}), 401
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"access_token": token})
