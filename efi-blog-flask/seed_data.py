# seed_data.py
from app import create_app, db
from models.user import User

app = create_app()

with app.app_context():
    # Evita duplicar usuarios si ya existen
    if not User.query.filter_by(email="admin@mail.com").first():
        admin = User(name="Admin", email="admin@mail.com", role="admin")
        admin.set_password("admin123")

        mod = User(name="Moderator", email="mod@mail.com", role="moderator")
        mod.set_password("mod123")

        user = User(name="User", email="user@mail.com", role="user")
        user.set_password("user123")

        db.session.add_all([admin, mod, user])
        db.session.commit()
        print("✅ Usuarios de prueba creados correctamente.")
    else:
        print("⚠️ Usuarios ya existen, no se crearon nuevos.")
