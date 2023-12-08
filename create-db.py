if __name__ == "__main__":
    from src.backend import db, create_app, models
    app=create_app()

    with app.app_context():
        db.create_all()