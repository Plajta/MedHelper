if __name__ == "__main__":
    from src.backend import db, create_app, models
    import uuid
    from src.backend.models import Doctor
    from werkzeug.security import generate_password_hash

    app=create_app()

    with app.app_context():
        db.create_all()
        id = str(uuid.uuid4())

        new_user = Doctor(id=id ,username="admin", displayname="Ing. Los Adminos Maximos", password=generate_password_hash("admin", method='pbkdf2'), rank="admin", level="0")

        db.session.add(new_user)
        db.session.commit()